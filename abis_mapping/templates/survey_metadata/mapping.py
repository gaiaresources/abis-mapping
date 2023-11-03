"""Provides ABIS mapper for `survey_metadata.csv` template"""

# Local
from abis_mapping import base
from abis_mapping import plugins
from abis_mapping import utils

# Standard
import datetime

# Third-party
import frictionless
import rdflib

# Typing
from typing import Optional, Iterator, Any


# Default Dataset Metadata
DATASET_DEFAULT_NAME = "Example Systematic Survey Metadata Dataset"
DATASET_DEFAULT_DESCRIPTION = "Example Systematic Survey Metadata Dataset by Gaia Resources"

# Constants / shortcuts
a = rdflib.RDF.type


class SurveyMetadataMapper(base.mapper.ABISMapper):
    template_id = "survey_metadata.csv"
    instructions_file = "instructions.pdf"

    def apply_validation(
            self,
            data: base.types.ReadableType
    ) -> frictionless.Report:
        """Applies Frictionless validation for the 'survey_metadata.csv' template

        Args:
            data (base.types.ReadableType): Raw data to be validated

        Returns:
            frictionless.Report: Validation report for the specified data.
        """
        # Construct Schema
        schema = frictionless.Schema.from_descriptor(self.schema())

        # Construct Resource
        resource = frictionless.Resource(
            data=data,
            format="csv",  # TODO -> Hardcoded to csv for now
            schema=schema,
        )

        # Validate
        report: frictionless.Report = resource.validate(
            checklist=frictionless.Checklist(
                checks=[
                    # Extra Custom Checks
                    plugins.tabular.IsTabular(),
                    plugins.empty.NotEmpty(),
                    plugins.chronological.ChronologicalOrder(
                        field_names=[
                            "temporalCoverageStartDate",
                            "temporalCoverageEndDate",
                        ]
                    ),
                    plugins.mutual_inclusion.MutuallyInclusive(
                        field_names=[
                            "spatialCoverageWKT",
                            "spatialCoverageGeodeticDatum",
                        ]
                    ),
                ],
                skip_errors=self.skip_errors
            ),
        )

        # Return validation report
        return report

    def apply_mapping(
            self,
            data: base.types.ReadableType,
            dataset_iri: Optional[rdflib.URIRef] = None,
            base_iri: Optional[rdflib.Namespace] = None,
            **kwargs: Any,
    ) -> Iterator[rdflib.Graph]:
        """Applies mapping for the `survey_metadata.csv` template.

        Args:
            data (base.types.ReadableType): Valid raw data to be mapped.
            dataset_iri (Optional[rdflib.URIRef]): Optional dataset IRI.
            base_iri (Optional[rdflib.Namespace]): Optional mapping base IRI.
            **kwargs (Any): Additional keyword arguments.

        Yields:
            rdflib.Graph: ABIS conformant RDF sub-graph from raw data chunk.
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
            dataset_iri = utils.rdf.uri(f"dataset/{DATASET_DEFAULT_NAME}", base_iri)

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

    def add_default_dataset(
        self,
        uri: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds Default Example Dataset to the Graph

        Args:
            uri (rdflib.URIRef): IRI of the dataset.
            graph (rdflib.Graph): Graph to add to.
        """
        # Add Default Dataset to Graph
        graph.add((uri, a, utils.namespaces.TERN.RDFDataset))
        graph.add((uri, rdflib.DCTERMS.title, rdflib.Literal(DATASET_DEFAULT_NAME)))
        graph.add((uri, rdflib.DCTERMS.description, rdflib.Literal(DATASET_DEFAULT_DESCRIPTION)))
        graph.add((uri, rdflib.DCTERMS.issued, utils.rdf.toTimestamp(datetime.date.today())))

    def apply_mapping_row(
        self,
        row: frictionless.Row,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
        base_iri: Optional[rdflib.Namespace] = None,
    ) -> None:
        """Applies mapping for a row in the `survey_metadata.csv` template.

        Args:
            row (frictionless.Row): Row to be processed in the dataset.
            dataset (rdflib.URIRef): Dataset IRI this row is a part of.
            graph (rdflib.URIRef): Graph to map row into.
            base_iri (Optional[rdflib.Namespace): Optional base IRI
                to use for mapping.
        """
        # Set the row number to start from the data, excluding header
        row_num = row.row_number - 1

        # Create BDR project IRI
        bdr_project = utils.rdf.uri(f"project/SSD-Survey-Project/{row_num}", base_iri)

        # Create BDR survey IRI
        bdr_survey = utils.rdf.uri(f"survey/SSD-Survey/{row_num}", base_iri)

        # Create survey method procedure IRI
        survey_method_procedure = utils.rdf.uri(f"survey/procedure/surveyMethod/{row_num}", base_iri)

        # Add BDR project
        self.add_bdr_project(
            uri=bdr_project,
            survey=bdr_survey,
            dataset=dataset,
            graph=graph,
            row=row,
        )

        # Add BDR survey
        self.add_bdr_survey(
            uri=bdr_survey,
            survey_method=survey_method_procedure,
            graph=graph,
        )

        # Attach temporal coverage if present
        self.add_temporal_coverage(
            uri=bdr_survey,
            row=row,
            graph=graph,
        )

        # Add survey method urls
        self.add_survey_methodologies(
            uri=survey_method_procedure,
            row=row,
            graph=graph,
        )

        # Add extra columns JSON
        self.add_extra_fields_json(
            subject_uri=bdr_survey,
            row=row,
            graph=graph,
        )

    def add_bdr_project(
        self,
        uri: rdflib.URIRef,
        survey: rdflib.URIRef,
        dataset: rdflib.URIRef,
        graph: rdflib.Graph,
        row: frictionless.Row,
    ) -> None:
        """Adds the BDR project to the graph

        Args:
            uri (rdflib.URIRef): URI to use for this node.
            survey (rdflib.URIRef): BDR survey uri.
            dataset (rdflib.URIRef): Dataset uri.
            graph (rdflib.Graph): Graph to add to.
            row (frictionless.Row): Row to be processed in dataset.
        """
        # Extract relevant values from row
        project_id = row["projectID"]
        project_name = row["projectTitleOrName"]
        purpose = row["purpose"]

        # Add type and attach to dataset
        graph.add((uri, a, utils.namespaces.BDR.Project))
        graph.add((uri, rdflib.VOID.inDataset, dataset))

        # Add (required) project name, id (not required) and purpose (not required).
        graph.add((uri, rdflib.DCTERMS.title, rdflib.Literal(project_name)))
        if project_id:
            graph.add((uri, rdflib.DCTERMS.identifier, rdflib.Literal(project_id)))
        if purpose:
            graph.add((uri, rdflib.DCTERMS.description, rdflib.Literal(purpose)))

        # Attach survey
        graph.add((uri, utils.namespaces.BDR.hasSurvey, survey))

    def add_bdr_survey(
        self,
        uri: rdflib.URIRef,
        survey_method: rdflib.URIRef,
        graph: rdflib.Graph,
    ) -> None:
        """Adds the BDR survey to the graph.

        Args:
            uri (rdflib.URIRef): URI of the survey.
            survey_method (rdflib.URIRef): URI of node associated with
                survey method data.
            graph (rdflib.Graph): The graph to be modified.
        """
        # Add type and dataset
        graph.add((uri, a, utils.namespaces.BDR.Survey))

        # Add survey method procedure node
        graph.add((uri, rdflib.SOSA.usedProcedure, survey_method))

    def add_temporal_coverage(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        graph: rdflib.Graph,
    ) -> None:
        """Adds the temporal coverage fields to the graph.

        Args:
            uri (rdflib.URIRef): Base URI the temporal information will be attached
            row (frictionless.Row): Data row provided in the data csv
            graph (rdflib.Graph): Graph to be modified
        """
        # Determine if any dates are present in the row
        start_date = row["temporalCoverageStartDate"]
        end_date = row["temporalCoverageEndDate"]
        if not start_date and not end_date:
            return

        # Create temporal coverage node
        temporal_coverage = rdflib.BNode()
        graph.add((temporal_coverage, a, rdflib.TIME.TemporalEntity))
        if start_date:
            graph.add((temporal_coverage, rdflib.TIME.hasBeginning, utils.rdf.toTimestamp(start_date)))
        if end_date:
            graph.add((temporal_coverage, rdflib.TIME.hasEnd, utils.rdf.toTimestamp(end_date)))

        # Attach to survey node
        graph.add((uri, rdflib.TIME.hasTime, temporal_coverage))

    def add_survey_methodologies(
        self,
        uri: rdflib.URIRef,
        row: frictionless.Row,
        graph: rdflib.Graph,
    ) -> None:
        """Adds the survey methodology URIs to the graph.

        Args:
            uri (rdflib.URIRef): Base URI the methodologies will be attached.
            row (frictionless.Row): Row containing CSV data row contents.
            graph (rdflib.Graph): Graph to be modified.
        """
        # Extract relevant values from row
        survey_method_urls = row["surveyMethodURL"]
        survey_method_description = row["surveyMethodDescription"]
        survey_method_refs = row["surveyMethodBibliographicReferences"]

        # If no relevant data provided then no change to graph
        if not (survey_method_urls or survey_method_description or survey_method_refs):
            return

        # Add type
        graph.add((uri, a, rdflib.SOSA.Procedure))

        # Attach survey methodologies
        if survey_method_urls:
            for survey_method_url in survey_method_urls:
                # Add literal containing the method URL
                graph.add((
                    uri,
                    rdflib.RDFS.isDefinedBy,
                    rdflib.Literal(survey_method_url, datatype=rdflib.XSD.anyURI)
                ))

        if survey_method_description:
            # Add literal containing the description
            graph.add((
                uri,
                rdflib.SKOS.definition,
                rdflib.Literal(survey_method_description),
            ))

        if survey_method_refs:
            for survey_method_ref in survey_method_refs:
                # Add bibliographic reference
                graph.add((
                    uri,
                    rdflib.SDO.citation,
                    rdflib.Literal(survey_method_ref),
                ))


base.mapper.ABISMapper.register_mapper(SurveyMetadataMapper)
