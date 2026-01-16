---
# Core Classification
protocol: Stader Labs
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53698
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/stader/sd-pool/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/stader/sd-pool/review.pdf
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
  - Sigma Prime
---

## Vulnerability Title

Fee Accounting Rounding Favours Users Over Protocol

### Overview


The report discusses a bug in the `accrueFee()` function that leads to rounding errors, resulting in the accrual of bad debt over time. This is caused by the use of integer division in the calculation of fees, which can lead to discrepancies between the total fees accrued and the fees accrued by individual users. To fix this, it is recommended to round up the accruing of fees to `utilizeIndex` and make adjustments to the `_repay()` function. This issue has been resolved in the latest commit `21ba418`.

### Original Finding Content

## Description
Rounding errors in `accrueFee()` may result in accrual of bad debt over time. Inside the `accrueFee()` function, fees are accrued by scaling both `totalUtilizedSD` and `utilizeSD` up by the `simpleFeeFactor`.

```c
/*
* Calculate the fee accumulated into utilized and totalProtocolFee and the new index:
* simpleFeeFactor = utilizationRate * blockDelta
* feeAccumulated = simpleFeeFactor * totalUtilizedSD
* totalUtilizedSDNew = feeAccumulated + totalUtilizedSD
* totalProtocolFeeNew = feeAccumulated * protocolFeeFactor + totalProtocolFee
* utilizeIndexNew = simpleFeeFactor * utilizeIndex + utilizeIndex
*/
```

```c
uint256 simpleFeeFactor = utilizationRatePerBlock * blockDelta;
uint256 feeAccumulated = (simpleFeeFactor * totalUtilizedSD) / DECIMAL;
totalUtilizedSD += feeAccumulated;
accumulatedProtocolFee += (protocolFee * feeAccumulated) / DECIMAL;
utilizeIndex += (simpleFeeFactor * utilizeIndex) / DECIMAL;
```

Since `utilizeIndex` < `totalUtilized`, there is a small discrepancy between the total amount of fees that accrue to `totalUtilizedSD` and the amount of fees that accrue to each utilizer via `utilizeIndex`, which results in rounding errors from integer division. Due to this behaviour, utilizers end up paying less interest than recorded (and claimable by delegators), potentially resulting in bad debt.

## Recommendations
Although the rounding error is minimal, it is still preferable for any rounding to favour the protocol over users. Consider rounding up the accruing of fees to `utilizeIndex` and calculations of utilizer balances. If this is done, then the `_repay()` function needs to be adjusted to account for potential underflow scenarios. An example of what the `_repay()` adjustment may look like:

```c
utilizerData[utilizer].principal = accountUtilizedPrev - repayAmountFinal;
utilizerData[utilizer].utilizeIndex = utilizeIndex;
totalUtilizedSD = totalUtilizedSD > repayAmountFinal ? totalUtilizedSD - repayAmountFinal : 0;
emit Repaid(utilizer, repayAmountFinal);
```

## Resolution
Calculation of `utilizeIndex` was modified to round up and `_repay()` was modified according to the recommendations. This issue has been addressed in commit `21ba418`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Stader Labs |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/stader/sd-pool/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/stader/sd-pool/review.pdf

### Keywords for Search

`vulnerability`

