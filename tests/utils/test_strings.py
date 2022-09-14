"""Provides Unit Tests for the `abis_mapping.utils.strings` module"""


# Local
from abis_mapping import utils


def test_strings_sanitise() -> None:
    """Tests the sanitise() function"""
    # Test Capitalisation
    assert utils.strings.sanitise("test") == "TEST"
    assert utils.strings.sanitise("Test") == "TEST"
    assert utils.strings.sanitise("TeSt") == "TEST"
    assert utils.strings.sanitise("TEST") == "TEST"

    # Test Stripping (Space, Hyphen, Underscore and Slash)
    assert utils.strings.sanitise("1/a b c") == "1ABC"
    assert utils.strings.sanitise("2/a-b-c") == "2ABC"
    assert utils.strings.sanitise("3/a_b_c") == "3ABC"
    assert utils.strings.sanitise("4/a-b_c") == "4ABC"

    # Test Stripping (Other)
    assert utils.strings.sanitise("a: b-c,d/e_f=g") == "ABCDEFG"
    assert utils.strings.sanitise("  p., /' 1 -Q-(2)r[ ] 3  s!*@(&#4  ") == "P1Q2R3S4"
