FROM python:3.12-slim

WORKDIR /app

# Build context is the repository root (single copy of data/). From repo root:
#   docker build -f mcp-server/Dockerfile -t bx-workflow-mcp .
# Deploy to Cloud Run by building/pushing the image, then deploying it:
#   docker push IMAGE && gcloud run deploy bx-workflow-mcp --image IMAGE --region us-central1
COPY mcp-server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY mcp-server/main.py .

# Bundle the demo data (ServiceNow incidents, logs, docs) into the image
# filesystem at /app/data so resources can read it at runtime.
COPY data ./data

# Cloud Run injects PORT; default 8080
ENV PORT=8080

EXPOSE 8080

CMD ["python", "main.py"]
