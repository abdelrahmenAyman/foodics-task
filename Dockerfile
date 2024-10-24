FROM python:3.12.7

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=1.5.1

WORKDIR /app

RUN apt-get update && apt-get install -y curl netcat-traditional && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

ENV PYTHONPATH=/app

# Create non-root user earlier in the process
RUN groupadd -r appgroup && useradd -r -g appgroup -u 1000 appuser

# Copy poetry files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry config virtualenvs.create false --local && poetry install --no-dev

# Copy application code
COPY . .

# Create alembic versions directory and set permissions
RUN mkdir -p /app/alembic/versions && \
    chown -R appuser:appgroup /app && \
    chmod -R 755 /app

# Switch to non-root user
USER appuser

CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]