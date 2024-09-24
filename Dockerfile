# Use an official Python runtime as a parent image.
FROM python:3.12.6-alpine

# Install development headers and libraries.
RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers pkgconfig mariadb-dev apache2-dev

# Update the pip manager to the latest version.
RUN pip install --upgrade pip

# Set the working directory.
RUN mkdir /app

# Copy files to the app.
COPY . /app

# Change CWD to the app.
WORKDIR /app

# Install app packages.
RUN pip install -r production_requirements.txt

# Remove dev headers and libraries.
RUN apk del .tmp

# The script to initialize the app.
ENTRYPOINT [ "sh", "./entrypoint.sh" ]