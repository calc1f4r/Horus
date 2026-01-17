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
solodit_id: 34106
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

[M-03] Race condition for bridged BTC

### Overview


This bug report describes a potential issue where users may lose their bridged BTC when using a specific transfer process. The severity of this bug is high, as it could result in users losing their funds. However, the likelihood of this happening is low and requires special conditions. 

The issue occurs when multiple users transfer their BTC to the same onramp address at the same time. The onramp may not have enough tokens to handle all of these orders, causing some users to lose their funds. 

To fix this issue, the report recommends implementing a queue mechanism for the off-chain relayer, which would handle users one by one. Alternatively, users could be instructed to transfer their BTC to the relayer's BTC address instead of the onramp's address. This would ensure that the onramp has enough tokens before completing the bridge process.

### Original Finding Content

**Severity**

**Impact:** High, users would lose bridged BTC.

**Likelihood:** Low, requires special conditions.

**Description**

To bridge BTC users need to transfer their funds to the onramp address (`scriptPubKeyHash`) and then the relayer would call `proveBtcTransfer()` and the target onramp would transfer the bridged token to the user. The issue is that multiple users may have transferred their BTC to that address at the same time and the onramp may not have enough tokens to handle all those orders so some of the users would lose their funds.

**Recommendations**

Add queue mechanism for off-chain relayer and handle users one by one.
Or don't ask users to transfer BTC directly to the onramp contract's `scriptPubKeyHash`. gather BTC in the relayer BTC address and when the bridge was successful in the BOB then transfer onramp's BTC.

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

