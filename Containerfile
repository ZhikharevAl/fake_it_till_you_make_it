FROM mcr.microsoft.com/playwright/python:v1.51.0-noble

WORKDIR /app

ENV PYTHONUNBUFFERED=1

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

COPY pyproject.toml uv.lock* ./

RUN uv venv && \
    uv pip install -e . && \
    uv pip install --group dev -e .

COPY . .

CMD ["/app/.venv/bin/python", "-m", "pytest"]
