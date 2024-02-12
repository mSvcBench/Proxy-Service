# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory in the container to /app
WORKDIR /app/proxy-service

# Copy the current directory contents into the container at /app
COPY ./src/ /app/proxy-service/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run proxy-service.py when the container launches
CMD ["kopf", "run", "--verbose", "proxy-service.py"]