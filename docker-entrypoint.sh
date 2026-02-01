#!/bin/sh
set -e

# Check if the first argument is 'interactive'
if [ "$1" = "interactive" ]; then
    shift
    exec chroma-oracle strategy -i "$@"
else
    # Default: Run the standard solver
    exec chroma-oracle "$@"
fi
