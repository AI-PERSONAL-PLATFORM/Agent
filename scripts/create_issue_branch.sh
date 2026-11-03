#!/usr/bin/env bash
set -euo pipefail
source "$(dirname -- "${BASH_SOURCE[0]}")/lib/branch_name.sh"

if (($# == 0)); then
  if [[ ! -t 0 ]]; then
    printf 'Usage: mise issue-branch <issue-number-or-url> [gh issue develop options]\n' >&2
    exit 2
  fi

  read -r -p 'Issue number or URL: ' issue
  read -r -p 'Branch name (e.g. feat/add-search, docs/update-guide; blank for GitHub default): ' branch_name
  if [[ -n "$branch_name" ]]; then
    set -- --name "$branch_name" "$@"
  fi
else
  issue="$1"
  shift
fi

args=("$@")
branch_name=""
for ((index = 0; index < ${#args[@]}; index++)); do
  case "${args[index]}" in
    --name)
      if ((index + 1 >= ${#args[@]})); then
        printf 'The --name option requires a branch name.\n' >&2
        exit 2
      fi
      branch_name="${args[index + 1]}"
      ;;
    --name=*)
      branch_name="${args[index]#*=}"
      ;;
  esac
done

if [[ -n "$branch_name" ]]; then
  validate_branch_name "$branch_name" || exit 2
fi

if [[ -z "$issue" ]]; then
  printf 'An issue number or URL is required.\n' >&2
  exit 2
fi

exec gh issue develop "$issue" --checkout "${args[@]}"
