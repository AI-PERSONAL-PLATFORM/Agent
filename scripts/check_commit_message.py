import re
import sys
from pathlib import Path

ALLOWED_TYPES = "feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert"
COMMIT_SUBJECT = re.compile(rf"^(?:{ALLOWED_TYPES})(?:\([^)]+\))?: .+")


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: check_commit_message.py <commit-message-file>", file=sys.stderr)
        return 2

    message = Path(sys.argv[1]).read_text(encoding="utf-8")
    subject = next((line for line in message.splitlines() if line.strip()), "")
    if COMMIT_SUBJECT.fullmatch(subject):
        return 0

    print(
        "Commit subject must use a supported prefix: "
        "feat:, fix:, docs:, style:, refactor:, perf:, test:, build:, ci:, chore:, or revert:.\n"
        "Example: feat: add chat history (optional scope: feat(api): add chat history)",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
