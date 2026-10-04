---
# Core Classification
protocol: Panoptic Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33824
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/panoptic-audit
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
  - OpenZeppelin
---

## Vulnerability Title

Liquidator Can Incur Loss During Liquidation

### Overview


This bug report discusses an issue where an account can lose money during the liquidation process if the total supply of shares is increased. This can result in the liquidator receiving less than the delegated shares' original value. The report suggests ensuring that the liquidator always gains a net profit to incentivize them to perform the liquidation. The issue has been resolved in the latest update.

### Original Finding Content

An account can be liquidated if it does not have enough collateral to cover its position(s), which is an important operation to ensure the health of the protocol. Administrating the insolvent account proceeds by first having the liquidator delegate an amount of shares to cover the account's position(s), then exercising the entire position list of the account, and finally returning the delegated amount plus a bonus to the liquidator. It's possible for a liquidator to lose money because when all positions are exercised, shares can be minted which increases the total supply of shares. This can result in the asset value of the delegated shares plus the bonus after the liquidation being less than the asset value of the delegated shares before the liquidation due to dilution of the share value. Consider ensuring that performing a liquidation always results in a net gain for the liquidator in order for there to be an incentive to perform the operation.


***Update:** Resolved at commit 02cd20d.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Panoptic Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/panoptic-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

