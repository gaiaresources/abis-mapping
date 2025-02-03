"""Helper utilities for testing."""

# Standard Library
import collections.abc
import contextlib
import json

# Third-party
import pydantic_settings
import rdflib
import rdflib.compare

# Local
from abis_mapping import settings


# Whenever a test needs to call apply_mapping(), use these for dataset_iri and base_iri.
TEST_DATASET_IRI = rdflib.URIRef("https://linked.data.gov.au/dataset/bdr/00000000-0000-0000-0000-000000000000")
TEST_BASE_NAMESPACE = rdflib.Namespace("https://linked.data.gov.au/dataset/bdr/00000000-0000-0000-0000-000000000000/")
TEST_SUBMISSION_IRI = rdflib.URIRef(
    "https://linked.data.gov.au/dataset/bdr/submission/00000000-0000-0000-0000-000000000000"
)


@contextlib.contextmanager
def override_settings(**overrides: object) -> collections.abc.Iterator[None]:
    """Context manager to override any number of settings,
    and restore the original settings at the end.

    This is non-trivial since the settings object is frozen.

    Args:
        **overrides:
            Pass settings to override as keyword arguments.

    Returns:
        Context manager to override the settings.
    """
    # Get current settings.
    initial_settings = settings.SETTINGS
    # Make new settings object and override settings with it
    settings.SETTINGS = TestSettings(**(initial_settings.model_dump() | overrides))

    yield

    # Restore the original settings on context exit
    settings.SETTINGS = initial_settings


class TestSettings(settings._Settings):
    """Version of the settings to use in the test suite."""

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[pydantic_settings.BaseSettings],
        init_settings: pydantic_settings.PydanticBaseSettingsSource,
        env_settings: pydantic_settings.PydanticBaseSettingsSource,
        dotenv_settings: pydantic_settings.PydanticBaseSettingsSource,
        file_secret_settings: pydantic_settings.PydanticBaseSettingsSource,
    ) -> tuple[pydantic_settings.PydanticBaseSettingsSource, ...]:
        """
        Define the sources and their order for loading the settings values.

        Args:
            settings_cls: The Settings class.
            init_settings: The `InitSettingsSource` instance.
            env_settings: The `EnvSettingsSource` instance.
            dotenv_settings: The `DotEnvSettingsSource` instance.
            file_secret_settings: The `SecretsSettingsSource` instance.

        Returns:
            A tuple containing the sources and their order for loading the settings values.
        """
        # In the tests, ignore all env, dotenv and secrets settings.
        # This is so the test suite is deterministic and isolated,
        # and won't be effected by any settings a particular developer has set locally.
        return (init_settings,)


def compare_graphs(
    graph1: rdflib.Graph | str,
    graph2: rdflib.Graph | str,
) -> bool:
    """Isomorphically compares to graphs for equality.

    Args:
        graph1: Graph or Turtle String to Compare
        graph2: Graph or Turtle String to Compare

    Returns:
        Whether the graphs are isomorphically equivalent.
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
        for s, p, o in graph.triples((None, None, None)):
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
