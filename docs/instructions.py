"""Provides instruction rendering for templates."""


# Standard
import argparse
import importlib.metadata
import io
import pathlib
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
        mapper = base.mapper.get_mapper(self.mapper_id)

        # Check mapper returned
        if mapper is None:
            raise ValueError(
                f"Template '{self.mapper_id}' not defined; got NoneType")

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


def render_index(filepath: pathlib.Path) -> str:
    """Renders the index.html for the build.

    Args:
        filepath (pathlib.Path): Path to output file containing markdown to be set
            as the homepage for redirection.

    Returns:
        str: Rendered index.html

    Raises:
        ValueError: If the supplied filename contains no parent directory.
    """
    # Parent directory name will be relative url path for redirect
    try:
        page_name = filepath.parent.parts[-1]
    except IndexError:
        raise ValueError(f"Path {filepath} contains no parent directory.")

    # Create loader
    loader = jinja2.FileSystemLoader("docs/templates")

    # Create env
    env = jinja2.Environment(
        loader=loader,
    )

    # Get template
    template = env.get_template("index.html")

    # Render and return
    return template.render(page_name=page_name)


if __name__ == "__main__":
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generates instruction documents.")
    parser.add_argument("mapper_id", type=str, help="Mapper template ID.")

    parser.add_argument(
        "-o", "--output",
        dest="output_dest",
        type=argparse.FileType("w"),
        default=sys.stdout,
        help="Output destination. Default is stdout."
    )

    parser.add_argument(
        "-i", "--index",
        dest="index",
        action="store_true",
        help="Set current template as homepage. This will generate an additional `index.md` document."
    )

    # Parse command line arguments
    args = parser.parse_args()

    # Generate instructions
    rendered = build_instructions(args.mapper_id)

    # Output to file
    print(rendered, file=args.output_dest)

    # Close file
    args.output_dest.close()

    # Check index flag and output is a file
    if args.index and isinstance(args.output_dest, io.FileIO):
        # Redeclaring here to help IDE
        od: io.FileIO = args.output_dest
        # Create Path object from output destination
        pth = pathlib.Path(od.name)
        rendered_index = render_index(pth)
        # Open destination index.html and write
        with open(f"{pth.parent}/index.html", "w") as f:
            f.write(rendered_index)
