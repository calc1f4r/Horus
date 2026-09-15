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
solodit_id: 10775
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/origin-dollar-audit/
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

[H02] Valid redemptions may fail

### Overview


The `_calculateRedeemOutputs` and `_redeem` functions in the `VaultCore` contract of the Origin Protocol are responsible for calculating and redeeming the amount of each asset held by the vault. The `_calculateRedeemOutputs` function calculates the amount of each asset to be redeemed based on the total amount held by the vault and strategies, summing the balance of each asset in each strategy without considering the asset’s default strategy. The `_redeem` function then uses the calculated redeem outputs to try to withdraw the total asset balance (across all strategies) from only the asset’s default strategy.

This mismatch between the calculated redeem outputs and the `_redeem` function can cause the redemption process to fail in some scenarios where the protocol has enough liquidity, such as when setting a new default strategy for a given asset without reallocating a sufficient amount from the old default strategy to the new default strategy. To solve this issue, Origin Protocol suggests either using the asset balance in all strategies to pay back the caller, or ensuring that each asset is only invested through its default strategy. However, the team has decided to keep the current system as it is. This is because some yield earning protocols are inherently attackable when users can force OUSD to move funds into and out of them, and allocations into and out of non-default strategies are currently handled by the strategist role. The team is also planning on transitioning this funds allocation to community governance.

### Original Finding Content

The [`_calculateRedeemOutputs` function](https://github.com/OriginProtocol/origin-dollar/blob/bf4ff28d5944ecc277e66294fd2c702fee5cd58b/contracts/contracts/vault/VaultCore.sol#L522) in the `VaultCore` contract calculates the amount of each asset to be redeemed based on the total amount held by the vault and strategies. For the latter, this amount is calculated by summing the balance of each asset in each strategy, without considering whether this strategy is the [asset’s default strategy](https://github.com/OriginProtocol/origin-dollar/blob/bf4ff28d5944ecc277e66294fd2c702fee5cd58b/contracts/contracts/vault/VaultAdmin.sol#L119-L132).


The [`_redeem` function](https://github.com/OriginProtocol/origin-dollar/blob/bf4ff28d5944ecc277e66294fd2c702fee5cd58b/contracts/contracts/vault/VaultCore.sol#L170) uses the calculated redeem outputs, then [iterates through the approved assets](https://github.com/OriginProtocol/origin-dollar/blob/bf4ff28d5944ecc277e66294fd2c702fee5cd58b/contracts/contracts/vault/VaultCore.sol#L195-L214) to try to [withdraw the total asset balance (across all strategies) from *only* the asset’s default strategy](https://github.com/OriginProtocol/origin-dollar/blob/bf4ff28d5944ecc277e66294fd2c702fee5cd58b/contracts/contracts/vault/VaultCore.sol#L204-L213), unless the vault already has a sufficient balance for the redemption.


Since the output ratios include balances held in non-default strategies, and `_redeem` only withdraws from the default strategy, this mismatch may cause the redemption process to fail in some scenarios where the protocol has enough liquidity. This can happen, for instance, when setting a new default strategy for a given asset without reallocating a sufficient amount from the old default strategy to the new default strategy.


Consider using the asset balance in all strategies to pay back the caller, instead of just the default strategy. Alternatively, consider ensuring that each asset is only invested through its default strategy.


**Update:** *Not fixed. The Origin team states:*



> We’ll keep this the way it is. Some yield earning protocols are inherently attackable when users can force OUSD to move funds into and out of them, either from entrance/withdrawal fees or economic attacks. In order to be able to use these, we have to have funds that can’t be deposited to or withdraw under direct user control. The allocations into and out of non-default strategies is currently handled by the strategist role, and we are planning on transitioning this funds allocation to community governance.
> 
>

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

