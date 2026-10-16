# Bounded agent execution protocol

This protocol exists to keep agent work focused, resumable, reviewable, and cost-controlled.

It applies to non-trivial repository work regardless of model or provider. Repository-specific `AGENTS.md`, safety rules, architecture constraints, and user instructions still take precedence.

## Core rule

**One bounded stage per agent run by default.**

Do not automatically continue into later stages after the current stage is complete. Finish the stage, verify it, persist the checkpoint, report, and stop.

A user may explicitly authorize a continuous multi-stage run, but that should be the exception rather than the default.

## Start gate

Before non-trivial work:

1. Read `AGENTS.md`.
2. Read only the repository checkpoint/memory/handoff documents required by `AGENTS.md`.
3. Check the current branch, `HEAD`, working tree, and relevant diff.
4. Identify the exact current stage and its exit condition.
5. Search for the owning symbols/files before opening broad areas of the repository.

Do not begin with a repository-wide reread when a narrow task boundary is available.

## Long task specifications

If a task has several independent implementation stages, a long brief, or is likely to require multiple agent runs, persist the durable task specification instead of carrying the full prompt through every turn.

Prefer, in order:

1. an existing matching GitHub Issue/handoff when that repository uses Issues for task continuity;
2. a task document such as `docs/tasks/<task-slug>.md`;
3. an existing canonical roadmap/spec section when it already captures the work precisely.

A durable task specification should contain:

- goal;
- non-goals;
- constraints;
- numbered stages;
- acceptance criteria;
- current active stage;
- checkpoint branch/SHA when useful;
- known blockers and unverified checks.

Subsequent agent prompts should be short: read the durable task specification, execute the named stage only, verify it, update the checkpoint, and stop.

Do not repeatedly inject the same large task brief into a long-running agent conversation.

## Stage contract

Every non-trivial stage should have:

- one concrete objective;
- a small, explicit scope;
- an exit condition;
- targeted validation;
- a checkpoint or commit when appropriate.

At stage completion:

1. run only the checks relevant to the changed behavior;
2. inspect the exact diff;
3. update the durable task/checkpoint source when needed;
4. leave the working tree in a known state;
5. report what changed, what was actually verified, and what remains unverified;
6. **STOP**.

Do not begin the next numbered stage automatically.

## Context discipline

Keep the model context proportional to the task.

- Prefer targeted search over broad file dumps.
- Read relevant sections rather than whole large documents.
- Do not reread unchanged files merely because the conversation was compacted.
- Reuse a verified checkpoint when code and requirements have not changed.
- For review, establish the exact diff first: PR base/head, `parent..commit`, or checkpoint-to-`HEAD`.
- Avoid generated files, dependency trees, caches, logs, screenshots, artifacts, and large data files unless they are directly required.

If a reconnect, provider failure, or context compaction occurs, reconstruct state from the repository, task specification, current branch, and diff. Do not replay the entire old conversation into a fresh run.

## Cost and loop circuit breaker

Metered agent sessions must not be allowed to loop indefinitely.

Stop and report instead of continuing when any of these is true:

- the same large context is being sent repeatedly without meaningful new progress;
- the same files are being reread over and over without a changed hypothesis;
- the same failing command/approach is repeated with no changed condition;
- the agent is repeatedly compacting/reconnecting and resuming the same work;
- an external provider returns quota/rate/service errors such as 403, 429, or 503;
- the current stage has already met its exit condition.

Do not turn one task into an unattended multi-hour chain of model calls merely because more stages remain.

## Model use

Repository-specific model policy remains authoritative. As a general operating pattern:

- use a fast/low-cost model for exploration, routine edits, tests, documentation, and mechanical Git work;
- use a stronger reasoning model for one bounded complex implementation/debugging stage when justified;
- use the strongest reviewer model for a narrow, exact-diff review when the cost of error warrants it.

A review model should review the exact requested range and should not silently expand into a full-repository audit or start implementing unrelated improvements.

The user's explicit model choice always wins.

## Review mode

For independent review:

1. define the exact commit/diff range;
2. inspect changed files plus directly coupled contracts/tests;
3. classify findings by severity;
4. distinguish confirmed problems from unverified platform/runtime risks;
5. do not edit code unless explicitly asked.

After fixes, prefer a short follow-up review of the fix commit instead of repeating the original full audit.

## Provider/runtime failure

If a model provider or runtime fails:

- do not assume implementation completed;
- inspect `git status`, branch, and recent log before resuming;
- preserve already-valid local work;
- resume from the factual repository state;
- do not reset to an old SHA unless the user explicitly asks.

A provider error is not evidence of a repository error.

## Verification language

Never claim a build, test, deployment, device check, or runtime acceptance passed when it was not actually executed.

Use explicit statuses such as:

- `PASSED`
- `FAILED`
- `WRITTEN / NOT EXECUTED`
- `STATICALLY REVIEWED`
- `NOT VERIFIED ON TARGET PLATFORM`

## End-of-run report

A bounded implementation run should end with a compact report containing, when relevant:

- branch and final `HEAD`;
- commits;
- files changed;
- behavior implemented;
- checks actually executed;
- checks not executed and why;
- blockers/risks;
- exact next stage.

Then stop and wait for the next instruction.
