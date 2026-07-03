#!/usr/bin/env bash
#
# Build the CGP demo MCP server image (repo-root context, single data/ copy)
# and deploy it to Google Cloud Run.
#
# Usage (from the repository root):
#   ./deploy.sh
#
# Configuration is via environment variables (all have sensible defaults except
# PROJECT_ID, which falls back to your active gcloud config):
#   PROJECT_ID   GCP project id            (default: `gcloud config get-value project`)
#   REGION       Cloud Run / AR region     (default: us-central1)
#   SERVICE      Cloud Run service name    (default: bx-workflow-mcp)
#   AR_REPO      Artifact Registry repo    (default: mcp)
#   TAG          Image tag                 (default: current git short SHA, else "latest")
#   ALLOW_UNAUTH Allow unauthenticated     (default: true)
#
set -euo pipefail

# Always operate from the repository root (the build context).
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_ROOT"

# ── Configuration ───────────────────────────────────────────────────────────────
PROJECT_ID="${PROJECT_ID:-$(gcloud config get-value project 2>/dev/null || true)}"
REGION="${REGION:-us-central1}"
SERVICE="${SERVICE:-bx-workflow-mcp}"
AR_REPO="${AR_REPO:-mcp}"
TAG="${TAG:-$(git rev-parse --short HEAD 2>/dev/null || echo latest)}"
ALLOW_UNAUTH="${ALLOW_UNAUTH:-true}"

if [[ -z "$PROJECT_ID" ]]; then
  echo "ERROR: PROJECT_ID is not set and no active gcloud project is configured." >&2
  echo "       Run 'gcloud config set project <id>' or 'PROJECT_ID=<id> ./deploy.sh'." >&2
  exit 1
fi

IMAGE="${REGION}-docker.pkg.dev/${PROJECT_ID}/${AR_REPO}/${SERVICE}:${TAG}"

echo "Project : ${PROJECT_ID}"
echo "Region  : ${REGION}"
echo "Service : ${SERVICE}"
echo "Image   : ${IMAGE}"
echo

# ── Prerequisites ───────────────────────────────────────────────────────────────
# Ensure the Artifact Registry repo exists (idempotent).
if ! gcloud artifacts repositories describe "$AR_REPO" \
      --project "$PROJECT_ID" --location "$REGION" >/dev/null 2>&1; then
  echo "Creating Artifact Registry repo '${AR_REPO}' in ${REGION}..."
  gcloud artifacts repositories create "$AR_REPO" \
    --project "$PROJECT_ID" --location "$REGION" \
    --repository-format=docker \
    --description="CGP demo MCP server images"
fi

# ── Build & push ────────────────────────────────────────────────────────────────
# The Dockerfile lives in mcp-server/ while the build context is the repo root
# (so COPY data ./data has a single source of truth). `gcloud builds submit --tag`
# only auto-detects a Dockerfile at the context root, so build locally with -f and
# push to Artifact Registry.
echo "Building image (context: repo root, Dockerfile: mcp-server/Dockerfile)..."
gcloud auth configure-docker "${REGION}-docker.pkg.dev" --quiet
docker build -f "${REPO_ROOT}/mcp-server/Dockerfile" -t "$IMAGE" "$REPO_ROOT"

echo "Pushing ${IMAGE}..."
docker push "$IMAGE"

# ── Deploy ──────────────────────────────────────────────────────────────────────
AUTH_FLAG="--no-allow-unauthenticated"
if [[ "$ALLOW_UNAUTH" == "true" ]]; then
  AUTH_FLAG="--allow-unauthenticated"
fi

echo "Deploying to Cloud Run..."
gcloud run deploy "$SERVICE" \
  --project "$PROJECT_ID" \
  --region "$REGION" \
  --image "$IMAGE" \
  --platform managed \
  $AUTH_FLAG

URL="$(gcloud run services describe "$SERVICE" \
  --project "$PROJECT_ID" --region "$REGION" \
  --format 'value(status.url)')"

echo
echo "Deployed ${SERVICE} -> ${URL}"
echo "MCP endpoint: ${URL}/mcp"
