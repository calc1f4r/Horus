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
solodit_id: 17883
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf
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

Missing events for critical operations

### Overview

See description below for full details.

### Original Finding Content

## Type: Access Controls
**Target:** Frax.sol

## Difficulty: High

## Description
Several critical operations do not trigger events. As a result, it is difficult to check the behavior of the contracts. Ideally, the following critical operations should trigger events:

### FRAXStablecoin
- refreshCollateralRatio
- addPool
- removePool
- setOwner
- setRedemptionFee
- setMintingFee
- setFraxStep
- setPriceTarget
- setRefreshCooldown
- setETHUSDOracle
- setFXSAddress
- setController
- setPriceBand
- setFRAXEthOracle
- setFXSAddress

### veFXS
- commit_smart_wallet_checker
- apply_smart_wallet_checker
- toggleEmergencyUnlock

### FRAXShares
- setFRAXAddress
- setFXSMinDAO
- setOwner
- toggleMinting
- toggleRedeeming
- toggleRecollateralize
- toggleBuyBack
- toggleCollateralPrice

### FraxPool
- setPoolParameters
- setTimelock
- setOwner

### CurveAMO_V3
- setTimelock
- setOwner
- setMiscRewardsCustodian
- setVoterContract
- setPool
- setThreePool
- setMetapool
- setVault
- setBorrowCap
- setMaxFraxOutstanding
- setMinimumCollateralRatio
- setConvergenceWindow
- setOverrideCollatBalance
- setCustomFloor
- setDiscountRate
- setSlippages
- recoverERC20
- mintRedeemPart1
- mintRedeemPart2
- burnFRAX
- burnFXS
- metapoolDeposit

Without events, users and blockchain-monitoring systems cannot easily detect suspicious behavior.

## Exploit Scenario
Eve compromises the `COLLATERAL_PRICE_PAUSER` role of `FraxPool`, calls `toggleCollateralPrice` with a very low price, and redeems her FRAX shares, draining a large amount of collateral from the pool. The Frax Finance team notices the change only when it is too late to mitigate it.

## Recommendations
Short term, add events for all critical operations. Events aid in contract monitoring and the detection of suspicious behavior. 

Long term, consider using a blockchain-monitoring system to track any suspicious behavior in the contracts. The system relies on several contracts to behave as expected. A monitoring mechanism for critical events would quickly detect any compromised system components.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
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

