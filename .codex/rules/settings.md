---
paths:
  - ".claude/settings.json"
  - ".claude/settings.local.json"
---

# Settings and Permissions Rules

When editing `.claude/settings.json` or `.claude/settings.local.json`:

- `settings.json` is checked into the repo — project-wide permissions and hooks go here
- `settings.local.json` is gitignored — user-specific overrides (API keys, personal allow-lists) go here
- The `permissions.deny` list uses tool call patterns: `Bash(command*)`, `Read(path)`, `Write(path)`
- The `permissions.allow` list pre-approves specific tool calls without user confirmation
- Hooks are defined under `hooks.<event>` — the shell runs these, not Claude, so they must be valid shell commands
- Do not add destructive commands (`rm -rf`, `git push --force`, `git reset --hard`) to `permissions.allow`
- After editing, verify the JSON is valid — malformed settings silently break hook execution
- `settings.local.json` must never be committed — it may contain secrets or personal tokens
