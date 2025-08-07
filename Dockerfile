FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /data
COPY pyproject.toml .
RUN uv sync --locked
CMD [""]