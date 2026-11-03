#!/usr/bin/env bash
set -euo pipefail
source "$(dirname -- "${BASH_SOURCE[0]}")/lib/branch_name.sh"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  printf 'Run this command from inside a Git repository.\n' >&2
  exit 2
fi

if ! gh stack --help >/dev/null 2>&1; then
  printf 'Install GitHub stack support first with: mise install-gh-stack\n' >&2
  exit 1
fi

validate_branches() {
  local mode=init
  local branch
  if [[ "${1:-}" == link ]]; then
    mode=link
    shift
  fi
  for branch in "$@"; do
    if [[ "$mode" == link && "$branch" =~ ^[0-9]+$ ]]; then
      continue
    fi
    validate_branch_name "$branch" || exit 2
  done
}

if (($# > 0)); then
  if [[ -n "$(git status --porcelain)" ]]; then
    printf 'Commit or stash your changes before initializing a stack.\n' >&2
    exit 1
  fi
  validate_branches "$@"
  exec gh stack init "$@"
fi

if [[ ! -t 0 ]]; then
  printf 'Run mise create-stack in a terminal, or pass branch names to initialize a stack.\n' >&2
  exit 2
fi

PS3='Choose a stack action: '
select action in \
  'Initialize local stack — create or adopt branches' \
  'Link existing branches or PRs — publish stack on GitHub' \
  'View — show stack branches and PRs' \
  'Add — create the next branch above the stack' \
  'Push — push stack branches without creating PRs' \
  'Submit — push branches and create draft PRs' \
  'Sync — update stack branches and PRs from GitHub' \
  'Rebase — update branches above the current branch' \
  'Checkout — switch to a branch or PR' \
  'Merge — merge a PR and its predecessors or a full stack'; do
  [[ -n "${action:-}" ]] && break
  [[ -n "${REPLY:-}" ]] || exit 1
  printf 'Choose a number from 1 to 10.\n' >&2
done

case "$REPLY" in
  1)
    [[ -z "$(git status --porcelain)" ]] || { printf 'Commit or stash your changes first.\n' >&2; exit 1; }
    printf 'Available branches:\n'
    git branch --all --format='  %(refname:short)'
    read -r -p 'Branch names (e.g. feat/api, docs/guide), bottom to top: ' -a branches
    ((${#branches[@]})) || { printf 'At least one branch name is required.\n' >&2; exit 2; }
    validate_branches "${branches[@]}"
    exec gh stack init "${branches[@]}"
    ;;
  2)
    printf 'Available branches:\n'
    git branch --all --format='  %(refname:short)'
    read -r -p 'Existing branch names or PR numbers (e.g. feat/api, docs/guide), bottom to top: ' -a branches
    ((${#branches[@]})) || { printf 'At least one branch or PR is required.\n' >&2; exit 2; }
    validate_branches link "${branches[@]}"
    exec gh stack link "${branches[@]}"
    ;;
  3) exec gh stack view --short ;;
  4)
    read -r -p 'New branch name: ' branch
    [[ -n "$branch" ]] || exit 2
    validate_branch_name "$branch" || exit 2
    exec gh stack add "$branch"
    ;;
  5) exec gh stack push ;;
  6) exec gh stack submit --auto ;;
  7) exec gh stack sync ;;
  8) exec gh stack rebase --upstack ;;
  9)
    read -r -p 'Branch, PR number, or URL: ' target
    [[ -n "$target" ]] || exit 2
    exec gh stack checkout "$target"
    ;;
  10)
    read -r -p 'PR or stack number to merge: ' target
    [[ -n "$target" ]] || exit 2
    exec gh stack merge "$target" --yes
    ;;
esac
