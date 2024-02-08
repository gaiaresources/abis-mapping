
from abis_mapping import base
import tempfile
import os
import shutil

from typing import BinaryIO

def test_apply_validation() -> None:
    fp = open(
        "abis_mapping/templates/incidental_occurrence_data/examples/margaret_river_flora/margaret_river_flora.csv",
        "rb"
    )
    tf = tempfile.NamedTemporaryFile(delete=False)
    shutil.copyfileobj(fp, tf)
    fp.close()

    mapper = base.mapper.get_mapper("incidental_occurrence_data.csv")
    report = mapper().apply_validation(
        data=tf
    )

    assert fp.closed
    assert tf.closed
    assert os.path.exists(tf.name)
    os.unlink(tf.name)
    assert not os.path.exists(tf.name)
    assert report.valid
