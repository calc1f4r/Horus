name: sherlock-judging
description: "Validate a security finding against Sherlock audit platform standards. Determines severity (High/Medium/Invalid), checks validity, and assesses duplication. Use when validating findings for Sherlock contests, determining Sherlock severity, or checking if an issue meets Sherlock judging criteria."
context: fork
agent: sherlock-judging
argument-hint: <finding-to-validate>
---

Validate the finding at `$ARGUMENTS` against Sherlock judging criteria.

## Severity thresholds

| Severity | Criteria |
|----------|----------|
| **High** | Direct loss of funds >1% of affected party AND >$10. No extensive limitations on scope/conditions. |
| **Medium** | Conditional loss or broken core functionality. Requires specific but reasonable conditions. |
| **Invalid** | Theoretical only, requires admin error, informational, or gas optimization. |

## Key Sherlock rules

- **Likelihood is ignored** — only impact magnitude matters for severity
- **Hierarchy of truth**: README > code > warden interpretation
- **Repeatable small losses** compound — don't dismiss them
- **Admin trust**: Admin actions per docs are trusted; admin-as-attacker is invalid unless contest says otherwise

## Validation checklist

- [ ] Does the finding meet the quantitative loss threshold?
- [ ] Is the attack path reachable without admin/owner?
- [ ] Are preconditions reasonable (not "99 things must align")?
- [ ] Does it break a core protocol invariant or just an edge case?
- [ ] Is it a duplicate of another finding (same root cause)?

For full criteria, see [sherlock-judging-criteria.md](../../resources/sherlock-judging-criteria.md).

## Related skills

- [/cantina-judge](../cantina-judge/SKILL.md) — Cantina criteria (different severity matrix)
- [/code4rena-judge](../code4rena-judge/SKILL.md) — Code4rena criteria
- [/issue-writer](../issue-writer/SKILL.md) — Polishes findings for submission
