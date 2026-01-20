# Use an official Python runtime as a parent image
FROM python:3.14.2-slim-trixie

# Install required packages
RUN apt-get update && apt-get install -y \
    traceroute
# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
COPY . /app
ENV PYTHONPATH=/app

# Install any needed packages specified in requirements.txt
RUN python -m pip install .

# Run the command to start your application
ENTRYPOINT ["hopmap"]
