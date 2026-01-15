---
# Core Classification
protocol: XPress
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 56817
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/XPress/Liquidity%20Vault/README.md#1-insecure-liquidity-valuation-with-oracle-updates
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


This bug report is about a problem found in the `addLiquidity` and `removeLiquidity` functions of the `LPManager` contract. The issue is that users can take advantage of sudden changes in prices to make a profit by supplying and removing liquidity in a single transaction. This is a critical problem because it can result in significant losses for the protocol. The recommended solution is to introduce a system of price epochs and update the minimum and maximum prices every time liquidity is added or removed. This will help prevent sudden price manipulations and protect the protocol from potential attacks.

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
| Protocol | XPress |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/XPress/Liquidity%20Vault/README.md#1-insecure-liquidity-valuation-with-oracle-updates
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

