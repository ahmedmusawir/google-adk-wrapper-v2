You are absolutely right. My mistake. I was mixing up the Streamlit deployment (which needs the `Procfile`) with this one. For a FastAPI server, we used a `Dockerfile`.

When you run `gcloud run deploy --source .`, if a `Dockerfile` is present, Cloud Build will use it as the definitive instruction. That's the process we followed for the wrapper.

Here is the corrected `deployment.md` file.

---

### `/docs/deployment.md` (Corrected)

````markdown
# ADK Wrapper Deployment Guide

This guide provides a step-by-step process for deploying the **ADK Wrapper** service to Google Cloud Run. The process uses the "deploy from source" method, which automatically builds the container from a local `Dockerfile` and deploys it.

---

## Prerequisites

Before you begin, ensure you have the following:

1.  **Google Cloud SDK (`gcloud` CLI):** Installed and authenticated. Run `gcloud auth login` and `gcloud config set project [YOUR_PROJECT_ID]`.
2.  **Project Source Code:** The complete ADK Wrapper project directory.

This lightweight wrapper does not require any special IAM permissions or secrets to be pre-configured.

---

## Core Files for Deployment

Two files are essential for a correct and reliable source-based deployment.

### 1. The Container Definition (`Dockerfile`)

This file provides the complete blueprint for building the application's container image, including installing dependencies and defining the startup command.

**File Location:** `/[PROJECT_ROOT]/Dockerfile`

```dockerfile
# Use an official lightweight Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Define the command to start the Uvicorn server
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]
```
````

### 2\. The Ignore File (`.gcloudignore`)

This file is critical for a clean and secure build. It prevents local development folders and sensitive files from being uploaded to the build environment.

**File Location:** `/[PROJECT_ROOT]/.gcloudignore`

```
# Ignore the virtual environment
.venv/

# Ignore Python cache files
__pycache__/
*.pyc

# Ignore Git directory and local environment files
.git/
.gitignore
.env

# Ignore any local configuration or key files
*.json
```

---

## Deployment Script

The deployment is handled by a single, reusable shell script.

### `deploy.sh`

```bash
#!/bin/bash
# Exit immediately if a command exits with a non-zero status.
set -e

# --- Configuration ---

# 1. The name for your Cloud Run service.
SERVICE_NAME="adk-wrapper-prod-v2"

# 2. The public URL of your deployed ADK agent bundle service.
ADK_BUNDLE_URL="_PASTE_YOUR_ADK_BUNDLE_PROD_V2_URL_HERE_"

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
```

---

## Deployment Steps

1.  **Prepare Files:** Ensure the `Dockerfile` and `.gcloudignore` files are present in your project's root directory.
2.  **Configure Script:** Open `deploy.sh` and replace the placeholder value for `ADK_BUNDLE_URL` with the live URL of your deployed ADK Agent Bundle.
3.  **Make Executable:** Run `chmod +x deploy.sh` in your terminal.
4.  **Deploy:** Run the script from your project's root directory: `./deploy.sh`.

<!-- end list -->

```

```
