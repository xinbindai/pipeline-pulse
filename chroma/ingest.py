#!/usr/bin/env python3
"""
RAG data ingest for a remote Chroma server.

Reads text files, splits them into overlapping chunks, and upserts them into a
Chroma collection. Embeddings are computed by the collection's embedding
function (Chroma's built-in MiniLM by default, or OpenAI with --embedding openai),
so you only need to supply text.

Examples
--------
# Local server started via docker compose
python chroma/ingest.py --host localhost --port 8000 \
    --collection cgp_docs --path data/document data/skills.md

# Remote Cloud Run server (HTTPS on 443) with token auth
python chroma/ingest.py --host chroma-server-xxxx-uc.a.run.app --port 443 --ssl \
    --token "$CHROMA_TOKEN" --collection cgp_docs --path data

# Re-ingest cleanly and use OpenAI embeddings
OPENAI_API_KEY=... python chroma/ingest.py --host localhost --port 8000 \
    --collection cgp_docs --path data --reset --embedding openai

# Use the recursive splitter (RecursiveCharacterTextSplitter)
python chroma/ingest.py --host localhost --port 8000 \
    --collection cgp_docs --path data/document --chunk-method recursive
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import chromadb
from chromadb.utils import embedding_functions

DEFAULT_EXTENSIONS = {".md", ".txt", ".log", ".csv"}


# ── File discovery & chunking ────────────────────────────────────────────────────
def discover_files(paths: list[str], extensions: set[str]) -> list[Path]:
    """Expand the given paths into a sorted list of text files."""
    found: set[Path] = set()
    for raw in paths:
        p = Path(raw)
        if p.is_file():
            found.add(p)
        elif p.is_dir():
            for f in p.rglob("*"):
                if f.is_file() and f.suffix.lower() in extensions:
                    found.add(f)
        else:
            print(f"WARNING: path not found, skipping: {p}", file=sys.stderr)
    return sorted(found)


def chunk_text(text: str, size: int, overlap: int) -> list[str]:
    """Split text into ~`size`-char chunks with `overlap` chars of context."""
    if size <= 0:
        return [text] if text.strip() else []
    if overlap >= size:
        raise ValueError("--chunk-overlap must be smaller than --chunk-size")

    chunks: list[str] = []
    start = 0
    n = len(text)
    step = size - overlap
    while start < n:
        chunk = text[start : start + size].strip()
        if chunk:
            chunks.append(chunk)
        start += step
    return chunks


def build_splitter(method: str, size: int, overlap: int):
    """
    Return a callable text -> list[str] for the chosen chunking method.

    - "char":      fixed-size sliding window over characters (see chunk_text).
    - "recursive": LangChain's RecursiveCharacterTextSplitter, which splits on a
                   hierarchy of separators (paragraphs → lines → words) to keep
                   chunks more semantically coherent.
    """
    if method == "recursive":
        try:
            from langchain_text_splitters import RecursiveCharacterTextSplitter
        except ImportError:
            raise SystemExit(
                "ERROR: --chunk-method recursive requires 'langchain-text-splitters'.\n"
                "       pip install langchain-text-splitters\n"
                "       (it is listed in chroma/requirements-ingest.txt)."
            )
        splitter = RecursiveCharacterTextSplitter(chunk_size=size, chunk_overlap=overlap)
        return lambda text: [c.strip() for c in splitter.split_text(text) if c.strip()]

    # Default: character sliding window.
    return lambda text: chunk_text(text, size, overlap)


# ── Embedding function ───────────────────────────────────────────────────────────
def build_embedding_function(kind: str, model: str | None):
    if kind == "openai":
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise SystemExit("ERROR: --embedding openai requires OPENAI_API_KEY to be set.")
        return embedding_functions.OpenAIEmbeddingFunction(
            api_key=api_key,
            model_name=model or "text-embedding-3-small",
        )
    # Default: Chroma's built-in ONNX MiniLM (all-MiniLM-L6-v2), downloaded once.
    return embedding_functions.DefaultEmbeddingFunction()


# ── Chroma client ────────────────────────────────────────────────────────────────
def build_client(args) -> chromadb.api.ClientAPI:
    headers = {}
    if args.token:
        if args.auth_header.lower() == "authorization":
            headers["Authorization"] = f"Bearer {args.token}"
        else:
            headers[args.auth_header] = args.token
    scheme = "https" if args.ssl else "http"
    try:
        return chromadb.HttpClient(
            host=args.host,
            port=args.port,
            ssl=args.ssl,
            headers=headers or None,
        )
    except Exception as e:  # noqa: BLE001 - surface a clear, actionable message
        raise SystemExit(
            f"ERROR: could not connect to a Chroma server at {scheme}://{args.host}:{args.port}.\n"
            f"       {type(e).__name__}: {e}\n"
            "       Check that the server is running and reachable, and that its chromadb\n"
            "       version matches this client (chroma/requirements.txt). Verify with:\n"
            f"         curl -s {scheme}://{args.host}:{args.port}/api/v2/heartbeat"
        )


# ── Main ─────────────────────────────────────────────────────────────────────────
def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Ingest text into a remote Chroma server for RAG.")
    ap.add_argument("--host", default=os.environ.get("CHROMA_HOST", "localhost"),
                    help="Chroma server host (default: localhost or $CHROMA_HOST).")
    ap.add_argument("--port", type=int, default=int(os.environ.get("CHROMA_PORT", "8000")),
                    help="Chroma server port (default: 8000; use 443 for Cloud Run HTTPS).")
    ap.add_argument("--ssl", action="store_true",
                    help="Use HTTPS (set this for Cloud Run).")
    ap.add_argument("--token", default=os.environ.get("CHROMA_TOKEN"),
                    help="Auth token, if the server requires one ($CHROMA_TOKEN).")
    ap.add_argument("--auth-header", default="Authorization",
                    help="Auth header name (default: Authorization/Bearer).")
    ap.add_argument("--collection", default="rag_docs",
                    help="Target collection name (default: rag_docs).")
    ap.add_argument("--path", nargs="+", required=True,
                    help="One or more files or directories to ingest.")
    ap.add_argument("--extensions", nargs="+", default=sorted(DEFAULT_EXTENSIONS),
                    help="File extensions to include when a directory is given.")
    ap.add_argument("--chunk-method", choices=["char", "recursive"], default="char",
                    help="Chunking strategy: 'char' (fixed sliding window) or "
                         "'recursive' (RecursiveCharacterTextSplitter). Default: char.")
    ap.add_argument("--chunk-size", type=int, default=1000, help="Chunk size in characters.")
    ap.add_argument("--chunk-overlap", type=int, default=150, help="Overlap in characters.")
    ap.add_argument("--batch-size", type=int, default=100, help="Upsert batch size.")
    ap.add_argument("--embedding", choices=["default", "openai"], default="default",
                    help="Embedding function (default: Chroma MiniLM).")
    ap.add_argument("--embedding-model", default=None,
                    help="Override embedding model name (OpenAI).")
    ap.add_argument("--reset", action="store_true",
                    help="Delete the collection before ingesting.")
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    extensions = {e if e.startswith(".") else f".{e}" for e in (x.lower() for x in args.extensions)}

    files = discover_files(args.path, extensions)
    if not files:
        print("No matching files found. Nothing to ingest.", file=sys.stderr)
        return 1
    print(f"Discovered {len(files)} file(s).")

    client = build_client(args)
    client.heartbeat()  # fail fast if the server is unreachable
    ef = build_embedding_function(args.embedding, args.embedding_model)
    split = build_splitter(args.chunk_method, args.chunk_size, args.chunk_overlap)
    print(f"Chunking method: {args.chunk_method} "
          f"(size={args.chunk_size}, overlap={args.chunk_overlap})")

    if args.reset:
        try:
            client.delete_collection(args.collection)
            print(f"Deleted existing collection '{args.collection}'.")
        except Exception:
            pass

    collection = client.get_or_create_collection(
        name=args.collection,
        embedding_function=ef,
        metadata={"hnsw:space": "cosine"},
    )

    ids: list[str] = []
    documents: list[str] = []
    metadatas: list[dict] = []

    def flush() -> None:
        if not ids:
            return
        collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
        print(f"  upserted {len(ids)} chunk(s) (collection total now {collection.count()})")
        ids.clear(); documents.clear(); metadatas.clear()

    total_chunks = 0
    for f in files:
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except Exception as e:  # noqa: BLE001
            print(f"WARNING: could not read {f}: {e}", file=sys.stderr)
            continue

        source = str(f)
        chunks = split(text)
        print(f"- {source}: {len(chunks)} chunk(s)")
        for i, chunk in enumerate(chunks):
            ids.append(f"{source}::chunk-{i}")
            documents.append(chunk)
            metadatas.append({"source": source, "chunk": i, "filename": f.name})
            total_chunks += 1
            if len(ids) >= args.batch_size:
                flush()
    flush()

    print(f"\nDone. Ingested {total_chunks} chunk(s) from {len(files)} file(s) "
          f"into collection '{args.collection}'.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
