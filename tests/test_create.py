import json
import pathlib
import zipfile

import pytest
from jsonschema import RefResolver, validate

from wakeword_training_record.create import _get_path, _write_wakeword_json, create


def validate_json(json_data, schema_name):
    """
    Validate payload with selected schema
    """
    schemas_dir = str(f"{pathlib.Path(__file__).parent.absolute()}/schemas")
    schema = json.loads(pathlib.Path(f"{schemas_dir}/{schema_name}").read_text())
    validate(
        json_data,
        schema,
        resolver=RefResolver(
            "file://" + str(pathlib.Path(f"{schemas_dir}/{schema_name}").absolute()),
            schema,  # it's used to resolve the file inside schemas correctly
        ),
    )


def test_write_wakeword_json(tmpdir):
    file = tmpdir.join("output.zip")
    data = {"key1": "value1", "key2": "value2"}
    _write_wakeword_json(file, data)
    assert file.check() == 1
    assert len(tmpdir.listdir()) == 1


def test_get_path_wakeword(tmpdir):
    path = str(tmpdir)
    p = _get_path(path, "test word")
    assert str(p) == f"{path}/wakeword-recording-test-word.zip"
    p.write_text("dummy")

    p_uuid = _get_path(path, "test word")
    p_uuid.write_text("dummy")
    assert str(p_uuid) != f"{path}/wakeword-recording-test-word.zip"
    assert len(tmpdir.listdir()) == 2

    with pytest.raises(FileExistsError):
        p = _get_path((str(p)), "test word")


def test_crate(tmpdir):

    create(
        tmpdir,
        "test word",
        syllables=["tes", "t", "wor", "d"],
        words=["test", "word"],
        language="en",
    )
    testpath = tmpdir / "wakeword-recording-test-word.zip"
    assert testpath.check()
    with pytest.raises(FileExistsError):
        create(
            testpath,
            "test word",
            syllables=["tes", "t", "wor", "d"],
            words=["test", "word"],
            language="en",
        )

    create(
        testpath,
        "test word",
        syllables=["tes", "t", "wor", "d"],
        words=["test", "word"],
        similar=["test world", "best word"],
        language="en",
        overwrite=True,
    )
    with zipfile.ZipFile(testpath, "r") as z:
        # Write the JSON string to the json_file
        data = json.loads(z.read("wakeword/wakeword.json"))
        validate_json(data, "wakeword.json")
