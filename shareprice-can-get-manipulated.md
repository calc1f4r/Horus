---
# Core Classification
protocol: Copra
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37577
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-23-Copra.md
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
  - Zokyo
---

## Vulnerability Title

`SharePrice` can get manipulated

### Overview


This bug report describes a critical issue in the `CurveLiquidityWarehouse.sol` contract where an attacker can manipulate the price of a LP share by front-running a legitimate transaction. This can result in an inflated or uninflated price for the share. The recommended solution is to calculate the amount of LP tokens to be burned off-chain to avoid price manipulation. The auditor has also suggested a partial mitigation fix by using two different oracles and checking for deviations in the spot price. However, the risk of vulnerabilities still remains and it is recommended to use off-chain mechanisms or external oracles to prevent manipulation.

### Original Finding Content

**Severity**: Critical	

**Status**: Acknowledged

**Description**

The `_withdrawFromTarget` function in the `CurveLiquidityWarehouse.sol` contract calculates the theoric price for a LP share relying on the spot price of the curve pool.

```solidity
uint256 sharePrice = curveStableSwapPool.calc_withdraw_one_coin(10 ** (withdrawTargetDecimals), curvePoolCoinIdx);
```

The `calc_withdraw_one_coin` function from the Curve’s StableSwap pool calculates the amount received when withdrawing a single coin. The amount returned from this function is calculated on chain; it works by retrieving the spot price from a pool which can lead to a price manipulation by an attacker. Once the transaction is pending in the mempool an attacker can front-run this legit transaction and submit a transaction to the curve pool that manipulates the price that is going to be returned by this function leading to getting an inflated or uninflated price for `sharePrice`.

**Recommendation**:

`sharePrice` is used to calculate `burnAmt` which represents the amount of LP tokens that needs to get burnt in order to withdraw `withdrawAmount` from the asset. Instead of calculating `burnAmt` on chain add a parameter representing this amount calculated of-chain to avoid price manipulation.

**Zokyo Auditor’s Comment**: 

Added a partial, but not complete, mitigation fix that involves retrieving the pool price from two different oracles, one of them using EMA, and checking if its deviation is within a dynamic threshold compared with the spot price, needing a larger amount of funds to manipulate. However, the risk of vulnerabilities has not been 100% mitigated, as it should not rely on on-chain manipulable calculations, but instead use off-chain mechanisms or rely on External oracles like Chainlink, pyth etc.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Copra |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-23-Copra.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

