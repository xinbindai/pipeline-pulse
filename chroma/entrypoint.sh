#!/usr/bin/env bash
#
# Start the Chroma server. Listens on $PORT (Cloud Run injects it; defaults to
# 8000 locally) and persists to $PERSIST_DIRECTORY.
#
# Optional token auth is enabled automatically when CHROMA_SERVER_AUTHN_CREDENTIALS
# is set (chromadb reads the CHROMA_SERVER_AUTHN_* env vars directly).
set -euo pipefail

PORT="${PORT:-8000}"
PERSIST_DIRECTORY="${PERSIST_DIRECTORY:-/data}"

mkdir -p "$PERSIST_DIRECTORY"

echo "Starting Chroma on 0.0.0.0:${PORT}, persisting to ${PERSIST_DIRECTORY}"
exec chroma run --host 0.0.0.0 --port "$PORT" --path "$PERSIST_DIRECTORY"
