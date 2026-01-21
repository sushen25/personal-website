#!/bin/bash

# Start FastAPI application with uvicorn
# Lambda Web Adapter will forward requests to this server

# Get port from environment variable (default: 8080)
PORT=${AWS_LWA_PORT:-8080}

# Start uvicorn server
exec python -m uvicorn src.main:app --host 0.0.0.0 --port $PORT
