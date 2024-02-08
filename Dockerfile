# Use an official Python runtime as a parent image
FROM python:3.11.8-slim-bookworm

# Install required packages
RUN apt-get update && apt-get install -y \
    traceroute
# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app
ENV PYTHONPATH=/app

# Install any needed packages specified in requirements.txt
RUN python -m pip install .

# Run the command to start your application
CMD ["hopmap plot"]