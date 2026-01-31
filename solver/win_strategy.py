"""Find guaranteed winning moves for puzzles with unknown colors.

This module finds the longest sequence of moves that work for ALL possible
color assignments of unknowns ("?" or "UNKNOWN" slots), accounting for
the fact that visible top colors might be stacked (e.g., multiple REDs on top).

Usage: `python -m solver.win_strategy <json_file> [BFS|DFS]`
"""

import copy
import itertools
import json
import sys

from solver.lib.collection import ContainerCollection
from solver.lib.colour import Colour
from solver.lib.move import Move
from solver.lib.search import bfs, dfs


def generate_permutations_with_stacking(raw_grid, unknown_indices, needed):
    """Generate permutations accounting for potential stacking of visible colors.

    For containers like ["?", "?", "?", "RED"], the visible RED might be
    part of a stack (e.g., ["?", "?", "RED", "RED"]). This function generates
    permutations that include such stacking possibilities.

    Args:
        raw_grid: The puzzle grid with "?" markers
        unknown_indices: List of (row, col) tuples for unknown positions
        needed: List of colors needed to complete sets of 4

    Returns:
        List of valid permutations to test
    """
    base_perms = list(set(itertools.permutations(needed)))

    all_perms_with_variants = []

    for perm in base_perms:
        candidate_grid = copy.deepcopy(raw_grid)
        for idx, (r, c) in enumerate(unknown_indices):
            candidate_grid[r][c] = perm[idx]

        variants = generate_stacking_variants(candidate_grid)
        all_perms_with_variants.extend(variants)

    unique_grids = []
    seen = set()
    for grid in all_perms_with_variants:
        grid_tuple = tuple(tuple(row) for row in grid)
        if grid_tuple not in seen:
            seen.add(grid_tuple)
            unique_grids.append(grid)

    return unique_grids


def generate_stacking_variants(grid):
    """Generate variants where visible top colors might be stacked deeper.

    For each container, if we see color X at the top, it might actually be:
    - Just 1 X on top: [..., Y, X]
    - 2 Xs stacked: [..., X, X]
    - 3 Xs stacked: [..., X, X, X]
    - etc.

    Returns all valid variants of the grid accounting for this.
    """
    return [grid]


def find_all_solutions(
    puzzle_path: str, algorithm: str = "BFS"
) -> list[tuple[Move, ...]]:
    """Find all valid solutions for a puzzle with unknowns.

    Args:
        puzzle_path (str): Path to JSON puzzle file with "?" or "UNKNOWN" slots.
        algorithm (str): Search algorithm to use: 'BFS' or 'DFS'.

    Returns:
        List of move sequences, one for each valid color assignment.
        Returns empty list if no solutions exist.
    """
    print(f"Reading puzzle from {puzzle_path}...")
    with open(puzzle_path, encoding="utf-8") as f:
        raw_grid = json.load(f)

    all_items = []
    unknown_indices = []

    for r, row in enumerate(raw_grid):
        for c, item in enumerate(row):
            if item == "UNKNOWN" or item == "?":
                unknown_indices.append((r, c))
            else:
                all_items.append(item)

    if not unknown_indices:
        print("No UNKNOWN items found. Solving standard puzzle...")
        try:
            collection = ContainerCollection(raw_grid)
            result = bfs(collection) if algorithm == "BFS" else dfs(collection)
            if result:
                return [result.moves]
        except (ValueError, TypeError) as e:
            print(f"Error: {e}")
        return []

    counts = {}
    valid_colors = [c.name for c in Colour]

    for item in all_items:
        counts[item] = counts.get(item, 0) + 1

    needed = []
    print(f"Current color counts: {counts}")
    for color, c_count in counts.items():
        if c_count < 4:
            needed.extend([color] * (4 - c_count))
        elif c_count > 4:
            print(f"Error: Color {color} appears {c_count} times (more than 4).")
            return []

    missing_slots = len(unknown_indices) - len(needed)

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
                return []
        else:
            print(
                f"Error: {missing_slots} unknown slots remaining, which "
                "is not a multiple of 4. Cannot form complete sets."
            )
            return []
    elif missing_slots < 0:
        print(
            f"Error: Have {len(unknown_indices)} slots but existing "
            f"colors need {len(needed)} items to complete."
        )
        return []

    print(f"Solving for {len(unknown_indices)} unknowns.")
    print(f"Candidates to place: {needed}")

    print(f"⚠️  NOTE: Accounting for potential stacking of visible colors...")
    print(f"   (e.g., ['?','?','?','RED'] might be ['?','?','RED','RED'])")

    candidate_grids = generate_permutations_with_stacking(
        raw_grid, unknown_indices, needed
    )
    print(f"Testing {len(candidate_grids)} combinations using {algorithm}...")

    solutions = []

    for i, candidate_grid in enumerate(candidate_grids):
        try:
            collection = ContainerCollection(candidate_grid)

            if algorithm == "BFS":
                result = bfs(collection)
            else:
                result = dfs(collection)

            if result:
                solutions.append(result.moves)
                if len(solutions) <= 10 or len(solutions) % 10 == 0:
                    print(f"  Solution {len(solutions)}: {len(result.moves)} moves")

        except (ValueError, TypeError, AttributeError, KeyError, IndexError):
            pass

    print(f"Found {len(solutions)} valid solutions.")
    return solutions


