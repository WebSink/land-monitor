# Agent Memory v2

This repository uses a tool-agnostic, GitHub-first memory protocol for work across ChatGPT, Codex, Claude Code and other repository-capable agents.

The goal is continuity without creating a second source of truth. Git/code remains the record of what changed; canonical project docs record durable state and decisions; GitHub Issues carry task/session context.

This protocol borrows the useful ideas of start-context injection, a meaningful-work threshold, a stop gate, typed memory events, stale-memory checks and failed-attempt prechecks. It does **not** vendor or require `.memory/`, `.projectmem/`, an MCP server or a local hook package.

## Start gate

Before non-trivial work:

1. Read `AGENTS.md`.
2. Read this file.
3. Read the canonical checkpoint for this repository: `docs/CURRENT_STATE.md`.
4. If continuing a task, read the matching GitHub Issue and newest handoff from `docs/HANDOFF.md`.
5. Verify the current branch/HEAD and inspect only the diff/commits relevant to the task.
6. Use targeted search before opening broad parts of the repository.

Do not treat a dated checkpoint or handoff as proof of current state.

## Precheck before repeating work

Before retrying an approach that may have been attempted before, search the relevant docs and GitHub Issue history for the exact error, symbol, subsystem or approach.

A previous failed attempt is a constraint until something material changed. Retry only when you can name the changed condition, for example a different credential class, dependency version, runtime topology, API contract, data shape or implementation path.

Do not burn another session rediscovering a known dead end.

## Memory routing

| Memory type | Canonical home |
|---|---|
| Current accepted state / active milestone | `docs/CURRENT_STATE.md` |
| Durable architecture or product decision | the relevant canonical project/subsystem doc once one exists |
| Future work / sequencing | the relevant roadmap once one exists |
| Task goal, session checkpoint, blockers | GitHub Issue + `docs/HANDOFF.md` |
| Failed experiment that matters only to one task | Matching Issue handoff |
| Failed experiment with cross-task reuse value | Relevant subsystem/runbook doc, plus link from the Issue |
| Code/config/schema truth | Repository files, migrations, tests and Git history |
| Detailed evidence / audits / snapshots | `docs/HANDOFF.md` and repository evidence |

Do not duplicate the same fact into several memory files. Link to the authoritative artifact instead.

## Meaningful-work threshold

Memory must be considered before ending a session when the work did any of the following:

- changed code, schema, configuration, infrastructure behavior or externally visible behavior;
- completed or materially advanced an accepted milestone/task;
- made a durable architecture/product/operations decision;
- found a failed approach that another agent could plausibly repeat;
- changed a production/runtime assumption or acceptance result.

Pure read-only inspection, trivial formatting, typo-only edits and disposable exploration do not require a memory write by themselves.

## Stop gate

Before ending after meaningful work, check all of these:

1. **State:** if durable accepted state changed, update `docs/CURRENT_STATE.md` or the more specific canonical document.
2. **Decision:** if a durable choice was made, record it in the relevant canonical project/subsystem doc once one exists or the owning subsystem document.
3. **Failure memory:** if an approach failed and repetition would waste time, record the approach, decisive evidence and exact retry condition.
4. **Task continuity:** when a matching Issue already exists, or the user explicitly asked to save/handoff progress, add one compact handoff following `docs/HANDOFF.md`.
5. **Evidence:** reference the commit/PR/test/run/snapshot instead of copying large output.
6. **Truthfulness:** distinguish automated checks from live/manual acceptance and name important checks that were not run.

Do not create a new Issue solely to satisfy this stop gate unless `docs/HANDOFF.md` and the current user instruction authorize it.

## Searchable event vocabulary

Use these exact prefixes in Issue handoffs when they apply. They make cross-agent search cheap without introducing another database:

- `decision:` — durable choice and why it won.
- `attempt-failed:` — attempted path, decisive failure evidence, and the condition required before retry.
- `fix:` — accepted change plus verification evidence.
- `blocker:` — unresolved dependency or condition preventing progress.

Example:

```text
attempt-failed: vk-native-photo — user-token upload reached docs.save but the returned credential class was unusable; retry only if token class/API contract changes.
```

Keep entries compact. Raw logs stay in their native artifact.

## Freshness rules

- Checkpoint dates and SHAs are hints, not authority.
- If HEAD advanced beyond the recorded checkpoint, inspect the relevant commits/diff instead of rerunning a full audit.
- If memory conflicts with code, CI, deployment or verified runtime state, the newer verified evidence wins and the stale memory should be repaired.
- Never convert “not measured” into “failed” or “zero”.
- Never present a previous test run as a new run.

## Cross-agent bridge

- `AGENTS.md` is the primary repository instruction file.
- `CLAUDE.md` is only a thin bridge that tells Claude Code to read `AGENTS.md` and this file.
- Do not copy project state into bridge files.
- An agent that cannot automatically load these files must read them explicitly before non-trivial work.

## Security

Never persist secrets, credentials, tokens, cookies, private keys, secret-bearing configs, sensitive personal data, full private conversations or large raw logs as agent memory.

Use sanitized facts, paths, commit SHAs and links to the authoritative artifact.
