---
# Core Classification
protocol: Kekotron
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31475
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Kekotron-security-review.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-03] Missing deadline check in swap functions

### Overview


This bug report discusses a minor issue with swap functions that do not have a deadline parameter. This parameter allows users to limit the execution of their transactions, preventing them from being executed at unfavorable times. While this may not be a major problem because the functions have slippage protection, it is recommended to introduce a deadline parameter in all swap functions to prevent users from missing out on positive slippage. 

### Original Finding Content

**Severity**

Impact: Low, the user would not be at a loss and would only miss positive slippage.

Likelihood: High, deadline parameter is missing.

**Description**

Swap functions don't have deadline parameter. This parameter can provide the user an option to limit the execution of their pending transaction.
Without a deadline parameter, users can execute their transactions at unexpected times when market conditions are unfavorable.

However, this is not a big problem in this case because the functions have slippage protection. Even though the users will get at least as much as they set, they may still be missing out on positive slippage if the exchange rate becomes favorable when the transaction is included in a block.

**Recommendations**

Introduce a `deadline` parameter in all swap functions.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Kekotron |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Kekotron-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

