validate_branch_name() {
  local branch_name="$1"

  if [[ ! "$branch_name" =~ ^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)/.+$ ]]; then
    printf 'Use a conventional type/slug branch name, such as feat/api or docs/guide.\n' >&2
    return 1
  fi

  if ! git check-ref-format --branch "$branch_name" >/dev/null 2>&1; then
    printf 'Invalid Git branch name: %s\n' "$branch_name" >&2
    return 1
  fi
}
