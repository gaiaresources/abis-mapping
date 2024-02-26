import tempfile
import os
import shutil
import abis_mapping.templates.incidental_occurrence_data.mapping

from typing import BinaryIO


def test_apply_validation() -> None:
    """Tests behaviour of apply validation with file stream input."""
    # Open up input file stream
    fp: BinaryIO = open(
        "abis_mapping/templates/incidental_occurrence_data/examples/margaret_river_flora/margaret_river_flora.csv",
        "rb"
    )
    # Copy to tempfile to simulate usage via backend
    tf = tempfile.NamedTemporaryFile(delete=False)
    shutil.copyfileobj(fp, tf)
    fp.close()

    assert isinstance(tf, tempfile._TemporaryFileWrapper)

    # Get mapper and produce report
    mapper = abis_mapping.templates.incidental_occurrence_data.mapping.IncidentalOccurrenceMapper()
    report = mapper.apply_validation(
        data=tf
    )

    # Both file objects should now be closed
    assert fp.closed
    assert tf.closed
    # Check to see tempfile still available at this stage
    assert os.path.exists(tf.name)
    # Check to see tempfile can be reopened
    with open(tf.name) as ftf:
        assert not ftf.closed
        assert ftf.tell() == 0
    # Make sure tempfile object closed
    assert ftf.closed
    # Delete tempfile from filesystem
    os.unlink(tf.name)
    assert not os.path.exists(tf.name)
    # Validation worked as expected.
    assert report.valid
