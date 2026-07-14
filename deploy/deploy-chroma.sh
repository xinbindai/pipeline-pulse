#!/usr/bin/env bash
#
# Build the Chroma server image and deploy it to Google Cloud Run, using a
# Cloud Storage bucket (mounted via gcsfuse at /data) as the persistence layer.
#
# Usage (from anywhere in the repository):
#   cp deploy/deploy-chroma.env.example deploy/deploy-chroma.env   # then edit
#   ./deploy/deploy-chroma.sh
#
# Configuration is loaded from deploy/deploy-chroma.env (override the path with
# ENV_FILE=...), then from environment variables (which take precedence). Defaults
# shown; PROJECT_ID falls back to your active gcloud config, BUCKET defaults to
# <project>-chroma-data:
#   PROJECT_ID   GCP project id            (default: `gcloud config get-value project`)
#   REGION       Cloud Run / AR region     (default: us-central1)
#   SERVICE      Cloud Run service name    (default: chroma-server)
#   AR_REPO      Artifact Registry repo    (default: mcp)
#   BUCKET       GCS bucket for /data       (default: <project>-chroma-data)
#   TAG          Image tag                 (default: current git short SHA, else "latest")
#   AUTH_TOKEN   If set, require this token (Authorization: Bearer <token>)
#   ALLOW_UNAUTH Allow unauthenticated     (default: true)
#
# IMPORTANT: Chroma persists to a single SQLite DB + index files. gcsfuse does not
# support concurrent writers safely, so this deploys with --max-instances=1.
set -euo pipefail

# Load KEY=value pairs from a config file. Lines may use an optional `export`
# prefix and quoted values; blank/`#` lines are ignored. Variables already set in
# the environment take precedence, so you can still override inline.
load_env_file() {
  local file="$1" line key val
  [[ -f "$file" ]] || return 0
  echo "Loading config from ${file}"
  while IFS= read -r line || [[ -n "$line" ]]; do
    line="${line%$'\r'}"
    [[ "$line" =~ ^[[:space:]]*(#|$) ]] && continue
    line="${line#export }"
    key="${line%%=*}"; val="${line#*=}"
    key="${key//[[:space:]]/}"
    val="${val#"${val%%[![:space:]]*}"}"; val="${val%"${val##*[![:space:]]}"}"
    [[ "$val" == \"*\" ]] && val="${val:1:${#val}-2}"
    [[ "$val" == \'*\' ]] && val="${val:1:${#val}-2}"
    [[ -z "$key" ]] && continue
    [[ -n "${!key:-}" ]] || export "$key=$val"
  done < "$file"
}

# This script lives in deploy/; the repo root is its parent.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
CHROMA_DIR="${REPO_ROOT}/chroma"
cd "$REPO_ROOT"

# Load deploy config (deploy/deploy-chroma.env by default; override via ENV_FILE).
ENV_FILE="${ENV_FILE:-${SCRIPT_DIR}/deploy-chroma.env}"
load_env_file "$ENV_FILE"

# ── Configuration ───────────────────────────────────────────────────────────────
PROJECT_ID="${PROJECT_ID:-$(gcloud config get-value project 2>/dev/null || true)}"
REGION="${REGION:-us-central1}"
SERVICE="${SERVICE:-chroma-server}"
AR_REPO="${AR_REPO:-mcp}"
TAG="${TAG:-$(git rev-parse --short HEAD 2>/dev/null || echo latest)}"
ALLOW_UNAUTH="${ALLOW_UNAUTH:-true}"

if [[ -z "$PROJECT_ID" ]]; then
  echo "ERROR: PROJECT_ID is not set and no active gcloud project is configured." >&2
  echo "       Run 'gcloud config set project <id>' or 'PROJECT_ID=<id> ...'." >&2
  exit 1
fi

BUCKET="${BUCKET:-${PROJECT_ID}-chroma-data}"
IMAGE="${REGION}-docker.pkg.dev/${PROJECT_ID}/${AR_REPO}/${SERVICE}:${TAG}"

echo "Project : ${PROJECT_ID}"
echo "Region  : ${REGION}"
echo "Service : ${SERVICE}"
echo "Bucket  : gs://${BUCKET} -> /data"
echo "Image   : ${IMAGE}"
echo

# ── Prerequisites ───────────────────────────────────────────────────────────────
# Artifact Registry repo (idempotent).
if ! gcloud artifacts repositories describe "$AR_REPO" \
      --project "$PROJECT_ID" --location "$REGION" >/dev/null 2>&1; then
  echo "Creating Artifact Registry repo '${AR_REPO}' in ${REGION}..."
  gcloud artifacts repositories create "$AR_REPO" \
    --project "$PROJECT_ID" --location "$REGION" \
    --repository-format=docker --description="CGP demo images"
fi

# GCS bucket for Chroma persistence (idempotent).
if ! gcloud storage buckets describe "gs://${BUCKET}" --project "$PROJECT_ID" >/dev/null 2>&1; then
  echo "Creating GCS bucket gs://${BUCKET}..."
  gcloud storage buckets create "gs://${BUCKET}" \
    --project "$PROJECT_ID" --location "$REGION" --uniform-bucket-level-access
fi

# ── Build & push ────────────────────────────────────────────────────────────────
echo "Building image (context: chroma/)..."
gcloud auth configure-docker "${REGION}-docker.pkg.dev" --quiet
docker build -f "${CHROMA_DIR}/Dockerfile" -t "$IMAGE" "$CHROMA_DIR"

echo "Pushing ${IMAGE}..."
docker push "$IMAGE"

# ── Deploy ──────────────────────────────────────────────────────────────────────
AUTH_FLAG="--no-allow-unauthenticated"
[[ "$ALLOW_UNAUTH" == "true" ]] && AUTH_FLAG="--allow-unauthenticated"

ENV_VARS="IS_PERSISTENT=TRUE,PERSIST_DIRECTORY=/data,ANONYMIZED_TELEMETRY=FALSE"
if [[ -n "${AUTH_TOKEN:-}" ]]; then
  ENV_VARS="${ENV_VARS},CHROMA_SERVER_AUTHN_PROVIDER=chromadb.auth.token_authn.TokenAuthenticationServerProvider,CHROMA_SERVER_AUTHN_CREDENTIALS=${AUTH_TOKEN}"
fi

echo "Deploying to Cloud Run (gen2, GCS volume, max-instances=1)..."
gcloud run deploy "$SERVICE" \
  --project "$PROJECT_ID" \
  --region "$REGION" \
  --image "$IMAGE" \
  --platform managed \
  --execution-environment gen2 \
  --add-volume "name=chroma-data,type=cloud-storage,bucket=${BUCKET}" \
  --add-volume-mount "volume=chroma-data,mount-path=/data" \
  --set-env-vars "$ENV_VARS" \
  --memory 2Gi --cpu 2 \
  --no-cpu-throttling \
  --max-instances 1 \
  --timeout 3600 \
  $AUTH_FLAG

URL="$(gcloud run services describe "$SERVICE" \
  --project "$PROJECT_ID" --region "$REGION" --format 'value(status.url)')"

echo
echo "Deployed ${SERVICE} -> ${URL}"
echo "Heartbeat: ${URL}/api/v2/heartbeat"
echo
echo "Ingest against it with:"
echo "  python chroma/ingest.py --host ${URL#https://} --port 443 --ssl \\"
echo "    ${AUTH_TOKEN:+--token \"\$AUTH_TOKEN\" }--collection cgp_docs --path data"