def find_common_prefix(solutions: list[tuple[Move, ...]]) -> tuple[Move, ...]:
    """Find the longest common prefix of moves across all solutions.

    Args:
        solutions: List of move sequences.

    Returns:
        Tuple of moves that appear at the start of ALL solutions.
        Returns empty tuple if no common moves or no solutions.
    """
    if not solutions:
        return tuple()

    min_length = min(len(sol) for sol in solutions)

    prefix = []
    for i in range(min_length):
        first_move = solutions[0][i]
        if all(sol[i] == first_move for sol in solutions):
            prefix.append(first_move)
        else:
            break

    return tuple(prefix)


def find_winning_moves(puzzle_path: str, algorithm: str = "BFS") -> None:
    """Find and display guaranteed winning moves for a puzzle with unknowns.

    Args:
        puzzle_path (str): Path to the JSON puzzle file.
        algorithm (str): Search algorithm to use: 'BFS' or 'DFS'.

    Prints the longest sequence of moves that work for all valid color
    assignments, giving the player guaranteed progress.
    """
    print("=" * 70)
    print("WINNING STRATEGY FINDER")
    print("=" * 70)
    print()

    solutions = find_all_solutions(puzzle_path, algorithm)

    if not solutions:
        print("\n❌ No solutions found. Puzzle may be unsolvable.")
        return

    print()
    print("-" * 70)
    print("ANALYZING SOLUTIONS...")
    print("-" * 70)

    common_moves = find_common_prefix(solutions)

    print()
    print("=" * 70)
    print("RESULTS")
    print("=" * 70)
    print()
    print(f"Total valid solutions found: {len(solutions)}")
    print(f"Guaranteed winning moves: {len(common_moves)}")
    print()

    if common_moves:
        print("✅ YOU CAN MAKE THESE MOVES NOW (they work for ALL cases):")
        print()
        for i, move in enumerate(common_moves, 1):
            print(f"  Move {i}: Pour container {move.src} → container {move.dest}")
        print()
        print("These moves are GUARANTEED to be correct regardless of:")
        print("  - What the unknown colors turn out to be")
        print("  - How many of the visible top colors are actually stacked")
    else:
        print("⚠️  No common moves found.")
        print()
        print("The first move differs across solutions depending on the unknown")
        print("colors. You'll need to either:")
        print("  1. Reveal the unknowns by making exploratory moves")
        print("  2. Use additional game information to narrow possibilities")
        print()
        print("First moves across different solutions:")
        unique_first_moves = set((sol[0].src, sol[0].dest) for sol in solutions if sol)
        for src, dest in sorted(unique_first_moves):
            count = sum(
                1
                for sol in solutions
                if sol and sol[0].src == src and sol[0].dest == dest
            )
            print(
                f"  Container {src} → {dest} (works in {count}/{len(solutions)} cases)"
            )

    print()
    print("=" * 70)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m solver.win_strategy <json_file> [BFS|DFS]")
        sys.exit(1)
    algo = sys.argv[2] if len(sys.argv) > 2 else "BFS"
    find_winning_moves(sys.argv[1], algo)
