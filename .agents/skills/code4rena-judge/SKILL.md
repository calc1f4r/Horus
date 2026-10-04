---
name: "code4rena-judge"
description: "Validate a security finding against Code4rena audit competition standards. Determines severity (High/Medium/QA/Invalid), checks in-scope validity, applies severity caps, and assesses submission quality. Use when validating findings for Code4rena contests, determining C4 severity, or checking if an issue meets C4 judging criteria."
---
Use the [code4rena-judge subagent](../../../.codex/agents/code4rena-judge.toml) when you want delegated execution.
That subagent is configured for live web search and may delegate to narrower repo subagents when the workflow splits cleanly.

Input: `<finding-to-validate>`.

Validate the finding at `<finding-to-validate>` against Code4rena judging criteria.

## Severity classification

| Severity | Criteria |
|----------|----------|
| **High** | Assets can be stolen/lost directly, or protocol can be rendered inoperable |
| **Medium** | Assets not at direct risk, but function of the protocol or availability could be impacted; or leak value with hypothetical attack path |
| **QA** | Low-risk issues: state handling, input validation, informational |
| **Gas** | Gas optimization only |
| **Invalid** | Out of scope, theoretical, already known, or duplicate |

## Key C4 rules

- **In-scope check** — Only files listed in the contest scope qualify
- **Known issues** — Findings in the known issues list are invalid
- **Bot race** — Automated findings from C4 bots are excluded from manual submissions
- **Severity downgrade** — Wardens can dispute, but judges make final call
- **Duplicates** — Same root cause = duplicate; best report chosen as primary

## Validation checklist

- [ ] Is the finding in the contest scope?
- [ ] Is it already in the known issues list?
- [ ] Does severity match the C4 criteria above?
- [ ] Is the attack path concrete (not theoretical)?
- [ ] Would a warden dispute succeed or fail?

For full criteria, see [code4rena-judging-criteria.md](../../../.codex/resources/code4rena-judging-criteria.md).

## Related skills

- [sherlock-judging](../sherlock-judging/SKILL.md) — Sherlock criteria
- [cantina-judge](../cantina-judge/SKILL.md) — Cantina criteria
- [issue-writer](../issue-writer/SKILL.md) — Polishes findings for submission
