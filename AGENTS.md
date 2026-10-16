# Repository agent instructions

## Current repository state

This repository is currently empty/minimal. Do not invent product architecture, requirements, deployment state, or acceptance criteria that are not present in GitHub or explicitly provided by the user.

When product files and durable project documentation are introduced, treat them as the source of truth and update this file accordingly.


## Context discipline

- Start non-trivial work with `AGENTS.md` -> `docs/AGENT_MEMORY.md` -> `docs/CURRENT_STATE.md` -> matching Issue/handoff when applicable -> exact task diff -> relevant files/tests.
- Establish the review boundary first: PR base/head, `parent..commit`, or the verified checkpoint to `HEAD`. Do not perform a repository-wide audit when a small exact diff answers the task.
- Use targeted search and read only relevant files/direct dependencies. Do not infer a future product from memory scaffolding.
- Perform a broad/full audit only when explicitly requested or when targeted inspection cannot localize a real problem.

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

## Model escalation policy

- When available, use **DeepSeek V4.1 Flash** as the default model for ordinary repository work: exploration, routine fixes, tests, documentation, Git operations, and small-to-medium refactors.
- Do not stop, defer, or request a stronger model merely because a task looks complex, spans many files, or has a large context. First inspect the relevant evidence, localize the problem, and make a concrete solution attempt when it is safe to do so.
- Recommend switching to **GPT-6.1 Sol** only when there is a concrete blocker that materially limits reliable progress, such as repeated evidence-backed debugging failure, conflicting cross-module constraints, unresolved architectural ambiguity, or insufficient confidence after relevant verification.
- Recommend **GPT-6 Astra** only for the highest-complexity or highest-cost-of-error work when stronger reasoning is justified, or when GPT-6.1 Sol is still insufficient. The user's explicit model choice always wins.
- A model-escalation recommendation must name the exact blocker and the evidence that caused it. Continue all useful work that does not depend on the switch instead of stopping early.
- Never claim that the active model has changed unless the runtime/UI actually confirms it. In ChatGPT/Codex Desktop, model switching remains a user action unless the client explicitly exposes an authorized model-switching tool.

## Bounded agent execution and cost discipline

- Read `docs/AGENT_EXECUTION.md` before non-trivial multi-stage agent work.
- Execute one bounded stage per agent run by default; after the stage is implemented, verified, checkpointed, and reported, **STOP** instead of automatically continuing to later stages.
- For long briefs or tasks with several stages, persist the durable task specification in the repository or matching GitHub Issue/handoff and use short stage-specific prompts on subsequent runs.
- Reconstruct context after compaction/reconnect from repository state, the durable task spec, current branch, and exact diff rather than replaying a large chat history.
- If the same large context/tool sequence repeats without meaningful progress, or the provider returns quota/rate/service failures, stop and report instead of looping.
- Keep expensive/strong-model work narrowly bounded. Prefer exact-diff independent review after implementation rather than repeated full-repository audits.
