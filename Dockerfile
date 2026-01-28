# Use specific version for stability
FROM python:3.13-slim-bookworm

# Ensure TLS certs exist for network access
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates && \
	rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy dependency definitions and installer files
COPY pyproject.toml ./
# Copy setup and requirements so setup.py can read requirements/base.txt
COPY setup.py ./
COPY requirements ./requirements

# Copy project files
COPY README.md docker-entrypoint.sh ./
COPY solver ./solver
COPY levels ./levels

# Install package and dependencies system-wide using pip
RUN python -m pip install --upgrade pip setuptools wheel && \
	python -m pip install --no-cache-dir .

# Make entrypoint executable
RUN chmod +x docker-entrypoint.sh

# System Python used; no in-image virtualenv

# Set the entrypoint to the custom script
ENTRYPOINT ["/app/docker-entrypoint.sh"]

# Default argument
CMD ["--help"]
