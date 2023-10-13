"""Provides Unit Tests for the `abis_mapping.plugins.tabular` module"""


# Third-Party
import frictionless

# Local
from abis_mapping import plugins


def test_checks_is_tabular() -> None:
    """Tests the IsTabular Checker"""
    # Construct Fake Resource
    resource = frictionless.Resource(
        source=__file__,
    )

    # Validate
    report: frictionless.Report = resource.validate(
        checklist=frictionless.Checklist(
            checks=[
                plugins.tabular.IsTabular(),
            ]
        )
    )

    # Check
    assert not report.valid
    assert len(report.flatten()) == 1
