# This docker file is used for production
# Creating image based on official python3 image
FROM python:3.11-slim-bullseye

# Installing all python dependencies
RUN pip install poetry

RUN mkdir /app

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false
RUN poetry lock
RUN poetry install


# Get the django project into the docker container
COPY . /app/
