#!/usr/bin/env bash
set -euo pipefail

exec gh pr create --template pull_request_template.md "$@"
