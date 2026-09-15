---
# Core Classification
protocol: Filament
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45623
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-08-15-Filament.md
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
  - Zokyo
---

## Vulnerability Title

Improper use of the whenNotPaused modifier for liquidations may result in the protocol taking on bad debt or resulting in users being liquidated as soon as unpause is executed

### Overview


The Escrow contract has a function called liquidatePosition that is used to remove users from the protocol if they do not have enough collateral due to market changes. However, the contract is currently set up so that this function cannot be used when the contract is paused. This can cause problems for both the protocol and users, as the protocol may take on bad debt and users may not be able to fix their positions. The report recommends either removing the paused restriction or implementing a grace period to allow users to fix their positions before being liquidated.

### Original Finding Content

**Severity**: Medium

**Status**: Resolved

**Description**

The Escrow contract contains the function liquidatePosition which is responsible for liquidating users from the protocol when they haven’t maintained a healthy state of over collateralisation as a result of the markets moving unfavorably. The whenNotPaused modifier effectively prevents the liquidation functionality from executing when the contract is paused. This may cause issues for both the protocol and the users depending on how long maintenance or security investigations take. Firstly, a drastic market turn may cause the protocol to take on bad debt with the lack of liquidations to keep the protocol's value in a healthy position. Secondly, user positions may be sunk and are out of the control of users to bring back into a healthy state since they cannot modify their position when the protocol is paused. Once the protocol comes out of a paused state, users may be eligible for forced liquidation.

**Recommendation**: 

There are two ways to go about fixing this issue:

First: Remove the whenNotPaused modifier on liquidation functionalities to continuously allow users to be liquidated, thus keeping the protocol in a healthy state. Continuously allow users to keep their positions in a healthy state even while the contract is paused. Opening new positions will still be blocked while the protocol is paused.
Second (and most recommended): If the protocol owners insist on having a pausable modifier for the liquidations, consider setting a grace period of a few hours to allow users to bring their positions back in a healthy state. This is what Aave 3.1’s protocol upgrade did to work with pausable modifiers on liquidation.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Filament |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-08-15-Filament.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

