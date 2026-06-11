#!/bin/bash
set -e
cd "$(dirname "$0")/.."
cd backend
py -3.11 -m uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
