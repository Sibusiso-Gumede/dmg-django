# Use an official Python runtime as a parent image.
FROM python:3.12.6-alpine

# Set environment variables.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory.
WORKDIR /app

# Update the pip manager to the latest version.
RUN pip install --upgrade pip

# Install dependencies.
COPY production_requirements.txt /app
RUN pip install -r production_requirements.txt

COPY ./dmg_django /app
COPY ./dmg_django_app /app
COPY __init__.py /app
COPY manage.py /app 

COPY ./entrypoint.sh /
ENTRYPOINT [ "sh", "/entrypoint.sh" ]