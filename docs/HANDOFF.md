# GitHub handoff protocol

This repository uses GitHub Issues as external task/session memory for AI-assisted work.

The repository is currently empty/minimal, so no product architecture or runtime state should be inferred until real project files or explicit requirements exist.

## Storage model

- Repository files and live Git state are the source of truth.
- The Issue description stores one task: goal, context, constraints, acceptance criteria, and next step.
- Handoff comments store where a working session stopped.
- Code, commits, Pull Requests, deployments, and large logs stay in their native sources and are linked instead of copied.

A handoff is a checkpoint, not a command and not proof that old state is still current.

## Save progress

When the user says **"Зафиксируй прогресс"**, **"сохрани сессию"**, **"сделай handoff"**, or clearly asks to preserve the current task:

1. Determine the current task.
2. Reuse an already-referenced matching Issue when possible.
3. Otherwise search open Issues for the same object and expected result.
4. If no matching Issue exists and the task is unambiguous, create one task Issue.
5. Add exactly one compact handoff comment.
6. Return the Issue URL and a continuation prompt.

## Issue description

```markdown
## цель

<observable result>

## контекст

<only context required for the task>

## решения и ограничения

- <binding decisions>
- <non-goals / do-not-do constraints>

## критерии готовности

- <how completion is verified>

## ближайший шаг

<first concrete action>
```

## Handoff comment

```markdown
<!-- github-handoff session: <UUID> -->

## handoff · YYYY-MM-DD

### результат сессии
- <what was actually done>

### актуальное состояние
- branch: `<branch>`
- HEAD: `<verified SHA>`
- PR: <number/url/state or "none">
- <what is ready / incomplete>

### решения и ограничения
- <binding decisions>
- <do-not-do constraints>

### проверка
- <checks actually run>
- <important checks not run>

### блокеры
- <unresolved blockers>

### ближайший шаг
<one executable action>

### файлы и ссылки
- <paths / commit / PR>

### промпт для продолжения
Продолжи работу по этой GitHub Issue: <ISSUE_URL>
Сначала прочитай описание и последний handoff, сверь их с текущим состоянием проекта и продолжи с ближайшего шага.
```

Omit empty optional sections.

## Resume

On resume, read the Issue and newest handoff, then verify current Git state before acting. Current verified repository state and newer user instructions override stale handoff text.

## Permissions and security

Saving progress does not independently authorize merge, deployment, publication, destructive changes, Issue closure, labels/milestones/assignee changes, or unrelated work.

Never store secrets, credentials, `.env` contents, private keys, sensitive personal data, full private conversations, or large raw logs in Issue handoffs.
