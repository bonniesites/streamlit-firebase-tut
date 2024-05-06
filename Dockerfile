### &&&&&&&&&&&&&&&&&&&&&& ###

# Use multi-stage builds to keep the final image clean and small
# Base image for building
FROM python:3.11-slim-bullseye as builder

# Install necessary system dependencies
# Combine RUN commands to reduce layers and remove redundant package installations
RUN apt-get update && apt-get install -y \
    curl \
    xz-utils \
    libpq-dev \
    build-essential \
    software-properties-common \
    git \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install poetry

# Set environment variables for Poetry
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Leverage Docker cache by copying only pyproject.toml and poetry.lock first
COPY pyproject.toml poetry.lock ./

# Install project dependencies
RUN poetry install --no-root --no-dev

# Final image for running the application
FROM python:3.11-slim-bullseye as runtime

# Copy virtual environment from builder stage
COPY --from=builder /.venv /.venv

# Set virtual environment path
ENV VIRTUAL_ENV=/.venv \
    PATH="/.venv/bin:$PATH"

# Set working directory and copy application code
WORKDIR /app
COPY . /app

# Expose port for the application
EXPOSE 8527

# Health check for the application
HEALTHCHECK CMD curl --fail http://localhost:8527/_stcore/health || exit 1

# Define the entrypoint command
ENTRYPOINT ["streamlit", "run", "Home.py", "--server.port=8527", "--server.address=0.0.0.0"]