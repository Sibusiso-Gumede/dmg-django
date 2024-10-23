# Use an official Python runtime as a parent image.
FROM python:3.12

# Set environment variables.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Update the pip manager to the latest version.
RUN pip install --upgrade pip

# Create and change directory to app.
WORKDIR /app

# Copy files into work directory.
COPY . .

# Install app packages.
RUN pip install -r production_requirements.txt

# The script to initialize the app.
ENTRYPOINT [ "sh", "./entrypoint.sh" ]