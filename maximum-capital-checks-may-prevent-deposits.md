---
# Core Classification
protocol: Size v1
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35983
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Size-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Size-Spearbit-Security-Review.pdf
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
finders_count: 4
finders:
  - 0xLeastwood
  - Slowfi
  - Hyh
  - 0x4non
---

## Vulnerability Title

Maximum capital checks may prevent deposits

### Overview


The report describes a bug in the Size protocol that can cause problems when depositing funds. The bug occurs when a user tries to deposit ETH as collateral, but the amount of borrow token exceeds the maximum amount set by the Size team. This can lead to the transaction being reverted, causing potential issues with liquidation. The recommended solution is to control the amount of emitted debt token. The bug has been fixed in a recent commit, but has not yet been reviewed by the Spearbit team.

### Original Finding Content

## Medium Risk Assessment

## Severity
**Medium Risk**

## Context
`Size.sol#L130-L131`

## Description
The deposit functions perform two validation checks after depositing either the collateral or borrow token. These two validations attempt to ensure that the maximum amounts defined by the Size team of each token on the protocol are not exceeded. The functions that perform the checks are:

- **validateCollateralTokenCap**
- **validateBorrowATokenCap**

The maximum amounts are initially designed to avoid an excessive amount of funds entering the protocol. Nevertheless, there are certain scenarios where these checks may arise functional problems.

The exposed scenario for illustrating this issue starts with a user attempting to deposit ETH as collateral. If the amount of borrow token, calculated as the total balance of aToken from funds deposited on Aave, has increased over the maximum amount, the transaction reverts. This can also have a higher impact when depositing collateral to avoid liquidation, as identified by the Size team.

## Recommendation
After a discussion with the Size team, the final conclusion for fixing this issue and any others related to maximum amounts check is to just control the amount of emitted debt token.

## Size
**Fixed in commit fee6ab85.**

## Spearbit
**Acknowledged but not reviewed.**

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Size v1 |
| Report Date | N/A |
| Finders | 0xLeastwood, Slowfi, Hyh, 0x4non |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Size-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Size-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

