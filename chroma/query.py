#!/usr/bin/env python3
"""
Smoke-test / query client for a remote Chroma server.

Verifies connectivity (heartbeat), can list collections, and runs a similarity
query against a collection — printing the top matches with their source metadata
and distances. Use the same --embedding you ingested with.

Examples
--------
# Confirm the server is up and list collections
python chroma/query.py --host localhost --port 8000 --list

# Query the cgp_docs collection
python chroma/query.py --host localhost --port 8000 \
    --collection cgp_docs --query "how do I troubleshoot outbound result delivery" -k 5

# Remote Cloud Run server over HTTPS with a token
python chroma/query.py --host chroma-server-xxxx-uc.a.run.app --port 443 --ssl \
    --token "$CHROMA_TOKEN" --collection cgp_docs --query "reference index checksum mismatch"
"""
from __future__ import annotations

import argparse
import os
import sys

import chromadb
from chromadb.utils import embedding_functions


def build_client(args) -> chromadb.api.ClientAPI:
    headers = {}
    if args.token:
        if args.auth_header.lower() == "authorization":
            headers["Authorization"] = f"Bearer {args.token}"
        else:
            headers[args.auth_header] = args.token
    scheme = "https" if args.ssl else "http"
    try:
        return chromadb.HttpClient(host=args.host, port=args.port, ssl=args.ssl, headers=headers or None)
    except Exception as e:  # noqa: BLE001 - surface a clear, actionable message
        raise SystemExit(
            f"ERROR: could not connect to a Chroma server at {scheme}://{args.host}:{args.port}.\n"
            f"       {type(e).__name__}: {e}\n"
            "       Check that the server is running and reachable, and that its chromadb\n"
            "       version matches this client (chroma/requirements.txt). Verify with:\n"
            f"         curl -s {scheme}://{args.host}:{args.port}/api/v2/heartbeat"
        )


def build_embedding_function(kind: str, model: str | None):
    if kind == "openai":
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise SystemExit("ERROR: --embedding openai requires OPENAI_API_KEY.")
        return embedding_functions.OpenAIEmbeddingFunction(
            api_key=api_key, model_name=model or "text-embedding-3-small"
        )
    return embedding_functions.DefaultEmbeddingFunction()


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Query/smoke-test a remote Chroma server.")
    ap.add_argument("--host", default=os.environ.get("CHROMA_HOST", "localhost"))
    ap.add_argument("--port", type=int, default=int(os.environ.get("CHROMA_PORT", "8000")))
    ap.add_argument("--ssl", action="store_true")
    ap.add_argument("--token", default=os.environ.get("CHROMA_TOKEN"))
    ap.add_argument("--auth-header", default="Authorization")
    ap.add_argument("--collection", default="rag_docs")
    ap.add_argument("--query", help="Query text (omit with --list).")
    ap.add_argument("-k", "--n-results", type=int, default=5)
    ap.add_argument("--embedding", choices=["default", "openai"], default="default")
    ap.add_argument("--embedding-model", default=None)
    ap.add_argument("--list", action="store_true", help="List collections and exit.")
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    client = build_client(args)

    hb = client.heartbeat()
    print(f"OK: connected to Chroma at {args.host}:{args.port} (heartbeat {hb})")

    if args.list:
        cols = client.list_collections()
        if not cols:
            print("No collections.")
            return 0
        print("Collections:")
        for c in cols:
            # chromadb >=0.6 returns names (str); older returns Collection objects.
            name = c if isinstance(c, str) else c.name
            try:
                count = client.get_collection(name).count()
            except Exception:
                count = "?"
            print(f"  - {name}  ({count} items)")
        return 0

    if not args.query:
        print("ERROR: provide --query TEXT (or use --list).", file=sys.stderr)
        return 2

    ef = build_embedding_function(args.embedding, args.embedding_model)
    collection = client.get_collection(args.collection, embedding_function=ef)

    res = collection.query(
        query_texts=[args.query],
        n_results=args.n_results,
        include=["documents", "metadatas", "distances"],
    )

    docs = res.get("documents", [[]])[0]
    metas = res.get("metadatas", [[]])[0]
    dists = res.get("distances", [[]])[0]
    ids = res.get("ids", [[]])[0]

    if not docs:
        print("No results.")
        return 0

    print(f"\nTop {len(docs)} match(es) for: {args.query!r}\n")
    for rank, (id_, doc, meta, dist) in enumerate(zip(ids, docs, metas, dists), start=1):
        src = (meta or {}).get("source", "?")
        snippet = " ".join(doc.split())[:240]
        print(f"[{rank}] distance={dist:.4f}  id={id_}")
        print(f"     source: {src}")
        print(f"     {snippet}{'...' if len(doc) > 240 else ''}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
