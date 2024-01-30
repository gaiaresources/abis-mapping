"""Dynamically loads template mappers"""


# Standard
import importlib
import pathlib
import abis_mapping.templates_deprecated.incidental_occurrence_data_deprecated.mapping


# Constants
PACKAGE_DIRECTORY = pathlib.Path(__file__).parent.parent
TEMPLATES_DIRECTORY = PACKAGE_DIRECTORY / "templates"


# Loop through modules in the directory
for mapping_module in TEMPLATES_DIRECTORY.glob("**/*.py"):
    # Determine Import Path
    relative_path = mapping_module.relative_to(PACKAGE_DIRECTORY.parent)
    import_string = ".".join(relative_path.with_suffix("").parts)

    # Dynamically import mapper
    importlib.import_module(import_string)
