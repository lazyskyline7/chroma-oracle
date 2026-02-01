"""
Invokable Module for CLI.

python -m chroma_oracle
"""

from chroma_oracle.cli.main import cli

if __name__ == "__main__":
    # Click injects a Context at runtime; silence static checkers about the missing ctx.
    cli()  # pylint: disable=no-value-for-parameter
