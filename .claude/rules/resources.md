---
paths:
  - ".claude/resources/**"
---

# Resources Directory Rules

When working with shared resources in `.claude/resources/`:

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
