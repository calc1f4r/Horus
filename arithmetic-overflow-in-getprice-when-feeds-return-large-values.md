---
# Core Classification
protocol: NUTS Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62694
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/NUTS%20Finance/Pike/README.md#1-arithmetic-overflow-in-getprice-when-feeds-return-large-values
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

Arithmetic Overflow in `getPrice` When Feeds Return Large Values

### Overview


The `ChainlinkOracleComposite` contract has a bug in its `getPrice` function. This causes the contract to freeze if a feed reports a price higher than $100,000, resulting in all contracts that depend on this oracle to also freeze. To fix this, it is recommended to either use a 512-bit safe-math library or reduce the `SCALING_DECIMALS` value. This issue is classified as high severity as it can affect multiple protocols that use this oracle.

### Original Finding Content

##### Description
This issue has been identified within the `getPrice` function of the `ChainlinkOracleComposite` contract. 

`getPrice` normalises each feed answer and then multiplies the current composite price by that rate:

```solidity
rate = uint256(price) 
     * 10**(SCALING_DECIMALS - feed.decimals());
compositePrice = (compositePrice * rate) 
               / SCALING_FACTOR; // 36-dec fixed-point
```

If a feed reports `price > 1.16 * 10^(5 + feed.decimals)` (≈ $100 000 when denominated in wei), the term  

```
compositePrice * rate * 10^36
```

exceeds the 256‑bit limit. The call reverts with arithmetic overflow, freezing every contract that depends on this oracle for lending, liquidation, or pricing logic.

The issue is classified as **high** severity because a single inflated data point bricks the entire oracle and all protocols integrated with it. 

##### Recommendation
We recommend either replacing the simple `* /` pair with a 512‑bit safe‑math library such as OpenZeppelin’s `mulDiv` or reducing `SCALING_DECIMALS`.


### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | NUTS Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/NUTS%20Finance/Pike/README.md#1-arithmetic-overflow-in-getprice-when-feeds-return-large-values
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

