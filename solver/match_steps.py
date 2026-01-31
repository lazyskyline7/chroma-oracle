"""Compare first N moves of solutions in a folder against a reference puzzle.

Usage: python -m solver.match_steps <folder> <reference_file> [N] [BFS|DFS]
"""

import json
import os

from solver.lib.collection import ContainerCollection
from solver.lib.search import bfs, dfs


def _get_first_moves(
    grid, n: int, algorithm: str
) -> tuple[tuple[int, int], ...] | None:
    """Return the first `n` moves for `grid` using `algorithm`.

    Args:
        grid: Puzzle grid (parsed JSON) to evaluate.
        n (int): Number of moves to return from the start of the solution.
        algorithm (str): 'BFS' or 'DFS' to select the solver.

    Returns:
        A tuple of `(src, dest)` move pairs of length up to `n`, or
        `None` when the puzzle has no solution under the chosen algorithm.
    """
    collection = ContainerCollection(grid)
    opt = bfs(collection) if algorithm == "BFS" else dfs(collection)
    if not opt:
        return None
    moves = tuple((m.src, m.dest) for m in opt.moves[:n])
    return moves


def match_first_steps(
    folder: str, reference_file: str, n: int = 2, algorithm: str = "BFS"
):
    """Compare first `n` moves of JSON puzzles in `folder` to `reference_file`.

    Scans `folder` for .json files, computes the first `n` moves for each
    using the selected `algorithm`, and prints whether each file fully
    matches, partially matches, or differs from the reference's first
    `n` moves. Returns a list of filenames that fully match.

    Args:
        folder (str): Directory containing candidate puzzle JSON files.
        reference_file (str): Path to the reference puzzle JSON file.
        n (int): Number of initial moves to compare (default 2).
        algorithm (str): 'BFS' or 'DFS' solver to use (default 'BFS').

    Returns:
        List[str]: Filenames in `folder` whose first `n` moves exactly match
        the reference's first `n` moves.
    """
    if not os.path.isdir(folder):
        raise ValueError(f"Folder not found: {folder}")

    with open(reference_file, encoding="utf-8") as f:
        ref_grid = json.load(f)

    ref_moves = _get_first_moves(ref_grid, n, algorithm)
    if ref_moves is None:
        print(
            f"Reference puzzle {reference_file} has no solution using " f"{algorithm}."
        )
        return

    print(f"Reference first {n} moves: {ref_moves}")

    matches = []
    for fname in sorted(os.listdir(folder)):
        if not fname.endswith(".json"):
            continue
        path = os.path.join(folder, fname)
        try:
            with open(path, encoding="utf-8") as f:
                grid = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            print(f"Skipping {fname}: cannot read ({e})")
            continue

        moves = _get_first_moves(grid, n, algorithm)
        if moves is None:
            print(f"{fname}: no solution")
            continue

        # compute common prefix length
        common = 0
        for a, b in zip(ref_moves, moves, strict=True):
            if a == b:
                common += 1
            else:
                break

        if common == n:
            print(f"MATCH {fname}: first {n} moves equal")
            matches.append(fname)
        elif common > 0:
            print(f"PARTIAL {fname}: {common}/{n} moves match")
        else:
            print(f"DIFFER {fname}: 0/{n} moves match")

    print(f"Done. {len(matches)} full matches found.")
    return matches
