"""Route files to the correct loader for convert to a collection."""

import pathlib

from solver.lib import json2collection
from solver.lib.collection import ContainerCollection


def load(path: str, reject_invalid: bool) -> ContainerCollection:
    """Load a file based on it's extension."""
    file = pathlib.Path(path)
    if file.suffix == ".json":
        with file.open(encoding="utf-8") as fh:
            return json2collection.load(fh, reject_invalid=reject_invalid)
    else:
        raise ValueError(
            f"Unsupported file extension: {file.suffix}. Only .json is supported."
        )
