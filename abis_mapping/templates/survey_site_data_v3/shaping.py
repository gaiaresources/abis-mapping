"""Generates a SHACL shape graph for the survey_site_data template v3."""

# Standard Library
import pathlib

# Third-party
import rdflib
import rdflib.term
import rdflib.collection
import pyshacl

# Local
from abis_mapping import utils
from abis_mapping import vocabs


# Constants
a = rdflib.RDF.type
SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")
TEMPORAL_DATATYPES = [
    (rdflib.TIME.inXSDDate, rdflib.XSD.date),
    (rdflib.TIME.inXSDDateTime, rdflib.XSD.dateTime),
    (rdflib.TIME.inXSDDateTimeStamp, rdflib.XSD.dateTimeStamp),
    (rdflib.TIME.inXSDgYearMonth, rdflib.XSD.gYearMonth),
    (rdflib.TIME.inXSDgYear, rdflib.XSD.gYear),
]

TEMPLATE_DIR = pathlib.Path(__file__).parent


def main() -> None:
    """Implementation of the SHACL generation."""

    # Create graph and bind shape namespace
    g = utils.rdf.create_graph()
    g.bind("sh", SH)

    # Call each of the major shape constructions
    dataset_shape = create_dataset_shape(g)
    add_site_shape(g, dataset_shape)
    add_site_visit_shape(g, dataset_shape)

    # Perform a validation
    d = rdflib.Graph().parse(source=TEMPLATE_DIR / "examples" / "minimal.ttl")
    s = rdflib.Graph().parse(data=g.serialize())
    valid, rgraph, rtext = pyshacl.validate(data_graph=d, shacl_graph=s)

    # Print report to stdout.
    print(rtext)

    # Raise exception if not valid.
    if not valid:
        raise AssertionError("not valid")

    # Write out to file
    g.serialize(TEMPLATE_DIR / "validators" / "validator.ttl")


def add_site_visit_shape(graph: rdflib.Graph, dataset_shape: rdflib.term.Node) -> rdflib.term.Node:
    """Defines and adds site visit shape to graph.

    Args:
        graph (rdflib.Graph): Graph to add site visit
        dataset_shape (rdflib.term.Node): Dataset reference node:

    Returns:
        rdflib.term.Node: Site visit shape node reference
    """

    # Declare shape uri
    site_visit_shape = utils.namespaces.BDR.SiteVisitShape

    # Add type and target class
    graph.add((site_visit_shape, a, SH.NodeShape))
    graph.add((site_visit_shape, SH.targetClass, utils.namespaces.TERN.SiteVisit))

    # Add dataset prop
    graph.add((site_visit_shape, SH.property, dataset_shape))

    # Add temporal entity prop
    temporal_entity_prop = rdflib.BNode()
    graph.add((temporal_entity_prop, SH["class"], rdflib.TIME.TemporalEntity))
    graph.add((temporal_entity_prop, SH.path, rdflib.TIME.hasTime))
    # # Add dates
    begin_prop = rdflib.BNode()
    graph.add((begin_prop, SH["class"], rdflib.TIME.Instant))
    graph.add((begin_prop, SH.path, rdflib.TIME.hasBeginning))
    temporal_type_opts = temporal_type_list(graph)
    graph.add((begin_prop, SH["or"], temporal_type_opts))
    graph.add((temporal_entity_prop, SH.property, begin_prop))
    end_prop = rdflib.BNode()
    graph.add((end_prop, SH["class"], rdflib.TIME.Instant))
    graph.add((end_prop, SH.path, rdflib.TIME.hasEnd))
    graph.add((end_prop, SH["or"], temporal_type_opts))
    graph.add((temporal_entity_prop, SH.property, end_prop))
    graph.add((site_visit_shape, SH.property, temporal_entity_prop))

    # Return reference uri
    return site_visit_shape


