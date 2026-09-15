---
# Core Classification
protocol: Sandclock
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1291
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-01-sandclock-contest
source_link: https://code4rena.com/reports/2022-01-sandclock
github_link: https://github.com/code-423n4/2022-01-sandclock-findings/issues/179

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - yield
  - yield_aggregator
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - defsec
---

## Vulnerability Title

[M-13] Incompatibility With Rebasing/Deflationary/Inflationary tokens

### Overview


This bug report is about a vulnerability in the Strategy contracts which do not appear to support rebasing/deflationary/inflationary tokens whose balance changes during transfers or over time. This vulnerability can have an impact on the user-supplied tokens. The proof of concept can be found in the given GitHub links. The tools used for this bug report was Code Review. The recommended mitigation steps are to make sure the token vault accounts for any rebasing/inflation/deflation, add support in contracts for such tokens before accepting user-supplied tokens, and check before/after balance on the vault.

### Original Finding Content

_Submitted by defsec_

The Strategy contracts do not appear to support rebasing/deflationary/inflationary tokens whose balance changes during transfers or over time. The necessary checks include at least verifying the amount of tokens transferred to contracts before and after the actual transfer to infer any fees/interest.

#### Proof of Concept

- <https://github.com/code-423n4/2022-01-sandclock/blob/main/sandclock/contracts/strategy/BaseStrategy.sol#L239>

- <https://github.com/code-423n4/2022-01-sandclock/blob/main/sandclock/contracts/strategy/BaseStrategy.sol#L221>

#### Recommended Mitigation Steps

- Make sure token vault accounts for any rebasing/inflation/deflation
- Add support in contracts for such tokens before accepting user-supplied tokens
- Consider to check before/after balance on the vault.

**[naps62 (Sandclock) disputed](https://github.com/code-423n4/2022-01-sandclock-findings/issues/179#issuecomment-1012485483):**
 > we did not intend to support those currencies in the first place

**[dmvt (judge) commented](https://github.com/code-423n4/2022-01-sandclock-findings/issues/179#issuecomment-1024341741):**
 > As with issues #55 and #164, this oversight can cause a loss of funds and therefor constitutes a medium risk. Simply saying you don't support something does not mean that thing doesn't exist or won't cause a vulnerability in the future.





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Sandclock |
| Report Date | N/A |
| Finders | defsec |

### Source Links

- **Source**: https://code4rena.com/reports/2022-01-sandclock
- **GitHub**: https://github.com/code-423n4/2022-01-sandclock-findings/issues/179
- **Contest**: https://code4rena.com/contests/2022-01-sandclock-contest

### Keywords for Search

`vulnerability`

