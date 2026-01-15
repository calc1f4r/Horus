---
# Core Classification
protocol: Hanji
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55148
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Hanji/Liquidity%20Vault/README.md#1-insecure-liquidity-valuation-with-oracle-updates
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Insecure Liquidity Valuation with Oracle Updates

### Overview


This bug report discusses an issue with the `addLiquidity` and `removeLiquidity` functions in the `LPManager` contract. The problem arises because Pyth oracles can be updated by users in the same transaction, allowing them to exploit sudden price changes for profit. This is classified as a critical issue because it can cause significant losses to the protocol. The report recommends implementing a system of price epochs and updating the minimum and maximum prices at each liquidity action to mitigate this problem.

### Original Finding Content

##### Description
This issue has been identified within the `addLiquidity` and `removeLiquidity` functions of the `LPManager` contract. 

Because Pyth oracles can be updated atomically by users in the same transaction, it is possible to supply liquidity at a low price and subsequently remove it at a higher price, all within a single transaction. This creates an arbitrage opportunity that can rapidly extract value from the protocol.

The issue is classified as **critical** severity because it allows attackers to exploit sudden price changes for profit, potentially causing substantial losses to the protocol.

##### Recommendation
We recommend introducing a system of price epochs with duration equals to `maxOracleAge` and updating the minimum/maximum tracked prices at each `addLiquidity`/`removeLiquidity`. Specifically:
- For `addLiquidity`, use the highest price from the last two epochs to calculate the minted shares.
- For `removeLiquidity`, use the lowest price from the last two epochs to calculate the amount of tokens to transfer.
- Update these historical price bounds every time liquidity is added or removed.

This approach helps mitigate abrupt, short-time price manipulations.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Hanji |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Hanji/Liquidity%20Vault/README.md#1-insecure-liquidity-valuation-with-oracle-updates
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

