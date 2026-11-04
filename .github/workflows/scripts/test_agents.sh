#!/usr/bin/env bash
set -euo pipefail

server_pid=""
cleanup() {
  if [[ -n "$server_pid" ]]; then
    kill "$server_pid" 2>/dev/null || true
    wait "$server_pid" 2>/dev/null || true
  fi
}
trap cleanup EXIT

mise x -- uv run --frozen uvicorn app.main:app --host 127.0.0.1 --port 8000 &
server_pid=$!

for attempt in {1..30}; do
  if curl --silent --fail --max-time 2 "$AGENT_API_URL/health" > /dev/null; then
    break
  fi
  if ! kill -0 "$server_pid" 2>/dev/null; then
    echo "::error::Agents service exited before becoming ready."
    exit 1
  fi
  sleep 1
done
curl --silent --show-error --fail --max-time 2 "$AGENT_API_URL/health"
mise run test-agent
