---
# Core Classification
protocol: Kuiper
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19820
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-09-defiProtocol
source_link: https://code4rena.com/reports/2021-09-defiProtocol
github_link: https://github.com/code-423n4/2021-09-defiprotocol-findings/issues/196

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
  - bridge
  - cdp
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-01] Use safeTransfer instead of transfer

### Overview


This bug report is about a potential issue with the `transfer()` function in the Auction.sol contract. It was submitted by hack3r-0m, and also found by itsmeSTYJ, JMukesh, leastwood, and shenwilly. The issue is that `transfer()` might return false instead of reverting, and if the return value is ignored, it could be considered successful, when it is not. To avoid this issue, it is recommended to use `safeTransfer()` or to check the return value if the length of the returned data is greater than 0. This issue was confirmed by frank-beard (Kuiper) and commented on by Alex the Entreprenerd (judge), who agreed with the finding and the severity, given the example given, as the funds would be stuck in the contract.

### Original Finding Content

_Submitted by hack3r-0m, also found by itsmeSTYJ, JMukesh, leastwood, and shenwilly_

<https://github.com/code-423n4/2021-09-defiProtocol/blob/main/contracts/contracts/Auction.sol#L146>

`transfer()` might return false instead of reverting, in this case, ignoring return value leads to considering it successful.

use `safeTransfer()` or check the return value if length of returned data is > 0.

**[frank-beard (Kuiper) confirmed](https://github.com/code-423n4/2021-09-defiprotocol-findings/issues/196)** 

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2021-09-defiprotocol-findings/issues/196#issuecomment-983125327):**
 > Agree with finding, agree with severity given the specific example given as the funds would be stuck in the contract

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Kuiper |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-09-defiProtocol
- **GitHub**: https://github.com/code-423n4/2021-09-defiprotocol-findings/issues/196
- **Contest**: https://code4rena.com/reports/2021-09-defiProtocol

### Keywords for Search

`vulnerability`

