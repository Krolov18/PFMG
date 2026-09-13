# Python library dev/test image (managed with uv).
# The Antora documentation build uses Dockerfile.docs instead.
FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    NLTK_DATA=/usr/share/nltk_data

WORKDIR /app

# Install dependencies first so this layer is cached across source changes.
COPY pyproject.toml uv.lock ./
RUN uv sync --all-groups --frozen --no-install-project

# Install the project, then pre-fetch the NLTK data the parser needs at runtime.
COPY . .
RUN uv sync --all-groups --frozen \
    && uv run python -m nltk.downloader -d "$NLTK_DATA" wordnet

CMD ["uv", "run", "pytest"]
