"""Unit tests for the Move data type."""

from unittest import TestCase

from chroma_oracle.lib.move import Move


class TestMove(TestCase):
    """Test cases for Move."""

    def test_move(self):
        """Ensure that move str() and reverse work."""
        move = Move(1, 2)
        self.assertEqual(move.src, 1, "Move source should be 1")
        self.assertEqual(move.dest, 2, "Move destination should be 2")
        self.assertEqual(
            str(move),
            "(1, 2)",
            "Move string representation should be formatted as a tuple",
        )
        self.assertEqual(
            repr(move),
            "Move(src=1, dest=2)",
            "Move debug representation should be verbose",
        )

    def test_move_reverse(self):
        """Ensure that move reverse works."""
        move = Move(1, 2)
        reverse_move = Move(2, 1)
        self.assertEqual(move.reverse(), reverse_move, "Move reversed should be (2, 1)")
