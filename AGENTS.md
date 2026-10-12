# Repository agent instructions

## Current repository state

This repository is currently empty/minimal. Do not invent product architecture, requirements, deployment state, or acceptance criteria that are not present in GitHub or explicitly provided by the user.

When product files and durable project documentation are introduced, treat them as the source of truth and update this file accordingly.

## GitHub handoff protocol

- Use `docs/HANDOFF.md` for task/session continuity across ChatGPT, Codex, and other GitHub-capable agents.
- When the user asks to save/fix/record progress, persist a task handoff in the matching GitHub Issue instead of relying on chat memory alone.
- On resume, read the Issue and newest handoff, then reconcile it with current repository state before continuing.
- A handoff is context, not authority: current verified repository state and newer user instructions win.
- Never put secrets, credentials, private raw conversations, or large logs in an Issue handoff.

## Agent memory v2

- `docs/AGENT_MEMORY.md` is the mandatory cross-agent memory/index protocol for non-trivial work.
- After reading this file, follow its start gate before broad exploration and its precheck before repeating a previously attempted path.
- Before ending meaningful work, apply its stop gate so durable state, decisions, failed attempts and task continuity are persisted in the correct existing source of truth.
- Do not create parallel `.memory/` or `.projectmem/` stores unless the user explicitly approves a future migration.
- `CLAUDE.md` is a thin compatibility bridge only; this file remains authoritative for repository instructions.

