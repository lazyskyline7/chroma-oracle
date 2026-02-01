"""Entry point for the CLI (cleaned strategy flow).

This CLI prints the initial raw puzzle state, computes guaranteed moves
using the library strategy helpers, and simulates those moves on the raw
puzzle (preserving UNKNOWNs). It deliberately avoids printing any
representative concrete candidate grids.
"""

import logging

import click

from solver.cli.printing import print_moves
from solver.cli.simulation import simulate_moves_on_grid
from solver.lib import file2collection
from solver.lib.collection import ContainerCollection
from solver.lib.search import Option, bfs, dfs
from solver.lib.unknown_solver import load_puzzle_with_unknowns
from solver.lib.strategy import find_all_solutions, find_common_prefix


@click.group(invoke_without_command=True)
@click.option(
    "-a",
    "--algorithm",
    type=click.Choice(["BFS", "DFS"], case_sensitive=False),
    default="BFS",
    show_default=True,
    help="Select which algorithm to use to solve the PUZZLE.",
)
@click.option(
    "-v",
    "--validate",
    is_flag=True,
    help="Ensure PUZZLE is valid and return an error if not.",
)
@click.option(
    "--verbose",
    is_flag=True,
    help="Show additional logging whilst running BFS search",
)
@click.pass_context
def cli(
    ctx: click.Context,
    algorithm: str = "BFS",
    verbose: bool = False,
    validate: bool = False,
) -> None:
    ctx.ensure_object(dict)
    ctx.obj["algorithm"] = algorithm
    ctx.obj["validate"] = validate
    ctx.obj["verbose"] = verbose

    if verbose:
        logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)

    if ctx.invoked_subcommand is not None:
        return

    click.echo(ctx.get_help())
    ctx.exit()


@cli.command(name="solve")
@click.argument("puzzle", type=click.Path(exists=True))
@click.option(
    "-a",
    "--algorithm",
    type=click.Choice(["BFS", "DFS"], case_sensitive=False),
    default="BFS",
    show_default=True,
    help="Select which algorithm to use to solve the PUZZLE.",
)
@click.option(
    "-v",
    "--validate",
    is_flag=True,
    help="Ensure PUZZLE is valid and return an error if not.",
)
@click.option(
    "--verbose",
    is_flag=True,
    help="Show additional logging whilst running BFS search",
)
def solve(puzzle: str, algorithm: str, validate: bool, verbose: bool) -> None:
    if verbose:
        logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)

    try:
        start: ContainerCollection = file2collection.load(
            puzzle, reject_invalid=validate
        )
    except ValueError as err:
        raise click.BadArgumentUsage("Invalid PUZZLE: " + str(err)) from err

    print("Initial state:")
    print(start, "\n")

    result: Option | None = None
    if algorithm == "BFS":
        print("Searching using Breadth-First Search\n")
        result = bfs(start)
    elif algorithm == "DFS":
        print("Searching using Depth-First Search\n")
        result = dfs(start)

    if result is None:
        print("Cannot be solved :(")
    else:
        print("solved in", len(result.moves), "moves")
        print("State after solving:")
        print(result.collection, "\n")
        print_moves(result.moves)


@cli.command()
@click.argument("puzzle", type=click.Path(exists=True))
@click.option(
    "-i",
    "--interactive",
    is_flag=True,
    help="Run in interactive mode to solve mystery puzzles step-by-step.",
)
@click.option(
    "-a",
    "--algorithm",
    type=click.Choice(["BFS", "DFS"], case_sensitive=False),
    default="BFS",
    show_default=True,
    help="Select which algorithm to use.",
)
def strategy(puzzle: str, interactive: bool, algorithm: str):
    """Calculate winning strategy or run interactive session."""
    if interactive:
        from solver.interactive_strategy import interactive_strategy_session

        interactive_strategy_session(puzzle, algorithm)
        return

    # Non-interactive: compute guaranteed moves across all candidates,
    # then simulate them on the original raw puzzle and report the
    # raw-puzzle final/partial state (preserving UNKNOWNs).
    try:
        start: ContainerCollection = file2collection.load(puzzle, reject_invalid=False)
        print("Initial state:")
        print(start, "\n")
    except ValueError as err:
        raise click.BadArgumentUsage("Invalid PUZZLE: " + str(err)) from err

    if algorithm == "BFS":
        print("Searching using Breadth-First Search\n")
    elif algorithm == "DFS":
        print("Searching using Depth-First Search\n")

    print(f"Analyzing {puzzle} for guaranteed safe moves...")
    solutions = find_all_solutions(puzzle, algorithm)

    if not solutions:
        print("No solutions found.")
        return

    # Check for unique solution (Eureka moment)
    if len(solutions) == 1:
        from solver.lib.unknown_solver import identify_hidden_items

        print(f"\nFound {len(solutions)} winning paths.")
        print("✨ MYSTERY SOLVED! Only one valid solution exists.")

        # Load raw grid again to compare to identify hidden items
        # We use the top-level imported load_puzzle_with_unknowns
        data = load_puzzle_with_unknowns(puzzle)

        resolved_grid = solutions[0][0]
        deductions = identify_hidden_items(data.raw_grid, resolved_grid)

        if deductions:
            print("\n🔍 DEDUCED HIDDEN ITEMS:")
            for d in deductions:
                print(f"  {d}")

        print(f"Guaranteed safe moves: {len(solutions[0][1])}\n")
        print_moves(solutions[0][1])

        # Show the FINAL solved state from the solution itself
        # No need to simulate on raw grid since we know the full truth
        final_coll = ContainerCollection(resolved_grid)
        # Apply all moves to get final state
        for move in solutions[0][1]:
            final_coll = final_coll.after(move)

        print("State after solving:")
        print(final_coll, "\n")
        return

    common = find_common_prefix(solutions)
    if len(solutions) > 1:
        print(f"\nFound {len(solutions)} winning paths.")

    print(f"Guaranteed safe moves: {len(common)}\n")

    print_moves(common)

    # Simulate on the raw puzzle and show raw final/partial state
    try:
        data = load_puzzle_with_unknowns(puzzle)
        raw_final, fail_idx = simulate_moves_on_grid(data.raw_grid, list(common))

        if fail_idx is None:
            raw_coll = ContainerCollection(raw_final)
            print(
                "These moves were successfully replayed on the raw puzzle. Raw-puzzle final state:"
            )
            print(raw_coll, "\n")
        else:
            print(
                f"Partial state after applying {fail_idx} moves (simulation stopped due to unknown values):"
            )
            raw_coll = ContainerCollection(raw_final)
            print(raw_coll, "\n")
    except Exception:
        import sys

        print(
            "Error: Failed to compute state after applying guaranteed moves.",
            file=sys.stderr,
        )


if __name__ == "__main__":
    cli()
