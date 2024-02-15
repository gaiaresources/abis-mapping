
import tempfile
import os
import shutil
import abis_mapping.templates.incidental_occurrence_data.mapping

from typing import BinaryIO, IO

def test_apply_validation() -> None:
    fp: BinaryIO = open(
        "abis_mapping/templates/incidental_occurrence_data/examples/margaret_river_flora/margaret_river_flora.csv",
        "rb"
    )
    tf = tempfile.NamedTemporaryFile(delete=False)
    shutil.copyfileobj(fp, tf)
    fp.close()

    mapper = abis_mapping.templates.incidental_occurrence_data.mapping.IncidentalOccurrenceMapper()
    report = mapper.apply_validation(
        data=tf
    )

    assert fp.closed
    assert tf.closed
    assert os.path.exists(tf.name)
    os.unlink(tf.name)
    assert not os.path.exists(tf.name)
    assert report.valid
