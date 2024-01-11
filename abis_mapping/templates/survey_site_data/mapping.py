"""Provides ABIS Mapper for `survey_site_data.csv` Template"""
import decimal

# Local
from abis_mapping import base
from abis_mapping import plugins
from abis_mapping import utils
from abis_mapping import vocabs

# Third-party
import rdflib
import frictionless
import shapely
import shapely.geometry

# Typing
from typing import Any, Optional, Iterator


# Constants and shortcuts
a = rdflib.RDF.type


class SurveySiteMapper(base.mapper.ABISMapper):
    """ABIS Mapper for `survey_site_data.csv`"""

    # Template ID and Instructions File
    template_id = "survey_site_data.csv"
    instructions_file = "instructions.pdf"

    # Default Dataset Metadata
    DATASET_DEFAULT_NAME = "Example Systematic Survey Site Dataset"
    DATASET_DEFAULT_DESCRIPTION = "Example Systematic Survey Site Dataset by Gaia Resources"

    def apply_validation(
        self,
        data: base.types.ReadableType,
        **kwargs: Any,
    ) -> frictionless.Report:
        """Applies Frictionless Validation for the `survey_site_data.csv` Template

        Args:
            data (base.types.ReadableType): Raw data to be validated.

        Returns:
            frictionless.Report: Validation report for the specified data.
        """
        # Construct schema
        schema = frictionless.Schema.from_descriptor(self.schema())

        # Construct resource
        resource = frictionless.Resource(
            data=data,
            format="csv",
            schema=schema,
        )

        # Validate
        report = resource.validate(
            checklist=frictionless.Checklist(
                checks=[
                    # Extra custom checks
                    plugins.tabular.IsTabular(),
                    plugins.empty.NotEmpty(),
                    plugins.mutual_inclusion.MutuallyInclusive(
                        field_names=[
                            "decimalLatitude",
                            "decimalLongitude",
                        ]
                    ),
                    plugins.logical_or.LogicalOr(
                        field_names=[
                            "footprintWKT",
                            "decimalLatitude",
                        ]
                    ),
                    plugins.chronological.ChronologicalOrder(
                        field_names=[
                            "siteVisitStart",
                            "siteVisitEnd"
                        ]
                    )
                ],
                skip_errors=self.skip_errors,
            )
        )

        # Return validation report
        return report

    def extract_geometry_defaults(
        self,
        data: base.types.ReadableType,
        **kwargs: Any,
    ) -> dict[str, str]:
        """Constructs a dictionary mapping site id to default WKT.

        The resulting string WKT returned can then be used as the missing
        geometry for other related templates i.e. the site occurrences

        Args:
            data (base.types.ReadableType): Raw data to be mapped.

        Returns:
            dict[str, str]: Keys are the site id; values are the
                appropriate point WKT serialized string. If none then
                there is no siteID key created.

        """
        # Construct schema
        schema = frictionless.Schema.from_descriptor(self.schema())

        resource = frictionless.Resource(
            data=data,
            format="csv",
            schema=schema,
        )

        with resource.open() as r:
            # Create empty dictionary to hold mapping values
            result = {}
            for row in r.row_stream:
                # Extract values
                site_id: str = row["siteID"]
                footprint_wkt: shapely.geometry.base.BaseGeometry = row["footprintWKT"]
                longitude: decimal.Decimal = row["decimalLongitude"]
                latitude: decimal.Decimal = row["decimalLatitude"]

                # Default to using the footprint wkt
                if footprint_wkt is not None:
                    result[site_id] = footprint_wkt.centroid.wkt
                    continue
                # If not footprint then we revert to using supplied longitude & latitude
                if longitude is not None and latitude is not None:
                    result[site_id] = shapely.Point([longitude, latitude]).wkt

            return result

    def apply_mapping(
        self,
        data: base.types.ReadableType,
        dataset_iri: Optional[rdflib.URIRef] = None,
        base_iri: Optional[rdflib.Namespace] = None,
        **kwargs: Any,
    ) -> Iterator[rdflib.Graph]:
        """Applies Mapping for the `survey_site_data.csv` Template

        Args:
            data (base.types.ReadableType): Valid raw data to be mapped.
            dataset_iri (Optional[rdflib.URIRef]): Optional dataset IRI.
            base_iri (Optional[rdflib.Namespace]): Optional mapping base IRI.

        Keyword Args:
            chunk_size (Optional[int]): How many rows of the original data to
                ingest before yielding a graph. `None` will ingest all rows.

        Yields:
            rdflib.Graph: ABIS Conformant RDF Sub-Graph from Raw Data Chunk.
        """
        # Construct Schema
        schema = self.extra_fields_schema(
            data=data,
            full_schema=True,
        )

        # Construct Resource
        resource = frictionless.Resource(
            data=data,
            format="csv",   # TODO -> Hardcoded to csv for now
            schema=schema,
        )

        # Initialise Graph
        graph = utils.rdf.create_graph()

        # Check if Dataset IRI Supplied
        if not dataset_iri:
            # Create Dataset IRI
            dataset_iri = utils.rdf.uri(f"dataset/{self.DATASET_DEFAULT_NAME}", base_iri)

            # Add the default dataset
            self.add_default_dataset(
                uri=dataset_iri,
                graph=graph,
            )

        # Open the Resource to allow row streaming
        with resource.open() as r:
            # Loop through rows
            for row in r.row_stream:
                # Map row
                self.apply_mapping_row(
                    row=row,
                    dataset=dataset_iri,
                    graph=graph,
                    base_iri=base_iri,
                )

            yield graph

    def apply_mapping_row(
        self,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
        base_iri: Optional[rdflib.Namespace],
    ) -> None:
        """Applies mapping for a row in the `survey_site_data.csv` template.

        Args:
            row (frictionless.Row): Row to be processed in the dataset.
            dataset (rdflib.URIRef): Dataset IRI this row is a part of.
            graph (rdflib.URIRef): Graph to map row into.
            base_iri (Optional[rdflib.Namespace]): Optional base IRI
                to use for mapping.
        """
        # Set the row number to start from the data, excluding header
        row_num = row.row_number - 1

        site_visit = utils.rdf.uri(f"visit/site/{row_num}", base_iri)
        site = dataset + f"/Site/{row['siteID']}"

        # Add site
        self.add_site(
            uri=site,
            dataset=dataset,
            site_visit=site_visit,
            row=row,
            graph=graph,
        )

        # Add site visit
        self.add_site_visit(
            uri=site_visit,
            dataset=dataset,
            graph=graph,
        )

        # Add temporal entity
        self.add_temporal_entity(
            uri=site_visit,
            row=row,
            graph=graph,
        )

        # Add geometry
        self.add_footprint_geometry(
            uri=site,
            row=row,
            graph=graph,
        )

        self.add_point_geometry(
            uri=site,
            row=row,
            graph=graph,
        )

        # Add extra fields
        self.add_extra_fields_json(
            subject_uri=site,
            row=row,
            graph=graph,
        )

    def add_site(
        self,
        uri: rdflib.URIRef,
        dataset: rdflib.URIRef,
        site_visit: rdflib.URIRef,
        row: frictionless.Row,
        graph: rdflib.Graph,
    ) -> None:
        """Adds site to the graph.

        Args:
           uri (rdflib.URIRef): URI to use for this node.
           dataset (rdflib.URIRef): Dataset to which data belongs.
           site_visit (rdflib.URIRef): Site visit the site corresponds to.
           row (frictionless.Row): Row to retrieve data from.
           graph (rdflib.Graph): Graph to be modified.
        """
        # Extract relevant values
        site_id = row["siteID"]
        site_name = row["siteName"]
        site_type = row["siteType"]
        site_description = row["siteDescription"]
        coordinate_uncertainty = row["coordinateUncertaintyInMeters"]

        # Add type
        graph.add((uri, a, utils.namespaces.TERN.Site))

        # Add dataset
        graph.add((uri, rdflib.VOID.inDataset, dataset))

        # Link to site visit
        graph.add((uri, utils.namespaces.TERN.hasSiteVisit, site_visit))

        # Add siteID
        graph.add((uri, rdflib.DCTERMS.identifier, rdflib.Literal(site_id)))

        # Add site tern featuretype
        graph.add((uri, utils.namespaces.TERN.featureType, vocabs.site_type.SITE.iri))

        # Retrieve vocab or create on the fly
        vocab = vocabs.site_type.SITE_TYPE.get(
            graph=graph,
            value=site_type,
            source=dataset,
        )

        # Add to site type graph
        graph.add((uri, rdflib.DCTERMS.type, vocab))

        # Add site name if available
        if site_name:
            graph.add((uri, rdflib.SDO.name, rdflib.Literal(site_name)))

        # Add site description if available
        if site_description:
            graph.add((uri, rdflib.SDO.description, rdflib.Literal(site_description)))

        # Add coordinate uncertainty if available
        if coordinate_uncertainty:
            accuracy = rdflib.Literal(coordinate_uncertainty, datatype=rdflib.XSD.double)
            graph.add((uri, utils.namespaces.GEO.hasMetricSpatialAccuracy, accuracy))

    def add_site_visit(
        self,
        uri: rdflib.URIRef,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds site visit to the graph.

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            dataset (rdflib.URIRef): Dataset to which data belongs.
            graph (rdflib.Graph): Graph to be modified.
        """
        # Add type
        graph.add((uri, a, utils.namespaces.TERN.SiteVisit))

        # Add to dataset
        graph.add((uri, rdflib.VOID.inDataset, dataset))

    def add_temporal_entity(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        graph: rdflib.Graph,
    ) -> None:
        """Adds visit times to the graph.

        Args:
            uri (rdflib.URIRef): URI that data will be associated.
            row (frictionless.Row): Row to retrieve data from.
            graph (rdflib.URIRef): Graph to be modified.
        """
        # Extract values
        site_visit_start: utils.types.Timestamp = row["siteVisitStart"]
        site_visit_end: utils.types.Timestamp = row["siteVisitEnd"]

        # Create temporal entity node
        temporal_entity = rdflib.BNode()
        graph.add((temporal_entity, a, rdflib.TIME.TemporalEntity))

        # Add dates
        graph.add((temporal_entity, rdflib.TIME.hasBeginning, site_visit_start.to_rdf_literal()))
        if site_visit_end:
            graph.add((temporal_entity, rdflib.TIME.hasEnd, site_visit_end.to_rdf_literal()))

        # Attach to node
        graph.add((uri, rdflib.TIME.hasTime, temporal_entity))

    def add_footprint_geometry(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        graph: rdflib.Graph,
    ) -> None:
        """Adds footprint geometry details to the graph.

        Args:
            uri (rdflib.URIRef): URI to attach.
            row (frictionless.Row): Row to retrieve data from.
            graph (rdflib.Graph): Graph to be modified.
        """
        # Extract values
        geodetic_datum = row["geodeticDatum"]
        footprint_wkt = row["footprintWKT"]

        if not footprint_wkt:
            return

        # Construct wkt literal
        wkt = utils.rdf.to_wkt_literal(
            geometry=footprint_wkt,
            datum=vocabs.geodetic_datum.GEODETIC_DATUM.get(geodetic_datum),
        )

        # Construct node
        geometry_node = rdflib.BNode()
        graph.add((geometry_node, a, utils.namespaces.GEO.Geometry))
        graph.add((geometry_node, utils.namespaces.GEO.asWKT, wkt))
        graph.add((uri, utils.namespaces.GEO.hasGeometry, geometry_node))

    def add_point_geometry(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        graph: rdflib.Graph,
    ) -> None:
        """Adds site point geometry details to the graph.

        Args:
            uri (rdflib.URIRef): URI to attach.
            row (frictionless.Row): Row to retrieve data from.
            graph (rdflib.Graph): Graph to be modified.
        """
        # Extract values
        decimal_latitude = row["decimalLatitude"]
        decimal_longitude = row["decimalLongitude"]
        geodetic_datum = row["geodeticDatum"]

        if not decimal_latitude or not decimal_longitude:
            return

        # Construct wkt literal
        wkt = utils.rdf.to_wkt_point_literal(
            latitude=decimal_latitude,
            longitude=decimal_longitude,
            datum=vocabs.geodetic_datum.GEODETIC_DATUM.get(geodetic_datum),
        )

        # Construct node
        geometry_node = rdflib.BNode()
        graph.add((geometry_node, a, utils.namespaces.GEO.Geometry))
        graph.add((geometry_node, utils.namespaces.GEO.asWKT, wkt))
        graph.add((uri, utils.namespaces.GEO.hasGeometry, geometry_node))


# Register Mapper
base.mapper.ABISMapper.register_mapper(SurveySiteMapper)
