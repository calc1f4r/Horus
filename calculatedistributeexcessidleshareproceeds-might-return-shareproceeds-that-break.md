---
# Core Classification
protocol: Hyperdrive March 2024
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35928
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Delv-Spearbit-Security-Review-March-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Delv-Spearbit-Security-Review-March-2024.pdf
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
finders_count: 4
finders:
  - Saw-Mon and Natalie
  - Christoph Michel
  - Deivitto
  - M4rio.eth
---

## Vulnerability Title

calculateDistributeExcessIdleShareProceeds might return shareProceeds that break LP price invariant

### Overview


This bug report discusses a problem with the code in LPMath.sol related to calculating withdrawal shares in a function called calculateDistributeExcessIdle. The issue arises when the withdrawal shares are greater than the total outstanding shares, causing the function to use a more complex method to find a solution. However, this method may not always work, leading to incorrect results and breaking the intended behavior of the code. The report suggests adding a check to ensure the calculated value is close to a solution before returning it, and also proposes a new function to handle these cases. The bug has been fixed in a recent code update.

### Original Finding Content

## Severity: Medium Risk

## Context
- `LPMath.sol#L583-L610`
- `LPMath.sol#L928`

## Description
Step 3 of `calculateDistributeExcessIdle` computes the withdrawal shares `dw` that can be removed along with removing `dz_max` vault shares to keep the LP price \( \frac{PV}{L} \) constant. If the withdrawal shares `dw` are more than the total outstanding withdrawal shares `w`, the inverse problem of finding `dz` given `w` is solved in step 4.

Solving this problem is harder, and Newton's method is used to solve \( F(dz) = 0 \) with 

\[
F(dz) = PV(dz) - PV(0) - (l - w).
\]

A fixed number of `SHARE_PROCEEDS_MAX_ITERATIONS` iterations is used, and `calculateDistributeExcessIdleShareProceeds` can return a `dz` that is not the solution, and therefore does not keep the LP price constant, breaking the invariant.

## Recommendation
Before returning the `shareProceeds` value at the end of the function, consider checking that this value is indeed close to a solution of \( F(dz) \); otherwise, return `0`. Consider adding a public `distributeExcessIdle` function taking off-chain computed `(dz, dw)` parameters that preserve the invariant, in case the current `SHARE_PROCEEDS_MAX_ITERATIONS` are not sufficient and the withdrawal shares redemptions are stuck.

## Delv
Fixed in PR 925.

## Spearbit
Fixed. Tolerance is not checked for the `calculateDistributeExcessIdleShareProceedsNetLongEdgeCaseSafe`, but that's ok given: The invariant \( \frac{PV}{L} \) should stay the same up to division errors due to how \( dz \) gets calculated in `calculateDistributeExcessIdleShareProceedsNetLongEdgeCaseSafe`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Hyperdrive March 2024 |
| Report Date | N/A |
| Finders | Saw-Mon and Natalie, Christoph Michel, Deivitto, M4rio.eth |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Delv-Spearbit-Security-Review-March-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Delv-Spearbit-Security-Review-March-2024.pdf

### Keywords for Search

`vulnerability`

