"""Library helpers for finding solutions and common prefixes.

These functions are refactored out of the CLI-facing win_strategy module so
other parts of the codebase (CLI and interactive) can reuse the logic
without inheriting its user-facing printing and SystemExit behaviour.
"""

from solver.lib.collection import ContainerCollection
from solver.lib.move import Move
from solver.lib.search import bfs, dfs
from solver.lib.unknown_solver import (
    calculate_needed_colors,
    generate_candidate_grids,
    load_puzzle_with_unknowns,
    solve_all_candidates,
)


def find_all_solutions(
    puzzle_path: str, algorithm: str = "BFS"
) -> list[tuple[list[list[str]], tuple[Move, ...]]]:
    """Find all valid solutions for a puzzle with unknowns.

    Unlike the CLI variant, this function avoids printing and exiting the
    process. It returns a list of (candidate_grid, moves) pairs.
    """
    data = load_puzzle_with_unknowns(puzzle_path)

    if not data.unknown_indices:
        try:
            collection = ContainerCollection(data.raw_grid)
            result = bfs(collection) if algorithm == "BFS" else dfs(collection)
            if result:
                return [(data.raw_grid, result.moves)]
        except (ValueError, TypeError):
            return []

    needed = calculate_needed_colors(data)
    if needed is None:
        return []

    candidate_grids = generate_candidate_grids(data, needed)
    solutions = solve_all_candidates(candidate_grids, algorithm)
    return solutions


def find_common_prefix(
    solutions: list[tuple[list[list[str]], tuple[Move, ...]]],
) -> tuple[Move, ...]:
    """Find the longest common prefix of moves across all solutions.

    Returns a tuple of Move objects that appear at the start of every
    solution's move sequence.
    """
    if not solutions:
        return ()

    move_seqs = [moves for _grid, moves in solutions]
    min_length = min(len(sol) for sol in move_seqs)

    prefix: list[Move] = []
    for i in range(min_length):
        first_move = move_seqs[0][i]
        if all(sol[i] == first_move for sol in move_seqs):
            prefix.append(first_move)
        else:
            break

    return tuple(prefix)
