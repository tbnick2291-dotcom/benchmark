#!/bin/bash
set -e
cd "$(dirname "$0")/.."
cd backend
py -3.11 -m alembic upgrade head
echo "Database initialized."
