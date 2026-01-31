# Use specific version for stability
FROM python:3.13-slim-bookworm

# Copy uv from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Ensure TLS certs exist for network access
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates && \
	rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy dependency definitions
COPY pyproject.toml uv.lock README.md ./

# Install dependencies using uv
# Install dependencies from pyproject.toml first to leverage Docker caching
RUN uv pip install --system --no-cache -r pyproject.toml

# Copy project files
COPY solver ./solver
COPY levels ./levels
COPY docker-entrypoint.sh ./

# Make entrypoint executable
RUN chmod +x docker-entrypoint.sh

# Install the project itself (no-deps because we already installed them)
RUN uv pip install --system --no-cache --no-deps .

# Set the entrypoint to the custom script
ENTRYPOINT ["/app/docker-entrypoint.sh"]

# Default argument
CMD ["--help"]
