#!/bin/bash
set -e

# Get port from environment variable, default to 8000
PORT=${PORT:-8000}

echo "🚀 Starting Climate Adaptation Backend on port $PORT"

# Start uvicorn with the correct port
exec uvicorn app.main:app \
    --host 0.0.0.0 \
    --port "$PORT" \
    --log-level info \
    --access-log
