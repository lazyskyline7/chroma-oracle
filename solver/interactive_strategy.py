"""Interactive iterative strategy mode for puzzles with unknowns.

This module provides an interactive session where players:
1. Get guaranteed safe moves
2. Execute them in the game
3. Report what colors were revealed
4. Get next set of safe moves
5. Repeat until puzzle solved

Usage: `python solver/interactive_strategy.py <json_file> [BFS|DFS]`
"""

import copy
import json
import sys

from solver.lib.collection import ContainerCollection
from solver.lib.move import Move
from solver.lib.strategy import find_all_solutions, find_common_prefix


def simulate_move(grid, move):
    """Simulate a move and return the updated grid.

    Args:
        grid: Current puzzle state
        move: Move to execute (src, dest tuple or Move object)

    Returns:
        Updated grid after the move, or None if move is invalid
    """
    try:
        collection = ContainerCollection(grid)
        move_obj = Move(move[0], move[1]) if isinstance(move, tuple) else move

        if not collection.is_valid(move_obj):
            return None

        new_collection = collection.after(move_obj)

        new_grid = []
        for container in new_collection.data:
            new_grid.append([item.colour.name for item in container.data])

        return new_grid
    except Exception:
        return None


def count_unknowns(grid):
    """Count total unknown positions in grid."""
    count = 0
    for row in grid:
        for item in row:
            if item == "?" or item == "UNKNOWN":
                count += 1
    return count


