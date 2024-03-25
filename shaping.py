import rdflib
import rdflib.term
import rdflib.collection
import pyshacl

from abis_mapping import utils
from abis_mapping import vocabs

a = rdflib.RDF.type
SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")


def main():
    g = utils.rdf.create_graph()
    g.bind("sh", SH)

    site_shape = utils.namespaces.BDR.SiteShape

    # Set the target class
    g.add((site_shape, a, SH.NodeShape))
    g.add((site_shape, SH.targetClass, utils.namespaces.TERN.Site))

    # Add the dataset prop
    dataset_prop = rdflib.BNode()
    g.add((dataset_prop, SH.path, rdflib.VOID.inDataset))
    g.add((dataset_prop, SH["class"], utils.namespaces.TERN.RDFDataset))
    g.add((dataset_prop, SH.minCount, rdflib.Literal(1)))
    g.add((dataset_prop, SH.maxCount, rdflib.Literal(1)))
    g.add((site_shape, SH.property, dataset_prop))

    # Add the site visit prop
    site_visit_prop = rdflib.BNode()
    g.add((site_visit_prop, SH["class"], utils.namespaces.TERN.SiteVisit))
    g.add((site_visit_prop, SH.path, utils.namespaces.TERN.hasSiteVisit))
    g.add((site_shape, SH.property, site_visit_prop))

    # Add the site id property
    site_id_prop = rdflib.BNode()
    g.add((site_id_prop, SH.path, rdflib.DCTERMS.identifier))
    g.add((site_id_prop, SH.datatype, rdflib.XSD.string))
    g.add((site_shape, SH.property, site_id_prop))

    # Add the feature type prop
    feature_type_prop = rdflib.BNode()
    g.add((feature_type_prop, SH.path, utils.namespaces.TERN.featureType))
    g.add((feature_type_prop, SH.hasValue, vocabs.site_type.SITE.iri))
    g.add((site_shape, SH.property, feature_type_prop))



    # Add the dcterms type prop
    dcterms_type_prop = rdflib.BNode()
    terms_list = rdflib.BNode()
    g.add((dcterms_type_prop, SH.path, rdflib.DCTERMS.type))
    rdflib.collection.Collection(g, terms_list, list(vocabs.site_type.SITE_TYPE.mapping.values()))
    g.add((dcterms_type_prop, SH["in"], terms_list))
    g.add((site_shape, SH.property, dcterms_type_prop))

    g.serialize("result.ttl")

    d = rdflib.Graph().parse(source="abis_mapping/templates/survey_site_data/examples/minimal.ttl")
    s = rdflib.Graph().parse(source="result.ttl")
    pyshacl.validate(data_graph=d, shacl_graph=s)


def add_skos_concept(g: rdflib.Graph) -> rdflib.term.Node:
    # Add SKOS concept shapetype
    concept_shape = utils.namespaces.BDR.ConceptShape
    g.add((concept_shape, a, SH.NodeShape))
    g.add((concept_shape, SH.targetClass, rdflib.SKOS.Concept))

    # Add definition prop
    definition_prop = rdflib.BNode()
    g.add((definition_prop, SH.path, rdflib.SKOS.definition))

    return concept_shape

if __name__ == "__main__":
    main()