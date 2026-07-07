# Chroma remote server + RAG ingest

A [Chroma](https://www.trychroma.com/) vector-database server you can run locally
in Docker and deploy to **GCP Cloud Run**, using a **Cloud Storage** bucket as the
persistence layer. Plus `ingest.py`, a script to chunk text and upsert it into the
server for RAG.

## Files
| File | Purpose |
|------|---------|
| `Dockerfile` | Self-contained Chroma server image (listens on `$PORT`, persists to `/data`). |
| `entrypoint.sh` | Starts `chroma run` on `$PORT`, persisting to `$PERSIST_DIRECTORY`. |
| `requirements.txt` | Server dependency (`chromadb`). |
| `docker-compose.yml` | Local test harness (server on `localhost:8001`, data in `./.chroma-data`). |
| `ingest.py` | RAG ingest: discover files → chunk → upsert (text; embeddings via the collection EF). |
| `query.py` | Smoke-test / query client: heartbeat, list collections, similarity search. |
| `requirements-ingest.txt` | Client dependencies for `ingest.py` / `query.py`. |
| `../deploy/deploy-chroma.sh` | Build + deploy to Cloud Run with a GCS volume mount. |

> **Version pin:** `chromadb==0.6.3` in `requirements.txt`, `requirements-ingest.txt`,
> and the MCP server (`mcp-server/requirements.txt`). Keep these identical; bump
> deliberately after validating locally.

## 1. Test locally in Docker

```bash
# from the repo root
docker compose -f chroma/docker-compose.yml up --build
# server: http://localhost:8001   heartbeat: http://localhost:8001/api/v2/heartbeat
```

> The server is published on host port **8001** (container listens on 8000).
> Port 8000 is intentionally avoided — a Chainlit app commonly runs there, and a
> Chroma client pointed at it fails with `orjson.JSONDecodeError` (it gets HTML,
> not JSON). Always point ingest/query at the port Chroma is actually on.

In another shell, ingest some docs:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r chroma/requirements-ingest.txt

python chroma/ingest.py --host localhost --port 8001 \
    --collection cgp_docs --path data/document data/skills.md
```

Data survives restarts because it's persisted to `chroma/.chroma-data` on the host.

Verify and query it with the smoke-test client:

```bash
python chroma/query.py --host localhost --port 8001 --list
python chroma/query.py --host localhost --port 8001 \
    --collection cgp_docs --query "how do I troubleshoot outbound result delivery" -k 5
```

## 2. Deploy to Cloud Run (Cloud Storage persistence)

```bash
# BUCKET defaults to <project>-chroma-data; it is created if missing.
BUCKET=my-chroma-bucket ./deploy/deploy-chroma.sh
# optional token auth:
AUTH_TOKEN="$(openssl rand -hex 24)" BUCKET=my-chroma-bucket ./deploy/deploy-chroma.sh
```

The script builds the image, ensures the Artifact Registry repo and GCS bucket
exist, and deploys with:
- `--execution-environment gen2` + a **Cloud Storage volume** mounted at `/data`
  (gcsfuse) — this is the persistence layer.
- `--max-instances 1` — **required**, because Chroma uses SQLite and gcsfuse does
  not support concurrent writers safely.
- `--no-cpu-throttling` so the DB stays responsive.

Then ingest against the deployed URL (HTTPS on 443):

```bash
python chroma/ingest.py --host chroma-server-xxxx-uc.a.run.app --port 443 --ssl \
    --token "$AUTH_TOKEN" --collection cgp_docs --path data
```

## Ingest options (highlights)

```
--path P [P ...]     files or dirs to ingest (dirs walked for .md/.txt/.log/.csv)
--collection NAME    target collection (default: rag_docs)
--chunk-method char|recursive    char = fixed sliding window (default);
                                 recursive = RecursiveCharacterTextSplitter
                                 (needs langchain-text-splitters)
--chunk-size / --chunk-overlap   chunk size / overlap in characters (default 1000 / 150)
--embedding default|openai       default = built-in MiniLM; openai needs OPENAI_API_KEY
--reset              drop the collection before ingesting
--token / --ssl      auth + HTTPS for a remote (Cloud Run) server
```

Re-running is safe: chunk IDs are deterministic (`<source>::chunk-<n>`) and the
script uses `upsert`. Pass `--reset` to drop and rebuild the collection instead.

## Use it from the MCP server (`rag_search` tool)

The MCP server (`mcp-server/main.py`) exposes a `rag_search(query, collection, n_results)`
tool that retrieves chunks from this Chroma server. Configure it via environment
variables on the MCP service:

```bash
CHROMA_HOST=chroma-server-xxxx-uc.a.run.app   # required
CHROMA_SSL=true                               # HTTPS (Cloud Run); default false
CHROMA_PORT=443                               # default: 443 if SSL else 8000
CHROMA_TOKEN=...                              # if the server requires auth
CHROMA_COLLECTION=cgp_docs                    # default collection
CHROMA_EMBEDDING=default                      # must match what you ingested with
```

The embedding function must match the one used at ingest time (default MiniLM, or
`openai`) so the query vector lands in the same space.

## Caveats
- **Single writer.** Keep `--max-instances 1`. For higher throughput or HA, move
  to a managed vector DB or Chroma's distributed/cloud offering.
- **Pin versions.** Keep `chromadb` identical in `requirements.txt` and
  `requirements-ingest.txt` to avoid client/server API drift.
- **Cold starts.** With CPU always allocated the server stays warm within an
  instance; the first ingest downloads the MiniLM embedding model to the client.
