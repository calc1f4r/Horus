# Codex Compatibility Layer

This directory is a generated Codex/GPT-facing mirror of the Claude playbook tree in `.claude/`.

It exists so the repository can preserve the original Claude skills, agents, resources, and rules unchanged while also giving Codex/GPT a portable, repo-local instruction surface.

## What Is Mirrored

- `skills/`: 35 mirrored skill wrappers
- `agents/`: 35 mirrored agent playbooks
- `resources/`: 49 mirrored reference files
- `rules/`: 13 mirrored rule files

## How To Use

1. Start with `CATALOG.md` or `FLOWS.md` to pick the right skill/flow.
2. Open the relevant file under `skills/`.
3. Follow the linked implementation playbook under `agents/`.
4. Load any referenced files from `resources/` or `rules/` as needed.

## Sync

Regenerate this layer after changing `.claude/` content:

```bash
python3 scripts/sync_codex_compat.py
```

Validate that the committed mirror is up to date:

```bash
python3 scripts/sync_codex_compat.py --check
```
