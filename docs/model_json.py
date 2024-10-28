"""Generates json schemas from models"""

# Standard
import argparse
import importlib
import json

# Third-party
import pydantic

# Typing
from typing import Type


def import_model(path: str) -> Type[pydantic.BaseModel]:
    """Import pydantic model class from a module given its import path.

    Args:
        path: Import path to model class of the form `path.to.Model`

    Returns:
        Reference to model.

    Raises:
        ValueError: Invalid path supplied or if path does not resolve
            to a pydantic model.
    """
    # Check path is valid
    splt = path.rsplit(".", 1)

    # Split out last element
    if len(splt) < 2:
        raise ValueError(f"Invalid path: {path}")

    # Declare common error for remaining checks
    resolve_err = ValueError(f"Path: {path} does not resolve to a pydantic model.")

    # Attempt class import
    try:
        module = importlib.import_module(splt[0])
        result: Type[pydantic.BaseModel] = getattr(module, splt[1])
    except (ModuleNotFoundError, AttributeError) as exc:
        raise resolve_err from exc

    # Check the class is a pydantic model
    if issubclass(result, pydantic.BaseModel):
        # Return
        return result

    # Raise error if not
    raise resolve_err


def create_json_schema(model: Type[pydantic.BaseModel], path: str | None) -> str:
    """Create json schema from model.

    Args:
        model: Model reference.
        path: Optional file path to save JSON schema to.

    Returns:
        JSON schema as string.
    """
    # Create schema
    schema = json.dumps(model.model_json_schema(), indent=2)

    # Check path
    if path is not None:
        # Output to file
        with open(path, "w") as f:
            f.write(schema)
    # Return
    return schema


if __name__ == "__main__":
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Generates a json schema representation of a model.")
    parser.add_argument("model_path", type=str, help="Path to model of the form `path.to.Model`.")

    parser.add_argument(
        "-o",
        "--output",
        dest="output_dest",
        type=str,
        default=None,
        help="Optional output file.",
    )

    # Parse command line args
    args = parser.parse_args()

    # Get model
    model = import_model(args.model_path)

    # Generate Schema
    schema = create_json_schema(model, args.output_dest)

    # Print to stdout if no output file
    if args.output_dest is None:
        print(schema)

