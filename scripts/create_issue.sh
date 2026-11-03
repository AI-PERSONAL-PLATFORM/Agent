#!/usr/bin/env bash
set -euo pipefail

template=""

select_template() {
  case "$1" in
    bug-report) template="Bug report" ;;
    feature-request) template="Feature request" ;;
    *)
      printf 'Unknown issue template: %s\n' "$1" >&2
      printf 'Choose "bug-report" or "feature-request".\n' >&2
      exit 2
      ;;
  esac
}

if (($# > 0)); then
  case "$1" in
    --template)
      if (($# < 2)); then
        printf 'Usage: mise create-issue --template bug-report|feature-request [gh issue create options]\n' >&2
        exit 2
      fi
      select_template "$2"
      shift 2
      ;;
    --template=*)
      select_template "${1#*=}"
      shift
      ;;
    bug-report|feature-request)
      select_template "$1"
      shift
      ;;
  esac
fi

if [[ -z "$template" ]]; then
  if [[ ! -t 0 ]]; then
    printf 'Select a template with --template bug-report|feature-request.\n' >&2
    exit 2
  fi

  PS3='Choose an issue template: '
  select choice in 'Bug report' 'Feature request'; do
    case "$REPLY" in
      1) template="Bug report"; break ;;
      2) template="Feature request"; break ;;
      *)
        if [[ -z "${REPLY:-}" ]]; then
          printf 'Template selection cancelled.\n' >&2
          exit 1
        fi
        printf 'Choose 1 or 2.\n' >&2
        ;;
    esac
  done
fi

exec gh issue create --template "$template" --assignee @me "$@"
