#!/usr/bin/env python3
"""GitHub PR gate for the repository Agent Memory v2 protocol.

The gate is intentionally conservative:
- docs-only / tests-only / workflow-only PRs pass;
- behavior/config/schema/source changes are "meaningful";
- meaningful PRs must either update durable Markdown memory/docs, or carry an
  explicit searchable memory note in the PR body.

No network access or third-party Python packages are required.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import PurePosixPath


TYPED_EVENT_RE = re.compile(
    r"(?im)^\s*(decision|attempt-failed|fix|blocker)\s*:\s*\S"
)
NO_MEMORY_RE = re.compile(
    r"(?im)^\s*memory(?:[- ]impact)?\s*:\s*none\s*(?:[-—:]\s*)(.{12,})$"
)


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True).strip()


def changed_paths(base_sha: str, head_sha: str) -> list[str]:
    out = git("diff", "--name-only", "--diff-filter=ACMRD", base_sha, head_sha)
    return [line.strip() for line in out.splitlines() if line.strip()]


def is_docs_or_test_only(path: str) -> bool:
    p = PurePosixPath(path)
    s = path.lower()

    if s.endswith((".md", ".mdx", ".rst", ".txt")):
        return True
    if s.startswith(("docs/", ".github/")):
        return True
    if s in {"agents.md", "claude.md", "readme.md", "roadmap.md"}:
        return True

    parts = {part.lower() for part in p.parts}
    if parts & {"test", "tests", "__tests__", "__snapshots__"}:
        return True

    if s == "scripts/agent_memory_gate.py":
        return True

    return False


def is_memory_artifact(path: str) -> bool:
    s = path.lower()
    if s in {"agents.md", "claude.md", "roadmap.md"}:
        return True
    if s.startswith("docs/") and s.endswith((".md", ".mdx", ".rst", ".txt")):
        return True
    return False


def main() -> int:
    base_sha = os.environ.get("MEMORY_GATE_BASE_SHA", "").strip()
    head_sha = os.environ.get("MEMORY_GATE_HEAD_SHA", "").strip()
    pr_body = os.environ.get("MEMORY_GATE_PR_BODY", "") or ""

    if not base_sha or not head_sha:
        print("Agent Memory Gate: missing base/head SHA; refusing to guess.")
        return 2

    paths = changed_paths(base_sha, head_sha)
    print("Agent Memory Gate")
    print(f"base: {base_sha}")
    print(f"head: {head_sha}")
    print(f"changed files: {len(paths)}")

    meaningful = [p for p in paths if not is_docs_or_test_only(p)]
    memory_artifacts = [p for p in paths if is_memory_artifact(p)]

    if not meaningful:
        print("PASS: no meaningful product/runtime/config/schema/source change detected.")
        return 0

    print("meaningful changes:")
    for path in meaningful:
        print(f"  - {path}")

    if memory_artifacts:
        print("PASS: durable repository memory/docs changed:")
        for path in memory_artifacts:
            print(f"  - {path}")
        return 0

    if TYPED_EVENT_RE.search(pr_body):
        print("PASS: PR body contains a searchable typed memory event.")
        return 0

    no_memory = NO_MEMORY_RE.search(pr_body)
    if no_memory:
        print("PASS: PR body explicitly records that no durable memory update is needed.")
        print(f"reason: {no_memory.group(1).strip()}")
        return 0

    print("")
    print("FAIL: meaningful changes were detected, but no memory evidence was found.")
    print("")
    print("Do one of the following before merge:")
    print("  1. Update the relevant durable Markdown state/decision/subsystem doc; or")
    print("  2. Add a searchable PR-body event such as:")
    print("       fix: <accepted change + verification>")
    print("       decision: <durable choice + why>")
    print("       attempt-failed: <failed path + retry condition>")
    print("       blocker: <unresolved condition>")
    print("  3. If no durable memory change is genuinely needed, add:")
    print("       Memory: none — <specific reason, at least 12 characters>")
    print("")
    print("See docs/AGENT_MEMORY.md. The gate does not create Issues or rewrite memory.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