def interactive_strategy_session(puzzle_path: str, algorithm: str = "BFS"):
    """Run an interactive strategy session.

    Args:
        puzzle_path: Path to initial puzzle JSON
        algorithm: BFS or DFS
    """
    print("=" * 70)
    print("INTERACTIVE WINNING STRATEGY SESSION")
    print("=" * 70)
    print()
    print("This tool will guide you through solving the puzzle step by step.")
    print("After each set of moves, you'll update the puzzle state with what")
    print("you observed, and we'll find the next safe moves.")
    print()

    with open(puzzle_path, encoding="utf-8") as f:
        current_grid = json.load(f)

    iteration = 1
    total_moves_made = 0

    while True:
        print("=" * 70)
        print(f"ITERATION {iteration}")
        print("=" * 70)
        print()

        unknowns_remaining = count_unknowns(current_grid)
        print(f"Unknown positions remaining: {unknowns_remaining}")
        print()

        if unknowns_remaining == 0:
            print("✅ No more unknowns! Puzzle fully revealed.")
            print("You can now use the standard solver to complete it.")
            print()

            try:
                collection = ContainerCollection(current_grid)
                if collection.is_solved:
                    print("🎉 PUZZLE ALREADY SOLVED! Congratulations!")
                else:
                    print("Running final solve...")
                    from solver.lib.search import bfs, dfs

                    result = bfs(collection) if algorithm == "BFS" else dfs(collection)

                    if result:
                        print(f"✅ Solution found: {len(result.moves)} moves needed")
                        print()
                        print("Remaining moves:")
                        for i, move in enumerate(result.moves, 1):
                            print(f"  {i}. Container {move.src} -> {move.dest}")
                    else:
                        print("❌ No solution found (puzzle may be unsolvable)")
            except Exception as e:
                print(f"Error: {e}")
            break

        print("Finding guaranteed safe moves...")
        print()

        # Print current puzzle state and search message to match CLI output
        try:
            collection = ContainerCollection(current_grid)
            print("Initial state:")
            print(collection, "\n")
        except Exception:
            # If printing fails, continue without blocking the interactive flow
            pass

        if algorithm == "BFS":
            print("Searching using Breadth-First Search\n")
        elif algorithm == "DFS":
            print("Searching using Depth-First Search\n")

        temp_file = f"/tmp/chroma_oracle_temp_iter{iteration}.json"
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(current_grid, f)

        solutions = find_all_solutions(temp_file, algorithm)

        if not solutions:
            print("❌ No solutions found from this state.")
            print("The puzzle may be unsolvable, or you may have made an error.")
            break

        # Check for unique solution (Eureka moment)
        if len(solutions) == 1:
            from solver.lib.unknown_solver import identify_hidden_items

            print()
            print("=" * 70)
            print("✨ MYSTERY SOLVED! ✨")
            print("=" * 70)
            print()
            print("There is only ONE valid solution to this puzzle.")
            print("This means we know exactly what the hidden items are.")
            print()

            resolved_grid = solutions[0][0]
            deductions = identify_hidden_items(current_grid, resolved_grid)

            if deductions:
                print("🔍 DEDUCED HIDDEN ITEMS:")
                for d in deductions:
                    print(f"  {d}")
                print()

            print(f"Guaranteed safe moves: {len(solutions[0][1])}\n")
            full_moves = solutions[0][1]
            for i, move in enumerate(full_moves, 1):
                print(f"  {i}. Container {move.src} -> {move.dest}")
            print()
            print("You can execute all these moves to finish the game.")

            # Show the FINAL solved state from the solution itself
            # No need to simulate on raw grid since we know the full truth
            final_coll = ContainerCollection(resolved_grid)
            # Apply all moves to get final state
            for move in solutions[0][1]:
                final_coll = final_coll.after(move)

            print("State after solving:")
            print(final_coll, "\n")
            break

        common_moves = find_common_prefix(solutions)

        print()
        print("-" * 70)
        print("RESULTS")
        print("-" * 70)
        print()
        print(f"Valid solution paths: {len(solutions)}")
        print(f"Guaranteed safe moves: {len(common_moves)}")
        print()

        if not common_moves:
            print("⚠️  No common moves found at this point.")
            print()
            print("Solutions diverge here. You need to:")
            print("  1. Make an exploratory move to reveal more colors")
            print("  2. Or check if any containers are now fully visible")
            print()
            print("Possible first moves:")
            unique_first: dict[tuple[int, int], int] = {}
            for sol in solutions:
                moves = sol[1]
                if moves:
                    first_move = moves[0]
                    key = (first_move.src, first_move.dest)
                    unique_first[key] = unique_first.get(key, 0) + 1

            for (src, dest), count in sorted(unique_first.items(), key=lambda x: -x[1]):
                percentage = (count / len(solutions)) * 100
                print(
                    f"  Container {src} -> {dest} ({count}/{len(solutions)} = {percentage:.1f}% of solutions)"
                )

            print()
            print("💡 Recommendation: Try the move with highest percentage")
            break

        print(f"✅ EXECUTE THESE {len(common_moves)} MOVE(S) NOW:")
        print()
        for i, move in enumerate(common_moves, 1):
            print(f"  Move {total_moves_made + i}: Container {move.src} -> {move.dest}")
        print()
        print("These moves are SAFE - they work for all possible unknown values.")
        print()

        print("-" * 70)
        print("SIMULATION: What will the state be after these moves?")
        print("-" * 70)
        print()

        simulated_grid = copy.deepcopy(current_grid)
        for i, move in enumerate(common_moves):
            simulated_grid = simulate_move(simulated_grid, move)
            if simulated_grid is None:
                print(
                    f"Note: Simulation stopped at move {i + 1} (involves unknown items)"
                )
                simulated_grid = current_grid
                break

        if simulated_grid:
            print("After executing the moves, containers will look like:")
            print()
            # Use ContainerCollection string representation for consistency
            try:
                coll = ContainerCollection(simulated_grid)
                # Annotate containers that changed compared to the current collection
                orig_coll = ContainerCollection(current_grid)
                orig_lines = str(orig_coll).splitlines()
                sim_lines = str(coll).splitlines()
                annotated = []
                for i, line in enumerate(sim_lines):
                    if i < len(orig_lines) and line != orig_lines[i]:
                        annotated.append(line + " (changed)")
                    else:
                        annotated.append(line)
                print("\n".join(annotated), "\n")
            except Exception:
                # Fallback to previous display if construction fails
                for idx, container in enumerate(simulated_grid):
                    if container:
                        display = " ".join(
                            str(c) if c not in ["?", "UNKNOWN"] else "?"
                            for c in container
                        )
                        print(f"  Container {idx}: [{display}]")
                    else:
                        print(f"  Container {idx}: [empty]")
                print()

        print("-" * 70)
        print("NEXT STEPS")
        print("-" * 70)
        print()
        print("1. Execute the moves above in your game")
        print("2. Observe what colors are revealed (if any)")
        print("3. Update your JSON file with the new information:")
        print(f"   - Edit: {puzzle_path}")
        print("   - Replace '?' with actual colors you now see")
        print("4. Run this tool again to get the next set of moves")
        print()

        choice = (
            input("Have you executed the moves and updated the JSON? (y/n): ")
            .strip()
            .lower()
        )
        if choice != "y":
            print()
            print("Come back after you've updated the file!")
            break

        print()
        print("Reloading updated puzzle state...")
        with open(puzzle_path, encoding="utf-8") as f:
            new_grid = json.load(f)

        if new_grid == current_grid:
            print("⚠️  Warning: Puzzle state hasn't changed. Did you update the file?")
            choice = input("Continue anyway? (y/n): ").strip().lower()
            if choice != "y":
                break

        current_grid = new_grid
        total_moves_made += len(common_moves)
        iteration += 1
        print()

    print()
    print("=" * 70)
    print("SESSION COMPLETE")
    print("=" * 70)
    print(f"Total guaranteed moves executed: {total_moves_made}")
    print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python solver/interactive_strategy.py <json_file> [BFS|DFS]")
        sys.exit(1)

    puzzle_file = sys.argv[1]
    algo = sys.argv[2] if len(sys.argv) > 2 else "BFS"

    interactive_strategy_session(puzzle_file, algo)
