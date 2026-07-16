# Pipeline Pulse

**Quest AI Hackathon 2026**

Pipeline Pulse helps the bioinformatics operations team troubleshoot incidents in the
Quest **CGP** (Comprehensive Genomic Profiling) workflow. When an incident is filed as a
ticket, an AI assistant reads the ticket, pulls the relevant pipeline and proxy logs,
searches past incidents, and consults the SOP and architecture docs to explain what broke
and what to do about it.

This repository holds the **data and services** the assistant runs on:

- an **MCP server** exposing log and ticket search tools,
- a **Chroma** vector server plus the ingest script that powers RAG over the CGP documents,
- **deploy scripts** that put both on Google Cloud Run.

The agent itself lives in a separate repo: **pipeline-pulse-agent**.

```
ticket / question
       │
       ▼
   agent (pipeline-pulse-agent)
       │
       ├── MCP server ──► servicenow incidents, CGP.log, nginx.log   (mcp-server/, GCS)
       └── rag_search  ──► Chroma vector server                      (chroma/, GCS)
```

---

## Repository layout

| Path | What it is |
|------|------------|
| [data/](data/) | Mockup CGP workflow dataset: documents, logs, tickets. |
| [mcp-server/](mcp-server/) | FastMCP server exposing log / ticket / RAG search tools. |
| [chroma/](chroma/) | Remote Chroma vector server + `ingest.py` (the ingest half of RAG). |
| [deploy/](deploy/) | Scripts to deploy both services to GCP Cloud Run. |

### `data/` — mockup CGP workflow

Everything here is fabricated for the demo; no real patient or production data.

- [data/document/](data/document/) — SOP and architecture material, ingested into Chroma for RAG.
  - [CGP-reference-guide.md](data/document/CGP-reference-guide.md) — TruSight Oncology 500 assay reference guide (sample prep, consumables, protocol).
  - [CGP-troubleshooting-guide.md](data/document/CGP-troubleshooting-guide.md) — system overview, data flow, and the triage gates (A–D) the assistant reasons over.
- [data/log/](data/log/) — logs for the two modules in the CGP workflow.
  - [CGP.log](data/log/CGP.log) — the analysis pipeline (DRAGEN, annotation, reporting hand-off).
  - [nginx.log](data/log/nginx.log) — the proxy server in front of the reporting tool.
- [data/servicenow/](data/servicenow/) — [incidents.csv](data/servicenow/incidents.csv), mockup ServiceNow tickets
  (`incident_id, status, created, configuration_item, description_and_note`). Mostly
  closed incidents (the searchable history) plus a couple of open ones to troubleshoot.

Logs and tickets are served by the MCP server; documents are embedded into Chroma.

The **Illumina Run ID** is the correlation key that ties a ticket to the pipeline log and
the proxy log — see section 1 of the troubleshooting guide.

> Note: `data/skills.md` is currently an empty placeholder.

### `mcp-server/` — log and ticket search over MCP

A [FastMCP](https://github.com/jlowin/fastmcp) server, runnable locally and deployable to
Cloud Run. It speaks streamable HTTP (stateless), so the endpoint is `<url>/mcp`.

| Tool / resource | Purpose |
|---|---|
| `servicenow(field, query)` | Search incidents by any CSV field. |
| `servicenow://incidents` (resource) | List all incidents. |
| `cgp_log_search(run_id, sample_id, …)` | Search the CGP pipeline log. |
| `nginx_log_search(run_id, status, …)` | Search the nginx proxy log. |
| `rag_search(query, collection, n_results)` | Retrieve document chunks from Chroma. |
| `get_stock_price(ticker, date)`, `calculate(a, op, b)` | Demo tools, unrelated to CGP. |

Tickets and logs load from a **GCS bucket** when `GCS_BUCKET` is set (Cloud Run uses its
service account; locally, Application Default Credentials), and fall back to the bundled
`data/` files otherwise.

Run it locally:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r mcp-server/requirements.txt

python mcp-server/main.py          # http://localhost:8080/mcp  (PORT to override)
```

With no `GCS_BUCKET` set it reads the local `data/` folder — that's the quickest way to test.

### `chroma/` — vector service and RAG ingest

A Chroma server you can run in Docker locally or deploy to Cloud Run with a GCS bucket
mounted at `/data` for persistence. `ingest.py` discovers files, chunks them, and upserts
them into a collection; `query.py` is a smoke-test client. Re-running ingest is safe —
chunk IDs are deterministic.

```bash
docker compose -f chroma/docker-compose.yml up --build     # server on :8001

pip install -r chroma/requirements-ingest.txt
python chroma/ingest.py --host localhost --port 8001 \
    --collection cgp_docs --path data/document
python chroma/query.py --host localhost --port 8001 \
    --collection cgp_docs --query "report never generated" -k 5
```

See [chroma/README.md](chroma/README.md) for ingest options, Cloud Run deployment, the
`CHROMA_*` env vars the MCP server's `rag_search` needs, and the single-writer caveat
(`--max-instances 1`, because Chroma uses SQLite over gcsfuse).

### `deploy/` — Cloud Run

Both scripts read `deploy/*.env` (copy the `.example` files), fall back to your active
gcloud project, and create the Artifact Registry repo and GCS buckets they need.

```bash
cp deploy/deploy-mcp.env.example    deploy/deploy-mcp.env
cp deploy/deploy-chroma.env.example deploy/deploy-chroma.env

./deploy/deploy-chroma.sh                      # vector server → <project>-chroma-data
GCS_BUCKET=<bucket> python mcp-server/gcs_upload.py   # upload logs + tickets
./deploy/deploy-mcp.sh                         # MCP server  → <project>-mcp-data
```

`deploy-mcp.sh` prints the MCP endpoint (`<url>/mcp`); `deploy-chroma.sh` prints the
heartbeat URL and the matching ingest command. Point the MCP service at Chroma with
`CHROMA_HOST` / `CHROMA_SSL` / `CHROMA_PORT` / `CHROMA_TOKEN` / `CHROMA_COLLECTION`, and
make sure `CHROMA_EMBEDDING` matches what you ingested with.

---

## End-to-end setup

1. **Ingest the docs.** Start Chroma (local or Cloud Run) and run `chroma/ingest.py` over
   `data/document` into the `cgp_docs` collection.
2. **Stage the tool data.** Either leave `GCS_BUCKET` unset to use the bundled `data/`
   files locally, or run `mcp-server/gcs_upload.py` to populate the bucket.
3. **Start the MCP server** with the `CHROMA_*` env vars pointing at Chroma.
4. **Connect the agent** (pipeline-pulse-agent) to `<mcp-url>/mcp` and ask it things like:

   - *"List two open tickets"* → `INC0042046` (missing report for `sample_2026_0050`) and
     `INC0042047` (missing report for `sample_2026_0076`).
   - *"Why is the report for sample_2026_0050 missing?"* → the agent correlates the ticket
     with `CGP.log` and `nginx.log` and checks the troubleshooting guide via RAG.

## Requirements

- Python 3.12, Docker, and `gcloud` (authenticated) for the GCP path.
- `chromadb==0.6.3` is pinned in `mcp-server/requirements.txt`, `chroma/requirements.txt`,
  and `chroma/requirements-ingest.txt` — keep the three identical to avoid client/server drift.
