#!/bin/sh
set -e

# Check if the first argument is 'interactive'
if [ "$1" = "interactive" ]; then
    shift
    exec python chroma_oracle/interactive_strategy.py "$@"
else
    # Default: Run the standard solver
    exec python -m solver "$@"
fi
