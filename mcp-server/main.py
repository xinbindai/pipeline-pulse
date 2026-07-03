"""
FastMCP Demo Server
- Resource : stock://{ticker}/{date}                  → Yahoo Finance closing price
- Resource : servicenow://incidents                   → list all ServiceNow incidents
- Tool     : servicenow(field, query)                 → search incidents by a field
- Tool     : calculate(a, op, b)                       → performs basic arithmetic
Runs as a Streamable HTTP server (stateless, works on Cloud Run).
"""

import csv
import datetime as dt
import json
import os
from pathlib import Path

import yfinance as yf
from fastmcp import FastMCP

mcp = FastMCP(
    name="demo-server",
    instructions="A simple demo MCP server running on Google Cloud Run.",
)


# ── Resource: stock price via Yahoo Finance ─────────────────────────────────────
@mcp.resource("stock://{ticker}/{date}")
def get_stock_price(ticker: str, date: str) -> str:
    """
    Return the closing stock price for a ticker on a given date.

    URI: stock://{ticker}/{date}
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
