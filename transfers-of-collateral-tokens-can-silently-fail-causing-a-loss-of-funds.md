---
# Core Classification
protocol: Frax Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17881
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf
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
  - dexes
  - cdp
  - yield
  - services

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Travis Moore | Frax Finance travis@frax.ﬁnance Spencer Michaels
  - Natalie Chin
  - Maximilian Krüger
---

## Vulnerability Title

Transfers of collateral tokens can silently fail, causing a loss of funds

### Overview


This bug report is about data validation in Frax.sol, FraxPool.sol, and FXS.sol. It is considered to be a high difficulty issue. The issue is that the FraxPool does not check the return value of collateral_token.transfer or collateral_token.transferFrom. This means that certain tokens, such as BAT, return false instead of reverting if a transfer fails. This could allow users to mint FRAX without providing collateral, which would break the system and the FRAX peg. This issue is also present in the functions FraxPool.mint1t1FRAX, FraxPool.mintFractionalFRAX, FraxPool.collectRedemption, FraxPool.recollateralizeFRAX, and FraxPool.buyBackFXS.

The exploit scenario is that FRAX is collateralized by 80%. If a new FraxPool with collateral token T is added to the system, and the transferFrom function of this token returns false instead of reverting to signal a failure, Alice, who does not hold any T, can call FraxPool.mintFractionalFRAX. As long as Alice has enough FXS to mint the requested amount of FRAX, the transaction will succeed and Alice will have minted FRAX by paying only 20% of its value.

The short-term recommendation is to always use SafeERC20.safeTransfer and .safeTransferFrom to ensure the proper handling of failed transfers, including token transfers that do not revert upon failing or have no return value. The long-term recommendation is to integrate Slither into the continuous integration pipeline to catch missing return value checks, and review Appendix B, which outlines ERC20 token best practices.

### Original Finding Content

## Data Validation Report

## Type
Data Validation

## Targets
- Frax.sol
- FraxPool.sol
- FXS.sol

## Difficulty
High

## Description
FraxPool does not check the return value of `collateral_token.transfer` or `collateral_token.transferFrom`. Certain tokens, such as BAT, return false rather than reverting if a transfer fails. If a pool for one of these tokens is added, users will be able to mint FRAX without providing collateral. This would break the system and the FRAX peg. This issue is also present in the following functions:
- `FraxPool.mint1t1FRAX`
- `FraxPool.mintFractionalFRAX`
- `FraxPool.collectRedemption`
- `FraxPool.recollateralizeFRAX`
- `FraxPool.buyBackFXS`

## Exploit Scenario
FRAX is collateralized by 80%. A new FraxPool with collateral token T is added to the system. The `transferFrom` function of this token returns false instead of reverting to signal a failure. Alice, who does not hold any T, calls `FraxPool.mintFractionalFRAX`. As long as Alice has enough FXS to mint the requested amount of FRAX, the transaction will succeed and Alice will have minted FRAX by paying only 20% of its value.

## Recommendations
- **Short term:** Always use `SafeERC20.safeTransfer` and `.safeTransferFrom` to ensure the proper handling of failed transfers, including token transfers that do not revert upon failing or have no return value.
- **Long term:** Integrate Slither into the continuous integration pipeline to catch missing return value checks, and review [Appendix B](#), which outlines ERC20 token best practices.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Frax Finance |
| Report Date | N/A |
| Finders | Travis Moore | Frax Finance travis@frax.ﬁnance Spencer Michaels, Natalie Chin, Maximilian Krüger |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf

### Keywords for Search

`vulnerability`

