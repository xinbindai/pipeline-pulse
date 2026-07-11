# Chroma vector-database server, runnable locally and on Cloud Run.
#
# Build context is this chroma/ folder (the server image is self-contained):
#   docker build -t chroma-server ./chroma
FROM python:3.12-slim

WORKDIR /chroma

# Pin chromadb to the version you tested; keep server and ingest client in sync.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Persistence dir. Locally this is a docker volume; on Cloud Run it is a
# Cloud Storage bucket mounted here via gcsfuse (see deploy/deploy-chroma.sh).
ENV IS_PERSISTENT=TRUE \
    PERSIST_DIRECTORY=/data \
    ANONYMIZED_TELEMETRY=FALSE

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Local default; Cloud Run injects PORT and the entrypoint honours it.
EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
