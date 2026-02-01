"""Shared printing utilities for CLI output."""

from collections.abc import Iterable

from solver.lib.move import Move


def print_moves(moves: Iterable[Move]) -> None:
    """Print moves in the standardized numbered format.

    Kept as a separate function to allow reuse across multiple CLI commands.
    """
    for i, move in enumerate(moves, 1):
        print(f"{i}. Container {move.src} -> {move.dest}")
