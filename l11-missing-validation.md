---
# Core Classification
protocol: Origin Dollar Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 10794
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/origin-dollar-audit/
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
  - cdp
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[L11] Missing validation

### Overview

See description below for full details.

### Original Finding Content

There are currently some unvalidated assumptions in the codebase. For example:


* The `VaultCore` contract [checks if the trustee is defined](https://github.com/OriginProtocol/origin-dollar/blob/bf4ff28d5944ecc277e66294fd2c702fee5cd58b/contracts/contracts/vault/VaultCore.sol#L375) before sending it fees, but [assumes it is defined](https://github.com/OriginProtocol/origin-dollar/blob/bf4ff28d5944ecc277e66294fd2c702fee5cd58b/contracts/contracts/vault/VaultCore.sol#L350) and has a `swap` function when triggering the buyback mechanism. If this assumption does not hold, the contract will be unable allocate funds.
* The [`ThreePoolStrategy` contract](https://github.com/OriginProtocol/origin-dollar/blob/bf4ff28d5944ecc277e66294fd2c702fee5cd58b/contracts/contracts/strategies/ThreePoolStrategy.sol) makes [assumptions that `assetsMapped` is of length 3](https://github.com/OriginProtocol/origin-dollar/blob/bf4ff28d5944ecc277e66294fd2c702fee5cd58b/contracts/contracts/strategies/ThreePoolStrategy.sol#L116-L120), but there’s nothing [in the `_initialize` function](https://github.com/OriginProtocol/origin-dollar/blob/bf4ff28d5944ecc277e66294fd2c702fee5cd58b/contracts/contracts/utils/InitializableAbstractStrategy.sol#L72-L75) that enforces that. The [`deposit`](https://github.com/OriginProtocol/origin-dollar/blob/bf4ff28d5944ecc277e66294fd2c702fee5cd58b/contracts/contracts/strategies/ThreePoolStrategy.sol#L90-L93) and [`depositAll`](https://github.com/OriginProtocol/origin-dollar/blob/bf4ff28d5944ecc277e66294fd2c702fee5cd58b/contracts/contracts/strategies/ThreePoolStrategy.sol#L124-L126) functions would revert if the `assetsMapped` were ever more than 3 elements long.
* The [`startCampaign`](https://github.com/OriginProtocol/origin-dollar/blob/bf4ff28d5944ecc277e66294fd2c702fee5cd58b/contracts/contracts/liquidity/LiquidityReward.sol#L98) function from the `LiquidityReward` contract does not validate that `_numBlocks` is not zero. This could emit confusing events and update values such as `startBlock`, `endBlock`, and `pool.lastRewardBlock` without reason.


Consider adding validation in these and all other places where assumptions are currently unchecked to reduce the chance of errors when interacting with and refactoring the contracts.


**Update:** *Fixed in [PR#632](https://github.com/OriginProtocol/origin-dollar/pull/632), [PR#688](https://github.com/OriginProtocol/origin-dollar/pull/688), and [PR#715](https://github.com/OriginProtocol/origin-dollar/pull/715).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Origin Dollar Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/origin-dollar-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

