---
# Core Classification
protocol: Bob Onramp
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34105
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/BOB-Onramp-security-review.md
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

[M-02] BTC transactions can have multiple inputs and outputs

### Overview


The bug report discusses an issue where a relayer is not properly choosing the recipient and onramp contract for BTC transactions, resulting in potential funds going to the wrong address. It is recommended to ensure that the relayer uses the correct recipient address to avoid this issue.

### Original Finding Content

**Severity**

**Impact:** Medium

**Likelihood:** Medium

**Description**

BTC txs can have multiple inputs and outputs and the relayer chooses the `reciever` and `onramp` contract based on the BTC transaction after users make the BTC transactions. The issue is that it's not clear which input address would be chosen as a token receiver and which output address is going to be chosen as an onramp contract. Funds may go to a different receiver address or the relayer may use the wrong onramp contract. If the relayer handles only specific BTC txs users should be informed about relayer limitations.

**Recommendations**

Ensure the relayer uses the correct recipient address.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Bob Onramp |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/BOB-Onramp-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

