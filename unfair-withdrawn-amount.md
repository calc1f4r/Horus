---
# Core Classification
protocol: Abyss Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28627
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Abyss%20Finance/Abyss%20LockUp/README.md#1-unfair-withdrawn-amount
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

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

Unfair withdrawn amount

### Overview


This bug report is about an unfair behavior in a deflationary token system. It describes a situation where Alice, Bob, and Eve each deposit the same amount of tokens, but when they withdraw their tokens, Alice loses more funds than Eve. The bug is reproducible by following the steps outlined in the report. The recommendation is to refactor the rebase logic and reduce the amount of code duplication. This bug report is important for deflationary token systems because it highlights the potential for unfair behavior if the code is not properly maintained.

### Original Finding Content

##### Description
How to reproduce bug:
 - Deposit N tokens from Alice
 - Deposit N tokens from Bob
 - Deposit N tokens from Eve
 - Request and withdraw N tokens to Alice
 - Request and withdraw N tokens to Bob
 - Request and withdraw N tokens to Eve
 - At this point participant got different withdrawn amount(first lost more funds)

Detailed explanation:
 - Use particular deflationary token as depositing asset https://gist.github.com/algys/eb905ec8efa41f80cf1eab57a3b31649
 - After all withdrawals Alice lost more funds than Eve, that behavior is unfair because they deposited same amount and just lost funds depending on withdrawal order

##### Recommendation
It is recommended to refactor rebase logic and reduce amount of code duplication.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Abyss Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Abyss%20Finance/Abyss%20LockUp/README.md#1-unfair-withdrawn-amount
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

