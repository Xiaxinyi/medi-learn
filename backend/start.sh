#!/bin/bash
set -e

echo "Starting Medi-Learn Backend..."
uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"
