---
# Core Classification
protocol: Ammplify
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63178
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/1054
source_link: none
github_link: https://github.com/sherlock-audit/2025-09-ammplify-judging/issues/465

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
finders_count: 12
finders:
  - x15
  - panprog
  - globalace
  - neeloy
  - 0xnija
---

## Vulnerability Title

H-12: Missing width scaling in FeeWalker.up (non-visited) undercredits compounding maker fees

### Overview


The bug report discusses an issue found in a code related to compounding maker fees in a financial system. The problem is caused by inconsistent units, where the applied compounding quantity in the non-visited path is not scaled properly. This results in undercrediting compounding makers on non-visited nodes, causing a decrease in user yield and future principal. The suggested mitigation is to multiply by width in the non-visited path to match the logic used in the visited path. 

### Original Finding Content


Source: https://github.com/sherlock-audit/2025-09-ammplify-judging/issues/465 

## Found by 
0xnija, SOPROBRO, anonymousjoe, blockace, globalace, hjo, holtzzx, maigadoh, neeloy, panprog, thimthor, x15

## Summary
In `FeeWalker.up` when `visit == false`, the code credits compounding maker fees using `compoundingLiq = mLiq - ncLiq` without multiplying by `key.width()`, while the per-column rate denominator (`totalMLiq`) includes width scaling. This undercredits compounding makers on non-visited nodes compared to the visited path which correctly uses `width * (mLiq - ncLiq)`.


## Root Cause
Inconsistent units—column rates are per column-liquidity (width-scaled), but the applied compounding quantity in the non-visited path is not width-scaled.

Link (non-visited path):
https://github.com/sherlock-audit/2025-09-ammplify/blob/main/Ammplify/src/walkers/Fee.sol#L249-L267

```solidity
// We charge/pay our own fees.
node.fees.takerXFeesPerLiqX128 += colTakerXRateX128;
node.fees.takerYFeesPerLiqX128 += colTakerYRateX128;
node.fees.makerXFeesPerLiqX128 += colMakerXRateX128;
node.fees.makerYFeesPerLiqX128 += colMakerYRateX128;
// We round down to avoid overpaying dust.
uint256 compoundingLiq = node.liq.mLiq - node.liq.ncLiq; // vulnerable: missing * key.width()
node.fees.xCFees = add128Fees(
    node.fees.xCFees,
    FullMath.mulX128(colMakerXRateX128, compoundingLiq, false),
    data,
    true
);
node.fees.yCFees = add128Fees(
    node.fees.yCFees,
    FullMath.mulX128(colMakerYRateX128, compoundingLiq, false),
    data,
    false
);
```

Contrast (visited path correct):
https://github.com/sherlock-audit/2025-09-ammplify/blob/main/Ammplify/src/walkers/Fee.sol#L418-L424

```solidity
uint256 compoundingLiq = width * (node.liq.mLiq - node.liq.ncLiq);
node.fees.xCFees = add128Fees(
    node.fees.xCFees,
    FullMath.mulX128(colMakerXRateX128, compoundingLiq, false),
    data,
    true
);
```


## Attack Path
 Undercredited compounding makers at non-visited nodes

1. Provide compounding maker liquidity such that the node is charged in the propagation (non-visited) path (common during walks up ancestors where `visit == false`).
2. Trigger walks frequently; accrued compounding fees into `xCFees/yCFees` are undercounted due to missing `width` multiplier.
3. No downstream normalization exists; `xCFees/yCFees` are later used directly for earnings and compounding.


## Impact
- Makers are underpaid on non-visited nodes; compounding growth is reduced. The shortfall scales with node width (e.g., width=8 → ~87.5% undercredit for that node’s compounding portion), causing material loss of user yield and future principal via compounding.


## Mitigation
- Multiply by width in the non-visited path to match visited-path logic:
  - `uint256 compoundingLiq = uint256(key.width()) * (node.liq.mLiq - node.liq.ncLiq);`




### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Ammplify |
| Report Date | N/A |
| Finders | x15, panprog, globalace, neeloy, 0xnija, blockace, thimthor, holtzzx, anonymousjoe, hjo, maigadoh, SOPROBRO |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-09-ammplify-judging/issues/465
- **Contest**: https://app.sherlock.xyz/audits/contests/1054

### Keywords for Search

`vulnerability`

