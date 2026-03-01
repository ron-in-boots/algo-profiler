FROM ubuntu:22.04

# Install only what's needed — no extras
RUN apt-get update && apt-get install -y \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user for running code
RUN useradd -m -u 1001 sandbox

# Working directory
WORKDIR /sandbox

# Switch to non-root user
USER sandbox
