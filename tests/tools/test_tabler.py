"""Provides unit tests for the tabler module"""

# Third party
import pytest

# Local
import tools.fields


def test_tabler_init_raises_invalid_template_id() -> None:
    """Tests initialisation raises on invalid template id."""

    with pytest.raises(ValueError):
        tools.fields.FieldTabler("FAKE_ID")

