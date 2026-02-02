#!/usr/bin/env bash
# Convenience wrapper to run the chroma-oracle image with the current
# working directory mounted into the container at /app so outputs persist
# on the host by default.

set -euo pipefail

IMAGE_NAME=${1:-chroma-oracle}
shift || true

# If first arg looks like a subcommand, keep it. Allow passing
# arbitrary docker run flags by setting DOCKER_RUN_FLAGS env if needed.

PWD_HOST="$(pwd)"

docker run --rm -it \
  -v "$PWD_HOST":/app \
  -w /app \
  "$IMAGE_NAME" "$@"
