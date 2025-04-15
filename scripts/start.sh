#!/bin/bash
set -e

# 🔍 Log everything to deploy.log
exec > >(tee -a /home/LogFiles/deploy.log) 2>&1

# Set default port if not provided
PORT=${PORT:-8000}

echo "🎯 Launching Streamlit on port $PORT..."
streamlit run src/client/app.py --server.port $PORT --server.address 0.0.0.0 &

echo "🚀 Starting FastAPI (port 8001)..."
uvicorn src.server.main:app --host 0.0.0.0 --port=8001 &

# Wait for FastAPI health check
echo "⏳ Waiting for FastAPI to be ready..."
for i in {1..240}; do
  if curl -s http://localhost:8001/health > /dev/null; then
    echo "✅ FastAPI is up!"
    break
  else
    echo "⏳ Attempt $i/240: FastAPI not ready yet..."
    sleep 1
  fi
done

echo "✅ All services launched. Ready to play ball!"
wait
