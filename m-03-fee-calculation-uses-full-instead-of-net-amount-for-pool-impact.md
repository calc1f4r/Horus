---
# Core Classification
protocol: Hyperhyper_2025-03-30
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57746
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Hyperhyper-security-review_2025-03-30.md
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-03] Fee calculation uses full instead of net amount for pool impact

### Overview


The bug report highlights a discrepancy in the `_calcAddLiquidity` function of the Hyperhyperfi protocol. This function calculates the amount of token to be added to a liquidity pool, but there is a mismatch between the amount used for fee calculation and the actual amount added to the pool. This can result in incorrect fee calculations, as the actual pool impact is less than what was used to calculate the fee. The report recommends charging the Liquidity Provider with the total amount added to the pool, including the fee. 

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

[Link](https://github.com/Hyperhyperfi/protocol/blob/212acfdcd4066334ff5ea06ce46b0bbca7ca212f/src/core/pool/facets/LiquidityFacet.sol#L318-L319)

In the `_calcAddLiquidity` function, there exists a discrepancy between the amount used for fee calculation(`_amountIn`) and the actual amount added to the pool(`netAmount`). The issue occurs in the following sequence:

```solidity
// In _calcAddLiquidity:
valueChange = (_amountIn * tokenPrice).toDecimals(tokenDecimals + provDecimals, 18);
(, pFee) = _calcFeeRate(_token, _amountIn, valueChange, baseSetUp.addRemoveLiquidityFee, true);
netAmount = _amountIn - pFee;
```

The `valueChange` is calculated using the full `_amountIn` before any fees are deducted. This value is then used in `_calcFeeRate` to determine the pool's token ratio impact through the `_calcDelta` function.
However, the actual amount being added to the pool is `netAmount` (which is `_amountIn - pFee`).

This creates a mismatch between:

1. The impact assessment used for fee calculation (based on the full amount).
2. The actual impact on the pool (based on net amount after fees).

For example, if a user adds `1000` Token with a 3% fee:

- The fee calculation assesses the pool impact using `1000` Token.
- But only `970` token is actually added to the pool.
- This leads to incorrect fee calculations as the actual pool impact is less than what was used to calculate the fee.

## Recommendations

Charge Liquidity Provider with `_amountIn+pFee`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Hyperhyper_2025-03-30 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Hyperhyper-security-review_2025-03-30.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

