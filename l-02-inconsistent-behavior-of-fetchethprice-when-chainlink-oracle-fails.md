---
# Core Classification
protocol: Ouroboros_2024-12-06
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45961
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Ouroboros-security-review_2024-12-06.md
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

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

[L-02] Inconsistent behavior of `fetchEthPrice()` when Chainlink oracle fails

### Overview

See description below for full details.

### Original Finding Content

The `EthPriceFeed.fetchEthPrice()` function reverts when `status == Status.chainlinkBroken`. This status is set after the Chainlink oracle has returned wrong or outdated data, or the price has deviated too much from the previous price. However, when this happens, the latest valid price is returned.

This provokes that the wrong value can be returned in the transaction where the Chainlink oracle fails, but instead a revert happens in the next transaction.

Let's consider the following scenario:
The current ETH price is $4000.

- Price falls to $1999.
- When `fetchEthPrice` is called it returns the latest valid price of $4000 and sets the status to `chainlinkBroken`.
- In the next transaction the price is still $1999, but in this case, the function reverts.

Consider either always reverting or always returning the latest valid price when the Chainlink oracle fails.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Ouroboros_2024-12-06 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Ouroboros-security-review_2024-12-06.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

