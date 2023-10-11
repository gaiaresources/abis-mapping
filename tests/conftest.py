"""Provides Fixtures and Helpers for the Unit Tests"""


# Third-Party
import rdflib
import rdflib.compare

# Typing
from typing import Union


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

    # Replace Timestamps
    # In many cases, dates and datetimes are generately systematically as a
    # timestamp for "now". When unit testing, we don't care if "now" has
    # changed when comparing graphs. As such, we want to replace all literals
    # with a datatype `xsd:date`, `xsd:dateTime` or `xsd:dateTimeStamp` with a
    # pre-generate value.
    for graph in (graph1, graph2):
        for (s, p, o) in graph.triples((None, None, None)):
            if isinstance(o, rdflib.Literal):
                if o.datatype in (rdflib.XSD.date, rdflib.XSD.dateTime, rdflib.XSD.dateTimeStamp):
                    graph.set((s, p, rdflib.Literal("test-value")))

    # Compare Graphs
    return rdflib.compare.isomorphic(
        graph1=graph1,
        graph2=graph2,
    )
