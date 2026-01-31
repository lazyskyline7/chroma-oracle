"""
Invokable Module for CLI.

python -m solver
"""

from solver.cli.main import cli

if __name__ == "__main__":
    cli(ctx=None, prog_name="chroma-oracle")
