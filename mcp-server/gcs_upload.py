#!/usr/bin/env python3
"""
Upload the MCP server's data files to a Google Cloud Storage bucket.

The MCP tools (servicenow, cgp_log_search, nginx_log_search) read their data from
GCS when GCS_BUCKET is set. Use this script to populate/refresh that bucket from
the local data/ folder.

Authentication uses Application Default Credentials (ADC):
  - Local development:  gcloud auth application-default login
  - Cloud / CI:         a service account with roles/storage.objectAdmin

By default it uploads the three objects the tools expect, preserving the data/
layout:
    servicenow/incidents.csv
    log/CGP.log
    log/nginx.log

Examples
--------
# Upload the default set from ./data (or ../data) to the bucket
GCS_BUCKET=my-bucket python mcp-server/gcs_upload.py

# Explicit bucket + data dir
python mcp-server/gcs_upload.py --bucket my-bucket --data-dir data

# Upload only some objects, or an arbitrary local file to an object path
python mcp-server/gcs_upload.py --bucket my-bucket --object log/CGP.log
python mcp-server/gcs_upload.py --bucket my-bucket --file ./out.csv servicenow/incidents.csv
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from google.cloud import storage

DEFAULT_OBJECTS = [
    "servicenow/incidents.csv",
    "log/CGP.log",
    "log/nginx.log",
]


def resolve_data_dir(explicit: str | None) -> Path:
    """Find the local data/ root: --data-dir, else ./data, else ../data from here."""
    if explicit:
        return Path(explicit)
    here = Path(__file__).resolve().parent
    for candidate in (Path("data"), here / "data", here.parent / "data"):
        if candidate.is_dir():
            return candidate
    raise SystemExit("ERROR: could not find a data/ directory; pass --data-dir.")


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Upload MCP data files to GCS (ADC auth).")
    ap.add_argument("--bucket", default=os.environ.get("GCS_BUCKET"),
                    help="Target GCS bucket (or $GCS_BUCKET).")
    ap.add_argument("--project", default=os.environ.get("GOOGLE_CLOUD_PROJECT"),
                    help="GCP project (optional; defaults from ADC).")
    ap.add_argument("--data-dir", default=None,
                    help="Local data root (default: ./data or ../data).")
    ap.add_argument("--object", dest="objects", action="append", metavar="PATH",
                    help="Object path to upload (repeatable); local file taken from "
                         "<data-dir>/<PATH>. Defaults to the standard three objects.")
    ap.add_argument("--file", nargs=2, action="append", metavar=("LOCAL", "OBJECT"),
                    help="Upload a specific local file to an object path (repeatable).")
    ap.add_argument("--dry-run", action="store_true", help="Print actions only.")
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    if not args.bucket:
        raise SystemExit("ERROR: set --bucket or the GCS_BUCKET env var.")

    # Build the (local_path, object_path) upload list.
    uploads: list[tuple[Path, str]] = []
    if args.file:
        uploads += [(Path(local), obj) for local, obj in args.file]
    if args.objects or not args.file:
        data_dir = resolve_data_dir(args.data_dir)
        for obj in (args.objects or DEFAULT_OBJECTS):
            uploads.append((data_dir / obj, obj))

    client = storage.Client(project=args.project) if args.project else storage.Client()
    bucket = client.bucket(args.bucket)

    failures = 0
    for local_path, object_path in uploads:
        if not local_path.is_file():
            print(f"SKIP  {local_path} -> gs://{args.bucket}/{object_path} (missing)", file=sys.stderr)
            failures += 1
            continue
        print(f"{'DRY  ' if args.dry_run else 'PUT  '}{local_path} -> gs://{args.bucket}/{object_path}")
        if not args.dry_run:
            bucket.blob(object_path).upload_from_filename(str(local_path))

    if failures:
        print(f"\nCompleted with {failures} skipped/missing file(s).", file=sys.stderr)
        return 1
    print(f"\nUploaded {len(uploads)} file(s) to gs://{args.bucket}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
