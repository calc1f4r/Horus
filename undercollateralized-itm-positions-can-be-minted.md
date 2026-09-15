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
solodit_id: 33815
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/panoptic-audit
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
  - OpenZeppelin
---

## Vulnerability Title

Undercollateralized ITM Positions Can Be Minted

### Overview


The bug report discusses an issue with the collateral requirements for minting short options. The current formula for calculating collateral is causing problems because it does not take into account the profit/loss of a new position when it is in the money (ITM). This can lead to the required collateral being higher than expected and can result in the user's position being undercollateralized and vulnerable to liquidation. The bug has been resolved in a recent update.

### Original Finding Content

When minting short options, the collateral requirements are computed as `amount * collateralRatio * maintenanceMarginRatio` where `amount` is the number of options contracts denominated in the numeraire, `collateralRatio` is between 0.2 and 1 depending on the current pool utilization, and `maintenanceMarginRatio` is a fixed quantity (1.3333). The position can be liquidated if the required value is more than the token value of the account balance. These values are calculated from the token data returned by `getAccountMarginDetails`. This function will use an additional term in calculating the required collateral of a position to evaluate the profit/loss of that position when it is ITM, which can result in the required collateral being higher than when minting and can exceed the collateral balance of the user. The user is then immediately vulnerable to liquidation because their position is undercollateralized.


When minting a new ITM position, the profit/loss of the new position is not considered immediately in the collateral calculation, resulting in a position that can be liquidated right away following the mint. Consider calculating collateralization requirements the same way during both minting and when checking if an account is liquidatable.


***Update:** Resolved at commit 4e1de7a.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

