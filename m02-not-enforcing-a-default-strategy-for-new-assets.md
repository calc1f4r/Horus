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
solodit_id: 10780
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

[M02] Not enforcing a default strategy for new assets

### Overview


This bug report describes an issue with the `supportAsset` function in the Origin Protocol's VaultCore contract. This function allows the governor to add a new asset to the VaultCore, but it does not enforce a default strategy for it. This can potentially cause a misbehavior when allocating assets from the vault to the strategies, as the new asset will contribute to the utilization of the vault buffer but not be deposited to any strategy, skewing the investment ratio and draining the buffer that should be used for future redemptions. The Origin team has stated that this issue will not lose any funds, and may be beneficial in times when the Origin Dollar doesn't trust any lending protocol/strategy, as it increases stability. However, the team has decided to keep the function as is and not enforce configuration of the asset's default strategy.

### Original Finding Content

The [`supportAsset` function](https://github.com/OriginProtocol/origin-dollar/blob/bf4ff28d5944ecc277e66294fd2c702fee5cd58b/contracts/contracts/vault/VaultAdmin.sol#L139) allows the governor to add a new asset to the `VaultCore` contract, but it does not enforce a default strategy for it [by calling the `setAssetDefaultStrategy`](https://github.com/OriginProtocol/origin-dollar/blob/bf4ff28d5944ecc277e66294fd2c702fee5cd58b/contracts/contracts/vault/VaultAdmin.sol#L119).


This can potentially cause a misbehavior when allocating assets from the vault to the strategies. The new asset can still be deposited through the [`mint`](https://github.com/OriginProtocol/origin-dollar/blob/bf4ff28d5944ecc277e66294fd2c702fee5cd58b/contracts/contracts/vault/VaultCore.sol#L43) or [`mintMultiple`](https://github.com/OriginProtocol/origin-dollar/blob/bf4ff28d5944ecc277e66294fd2c702fee5cd58b/contracts/contracts/vault/VaultCore.sol#L95) functions, and it will contribute to the [utilization of the vault buffer](https://github.com/OriginProtocol/origin-dollar/blob/bf4ff28d5944ecc277e66294fd2c702fee5cd58b/contracts/contracts/vault/VaultCore.sol#L282), but it will [not be deposited to any strategy](https://github.com/OriginProtocol/origin-dollar/blob/bf4ff28d5944ecc277e66294fd2c702fee5cd58b/contracts/contracts/vault/VaultCore.sol#L310-L321). This skews the investment ratio so a higher percentage of *all the other assets* will be moved to the strategies, draining the buffer that should be used for future redemptions.


Consider enforcing configuration of the asset’s default strategy in the `supportAsset` function.


**Update:** *Not fixed. The Origin team states:*



> We’ll keep this the way it is. This won’t lose any funds if it’s not set. The vault still operates without a default strategy (both places it is used, allocating and redeeming check if this is set and skip it if it is not). It is possible that there may be temporary times in DeFi when the Origin Dollar doesn’t trust any lending protocol/strategy, and goes to purely holding assets to increase stability until things settle down.
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

