<!-- AUTO-GENERATED from `.claude/rules/rules.md`; source_sha256=4570f1454d4f83dc07db8decb5181b25033f0fc5e95f62d6cc7d614ff3dc9ca9 -->

> Codex/GPT compatibility layer.
> Source of truth: `.claude/rules/rules.md`.
> This mirrored rule preserves the original content with `.claude/...` links rewritten to `codex/...` where needed.

---
paths:
  - "codex/rules/*.md"
---

# Rules File Conventions

When editing path-scoped rules in `codex/rules/`:

- Each rule file must have a `paths:` frontmatter block listing the glob patterns that trigger it
- Globs follow gitignore syntax — `**` matches any depth, `*` matches within a single directory
- Rule files are auto-loaded by Claude Code when working with files matching the path patterns
- Keep rules concise and actionable — agents read these at runtime, not as documentation
- Do not duplicate content from CLAUDE.md into rules — rules supplement, CLAUDE.md leads
- When adding a new rule file, also update the `Rules` section in `CLAUDE.md` with the new entry and its path patterns
- Redundant path entries in a single rule are allowed but prefer the broadest glob that is still specific enough
- Rules for subdirectories of an already-covered path are fine if they need separate, more specific guidance
