---
name: "cantina-judge"
description: "Validate a security finding against Cantina audit platform standards. Determines severity using impact × likelihood matrix, applies severity caps, and checks for invalid/duplicate categories. Use when validating findings for Cantina submission, determining Cantina severity, or checking if a finding would be capped or invalid."
---
Use the [cantina-judge subagent](../../../.codex/agents/cantina-judge.toml) when you want delegated execution.
That subagent is configured for live web search and may delegate to narrower repo subagents when the workflow splits cleanly.

Input: `<finding-to-validate>`.

Validate the finding at `<finding-to-validate>` against Cantina judging criteria.

## Severity matrix: Impact × Likelihood

|  | High Impact | Medium Impact | Low Impact |
|--|-------------|---------------|------------|
| **High Likelihood** | Critical | High | Medium |
| **Medium Likelihood** | High | Medium | Low |
| **Low Likelihood** | Medium | Low | Low |

## Key Cantina rules

- Severity = Impact × Likelihood (both dimensions matter, unlike Sherlock)
- **Severity caps apply** — certain finding types are capped regardless of impact
- **Out-of-scope** findings are invalid even if technically correct
- Duplicates: same root cause = duplicate, even if different impact description

## Validation checklist

- [ ] Impact correctly classified (High/Medium/Low)?
- [ ] Likelihood correctly classified (High/Medium/Low)?
- [ ] Matrix lookup gives correct severity?
- [ ] Any severity caps applicable?
- [ ] Finding is in-scope per contest rules?

For full criteria, see [cantina-criteria.md](../../../.codex/resources/cantina-criteria.md).

## Related skills

- [sherlock-judging](../sherlock-judging/SKILL.md) — Sherlock criteria (impact-only severity)
- [code4rena-judge](../code4rena-judge/SKILL.md) — Code4rena criteria
- [issue-writer](../issue-writer/SKILL.md) — Polishes findings for submission
