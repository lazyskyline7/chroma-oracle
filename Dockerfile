# Use specific version for stability
FROM python:3.13-slim-bookworm

# Install uv for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set working directory
WORKDIR /app

# Copy dependency definitions
COPY pyproject.toml uv.lock ./

# Copy project files
COPY README.md docker-entrypoint.sh ./
COPY solver ./solver
COPY levels ./levels

# Install dependencies
RUN uv sync --frozen

# Make entrypoint executable
RUN chmod +x docker-entrypoint.sh

# Add virtual environment to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Set the entrypoint to the custom script
ENTRYPOINT ["/app/docker-entrypoint.sh"]

# Default argument
CMD ["--help"]