def temporal_type_list(graph: rdflib.Graph) -> rdflib.term.Node:
    """Creates an rdf list of temporal types.

    Args:
        graph (rdflib.Graph): Graph the list will be added:

    Returns:
        rdflib.term.Node: Reference to the list
    """
    # Declare temporal type list uri
    temporal_type_opts = utils.namespaces.BDR.TemporalTypesList

    # Empty list to hold the temporal datatypes
    temporal_type_nodes: list[rdflib.term.Node] = []
    for in_xsd, data_type in TEMPORAL_DATATYPES:
        new_node = rdflib.BNode()
        graph.add((new_node, SH.path, in_xsd))
        graph.add((new_node, SH.datatype, data_type))
        temporal_type_nodes.append(new_node)

    # Create a collection and add to the graph
    rdflib.collection.Collection(graph, temporal_type_opts, temporal_type_nodes)

    # Return the top reference uri
    return temporal_type_opts


def create_dataset_shape(graph: rdflib.Graph) -> rdflib.term.Node:
    """Creates the dataset shape and adds to graph.

    Args:
        graph (rdflib.Graph): Graph to be added to.

    Returns:
        rdflib.term.Node: Reference to the dataset shape.
    """
    # Add the dataset prop
    dataset_prop = utils.namespaces.BDR.DatasetShape
    graph.add((dataset_prop, a, SH.PropertyShape))
    graph.add((dataset_prop, SH.path, rdflib.VOID.inDataset))
    graph.add((dataset_prop, SH["class"], utils.namespaces.TERN.Dataset))
    graph.add((dataset_prop, SH.minCount, rdflib.Literal(1)))
    graph.add((dataset_prop, SH.maxCount, rdflib.Literal(1)))

    # Return reference uri
    return dataset_prop


def add_site_shape(g: rdflib.Graph, dataset_shape: rdflib.term.Node) -> rdflib.term.Node:
    """Adds the site shape to the graph.

    Args:
        g (rdflib.Graph): Graph to be modified.
        dataset_shape (rdflib.term.Node): Reference to the dataset shape

    Returns:
        rdflib.term.Node: Reference to the site shape.

    """
    # Declare the shape uri
    site_shape = utils.namespaces.BDR.SiteShape

    # Set the target class
    g.add((site_shape, a, SH.NodeShape))
    g.add((site_shape, SH.targetClass, utils.namespaces.TERN.Site))

    # Add the dataset prop
    g.add((site_shape, SH.property, dataset_shape))

    # Add the site visit prop
    site_visit_prop = rdflib.BNode()
    g.add((site_visit_prop, SH["class"], utils.namespaces.TERN.SiteVisit))
    g.add((site_visit_prop, SH.path, utils.namespaces.TERN.hasSiteVisit))
    g.add((site_visit_prop, SH.minCount, rdflib.Literal(1)))
    g.add((site_visit_prop, SH.maxCount, rdflib.Literal(1)))
    g.add((site_shape, SH.property, site_visit_prop))

    # Add the site id property
    site_id_prop = rdflib.BNode()
    g.add((site_id_prop, SH.path, rdflib.SDO.identifier))
    g.add((site_id_prop, SH.datatype, rdflib.XSD.string))
    g.add((site_id_prop, SH.minCount, rdflib.Literal(1)))
    g.add((site_id_prop, SH.maxCount, rdflib.Literal(1)))
    g.add((site_shape, SH.property, site_id_prop))

    # Add the feature type prop
    feature_type_prop = rdflib.BNode()
    g.add((feature_type_prop, SH.path, utils.namespaces.TERN.featureType))
    g.add((feature_type_prop, SH.hasValue, vocabs.site_type.SITE.iri))
    g.add((feature_type_prop, SH.minCount, rdflib.Literal(1)))
    g.add((feature_type_prop, SH.maxCount, rdflib.Literal(1)))
    g.add((site_shape, SH.property, feature_type_prop))

    # Add the dcterms type prop
    dcterms_type_prop = rdflib.BNode()
    terms_list = rdflib.BNode()
    terms_list_shape = rdflib.BNode()
    dcterms_type_opts = rdflib.BNode()
    g.add((dcterms_type_prop, SH.path, rdflib.SDO.additionalType))
    site_type_vocab_values: list[rdflib.term.Node] = [v.iri for v in vocabs.site_type.SiteType.terms if v is not None]
    rdflib.collection.Collection(g, terms_list, site_type_vocab_values)
    g.add((terms_list_shape, SH["in"], terms_list))
    site_type_concept_shape = site_type_concept(g)
    rdflib.collection.Collection(g, dcterms_type_opts, [terms_list_shape, site_type_concept_shape])
    g.add((dcterms_type_prop, SH.xone, dcterms_type_opts))
    g.add((dcterms_type_prop, SH.minCount, rdflib.Literal(1)))
    g.add((dcterms_type_prop, SH.maxCount, rdflib.Literal(1)))
    g.add((site_shape, SH.property, dcterms_type_prop))

    # Add SDO name prop
    sdo_name_prop = rdflib.BNode()
    g.add((sdo_name_prop, SH.path, rdflib.SDO.name))
    g.add((sdo_name_prop, SH.datatype, rdflib.XSD.string))
    g.add((sdo_name_prop, SH.maxCount, rdflib.Literal(1)))
    g.add((site_shape, SH.property, sdo_name_prop))

    # Add SDO description prop
    sdo_description_prop = rdflib.BNode()
    g.add((sdo_description_prop, SH.path, rdflib.SDO.description))
    g.add((sdo_description_prop, SH.datatype, rdflib.XSD.string))
    g.add((sdo_description_prop, SH.maxCount, rdflib.Literal(1)))
    g.add((site_shape, SH.property, sdo_description_prop))

    # Add coord uncertainty prop
    coord_uncert_prop = rdflib.BNode()
    g.add((coord_uncert_prop, SH.path, utils.namespaces.GEO.hasMetricSpatialAccuracy))
    g.add((coord_uncert_prop, SH.datatype, rdflib.XSD.double))
    g.add((coord_uncert_prop, SH.maxCount, rdflib.Literal(1)))
    g.add((site_shape, SH.property, coord_uncert_prop))

    # Add geometry prop
    site_geometry_prop = rdflib.BNode()
    g.add((site_geometry_prop, SH.path, rdflib.SDO.spatial))
    g.add((site_geometry_prop, SH["class"], utils.namespaces.GEO.Geometry))
    g.add((site_geometry_prop, SH.maxCount, rdflib.Literal(2)))  # Both point and footprintWKT supplied
    wkt_prop = rdflib.BNode()
    g.add((wkt_prop, SH.path, utils.namespaces.GEO.asWKT))
    g.add((wkt_prop, SH.datatype, utils.namespaces.GEO.wktLiteral))
    g.add((wkt_prop, SH.minCount, rdflib.Literal(1)))
    g.add((wkt_prop, SH.minCount, rdflib.Literal(1)))
    g.add((site_geometry_prop, SH.property, wkt_prop))
    g.add((site_shape, SH.property, site_geometry_prop))

    # Return ref to site shape
    return site_shape


