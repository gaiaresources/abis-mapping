"""Provides Unit Tests for the `abis_mapping.plugins.tabular` module"""


# Third-Party
import frictionless

# Local
from abis_mapping import plugins


def test_checks_not_tabular() -> None:
    """Tests the NotTabular Checker"""
    # Construct Fake Resource
    resource = frictionless.Resource(
        source=__file__,
    )

    # Validate
    report: frictionless.Report = resource.validate(
        checks=[
            plugins.tabular.NotTabular(),
        ]
    )

    # Check
    assert not report.valid
    assert len(report.flatten()) == 1
