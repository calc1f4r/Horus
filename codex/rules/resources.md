<!-- AUTO-GENERATED from `.claude/rules/resources.md`; source_sha256=f3ecc88ac638caa8fc956d0c3ea894e251953b213ed98b2e9d7e3e470b399a86 -->

> Codex/GPT compatibility layer.
> Source of truth: `.claude/rules/resources.md`.
> This mirrored rule preserves the original content with `.claude/...` links rewritten to `codex/...` where needed.

---
paths:
  - "codex/resources/**"
---

# Resources Directory Rules

When working with shared resources in `codex/resources/`:

- Resources are reference material shared across all agents and skills
- Agents and skills link to resources — resources are NOT duplicated per-skill
- Do not create per-skill `resources/` directories; always use this global location
- Resource categories:
  - **Templates**: `audit-report-template.md`, `poc-templates.md`, `medusa-templates.md`, `certora-templates.md`, `certora-sui-move-templates.md`
  - **API references**: `certora-reference.md`, `medusa-reference.md`, `sui-prover-reference.md`, `certora-sui-move-reference.md`
  - **Judging criteria**: `sherlock-judging-criteria.md`, `cantina-criteria.md`, `code4rena-judging-criteria.md`
  - **Knowledge bases**: `reasoning-skills.md`, `domain-decomposition.md`, `vulnerability-taxonomy.md`, `feynman-question-framework.md`, `pattern-abstraction-ladder.md`, `root-cause-analysis.md`, `missing-validation-knowledge.md`
  - **Pipeline specs**: `inter-agent-data-format.md`, `orchestration-pipeline.md`, `output-requirements.md`, `protocol-detection.md`
  - **Static analysis**: `codeql/`, `semgrep/`
- Keep resources factual and reusable — not agent-specific instructions
