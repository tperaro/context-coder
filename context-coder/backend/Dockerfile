# Backend Dockerfile - FastAPI + Python 3.11
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for Node.js (needed for MCP npx commands)
RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry==1.7.1

# Configure Poetry to not create virtual envs (we're in Docker)
RUN poetry config virtualenvs.create false

# Copy dependency files
COPY pyproject.toml ./

# Generate lock file and install dependencies
RUN poetry lock --no-update && \
    poetry install --no-root --no-interaction --no-ansi

# Copy source code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI with hot-reload
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

