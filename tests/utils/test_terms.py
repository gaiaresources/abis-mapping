"""Provides unit tests for the utils.terms module"""

# Standard
import re

# Third-party
import pytest
import pytest_mock
import rdflib.graph
import rdflib.term

# Local
from abis_mapping import utils


a = rdflib.RDF.type


@pytest.fixture
def patch_rdflib_bnode(mocker: pytest_mock.MockerFixture) -> None:
    """Expected overriding/patching of rdflib.BNode will be done at the start of a module"""
    mocker.patch.object(rdflib.term, "BNode", new=utils.terms.BNodeAlwaysUUID4)
    mocker.patch.object(rdflib, "BNode", new=utils.terms.BNodeAlwaysUUID4)


def test_bnode_with_value(patch_rdflib_bnode: None) -> None:
    """Tests BNodeAlwaysUUID4 with value supplied."""
    # Should raise a ValueError
    with pytest.raises(ValueError, match="value=hello"):
        rdflib.BNode("hello")


def test_bnode(patch_rdflib_bnode: None) -> None:
    """Test BNodeAlwaysUUID4."""
    # Create node
    bnode = rdflib.BNode()

    # Assert type
    assert isinstance(bnode, utils.terms.BNodeAlwaysUUID4)

    # Confirm id matches a hex representation of a uuid4
    re_id = re.compile(r"^N[0-f]{32}$")
    assert re_id.match(str(bnode))

    # Add to a graph
    graph = rdflib.Graph()
    jd = rdflib.URIRef("http://example.com/JohnDoe")
    graph.add((jd, rdflib.SDO.hasPart, bnode))

    # Ensure added to graph
    assert len(graph) == 1
    assert next(graph.objects(jd, rdflib.SDO.hasPart)) == bnode


@pytest.mark.skip(
    reason=(
        "currently this test fails since the parser implementation of rdflib's TurtleParser assigns a name"
        " to a blank node prior to creating it, violating the BNodeAlwaysUUID4 implementation."
    )
)
def test_bnode_called_during_parsing(patch_rdflib_bnode: None) -> None:
    """Tests BNodeAlwaysUUID4 called during parsing rdf."""
    # Create Bnode
    bnode = rdflib.BNode()

    # Add to a graph
    graph = rdflib.Graph()
    jd = rdflib.URIRef("http://example.com/JohnDoe")
    graph.add((jd, rdflib.SDO.hasPart, bnode))
    graph.add((bnode, a, rdflib.SDO.actor))

    # Create turtle
    ttl = graph.serialize(format="turtle")

    # Create new graph
    graph2 = rdflib.Graph().parse(data=ttl)

    # Check for type created
    s = next(graph2.subjects(a, rdflib.SDO.actor))
    o = next(graph2.objects(jd, rdflib.SDO.hasPart))
    assert isinstance(s, utils.terms.BNodeAlwaysUUID4)
    assert isinstance(o, utils.terms.BNodeAlwaysUUID4)
