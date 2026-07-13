"""
FastMCP Demo Server
- Resource : servicenow://incidents                   → list all ServiceNow incidents
- Tool     : get_stock_price(ticker, date)            → Yahoo Finance closing price
- Tool     : servicenow(field, query)                 → search incidents by a field
- Tool     : cgp_log_search(run_id, sample_id, ...)   → search the CGP pipeline log
- Tool     : nginx_log_search(run_id, status, ...)    → search the nginx proxy log
- Tool     : rag_search(query, collection, n)         → retrieve chunks from Chroma
- Tool     : calculate(a, op, b)                       → performs basic arithmetic
Runs as a Streamable HTTP server (stateless, works on Cloud Run).
"""

import csv
import datetime as dt
import json
import os
import re
from pathlib import Path

import yfinance as yf
from fastmcp import FastMCP

mcp = FastMCP(
    name="demo-server",
    instructions="A simple demo MCP server running on Google Cloud Run.",
)


# ── Tool: stock price via Yahoo Finance ─────────────────────────────────────────
@mcp.tool()
def get_stock_price(ticker: str, date: str) -> str:
    """
    Return the closing stock price for a ticker on a given date.

    Args:
        ticker: Stock symbol, e.g. AAPL.
        date:   'YYYY-MM-DD', or 'today' for the latest trading day.

    If the requested date is not a trading day (weekend/holiday), the most
    recent close on or before that date is returned.
    """
    if date.lower() == "today":
        target = dt.date.today()
    else:
        try:
            target = dt.date.fromisoformat(date)
        except ValueError:
            raise ValueError(f"Invalid date '{date}'. Use 'YYYY-MM-DD' or 'today'.")

    symbol = ticker.upper()
    # end is exclusive in yfinance, so add a day to include `target`'s close.
    history = yf.Ticker(symbol).history(
        start=target.isoformat(),
        end=(target + dt.timedelta(days=1)).isoformat(),
    )

    # Fall back to the most recent close on/before target (markets closed that day).
    if history.empty:
        window = yf.Ticker(symbol).history(period="7d")
        history = window[window.index.date <= target]

    if history.empty:
        raise ValueError(f"No price data for {symbol} on or before {target.isoformat()}.")

    price = float(history["Close"].iloc[-1])
    as_of = history.index[-1].date().isoformat()
    return f"{symbol} close on {as_of}: {price:.2f} USD"


# ── Resource: ServiceNow incident search ────────────────────────────────────────
# Columns available in the incidents CSV.
SN_FIELDS = (
    "incident_id",
    "status",
    "created",
    "configuration_item",
    "description_and_note",
)


