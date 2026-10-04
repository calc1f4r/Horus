---
# Core Classification
protocol: Surge
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55141
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Surge-Security-Review.md
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

protocol_categories:
  - liquid_staking
  - cdp
  - yield
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Shieldify Security
---

## Vulnerability Title

[H-02] Missing Implementation in `PositionManager.sol` Causes the Liquidity in Positions to Not Be Retrievable

### Overview


This bug report discusses a problem with the `PositionManager` code that can result in a high risk situation. The code allows for the collection of fees and addition of liquidity, but there is no way for the admin to transfer these positions or access the liquidity they hold. This can lead to a loss of funds and make it difficult for the admin to collect fees efficiently. The recommendation is to implement logic that allows for the transfer of LP positions or access to the underlying liquidity. The team has acknowledged the issue.

### Original Finding Content

## Severity

High Risk

## Description

`PositionManager` can receive liquidity position NFTs, collect fees, and add liquidity to them but there is no way for the admin to transfer these positions outside the contract, access the liquidity they are holding, or burn them.

## Location of Affected Code

File: [PositionManager.sol]()

## Impact

As a result, the underlying liquidity will not be accessible anymore resulting in a loss of funds. Furthermore, these LP positions will be configured for a specific price range. Once the price goes outside of this price range it is normal for liquidity providers to be able to move the liquidity to another price range that is more profitable by decreasing the liquidity from their current LP position and to create a new position with a more relevant price range.

So over some time when the price moves the admin will not be able to collect fees efficiently as well.

## Recommendation

Consider implementing logic for either transferring the LP position out of the contract or logic that will be able to access the underlying liquidity of the LP positions that are in control of the `PositionManager`.

## Team Response

Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Surge |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Surge-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

