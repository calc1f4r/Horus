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
solodit_id: 10791
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

[L08] Simplify redeem outputs calculation

### Overview

See description below for full details.

### Original Finding Content

The [calculation](https://github.com/OriginProtocol/origin-dollar/blob/bf4ff28d5944ecc277e66294fd2c702fee5cd58b/contracts/contracts/vault/VaultCore.sol#L522) to split a value into a fair distribution of coins is unnecessarily complicated. In particular, the [total balance of all stablecoins](https://github.com/OriginProtocol/origin-dollar/blob/bf4ff28d5944ecc277e66294fd2c702fee5cd58b/contracts/contracts/vault/VaultCore.sol#L576) is redundant and can be ignored (or set to 1), which makes the calculation easier to reason about, as follows:


* the [`ratio` parameter](https://github.com/OriginProtocol/origin-dollar/blob/bf4ff28d5944ecc277e66294fd2c702fee5cd58b/contracts/contracts/vault/VaultCore.sol#L588) would become the product of the balance and the price (i.e., the value of the asset held in the vault).
* the [`totalOutputRatio` parameter](https://github.com/OriginProtocol/origin-dollar/blob/bf4ff28d5944ecc277e66294fd2c702fee5cd58b/contracts/contracts/vault/VaultCore.sol#L592) could be renamed to `totalValue`, since it represents the value held by the vault.
* the [`factor` parameter](https://github.com/OriginProtocol/origin-dollar/blob/bf4ff28d5944ecc277e66294fd2c702fee5cd58b/contracts/contracts/vault/VaultCore.sol#L595) now corresponds to the fraction of the vault that is being redeemed.
* the [`outputs` parameter](https://github.com/OriginProtocol/origin-dollar/blob/bf4ff28d5944ecc277e66294fd2c702fee5cd58b/contracts/contracts/vault/VaultCore.sol#L597) has the same value as before, but now it can be directly interpreted as the same fraction of each asset balance.


Consider removing the `totalBalance` parameter from the calculation.


**Update:** *Acknowledged. The Origin team states:*



> We’ll keep this the way it is. While it is correct that calculating the total balance of all stablecoins is not a requirement to calculate the outputs, returning that number from the function does provide a considerable gas optimization for the redeem process. Getting the total balance is very expensive, since each strategy needs to check each stablecoin that it supports, and the strategy needs to check each place that it could have assets, and some of the strategies assets are not directly denominated in stables, which require further computation to get the exchange rate. Since we are doing all this work anyway in this output calculation function, we do just extra three adds to sum to a total value here and return it for use outside this function.
> 
>

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

