
FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY api/pyproject.toml api/uv.lock ./

RUN uv sync --frozen --no-install-project

COPY api/ ./api/

COPY frontend/ /frontend/

CMD ["uv", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--forwarded-allow-ips", "*"]
