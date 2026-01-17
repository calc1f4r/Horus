---
# Core Classification
protocol: EigenLayer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53552
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Layr_Labs_EigenLayer_Slashing_Security_Assessment_Report_v2_0.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Layr_Labs_EigenLayer_Slashing_Security_Assessment_Report_v2_0.pdf
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

getMinimumSlashableStake() Does not Account For Removed Strategies

### Overview

See description below for full details.

### Original Finding Content

## Description

The `getMinimumSlashableStake()` function in the `AllocationManager.sol` does not validate whether a given strategy is currently part of the operator set, potentially returning inaccurate values if strategies are removed from the set after initial inclusion.

Operator sets are dynamic entities that can have strategies added or removed over time by AVSs. The `removeStrategiesFromOperatorSet()` function allows for the removal of strategies from an operator set. However, the `getMinimumSlashableStake()` function does not account for these potential changes when calculating the minimum slashable stake for an operator.

`getMinimumSlashableStake()` iterates through all strategies provided as input, regardless of whether they are still part of the active operator set. This approach can lead to the inclusion of strategies that are no longer part of the active operator set in the calculation, resulting in an inflated or otherwise incorrect minimum slashable stake value.

## Code Snippet

```solidity
AllocationManager.sol::getMinimumSlashableStake()
for (uint256 j = 0; j < strategies.length; j++) {
    // @audit no check for strategy being part of operator set
    IStrategy strategy = strategies[j];
    // Fetch the max magnitude and allocation for the operator/strategy.
    // Prevent division by 0 if needed. This mirrors the "FullySlashed" checks
    // in the DelegationManager
    uint64 maxMagnitude = _maxMagnitudeHistory[operator][strategy].latest();
    if (maxMagnitude == 0) {
        continue;
    }
    Allocation memory alloc = getAllocation(operator, operatorSet, strategy);
    // ...
    slashableStake[i][j] = delegatedStake[i][j].mulWad(slashableProportion);
}
```

Once a strategy is removed from an operator set, the operator is no longer slashable for that strategy. Therefore, it is misleading to include the slashable stake as part of `getMinimumSlashableStake()`.

## Recommendations

The `getMinimumSlashableStake()` function should be modified to only consider strategies that are currently part of the active operator set. This can be achieved by validating that the strategy is part of the operator set, similar to the validation performed in `slashOperator()`, and reverting with the error `StrategyNotInOperatorSet()`.

## Resolution

The EigenLayer team has acknowledged this issue with the following comment:

"AVSs are the primary user of this method. They are expected to know which strategies are configured to be a part of the operator set."

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | EigenLayer |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Layr_Labs_EigenLayer_Slashing_Security_Assessment_Report_v2_0.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Layr_Labs_EigenLayer_Slashing_Security_Assessment_Report_v2_0.pdf

### Keywords for Search

`vulnerability`

