# Multi-stage build for optimized image size
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies and UV
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && curl -LsSf https://astral.sh/uv/install.sh | sh

# Copy project files
COPY pyproject.toml ./
COPY uv.lock* ./

# Install dependencies with UV
ENV PATH="/root/.local/bin:$PATH"
RUN uv sync --frozen --no-dev

# Production stage
FROM python:3.11-slim

# Install curl for health checks
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Copy UV and Python dependencies from builder
COPY --from=builder /root/.local/bin/uv /usr/local/bin/uv
COPY --from=builder --chown=appuser:appuser /app/.venv /home/appuser/.venv

# Copy application code
COPY --chown=appuser:appuser . .

# Set environment variables
ENV PATH=/home/appuser/.venv/bin:$PATH
ENV VIRTUAL_ENV=/home/appuser/.venv
ENV UV_PROJECT_ENVIRONMENT=/home/appuser/.venv
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/health')"

# Run the application with gunicorn via python module
CMD ["uv", "run", "--frozen", "python", "-m", "gunicorn", "--bind", "0.0.0.0:8080", "--workers", "4", "--threads", "2", "--timeout", "60", "--access-logfile", "-", "--error-logfile", "-", "run:app"]