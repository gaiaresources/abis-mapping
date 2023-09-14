"""Provides unit tests for the `abis_mapping.plugins.chronological` module"""


# Third-party
import frictionless
import pytest

# Local
from abis_mapping import plugins

# Typing
from typing import Optional


@pytest.mark.parametrize("source, field_names, n_errors", [
    ([
        # Missing
        {"name": "A", "start": "2022-09-11T15:15:15Z", "end": None},
        {"name": "B", "start": None, "end": "2022-09-11T15:15:15Z"},
        {"name": "C", "start": None, "end": None},

        # Valid
        {"name": "D", "start": "2022-09-11T15:15:15Z", "end": "2023-09-11T15:15:15Z"},

        # Invalid - start 1 year after end
        {"name": "E", "start": "2023-09-11T15:15:15Z", "end": "2022-09-11T15:15:15Z"},
    ], ["start", "end"], 1),
    ([
        # Missing
        {"name": "A", "start": "2022-09-11", "end": None},
        {"name": "B", "start": None, "end": "2022-09-11"},
        {"name": "C", "start": None, "end": None},

        # Valid
        {"name": "D", "start": "2022-09-11", "end": "2023-09-11"},

        # Invalid - start 1 year after end
        {"name": "E", "start": "2023-09-11", "end": "2022-09-11"},
    ], ["start", "end"], 1),
    ([
        # Missing
        {"name": "A", "start": "2022-09-11", "end": None},
        {"name": "B", "start": None, "end": "2022-09-11"},
        {"name": "C", "start": None, "end": None},

        # Valid - same date
        {"name": "D", "start": "2022-09-11", "end": "2022-09-11"},

        # Valid - start 1 year before end
        {"name": "E", "start": "2022-09-11", "end": "2023-09-11"},
    ], ["start", "end"], 0),
    ([
        # Missing
        {"name": "A", "start": "2022-09-11", "middle": "2022-10-11", "end": None},
        {"name": "B", "start": None, "middle": None, "end": "2022-09-11"},
        {"name": "C", "start": None, "middle": "2022-09-11", "end": None},

        # Valid
        {"name": "D", "start": "2022-09-11", "middle": "2023-05-11", "end": "2023-09-11"},

        # Invalid - start 1 year after end
        {"name": "E", "start": "2023-09-11", "middle": "2023-05-11", "end": "2022-09-11"},
    ], ["start", "middle", "end"], 1),
    ([
        # Missing
        {"name": "A", "start": "2022-09-11", "middle": "2022-10-11", "end": None},
        {"name": "B", "start": None, "middle": None, "end": "2022-09-11"},
        {"name": "C", "start": None, "middle": "2022-09-11", "end": None},

        # Valid
        {"name": "D", "start": "2022-09-11", "middle": "2023-05-11", "end": "2023-09-11"},

        # Invalid - middle 1 year after end
        {"name": "E", "start": "2022-09-11", "middle": "2024-05-11", "end": "2023-09-11"},
    ], ["start", "middle", "end"], 1),
    ([
         # Missing
         {"name": "A", "start": "2022-09-11", "middle": "2022-10-11", "end": None},
         {"name": "B", "start": None, "middle": None, "end": "2022-09-11"},
         {"name": "C", "start": None, "middle": "2022-09-11", "end": None},

         # Valid
         {"name": "D", "start": "2022-09-11", "middle": "2023-05-11", "end": "2023-09-11"},

         # Valid - middle same date as end
         {"name": "E", "start": "2022-09-11", "middle": "2023-05-11", "end": "2023-05-11"},
     ], ["start", "middle", "end"], 0),
])
def test_checks_valid_chronological_order(
        source: list[dict[str, Optional[str]]],
        field_names: list[str],
        n_errors: int
) -> None:
    """Test the ChronologicalOrder checker"""
    # Construct fake resource
    resource = frictionless.Resource(
        source=source
    )

    # Validate
    report = resource.validate(
        checks=[
            plugins.chronological.ChronologicalOrder(
                field_names=field_names
            ),
        ]
    )

    # Assert no. of errors is expected
    assert report.stats["errors"] == n_errors
