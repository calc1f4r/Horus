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
solodit_id: 28628
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Abyss%20Finance/Abyss%20LockUp/README.md#2-potential-withdrawal-lock-and-invalid-distribution
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

Potential withdrawal lock and invalid distribution

### Overview


A bug has been reported related to a deflationary token and its lockup balance. The bug can be reproduced by depositing N tokens from Alice, Bob, and Eve, then sending a relatively huge amount M to the Lockup contract directly. After Alice, Bob, and Eve each request and withdraw N tokens, Alice has lost more funds than Eve, which is unfair as they both deposited the same amount. It is recommended to fix the rebase logic related to the lockup balance calculation in order to resolve this bug.

### Original Finding Content

##### Description
How to reproduce bug:
 - Deposit N tokens from Alice
 - Deposit N tokens from Bob
 - Deposit N tokens from Eve
 - Send M (relatively huge amount) to Lockup contract directly (via transfer)
 - Request and withdraw N tokens to Alice
 - Request and withdraw N tokens to Bob
 - Request and withdraw N tokens to Eve
 - At this point participant got different withdrawn amount(first lost more funds), and depending on M amount sometimes contract can be failed on `request` call

Detailed explanation:
 - Use particular deflationary token as depositing asset https://gist.github.com/algys/eb905ec8efa41f80cf1eab57a3b31649
 - After all withdrawals Alice lost more funds than Eve, that behavior is unfair because they deposited same amount and just lost funds depending on withdrawal order

##### Recommendation
It is recommended to fix rebase logic related to lockup balance based calculation

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Abyss%20Finance/Abyss%20LockUp/README.md#2-potential-withdrawal-lock-and-invalid-distribution
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

