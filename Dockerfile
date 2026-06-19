FROM ghcr.io/astral-sh/uv:alpine3.21

WORKDIR /app

COPY . /app

RUN uv sync --frozen --no-dev


CMD ["uv","run", "python", "run.py"]