"""Provides instruction rendering for templates."""

# Standard
import argparse
import importlib.metadata
import sys

# Third-partv
import jinja2

# Local
from abis_mapping import base
from docs import contexts

# Typing
from typing import Callable


class MapperLoader(jinja2.BaseLoader):
    def __init__(self, mapper_id: str):
        """Constructor for MapperLoader.

        Args:
            mapper_id (str): Mapper template ID.
        """
        self.mapper_id = mapper_id

    def get_source(
        self,
        environment: jinja2.Environment,
        template: str,
    ) -> tuple[str, str | None, Callable[[], bool] | None]:
        """Overloaded implementation of jinja2.BaseLoader.get_source.
        https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.BaseLoader.get_source

        Args:
            environment (jinja2.Environment): Jinja environment.
            template (str): Abis-mapping or base template name. If a base
                template name is provided, the docs/templates directory will
                be searched for that corresponding file.

        Returns:
            tuple[str, str | None, Callable[[], bool] | None]: The template
            source, filename and reload helper for a jinja template.

        Raises:
            ValueError: If mapper is not found.
            jinja2.TemplateNotFound: Template not found.
        """
        # Check to see if searching base templates
        if (splt := template.strip().split())[0] == "BASE_TEMPLATE":
            # Create a filesystem loader and use it to find and return
            fs_loader = jinja2.FileSystemLoader(searchpath="docs/templates")
            return fs_loader.get_source(environment, splt[1])

        # Get mapper
        try:
            mapper = base.mapper.get_mapper(self.mapper_id)
        except KeyError:
            raise ValueError(f"Template '{self.mapper_id}' not found.")

        # Check mapper returned
        if mapper is None:
            raise TypeError(f"Template '{self.mapper_id}' not defined; got NoneType")

        # Create path
        path = mapper().root_dir() / "templates" / template

        # Check file exists at path
        if not path.is_file():
            raise jinja2.TemplateNotFound(str(path))

        # Get current mtime
        mtime = path.stat().st_mtime

        # Read contents
        source = path.read_text()

        # Return
        return source, str(path), lambda: mtime == path.stat().st_mtime


def build_instructions(mapper_id: str) -> str:
    """Builds an instruction document.

    Args:
        mapper_id (str): Mapper template ID.

    Returns:
        str: The instruction document.

    Raises:
        ValueError: Mapper not found.
        jinja2.TemplateNotFound: Jinja template not found.
    """
    # Create jinja env
    env = jinja2.Environment(loader=MapperLoader(mapper_id))

    # Retrieve markdown instructions template
    template = env.get_template("instructions.md")

    # Load per template context
    ctx = contexts.base.get_context(mapper_id)

    # Add the project version if a dictionary has been returned
    if ctx is not None:
        ctx["project_version"] = importlib.metadata.version("abis-mapping")

    # Return render
    return template.render(ctx)


if __name__ == "__main__":
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Generates instruction documents.")
    parser.add_argument("mapper_id", type=str, help="Mapper template ID.")

    parser.add_argument(
        "-o", "--output",
        dest="output_dest",
        type=argparse.FileType("w"),
        default=sys.stdout,
        help="Output destination. Default is stdout."
    )

    # Parse command line arguments
    args = parser.parse_args()

    # Generate instructions
    rendered = build_instructions(args.mapper_id)

    # Output to file
    print(rendered, file=args.output_dest)

    # Close file
    args.output_dest.close()
