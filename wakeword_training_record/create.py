import json
import logging
import uuid
import zipfile
from pathlib import Path

_logger = logging.getLogger(__package__)


def create(
    path, wakeword, syllables=[], words=[], language="", similar="", overwrite=False
):
    wakeword_dict = {
        "language": language,
        "wakeword": wakeword,
        "syllabels": syllables,
        "words": words,
        "similar": similar,
    }

    if overwrite:
        p = Path(path)
        if p.is_file():
            p.unlink()

    p = _get_path(path, wakeword)
    _write_wakeword_json(p, wakeword_dict)


def _get_path(path, wakeword):
    """Generates a path for a new wakeword traning record

    Args:
        path (String): Path to a folder or a file where to create the new file
        wakeword (String): Wakeword

    Raises:
        FileExistsError: If a path to a .zip file is provided and that file exist

    Returns:
        Path: path of where to create the wakeword .zip file
    """
    path = Path(path)
    if path.suffix == ".zip":
        if path.exists():
            raise FileExistsError()
        else:
            return path

    if path.is_dir():
        p = path / f"wakeword-recording-{'-'.join( wakeword.split() )}.zip"
        if p.exists() is False:
            return p
        p = (
            path
            / f"wakeword-recording-{'-'.join( wakeword.split() )}-{uuid.uuid4()}.zip"
        )
        return p


def _write_wakeword_json(zip_file, dict):
    # Convert the dict to a JSON string
    json_data = json.dumps(dict, indent=2)
    # Open the zip file for writing
    with zipfile.ZipFile(zip_file, "w") as z:
        # Write the JSON string to the json_file
        z.writestr("wakeword/wakeword.json", json_data)
