"""Solve 'mystery' puzzles by assigning candidates to UNKNOWN slots.

This module provides `solve_mystery(puzzle_path, algorithm="BFS")`, which
loads a JSON puzzle grid containing UNKNOWN slots, generates candidate
assignments for the missing colors, and attempts to solve each completed
grid using the BFS or DFS solver in `solver.lib.search`.

Usage: `python -m solver.guess <json_file> [BFS|DFS]`.
"""

import copy
import itertools
import json
import sys
import os

from solver.lib.collection import ContainerCollection
from solver.lib.colour import Colour
from solver.lib.search import bfs, dfs


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
    with open(puzzle_path, encoding="utf-8") as f:
        raw_grid = json.load(f)

    # Flatten to count
    all_items = []
    unknown_indices = []  # List of (row_idx, col_idx)

    for r, row in enumerate(raw_grid):
        for c, item in enumerate(row):
            if item == "UNKNOWN" or item == "?":
                unknown_indices.append((r, c))
            else:
                all_items.append(item)

    if not unknown_indices:
        print("No UNKNOWN items found. Running standard solver...")
        print("Please use the standard solver for fully known puzzles.")
        return

    # Count existing
    counts = {}
    valid_colors = [c.name for c in Colour]

    for item in all_items:
        counts[item] = counts.get(item, 0) + 1

    # Determine needed
    needed = []
    print("Current color counts:", counts)
    for color, c_count in counts.items():
        if c_count < 4:
            needed.extend([color] * (4 - c_count))
        elif c_count > 4:
            print(
                f"Error: Color {color} appears {c_count} times (more than 4)."
            )
            return

    # Check for totally missing colors (if we have leftover unknowns)
    current_needed_len = len(needed)
    missing_slots = len(unknown_indices) - current_needed_len

    if missing_slots > 0:
        if missing_slots % 4 == 0:
            num_new_colors = missing_slots // 4
            unused_colors = [c for c in valid_colors if c not in counts]
            if len(unused_colors) >= num_new_colors:
                for i in range(num_new_colors):
                    needed.extend([unused_colors[i]] * 4)
                print(
                    f"Assumed {num_new_colors} fully hidden colors: "
                    f"{needed[-missing_slots:]}"
                )
            else:
                print(
                    f"Error: Need {num_new_colors} new colors but only "
                    f"have {len(unused_colors)} unused valid colors."
                )
                return
        else:
            print(
                f"Error: {missing_slots} unknown slots remaining, which "
                "is not a multiple of 4. Cannot form complete sets."
            )
            return
    elif missing_slots < 0:
        print(
            f"Error: Have {len(unknown_indices)} slots but existing "
            f"colors need {current_needed_len} items to complete."
        )
        return

    print(f"Solving for {len(unknown_indices)} unknowns.")
    print(f"Candidates to place: {needed}")

    # Permutations
    unique_perms = sorted(list(set(itertools.permutations(needed))))

    print(f"Testing {len(unique_perms)} combinations using {algorithm}...")

    solved_count = 0

    base_name, _ = os.path.splitext(puzzle_path)
    output_dir = f"{base_name}_solved"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i, perm in enumerate(unique_perms):
        # Construct candidate grid
        candidate_grid = copy.deepcopy(raw_grid)
        for idx, (r, c) in enumerate(unknown_indices):
            candidate_grid[r][c] = perm[idx]

        try:
            collection = ContainerCollection(candidate_grid)

            if algorithm == "BFS":
                result = bfs(collection)
            else:
                result = dfs(collection)

            if result:
                print(f"Found solution for configuration #{i + 1}")
                solved_count += 1

                # Save it
                out_filename = f"{output_dir}/{solved_count}.json"
                with open(out_filename, "w", encoding="utf-8") as out_f:
                    json.dump(candidate_grid, out_f, indent=4)
                print(f"  Saved to {out_filename}")
                print(f"  Assigned: {perm}")

        except ValueError as e:
            # Only ignore "Invalid move" or "Invalid PUZZLE" errors
            # that come from logic, but usually we want to see them if
            # they are unexpected like "not a valid Colour".
            # For now, let's print them if they aren't the standard
            # "no solution" ones (which usually return None, not raise).
            # ContainerCollection init might raise if invalid structure.
            # Item init raises ValueError if color unknown.
            print(f"  ValueError: {e}")
        except (TypeError, AttributeError, KeyError, IndexError) as e:
            print(f"  Error testing config: {e}")

    print(f"Finished. Found {solved_count} valid configurations.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m solver.guess <json_file> [BFS|DFS]")
        sys.exit(1)
    algo = sys.argv[2] if len(sys.argv) > 2 else "BFS"
    solve_mystery(sys.argv[1], algo)
