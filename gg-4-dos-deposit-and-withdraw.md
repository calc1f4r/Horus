---
# Core Classification
protocol: Bridges
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26580
audit_firm: Guardian Audits
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Guardian Audits/2022-05-21-Bridges.md
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
  - Guardian Audits
---

## Vulnerability Title

GG-4 | DoS Deposit and Withdraw

### Overview


This bug report concerns a vulnerability in pool 0 of a contract, which allowed users to prevent deposits and withdrawals. This was done by draining the BNB from the contract using a re-entrancy or by using the BNB function. The recommendation was to refactor the dividend payments so they are separate from withdrawals and deposits. The Bridges Team resolved the issue by refactoring the dividends and removing the emergency BNB function. This ensures that deposits and withdrawals can no longer be prevented by draining the BNB from the contract.

### Original Finding Content

**Description**

Because depositing and withdrawing from pool 0 relies on a successful BNB transfer for the dividends payment, it is possible to prevent deposits and withdrawals. If a user were to drain the BNB from the contract using the re-entrancy described earlier or the owner drained the BNB using the `BNB` function, then the `call` would fail and the transaction would revert.

**Recommendation**

Refactor the dividend payments so they are separate from withdrawals and deposits.

**Resolution**

Bridges Team:

- Dividends have been refactored and the emergency BNB function has been removed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Guardian Audits |
| Protocol | Bridges |
| Report Date | N/A |
| Finders | Guardian Audits |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Guardian Audits/2022-05-21-Bridges.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

