"""Simulation helpers used by CLI to replay move sequences on grids.

This module provides a single helper `simulate_moves_on_grid` which
attempts to apply a sequence of Move objects to a given grid (list of
container lists) and returns either the final grid or the index of the
first failing move.

The function is pure (no printing) so callers can decide how to report
results.
"""

from chroma_oracle.lib.collection import ContainerCollection
from chroma_oracle.lib.move import Move


def simulate_moves_on_grid(
    grid: list[list[str]], moves: list[Move]
) -> tuple[list[list[str]], int | None]:
    """Attempt to apply `moves` to `grid`.

    Args:
        grid: The puzzle grid as nested lists (as used elsewhere in the repo).
        moves: Sequence of Move objects to apply in order.

    Returns:
        (final_grid, None) if all moves succeed, where final_grid is the
        resulting grid after applying all moves.

        (partial_grid, failing_index) if a move fails to simulate. The
        partial_grid is the grid after applying moves up to but not
        including the failing move. `failing_index` is the 0-based index
        of the move that could not be applied.
    """
    try:
        coll = ContainerCollection(grid)
    except Exception:
        # If the grid cannot be constructed into a collection, treat as
        # immediate failure at move 0 with the original grid returned.
        return grid, 0

    current = coll
    for i, move in enumerate(moves):
        try:
            if not current.is_valid(move):
                # Return the grid state prior to failing move
                out_grid = [[item.colour.name for item in c.data] for c in current.data]
                return out_grid, i
            current = current.after(move)
        except Exception:
            out_grid = [[item.colour.name for item in c.data] for c in current.data]
            return out_grid, i

    # Success: return final grid and no failing index
    final_grid = [[item.colour.name for item in c.data] for c in current.data]
    return final_grid, None
