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
solodit_id: 10781
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/origin-dollar-audit/
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

[M03] Not checking asset balance in strategy before removal

### Overview


This bug report is about the `removePToken` function from the `InitializableAbstractStrategy`, which allows the governor to remove an asset from the strategy. However, there are no checks for whether the strategy still invests the asset in the underlying platform before removing it. This means that if the asset is removed, the invested amount will not be taken into account when calculating the total amount of assets held by a strategy, or when calculating the redeem outputs. Additionally, the invested amount will not be taken into account in the `withdrawAll` functions defined on each child contract. The Origin team has decided to keep this as it is, since it gives them a way to remove a strategy that is broken in some way and prevents other projects from causing a DOS (Denial of Service) attack.

### Original Finding Content

The [`removePToken` function](https://github.com/OriginProtocol/origin-dollar/blob/bf4ff28d5944ecc277e66294fd2c702fee5cd58b/contracts/contracts/utils/InitializableAbstractStrategy.sol#L148) from the `InitializableAbstractStrategy` lets the governor remove an asset from the strategy, by:


* Removing the asset address [from the `assetsMapped` array](https://github.com/OriginProtocol/origin-dollar/blob/bf4ff28d5944ecc277e66294fd2c702fee5cd58b/contracts/contracts/utils/InitializableAbstractStrategy.sol#L153-L156) (e.g., DAI, USDT, USDC addresses).
* Setting the `assetToPToken` mapping [for that particular asset address to `address(0)`](https://github.com/OriginProtocol/origin-dollar/blob/bf4ff28d5944ecc277e66294fd2c702fee5cd58b/contracts/contracts/utils/InitializableAbstractStrategy.sol#L157).


However, there are no checks for whether the strategy still invests the asset in the underlying platform before removing it. If the asset is removed, this invested amount will be disregarded when [checking the total amount of assets held by a strategy](https://github.com/OriginProtocol/origin-dollar/blob/bf4ff28d5944ecc277e66294fd2c702fee5cd58b/contracts/contracts/vault/VaultCore.sol#L448), which is used to perform allocations, or [when calculating the redeem outputs](https://github.com/OriginProtocol/origin-dollar/blob/bf4ff28d5944ecc277e66294fd2c702fee5cd58b/contracts/contracts/vault/VaultCore.sol#L572), which is used to perform redemptions. Additionally, the invested amount will be disregarded in the `withdrawAll` functions defined on each child contract.


Consider either reverting if the strategy still invests the asset, or sending the remaining balance to the vault contract.


**Update:** *Not fixed. The Origin team states:*



> We’ll keep this as it. We can recover funds if we need to by re-adding the strategy. By not checking amounts etc, it gives us a way to remove a strategy that is broken in some way, and prevents some other project’s DOS from being our DOS for long.
> 
>

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