def _resolve_incidents_csv() -> Path:
    """
    Locate the ServiceNow incidents CSV.

    Order of precedence:
        1. SERVICENOW_CSV env var (explicit path).
        2. ./data/servicenow/incidents.csv   (inside the container image, /app/data).
        3. ../data/servicenow/incidents.csv  (running locally from mcp-server/).
    """
    env = os.environ.get("SERVICENOW_CSV")
    if env:
        return Path(env)

    here = Path(__file__).resolve().parent
    candidates = [
        here / "data" / "servicenow" / "incidents.csv",
        here.parent / "data" / "servicenow" / "incidents.csv",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    # Fall back to the container path; error is raised on read if truly missing.
    return candidates[0]


_incidents_cache: list[dict] | None = None


def _load_incidents() -> list[dict]:
    """Load and cache incident rows from the CSV (read once per process)."""
    global _incidents_cache
    if _incidents_cache is None:
        path = _resolve_incidents_csv()
        with open(path, newline="", encoding="utf-8") as f:
            _incidents_cache = list(csv.DictReader(f))
    return _incidents_cache


@mcp.resource("servicenow://incidents", name="servicenow-list")
def list_incidents() -> str:
    """
    List every ServiceNow incident record as JSON.

    URI: servicenow://incidents
    """
    incidents = _load_incidents()
    return json.dumps({"count": len(incidents), "incidents": incidents}, indent=2)


@mcp.tool(name="servicenow")
def search_incidents(field: str, query: str) -> str:
    """
    Search ServiceNow incident records by a single field.

    Args:
        field: One of incident_id, status, created, configuration_item,
               description_and_note.
        query: The value to match.

    Matching rules (all case-insensitive):
        - description_and_note: keyword search. Whitespace-separated keywords are
          ANDed together; a row matches only if every keyword appears in its note.
        - all other fields: substring match (e.g. status='closed', a date prefix
          like created='2026-06', or configuration_item='CGP').

    Returns a JSON object with the query and the matching incidents.
    """
    field = field.strip().lower()
    if field not in SN_FIELDS:
        raise ValueError(
            f"Invalid field '{field}'. Choose one of: {', '.join(SN_FIELDS)}."
        )

    rows = _load_incidents()
    needle = query.strip().lower()

    if field == "description_and_note":
        keywords = needle.split()
        matches = [
            r
            for r in rows
            if all(kw in r["description_and_note"].lower() for kw in keywords)
        ]
    else:
        matches = [r for r in rows if needle in r[field].lower()]

    return json.dumps(
        {"field": field, "query": query, "count": len(matches), "incidents": matches},
        indent=2,
    )


# ── Tools: workflow log search (CGP pipeline + nginx proxy) ──────────────────────
# Both logs live under data/log/ and are bundled into the image at /app/data/log.
def _resolve_data_file(*relparts: str) -> Path:
    """
    Locate a bundled data file (e.g. log/CGP.log).

    Order of precedence:
        1. DATA_DIR env var (explicit data root).
        2. ./data/...   (inside the container image, /app/data).
        3. ../data/...  (running locally from mcp-server/).
    """
    here = Path(__file__).resolve().parent
    roots = []
    if os.environ.get("DATA_DIR"):
        roots.append(Path(os.environ["DATA_DIR"]))
    roots += [here / "data", here.parent / "data"]
    for root in roots:
        candidate = root.joinpath(*relparts)
        if candidate.exists():
            return candidate
    return roots[0].joinpath(*relparts)  # fall back; read raises if truly missing


_log_cache: dict[str, list[str]] = {}


def _load_log(*relparts: str) -> list[str]:
    """Load and cache the lines of a bundled log file (read once per process)."""
    key = "/".join(relparts)
    if key not in _log_cache:
        path = _resolve_data_file(*relparts)
        with open(path, encoding="utf-8", errors="replace") as f:
            _log_cache[key] = f.read().splitlines()
    return _log_cache[key]


# CGP line: "2026-06-25 11:02:18 ERROR [DNA-Align] <message>"
_CGP_LINE_RE = re.compile(
    r"^(?P<ts>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+"
    r"(?P<level>[A-Z]+)\s+\[(?P<stage>[^\]]+)\]\s+(?P<message>.*)$"
)


@mcp.tool(name="cgp_log_search")
def cgp_log_search(
    run_id: str | None = None,
    sample_id: str | None = None,
    log_type: str | None = None,
    limit: int = 100,
) -> str:
    """
    Search the CGP genomics pipeline log (data/log/CGP.log) to troubleshoot an
    analysis task. Filters are AND-combined; omit a filter to ignore it.

    Args:
        run_id:    Illumina run ID (substring), e.g. '250625_NB551234_0142_AHKVJ7BGXM'.
        sample_id: Sample/library ID (substring), e.g. 'CGP-0019'.
        log_type:  Log level: INFO, WARN, or ERROR (case-insensitive).
        limit:     Max matching records to return (default 100).

    Returns JSON with the matching log records, each parsed into timestamp, level,
    stage, and message (plus the raw line and 1-based line number).
    """
    lines = _load_log("log", "CGP.log")
    rid = (run_id or "").lower()
    sid = (sample_id or "").lower()
    lvl = (log_type or "").strip().upper()

    matches = []
    for n, line in enumerate(lines, start=1):
        low = line.lower()
        if rid and rid not in low:
            continue
        if sid and sid not in low:
            continue
        m = _CGP_LINE_RE.match(line)
        level = m.group("level") if m else None
        if lvl and (level or "").upper() != lvl:
            continue
        matches.append(
            {
                "line": n,
                "timestamp": m.group("ts") if m else None,
                "level": level,
                "stage": m.group("stage") if m else None,
                "message": m.group("message") if m else line,
                "raw": line,
            }
        )
        if len(matches) >= limit:
            break

    return json.dumps(
        {
            "log": "data/log/CGP.log",
            "filters": {"run_id": run_id, "sample_id": sample_id, "log_type": log_type},
            "count": len(matches),
            "records": matches,
        },
        indent=2,
    )


# nginx access line: '<ip> - - [ts] "METHOD PATH HTTP/1.1" STATUS ...'
_NGINX_ACCESS_RE = re.compile(
    r'^(?P<ip>\S+) \S+ \S+ \[(?P<ts>[^\]]+)\] '
    r'"(?P<method>[A-Z]+) (?P<path>\S+)[^"]*" (?P<status>\d{3})\b'
)
# nginx error line: '2026/06/26 04:00:16 [error] 2471#0: <message>'
_NGINX_ERROR_RE = re.compile(
    r"^(?P<ts>\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}) \[(?P<level>\w+)\] (?P<message>.*)$"
)


@mcp.tool(name="nginx_log_search")
def nginx_log_search(
    run_id: str | None = None,
    status: str | None = None,
    keyword: str | None = None,
    limit: int = 100,
) -> str:
    """
    Search the nginx reverse-proxy log (data/log/nginx.log) that sits between the
    CGP pipeline and the reporting tool. Contains both access and error entries.
    Filters are AND-combined; omit a filter to ignore it.

    Args:
        run_id:  Illumina run ID (substring); matches the runId= query parameter.
        status:  HTTP status code, e.g. '502' or '404' (applies to access entries).
        keyword: Free-text substring, e.g. 'timed out', 'connection refused', 'auth'.
        limit:   Max matching entries to return (default 100).

    Returns JSON with matching entries, each classified as 'access' or 'error' and
    parsed (method/path/status for access; level/message for error), plus the raw
    line and 1-based line number.
    """
    lines = _load_log("log", "nginx.log")
    rid = (run_id or "").lower()
    want_status = (status or "").strip()
    kw = (keyword or "").lower()

    matches = []
    for n, line in enumerate(lines, start=1):
        low = line.lower()
        if rid and rid not in low:
            continue
        if kw and kw not in low:
            continue

        access = _NGINX_ACCESS_RE.match(line)
        error = None if access else _NGINX_ERROR_RE.match(line)

        if want_status:
            # Status only applies to access entries; drop everything else.
            if not access or access.group("status") != want_status:
                continue

        if access:
            entry = {
                "line": n,
                "type": "access",
                "client_ip": access.group("ip"),
                "timestamp": access.group("ts"),
                "method": access.group("method"),
                "path": access.group("path"),
                "status": access.group("status"),
                "raw": line,
            }
        elif error:
            entry = {
                "line": n,
                "type": "error",
                "timestamp": error.group("ts"),
                "level": error.group("level"),
                "message": error.group("message"),
                "raw": line,
            }
        else:
            entry = {"line": n, "type": "other", "raw": line}

        matches.append(entry)
        if len(matches) >= limit:
            break

    return json.dumps(
        {
            "log": "data/log/nginx.log",
            "filters": {"run_id": run_id, "status": status, "keyword": keyword},
            "count": len(matches),
            "entries": matches,
        },
        indent=2,
    )


# ── Tool: RAG search over a Chroma server ────────────────────────────────────────
# Configured via environment (so it works against a local or Cloud Run Chroma):
#   CHROMA_HOST        Chroma host (required to use this tool)
#   CHROMA_PORT        Port (default: 443 when CHROMA_SSL=true, else 8000)
#   CHROMA_SSL         'true' for HTTPS (Cloud Run) — default false
#   CHROMA_TOKEN       Optional auth token (sent as Authorization: Bearer <token>)
#   CHROMA_COLLECTION  Default collection name (default: rag_docs)
#   CHROMA_EMBEDDING   'default' (built-in MiniLM) or 'openai' — must match ingest
_chroma_collection_cache: dict = {}


def _get_chroma_collection(collection: str):
    """Return a cached Chroma collection handle for the given name."""
    if collection in _chroma_collection_cache:
        return _chroma_collection_cache[collection]

    # Imported lazily so the rest of the server runs even without chromadb installed.
    import chromadb
    from chromadb.utils import embedding_functions

    host = os.environ.get("CHROMA_HOST")
    if not host:
        raise ValueError(
            "rag_search is not configured: set CHROMA_HOST (and CHROMA_PORT/"
            "CHROMA_SSL/CHROMA_TOKEN as needed)."
        )
    ssl = os.environ.get("CHROMA_SSL", "false").lower() in ("1", "true", "yes")
    port = int(os.environ.get("CHROMA_PORT", "443" if ssl else "8000"))
    token = os.environ.get("CHROMA_TOKEN")
    headers = {"Authorization": f"Bearer {token}"} if token else None

    if os.environ.get("CHROMA_EMBEDDING", "default").lower() == "openai":
        ef = embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.environ["OPENAI_API_KEY"],
            model_name=os.environ.get("CHROMA_EMBEDDING_MODEL", "text-embedding-3-small"),
        )
    else:
        ef = embedding_functions.DefaultEmbeddingFunction()

    client = chromadb.HttpClient(host=host, port=port, ssl=ssl, headers=headers)
    handle = client.get_collection(collection, embedding_function=ef)
    _chroma_collection_cache[collection] = handle
    return handle


