---
# Core Classification
protocol: Sushi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19610
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/sushi/bentobox-strategies-staking-contract/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/sushi/bentobox-strategies-staking-contract/review.pdf
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
  - dexes
  - cdp
  - yield
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

Non-standard ERC20 Tokens are Not Supported

### Overview


This bug report is about an issue with AaveStrategy in the BentoBox Strategies and Staking Contract. When trying to call _skim() via harvest() or skim() of the BaseStrategy, the transaction reverts because the call to strategyToken.approve() in line 71 has a different return value of approve() on the target contract. This is specifically true when the token’s approve() function does not adhere to the ERC20 interface, like the case of stablecoin USDT.

The testing team suggests further utilization of SafeTransferLib for AaveStrategy and the use of safeApprove() and the other functions to interact with the strategyToken. This issue also exists for SushiStrategy but, since that contract is meant to operate with the regular ERC20 SUSHI token only, the impact is reduced and inconsequential. However, conscious consideration of this issue should be employed when deriving future contracts from BaseStrategy.

### Original Finding Content

## Description

A strategyToken which does not strictly follow the ERC20 token interface might not be supported by the contract. Specifically, this is true when the token’s `approve()` function does not adhere to the ERC20 interface. One prominent example for such tokens is the stablecoin USDT.

When trying to call `_skim()` via `harvest()` or `skim()` of the BaseStrategy for such tokens, the transaction reverts. This is because the call to `strategyToken.approve()` in line [71] has a different return value of `approve()` on the target contract. In the case of USDT, the function does not return any value, which causes an execution error as a bool is expected.

## Recommendations

The base contract of AaveStrategy defined in `BaseStrategy.sol` is not susceptible to this issue because it’s using the “safe” function calls of `SafeTransferLib` for ERC20 tokens (see line [16]). The testing team suggests further utilisation of `SafeTransferLib` for AaveStrategy and the use of `safeApprove()` and the other functions to interact with the `strategyToken`. 

Please note, this issue also exists for SushiStrategy but, since that contract is meant to operate with the regular ERC20 SUSHI token only, the impact is reduced and inconsequential. However, conscious consideration of this issue should be employed when deriving future contracts from BaseStrategy.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Sushi |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/sushi/bentobox-strategies-staking-contract/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/sushi/bentobox-strategies-staking-contract/review.pdf

### Keywords for Search

`vulnerability`

