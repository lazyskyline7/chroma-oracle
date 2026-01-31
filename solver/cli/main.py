"""Entry point for the CLI."""

import logging

import click

from solver.lib import file2collection
from solver.lib.collection import ContainerCollection
from solver.lib.search import Option, bfs, dfs


class FlexibleGroup(click.Group):
    """A click Group that allows flexible invocation.

    If the first argument does not match any registered subcommand, this
    group treats the arguments as belonging to the default command rather
    than raising a usage error. It also allows extra args to be passed
    through to the invoked command.
    """

    def resolve_command(self, ctx, args):
        if not args:
            return None, None, []

        cmd = self.get_command(ctx, args[0])
        if cmd is not None:
            return args[0], cmd, args[1:]

        return None, None, args

    def invoke(self, ctx):
        args = list(getattr(ctx, "protected_args", []) or []) + list(ctx.args or [])

        if args:
            cmd_name, cmd, remaining = self.resolve_command(ctx, args)
            if cmd is not None:
                ctx.invoked_subcommand = cmd_name

                if self.callback is not None:
                    ctx.invoke(self.callback, **ctx.params)

                with cmd.make_context(cmd_name, remaining, parent=ctx) as cmd_ctx:
                    return cmd.invoke(cmd_ctx)

        ctx.args = args

        return click.Command.invoke(self, ctx)


@click.group(cls=FlexibleGroup, invoke_without_command=True)
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
    """Solve PUZZLE or run a subcommand.

    PUZZLE is the path to a json file describing the puzzle to solve.
    """
    ctx.ensure_object(dict)
    ctx.obj["algorithm"] = algorithm
    ctx.obj["validate"] = validate
    ctx.obj["verbose"] = verbose

    if verbose:
        logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)

    if ctx.invoked_subcommand is not None:
        return

    if not ctx.args:
        raise click.UsageError("Missing argument 'PUZZLE'.")

    puzzle = ctx.args[0]

    try:
        start: ContainerCollection = file2collection.load(
            puzzle, reject_invalid=validate
        )
    except ValueError as err:
        raise click.BadArgumentUsage("Invalid PUZZLE: " + str(err)) from err

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
        print(result.collection, "\n\n", result.moves, sep="")