@mcp.tool()
def rag_search(query: str, collection: str | None = None, n_results: int = 5) -> str:
    """
    Retrieve the most relevant document chunks for a query from the Chroma
    vector database (RAG retrieval). Chunks are ingested by chroma/ingest.py.

    Args:
        query:       Natural-language search text.
        collection:  Collection to search (default: $CHROMA_COLLECTION or 'rag_docs').
        n_results:   Number of chunks to return (default: 5).

    Returns a JSON object with the matches, each including the chunk text, its
    source metadata, and the similarity distance (lower = closer).
    """
    name = collection or os.environ.get("CHROMA_COLLECTION", "rag_docs")
    handle = _get_chroma_collection(name)

    res = handle.query(
        query_texts=[query],
        n_results=n_results,
        include=["documents", "metadatas", "distances"],
    )
    docs = res.get("documents", [[]])[0]
    metas = res.get("metadatas", [[]])[0]
    dists = res.get("distances", [[]])[0]
    ids = res.get("ids", [[]])[0]

    matches = [
        {"id": i, "document": d, "metadata": m, "distance": dist}
        for i, d, m, dist in zip(ids, docs, metas, dists)
    ]
    return json.dumps(
        {"query": query, "collection": name, "count": len(matches), "matches": matches},
        indent=2,
    )


# ── Tool ──────────────────────────────────────────────────────────────────────
@mcp.tool()
def calculate(a: float, op: str, b: float) -> str:
    """
    Perform basic arithmetic.

    Args:
        a:  Left operand.
        op: Operator — one of '+', '-', '*', '/'.
        b:  Right operand.

    Returns:
        A string with the expression and its result.
    """
    ops = {
        "+": lambda x, y: x + y,
        "-": lambda x, y: x - y,
        "*": lambda x, y: x * y,
        "/": lambda x, y: x / y,
    }
    if op not in ops:
        raise ValueError(f"Unsupported operator '{op}'. Use one of: +, -, *, /")
    if op == "/" and b == 0:
        raise ValueError("Division by zero is not allowed.")
    result = ops[op](a, b)
    return f"{a} {op} {b} = {result}"


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    # Streamable HTTP transport — stateless, Cloud Run friendly
    mcp.run(transport="streamable-http", host="0.0.0.0", port=port)
