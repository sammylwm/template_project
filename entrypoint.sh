#!/usr/bin/env bash

set -e

echo "Initialize aerich database (if not initialized)"
uv run aerich init-db || echo "Init-db already done or failed, continuing..."

echo "Apply aerich migrations"
uv run aerich upgrade

echo "Successfully applied migrations."

exec "$@"
