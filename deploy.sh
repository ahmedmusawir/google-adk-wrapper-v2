#!/bin/bash
# Exit immediately if a command exits with a non-zero status.
set -e

# --- Configuration ---

# 1. The name for your Cloud Run service.
SERVICE_NAME="adk-wrapper-prod-v2"

# 2. The *public URL* of your already deployed ADK agent bundle service.
ADK_BUNDLE_URL="https://adk-bundle-prod-v2-952978338090.us-east1.run.app"

# --- Deployment ---
echo "🚀 Beginning deployment for service: $SERVICE_NAME"
echo "   Using the 'deploy from source' method..."
echo "--------------------------------------------------"

gcloud run deploy "$SERVICE_NAME" \
  --source . \
  --set-env-vars "ADK_BUNDLE_URL=${ADK_BUNDLE_URL}" \
  --allow-unauthenticated

echo "--------------------------------------------------"
echo "✅ Deployment complete!"