"""Represent a single move between to containers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Move:
    """Represents a move between two containers in the game."""

    src: int
    dest: int

    def reverse(self) -> Move:
        """Get the reverse of this move."""
        return Move(self.dest, self.src)

    def __str__(self) -> str:  # keep __repr__ as dataclass default
        """String representation matching tuple style for CLI/tests."""
        return f"({self.src}, {self.dest})"
