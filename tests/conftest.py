"""Provides Fixtures and Helpers for the Unit Tests"""

# Standard
import json
import unittest.mock

# Third-Party
import pytest
import pytest_mock
import _pytest.skipping
import rdflib
import rdflib.compare

# Local
from abis_mapping import utils

# Typing
from typing import Union, Any, Callable


# def pytest_addoption(parser: pytest.Parser) -> None:
#     """Adds parser option to pytest cmd line.
# 
#     Adapted from https://stackoverflow.com/a/61503247
# 
#     Args:
#         parser (pytest.Parser): The pytest argparser.
#     """
#     # Add option to parser
#     parser.addoption(
#         "--no-skip",
#         action="store_true",
#         default=False,
#         help="disable skip marks",
#     )
# 
# 
# @pytest.hookimpl(tryfirst=True)
# def pytest_cmdline_preparse(config: pytest.Config, args: list[Any]) -> None:
#     """Determines if skips will be honoured by pytest.
# 
#     Adapted from https://stackoverflow.com/a/61503247
# 
#     Args:
#         config (pytest.Config): pytest config object.
#         args (list[Any]): List of items associated with hook.
#     """
#     # Check for no-skip flag
#     if "--no-skip" not in args:
#         return
# 
#     def no_skip(*args: list[Any], **kwargs: dict[str, Any]) -> None:
#         return
# 
#     # Assign no_skip as skip function within pytest
#     _pytest.skipping.skip = no_skip   # type: ignore[assignment]


@pytest.fixture
def mocked_vocab(mocker: pytest_mock.MockerFixture) -> unittest.mock.MagicMock:
    """Provides a mocked term fixture.

    Args:
        mocker (pytest_mock.MockerFixture): Pytest mocker fixture.

    Returns:
        unittest.mock.MagicMock: Mocked term fixture.
    """
    # Patch get_vocab
    mocked_vocab = mocker.patch("abis_mapping.utils.vocabs.get_vocab")

    # Patch terms
    mocked_vocab.return_value.terms = (
        utils.vocabs.Term(
            labels=("SOME LABEL", "ANOTHER LABEL", ),
            iri=rdflib.URIRef("https://example.org/some-term"),
            description="Some description.",
        ),
    )

    # Return
    return mocked_vocab


def compare_graphs(
    graph1: Union[rdflib.Graph, str],
    graph2: Union[rdflib.Graph, str],
) -> bool:
    """Isomorphically compares to graphs for equality.

    Args:
        graph1 (Union[rdflib.Graph, str]): Graph or Turtle String to Compare
        graph2 (Union[rdflib.Graph, str]): Graph or Turtle String to Compare

    Returns:
        bool: Whether the graphs are isomorphically equivalent.
    """
    # Serialize Graphs if Applicable
    # There appears to be a difference between the handling of blank-nodes in
    # graphs *constructed* programmatically by `rdflib`, and graphs *parsed* by
    # `rdflib`. As such, an easy work-around for testing is to do a round trip
    # of serialization and de-serialization before the isomorphic comparison.
    if isinstance(graph1, rdflib.Graph):
        graph1 = graph1.serialize(format="text/turtle")
    if isinstance(graph2, rdflib.Graph):
        graph2 = graph2.serialize(format="text/turtle")

    # Re-Parse Graphs
    graph1 = rdflib.Graph().parse(data=graph1, format="text/turtle")
    graph2 = rdflib.Graph().parse(data=graph2, format="text/turtle")

    # Asserts
    assert isinstance(graph1, rdflib.Graph)
    assert isinstance(graph2, rdflib.Graph)

    for graph in (graph1, graph2):
        for (s, p, o) in graph.triples((None, None, None)):
            if isinstance(o, rdflib.Literal):
                # Replace Timestamps
                # In many cases, dates and datetimes are generately systematically as a
                # timestamp for "now". When unit testing, we don't care if "now" has
                # changed when comparing graphs. As such, we want to replace all literals
                # with a datatype `xsd:date`, `xsd:dateTime` or `xsd:dateTimeStamp` with a
                # pre-generate value.
                if o.datatype in (rdflib.XSD.date, rdflib.XSD.dateTime, rdflib.XSD.dateTimeStamp):
                    graph.set((s, p, rdflib.Literal("test-value")))
                # Reformat JSON strings
                # Since the ordering of json keys could be in different ordering depending on
                # serializer, need to deserialize json then reserialize to ensure the same format
                # string literal for each.
                if o.datatype == rdflib.RDF.JSON:
                    o_dict = json.loads(str(o))
                    sorted_string = json.dumps(o_dict, sort_keys=True)
                    graph.set((s, p, rdflib.Literal(sorted_string, datatype=rdflib.RDF.JSON)))

    # Compare Graphs
    return rdflib.compare.isomorphic(
        graph1=graph1,
        graph2=graph2,
    )


@pytest.fixture
def graph_comparer() -> Callable[[rdflib.Graph | str, rdflib.Graph | str], bool]:
    """Make a fixture out of the compare_graphs function for convenience."""
    return compare_graphs
