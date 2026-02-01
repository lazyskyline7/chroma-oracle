"""Tests for the json2collection module."""

import pathlib
from unittest import TestCase

from chroma_oracle.lib import json2collection
from chroma_oracle.lib.collection import ContainerCollection


class TestJson2Collection(TestCase):
    """Test cases for the json2collection class."""

    def test_load_valid(self):
        """Test loading from a valid json file."""
        expected = ContainerCollection(
            [
                ["RED", "RED", "GREEN", "GREEN"],
                ["RED", "RED", "GREEN", "GREEN"],
                [],
            ]
        )
        with pathlib.Path("./levels/debug.json").open(encoding="utf-8") as reader:
            collection = json2collection.load(reader)
        self.assertEqual(collection, expected)

    def test_load_invalid_ignore(self):
        """Test loading from a invalid json file and not rejecting it."""
        expected = ContainerCollection(
            [
                ["RED", "RED", "GREEN", "GREEN"],
                ["RED", "RED", "RED", "GREEN"],
                [],
            ]
        )
        with pathlib.Path("./levels/bad.json").open(encoding="utf-8") as reader:
            collection = json2collection.load(reader, reject_invalid=False)
        self.assertEqual(collection, expected)

    def test_load_invalid_(self):
        """Test loading from a invalid json file and rejecting it."""
        with self.assertRaises(ValueError):  # noqa: SIM117
            with pathlib.Path("./levels/bad.json").open(encoding="utf-8") as reader:
                _ = json2collection.load(reader, reject_invalid=True)
