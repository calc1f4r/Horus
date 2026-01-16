---
# Core Classification
protocol: Curve Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27704
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Curve%20Finance/StableSwapNG/README.md#10-admin-balances-dont-account-for-potential-token-rebases
github_link: none

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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Admin balances don't account for potential token rebases

### Overview


A bug report has been filed regarding admin fees not taking into account potential slashings in an array. If admin fees are withdrawn first after a slashing event, then LPs are getting unfairly diluted. This issue has been assigned a medium severity level as admin balances don't account for both token rebases up and down, with slashings being rare events. The recommendation is to add a comment in the `_balances` function that admin balances don't account for token rebases. This bug report is important to ensure fairness in the system and prevent LPs from getting unfairly diluted.

### Original Finding Content

##### Description
Admin fees (stored in an array https://github.com/curvefi/stableswap-ng/blob/8c78731ed43c22e6bcdcb5d39b0a7d02f8cb0386/contracts/main/CurveStableSwapMetaNG.vy#L208) don't account for potential slashings. If admin fees are withdrawn first (after the slashing event), then LPs are getting unfairly diluted.
This issue has been assigned a MEDIUM severity level because admin balances don't account for both rebases up and down while slashings are quite rare events (so that rebases down would be outweighed with rebases up).

##### Recommendation
We recommend adding a comment in the `_balances` function that admin balances don't account for token rebases.


***

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Curve Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Curve%20Finance/StableSwapNG/README.md#10-admin-balances-dont-account-for-potential-token-rebases
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

