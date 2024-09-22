# Use an official Python runtime as a parent image.
FROM python:3.12.6-alpine

# Set environment variables.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install development headers and libraries.
RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers

# Update the pip manager to the latest version.
RUN pip install --upgrade pip

# Install app packages.
COPY ./production_requirements.txt /app
RUN pip install -r production_requirements.txt

# Remove dev headers and libraries.
RUN apk del .tmp

# Set the working directory.
RUN mkdir /app

# Change CWD to the app.
WORKDIR /app

# Copy files to the app.
COPY . .

# Create user.
RUN adduser -D dmg_user

# Create alias dirs and set user permission.
RUN mkdir -p /vol/web/static
RUN chown _R user:dmg_user
RUN chmod -R 755 /vol/web

# Switch to user.
USER dmg_user

# The script to initialize the app.
ENTRYPOINT [ "sh", "/entrypoint.sh" ]