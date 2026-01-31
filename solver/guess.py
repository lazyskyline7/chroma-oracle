"""Solve 'mystery' puzzles by assigning candidates to UNKNOWN slots.

This module provides `solve_mystery(puzzle_path, algorithm="BFS")`, which
loads a JSON puzzle grid containing UNKNOWN slots, generates candidate
assignments for the missing colors, and attempts to solve each completed
grid using the BFS or DFS solver in `solver.lib.search`.

Usage: `python -m solver.guess <json_file> [BFS|DFS]`.
"""

import json
import os
import sys

from solver.lib.unknown_solver import (
    calculate_needed_colors,
    generate_candidate_grids,
    load_puzzle_with_unknowns,
    solve_all_candidates,
)


def solve_mystery(puzzle_path: str, algorithm: str = "BFS") -> None:
    """Attempt to solve a puzzle with UNKNOWN slots by trying candidates.

    Args:
        puzzle_path (str): Path to the JSON puzzle file to read.
        algorithm (str): Search algorithm to use: 'BFS' or 'DFS'.

    The function loads the JSON grid, identifies UNKNOWN slots, computes
    which colors are needed to complete sets of four, generates unique
    permutations for the missing slots, and runs the selected solver on
    each completed grid. Found solutions are saved to a
    `<puzzle>_solved` directory as JSON files.
    """
    print(f"Reading puzzle from {puzzle_path}...")
    data = load_puzzle_with_unknowns(puzzle_path)

    if not data.unknown_indices:
        print("No UNKNOWN items found. Running standard solver...")
        print("Please use the standard solver for fully known puzzles.")
        return

    needed = calculate_needed_colors(data)
    if needed is None:
        return

    print(f"Solving for {len(data.unknown_indices)} unknowns.")
    print(f"Candidates to place: {needed}")

    candidate_grids = generate_candidate_grids(data, needed)
    print(f"Testing {len(candidate_grids)} combinations using {algorithm}...")

    solutions = solve_all_candidates(candidate_grids, algorithm)

    base_name, _ = os.path.splitext(puzzle_path)
    output_dir = f"{base_name}_solved"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for idx, (candidate_grid) in enumerate(solutions, 1):
        print(f"Found solution for configuration #{idx}")
        out_filename = f"{output_dir}/{idx}.json"
        with open(out_filename, "w", encoding="utf-8") as out_f:
            json.dump(candidate_grid, out_f, indent=4)
        print(f"  Saved to {out_filename}")

    print(f"Finished. Found {len(solutions)} valid configurations.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m solver.guess <json_file> [BFS|DFS]")
        sys.exit(1)
    algo = sys.argv[2] if len(sys.argv) > 2 else "BFS"
    solve_mystery(sys.argv[1], algo)
