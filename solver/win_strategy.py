"""Find guaranteed winning moves for puzzles with unknown colors.

This module finds the longest sequence of moves that work for ALL possible
color assignments of unknowns ("?" or "UNKNOWN" slots), allowing players
to make progress without guessing.

Usage: `python -m solver.win_strategy <json_file> [BFS|DFS]`
"""

import sys

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
    data = load_puzzle_with_unknowns(puzzle_path)

    if not data.unknown_indices:
        print("No UNKNOWN items found. Solving standard puzzle...")
        try:
            collection = ContainerCollection(data.raw_grid)
            result = bfs(collection) if algorithm == "BFS" else dfs(collection)
            if result:
                return [result.moves]
        except (ValueError, TypeError) as e:
            print(f"Error: {e}")
        return []

    needed = calculate_needed_colors(data)
    if needed is None:
        return []

    print(f"Solving for {len(data.unknown_indices)} unknowns.")
    print(f"Candidates to place: {needed}")

    candidate_grids = generate_candidate_grids(data, needed)
    print(f"Testing {len(candidate_grids)} combinations using {algorithm}...")

    solutions = solve_all_candidates(candidate_grids, algorithm)

    solution_moves = []
    for _, (_grid, moves) in enumerate(solutions, 1):
        solution_moves.append(moves)
        if len(solution_moves) <= 10 or len(solution_moves) % 10 == 0:
            print(f"  Solution {len(solution_moves)}: {len(moves)} moves")

    print(f"Found {len(solution_moves)} valid solutions.")
    return solution_moves


def find_common_prefix(solutions: list[tuple[Move, ...]]) -> tuple[Move, ...]:
    """Find the longest common prefix of moves across all solutions.

    Args:
        solutions: List of move sequences.

    Returns:
        Tuple of moves that appear at the start of ALL solutions.
        Returns empty tuple if no common moves or no solutions.
    """
    if not solutions:
        return ()

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
        unique_first_moves = {(sol[0].src, sol[0].dest) for sol in solutions if sol}
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
