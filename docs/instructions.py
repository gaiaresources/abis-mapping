"""Provides instruction rendering for templates."""

# Standard
import argparse
import sys

# Third-partv
import jinja2

# Local
from abis_mapping import base
from abis_mapping import vocabs
from docs import tables

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
            template (str): Jinja template name.

        Returns:
            tuple[str, str | None, Callable[[], bool] | None]: The template
            source, filename and reload helper for a jinja template.

        Raises:
            ValueError: If mapper is not found.
            jinja2.TemplateNotFound: Template not found.
        """
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

    # Create context
    ctx = {
        "tables": {
            "fields": tables.fields.FieldTabler(mapper_id).generate_table(as_markdown=True),
            "vocabularies": tables.vocabs.VocabTabler(mapper_id).generate_table(as_markdown=True),
            "threat_status": tables.threat_status.ThreatStatusTabler(mapper_id).generate_table(as_markdown=True),
        },
        "values": {
            "geodetic_datum_count": len(vocabs.geodetic_datum.GeodeticDatum.terms),
        },
        "anchors": {
            "vocabulary_list": "vocabulary-list",
        },
    }

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
