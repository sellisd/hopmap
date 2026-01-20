# Use an official Python runtime as a parent image
FROM ghcr.io/astral-sh/uv:python3.13-trixie-slim

# Install required packages
RUN apt-get update && apt-get install -y \
    traceroute

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
COPY . /app
ENV PYTHONPATH=/app
# Disable development dependencies
ENV UV_NO_DEV=1

RUN uv sync

# Run the command to start your application
ENTRYPOINT ["uv", "run", "hopmap"]