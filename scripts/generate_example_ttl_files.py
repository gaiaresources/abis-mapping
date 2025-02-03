"""Script to generate all example .ttl files from example CSV inputs.

Should be run after making any changes to template mapping,
to update the example ttl files with the result of those mapping changes."""

# standard library
import collections
import collections.abc
import hashlib
import inspect
import itertools
import pathlib
import unittest.mock

# third-party
import rdflib

# local
import abis_mapping
import abis_mapping.models.temporal
import tests.helpers
import tests.templates.conftest

# Global vars
COUNTERS: collections.abc.Mapping[bytes, collections.abc.Iterator[int]] = collections.defaultdict(itertools.count)
TTL_FILE_PATH: str = ""


def main() -> None:
    global TTL_FILE_PATH

    # Gather the example files to be regenerated.
    examples: list[tuple[str, pathlib.Path, pathlib.Path]] = [
        (template_test.template_id, mapping_test.data, mapping_test.expected)
        for template_test in tests.templates.conftest.TEST_CASES
        for mapping_test in template_test.mapping_cases
        if mapping_test.expected is not None
    ]

    # In order to produce consistent ttl output, and reduce the git diff
    # each time the mapping is changed, this script overrides some behavior.

    # 1. First override:
    # Here we override the BNode id generation function to generate IDs based on the
    # hash on the ttl file path being generated, and the
    # current stack of functions that were called to reach the BNode() call.
    # This is so that BNode IDs that are embedded in the ttl output,
    # are consistent between runs of this script,
    # and are consistent for a particular code path.

    # Check rdflib.BNode.__new__ has signature we expect
    b_node_signature = inspect.signature(rdflib.BNode.__new__)
    expected_params = ["cls", "value", "_sn_gen", "_prefix"]
    actual_params = [p.name for p in b_node_signature.parameters.values()]
    defaults = rdflib.BNode.__new__.__defaults__
    if actual_params != expected_params or defaults != (None, None, "N"):
        raise RuntimeError("BNode.__new__ had unexpected signature, the following code might need to be updated")
    # Override default _sn_gen function with our custom one.
    rdflib.BNode.__new__.__defaults__ = (defaults[0], _custom_sn_gen, defaults[2])

    # 2. second override:
    # Mock "Date.today()" function to always give the same result
    unittest.mock.patch.object(
        abis_mapping.models.temporal.Date,
        "today",
        new=lambda: abis_mapping.models.temporal.Date(2020, 1, 1),
    ).start()

    # Finished overrides.

    # Generate new ttl files.
    for template_id, input_csv_file_path, output_ttl_file_path in examples:
        print(f"Generating {output_ttl_file_path}...")

        # set global var
        TTL_FILE_PATH = str(output_ttl_file_path)

        # Get Mapper
        mapper = abis_mapping.get_mapper(template_id)
        if mapper is None:
            raise RuntimeError(f"Mapper not found for {template_id}")
        # Map data
        data = input_csv_file_path.read_bytes()
        graphs = list(
            mapper().apply_mapping(
                data=data,
                chunk_size=None,
                dataset_iri=tests.helpers.TEST_DATASET_IRI,
                base_iri=tests.helpers.TEST_BASE_NAMESPACE,
                submission_iri=tests.helpers.TEST_SUBMISSION_IRI,
            )
        )
        if len(graphs) != 1:
            raise RuntimeError("apply_mapping did not produce exactly 1 graph")
        # Write to output file
        graphs[0].serialize(destination=output_ttl_file_path, format="turtle")

    print("Done!")


def _custom_sn_gen() -> str:
    """Generate a BNode ID depending on the ttl file and the current code path.

    Returns:
        String to use for a BNode ID. Should be 32 hex digits to match rdflib default behavior.
    """
    # Generate ID with 32 hex digits (16 bytes) to match the normal behavior (which is uuid4().hex)
    # First 12 bytes are from hash of ttl file path and the code path taken to create the BNode().
    # Remaining 4 bytes are taken from a counter unique to the hash result.
    # i.e. when the same hash occurs, they will be numbered 0,1,2,etc. at the end of the ID.
    # This ensures each ID should be globally unique.
    code_path_hash = hashlib.blake2b(digest_size=12, person=b"gen_b_node_id")
    # hash ttl file path.
    code_path_hash.update(TTL_FILE_PATH.encode("utf-8"))
    # Hash functions in the abis_mapping module called to make this BNode()
    for frame in inspect.stack():
        # NOTE "abis_mapping" with underscore is the module name.
        # NOT "abis-mapping" with a dash which is the repository name.
        if "abis_mapping" in frame.filename:
            code_path_hash.update(frame.function.encode("utf-8"))
            # we don't include the frame.filename in the hash because this wil be
            # different depending on where abis-mapping is checked out.
    digest = code_path_hash.digest()
    number = next(COUNTERS[digest]).to_bytes(4, "big")
    return (digest + number).hex()  # concatenate bytes and return hex representation


if __name__ == "__main__":
    main()
