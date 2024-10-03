"""Provides unit tests for the `abis_mapping.plugins.chronological` module"""

# Third-party
import frictionless
import frictionless.fields
import pytest

# Local
from abis_mapping import plugins
from abis_mapping.types import temporal

# Typing
from typing import Optional


@pytest.mark.parametrize(
    "source, field_names, n_errors",
    [
        (
            [
                # Missing
                {"start": "2022-09-11T15:15:15Z", "end": None},
                {"start": None, "end": "2022-09-11T15:15:15Z"},
                # Valid
                {"start": "2022-09-11T15:15:15Z", "end": "2023-09-11T15:15:15Z"},
                {"start": "2022-09-11T15:15:15Z", "end": temporal.Year(2022)},
                {"start": "2022-09-11T15:15:15Z", "end": "9/2022"},
                # Invalid - start 1 year after end
                {"start": "2023-09-11T15:15:15Z", "end": "2022-09-11T15:15:15Z"},
            ],
            ["start", "end"],
            1,
        ),
        (
            [
                # Missing
                {"start": "2022-09-11", "end": None},
                {"start": None, "end": "2022-09-11"},
                # Valid
                {"start": "2022-09-11", "end": "2023-09-11"},
                {"start": "2022", "end": "2022-04"},
                {"start": "09/2022", "end": temporal.Year(2022)},
                # Invalid - start 1 year after end
                {"start": "2023-09-11", "end": "2022-09-11"},
                {"start": "09/2023", "end": "2022"},
                {"start": "2023", "end": temporal.Year(2022)},
            ],
            ["start", "end"],
            3,
        ),
        (
            [
                # Missing
                {"start": "2022-09-11", "end": None},
                {"start": None, "end": "2022-09-11"},
                # Valid - same date
                {"start": "2022-09-11", "end": "2022-09-11"},
                # Valid - start 1 year before end
                {"start": "2022-09-11", "end": "2023-09-11"},
            ],
            ["start", "end"],
            0,
        ),
        (
            [
                # Missing
                {"start": "2022-09-11", "middle": "2022-10-11", "end": None},
                {"start": None, "middle": None, "end": "2022-09-11"},
                {"start": None, "middle": "2022-09-11", "end": None},
                # Valid
                {"start": "2022-09-11", "middle": "2023-05-11", "end": "2023-09-11"},
                # Invalid - start 1 year after end
                {"start": "2023-09-11", "middle": "2023-05-11", "end": "2022-09-11"},
            ],
            ["start", "middle", "end"],
            1,
        ),
        (
            [
                # Missing
                {"start": "2022-09-11", "middle": "2022-10-11", "end": None},
                {"start": None, "middle": None, "end": "2022-09-11"},
                {"start": None, "middle": "2022-09-11", "end": None},
                # Valid
                {"start": "2022-09-11", "middle": "2023-05-11", "end": "2023-09-11"},
                # Invalid - middle 1 year after end
                {"start": "2022-09-11", "middle": "2024-05-11", "end": "2023-09-11"},
            ],
            ["start", "middle", "end"],
            1,
        ),
        (
            [
                # Missing
                {"start": "2022-09-11", "middle": "2022-10-11", "end": None},
                {"start": None, "middle": None, "end": "2022-09-11"},
                {"start": None, "middle": "2022-09-11", "end": None},
                # Valid
                {"start": "2022-09-11", "middle": "2023-05-11", "end": "2023-09-11"},
                # Valid - middle same date as end
                {"start": "2022-09-11", "middle": "2023-05-11", "end": "2023-05-11"},
            ],
            ["start", "middle", "end"],
            0,
        ),
    ],
)
def test_checks_valid_chronological_order(
    source: list[dict[str, Optional[str]]], field_names: list[str], n_errors: int
) -> None:
    """Test the ChronologicalOrder checker"""
    # Construct fake schema
    schema = frictionless.Schema.from_descriptor(
        {"fields": [{"name": n, "type": "timestamp", "allowYearMonth": True, "allowYear": True} for n in source[0]]}
    )
    # Construct fake resource
    resource = frictionless.Resource(schema=schema, source=source)

    # Validate
    report = resource.validate(
        checklist=frictionless.Checklist(
            checks=[
                plugins.chronological.ChronologicalOrder(field_names=field_names),
            ]
        )
    )

    # Assert no. of errors is expected and right type
    if n_errors > 0:
        assert set([code for codes in report.flatten(["type"]) for code in codes]) == {"row-constraint"}
    assert report.stats["errors"] == n_errors