def site_type_concept(g: rdflib.Graph) -> rdflib.term.Node:
    """Site type concept shape.

    Args:
        g (rdflib.Graph): Graph to be added to.

    Returns:
        rdflib.term.Node: Site type concept shape reference.

    """
    # Add SKOS concept shapetype
    concept_shape = utils.namespaces.BDR.SiteTypeConceptShape
    g.add((concept_shape, a, SH.NodeShape))
    g.add((concept_shape, SH.targetClass, rdflib.SKOS.Concept))

    # Add definition prop
    definition_prop = rdflib.BNode()
    g.add((definition_prop, SH.path, rdflib.SKOS.definition))
    g.add((definition_prop, SH.hasValue, rdflib.Literal("A type of site.")))
    g.add((concept_shape, SH.property, definition_prop))

    # Add scheme
    scheme_prop = rdflib.BNode()
    g.add((scheme_prop, SH.path, rdflib.SKOS.inScheme))
    g.add(
        (
            scheme_prop,
            SH.hasValue,
            rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/74aa68d3-28fd-468d-8ff5-7e791d9f7159"),
        )
    )
    g.add((concept_shape, SH.property, scheme_prop))

    # Add preflabel
    pref_label_prop = rdflib.BNode()
    g.add((pref_label_prop, SH.path, rdflib.SKOS.prefLabel))
    g.add((pref_label_prop, SH.datatype, rdflib.XSD.string))
    g.add((concept_shape, SH.property, pref_label_prop))

    # Return reference
    return concept_shape


if __name__ == "__main__":
    main()
