#!/bin/sh
set -e

# Check if the first argument is 'guess'
if [ "$1" = "guess" ]; then
    shift
    # Run the mystery guesser
    exec python -m solver.guess "$@"
else
    # Default: Run the standard solver
    exec python -m solver "$@"
fi
