#!/bin/bash
set -e

echo "🚀 Starting ADK Wrapper in 'cloud' mode..."
echo "   Targeting the live ADK Bundle on Cloud Run."
echo "--------------------------------------------------"

APP_ENV="cloud" uvicorn main:app --reload --port=8080