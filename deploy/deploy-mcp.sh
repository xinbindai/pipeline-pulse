#!/usr/bin/env bash
#
# Build the CGP demo MCP server image (repo-root context, single data/ copy)
# and deploy it to Google Cloud Run.
#
# Usage (from anywhere in the repository):
#   cp deploy/deploy-mcp.env.example deploy/deploy-mcp.env   # then edit
#   ./deploy/deploy-mcp.sh
#
# Configuration is loaded from deploy/deploy-mcp.env (override the path with
# ENV_FILE=...), then from environment variables (which take precedence). All have
# sensible defaults except PROJECT_ID, which falls back to your active gcloud config:
#   PROJECT_ID   GCP project id            (default: `gcloud config get-value project`)
#   REGION       Cloud Run / AR region     (default: us-central1)
#   SERVICE      Cloud Run service name    (default: bx-workflow-mcp)
#   AR_REPO      Artifact Registry repo    (default: mcp)
#   TAG          Image tag                 (default: current git short SHA, else "latest")
#   ALLOW_UNAUTH Allow unauthenticated     (default: true)
#   GCS_BUCKET   Bucket for tool data       (default: <project>-mcp-data; servicenow/CGP/
#                                            nginx tools read from GCS. The bucket is
#                                            created and granted read access on deploy.)
#   SERVICE_ACCOUNT  Cloud Run runtime SA   (optional; defaults to the compute SA)
#
# Upload the tool data to the bucket before the tools can serve it:
#   GCS_BUCKET=<bucket> python mcp-server/gcs_upload.py
#
set -euo pipefail

# Load KEY=value pairs from a config file. Lines may use an optional `export`
# prefix and quoted values; blank/`#` lines are ignored. Variables already set in
# the environment take precedence, so you can still override inline, e.g.
#   TAG=v2 ./deploy/deploy-mcp.sh
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

# Paths. This script lives in deploy/, so the repo root is its parent directory.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "$REPO_ROOT"

# Load deploy config (deploy/deploy-mcp.env by default; override path via ENV_FILE).
ENV_FILE="${ENV_FILE:-${SCRIPT_DIR}/deploy-mcp.env}"
load_env_file "$ENV_FILE"

# ── Configuration ───────────────────────────────────────────────────────────────
PROJECT_ID="${PROJECT_ID:-$(gcloud config get-value project 2>/dev/null || true)}"
REGION="${REGION:-us-central1}"
SERVICE="${SERVICE:-bx-workflow-mcp}"
AR_REPO="${AR_REPO:-mcp}"
TAG="${TAG:-$(git rev-parse --short HEAD 2>/dev/null || echo latest)}"
ALLOW_UNAUTH="${ALLOW_UNAUTH:-true}"
SERVICE_ACCOUNT="${SERVICE_ACCOUNT:-}"

if [[ -z "$PROJECT_ID" ]]; then
  echo "ERROR: PROJECT_ID is not set and no active gcloud project is configured." >&2
  echo "       Run 'gcloud config set project <id>' or 'PROJECT_ID=<id> ./deploy/deploy-mcp.sh'." >&2
  exit 1
fi

# Tool-data bucket defaults to <project>-mcp-data (created/granted on deploy).
GCS_BUCKET="${GCS_BUCKET:-${PROJECT_ID}-mcp-data}"

IMAGE="${REGION}-docker.pkg.dev/${PROJECT_ID}/${AR_REPO}/${SERVICE}:${TAG}"

if [[ -n "$GCS_BUCKET" ]]; then
  DATA_DESC="gs://${GCS_BUCKET} (GCS)"
else
  DATA_DESC="bundled data/ in image"
fi

echo "Project : ${PROJECT_ID}"
echo "Region  : ${REGION}"
echo "Service : ${SERVICE}"
echo "Image   : ${IMAGE}"
echo "Data    : ${DATA_DESC}"
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

# When GCS-backed data is requested, ensure the bucket exists and the Cloud Run
# runtime service account can read it.
if [[ -n "$GCS_BUCKET" ]]; then
  if ! gcloud storage buckets describe "gs://${GCS_BUCKET}" --project "$PROJECT_ID" >/dev/null 2>&1; then
    echo "Creating GCS bucket gs://${GCS_BUCKET}..."
    gcloud storage buckets create "gs://${GCS_BUCKET}" \
      --project "$PROJECT_ID" --location "$REGION" --uniform-bucket-level-access
  fi
  if [[ -z "$SERVICE_ACCOUNT" ]]; then
    PROJECT_NUMBER="$(gcloud projects describe "$PROJECT_ID" --format='value(projectNumber)')"
    SERVICE_ACCOUNT="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"
  fi
  echo "Granting roles/storage.objectViewer on gs://${GCS_BUCKET} to ${SERVICE_ACCOUNT}..."
  gcloud storage buckets add-iam-policy-binding "gs://${GCS_BUCKET}" \
    --project "$PROJECT_ID" \
    --member "serviceAccount:${SERVICE_ACCOUNT}" \
    --role roles/storage.objectViewer >/dev/null \
    || echo "WARNING: could not grant objectViewer; ensure ${SERVICE_ACCOUNT} can read the bucket."
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
DEPLOY_ARGS=(
  --project "$PROJECT_ID"
  --region "$REGION"
  --image "$IMAGE"
  --platform managed
)
if [[ "$ALLOW_UNAUTH" == "true" ]]; then
  DEPLOY_ARGS+=(--allow-unauthenticated)
else
  DEPLOY_ARGS+=(--no-allow-unauthenticated)
fi
[[ -n "$SERVICE_ACCOUNT" ]] && DEPLOY_ARGS+=(--service-account "$SERVICE_ACCOUNT")

# Point the tools at GCS when a bucket is configured (object paths default in-app;
# pass overrides through only if the caller set them).
if [[ -n "$GCS_BUCKET" ]]; then
  ENV_VARS="GCS_BUCKET=${GCS_BUCKET}"
  [[ -n "${SERVICENOW_OBJECT:-}" ]] && ENV_VARS="${ENV_VARS},SERVICENOW_OBJECT=${SERVICENOW_OBJECT}"
  [[ -n "${CGP_LOG_OBJECT:-}" ]]    && ENV_VARS="${ENV_VARS},CGP_LOG_OBJECT=${CGP_LOG_OBJECT}"
  [[ -n "${NGINX_LOG_OBJECT:-}" ]]  && ENV_VARS="${ENV_VARS},NGINX_LOG_OBJECT=${NGINX_LOG_OBJECT}"
  DEPLOY_ARGS+=(--set-env-vars "$ENV_VARS")
fi

echo "Deploying to Cloud Run..."
gcloud run deploy "$SERVICE" "${DEPLOY_ARGS[@]}"

URL="$(gcloud run services describe "$SERVICE" \
  --project "$PROJECT_ID" --region "$REGION" \
  --format 'value(status.url)')"

echo
echo "Deployed ${SERVICE} -> ${URL}"
echo "MCP endpoint: ${URL}/mcp"
if [[ -n "$GCS_BUCKET" ]]; then
  echo
  echo "Tools read data from gs://${GCS_BUCKET}. If you haven't already, upload it:"
  echo "  GCS_BUCKET=${GCS_BUCKET} python mcp-server/gcs_upload.py"
fi
