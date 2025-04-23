# ---------- base ----------
FROM python:3.11-slim AS base
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# деталь: ставим tini, чтобы красиво ловить SIGTERM
RUN apt-get update && apt-get install -y --no-install-recommends tini && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

# ---------- final image ----------
FROM base AS final
COPY . .
ENTRYPOINT ["/usr/bin/tini","--"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9000", "--workers", "4"]
EXPOSE 9000
