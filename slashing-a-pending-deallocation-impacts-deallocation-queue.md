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
solodit_id: 53550
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

Slashing A Pending Deallocation Impacts Deallocation Queue

### Overview

See description below for full details.

### Original Finding Content

## Description
When a pending deallocation is slashed, the value of the deallocation may round down to zero. Therefore, an operator is able to call `modifyAllocations()` to update this deallocation. As a result, the `deallocationQueue` may no longer be sorted based on `effectBlock`.

The root cause of the issue is that when `slashOperator()` is called, if there is a pending deallocation, it will be slashed. That slashed amount may result in the `allocation.pendingDiff` rounding down to zero. This will not clear the pending deallocation from the `deallocationQueue`.

## AllocationManager.sol::_slashOperator()
```solidity
if (allocation.pendingDiff < 0) {
    uint64 slashedPending =
        uint64(uint256(uint128(-allocation.pendingDiff)).mulWadRoundUp(params.wadsToSlash[i]));
    allocation.pendingDiff += int128(uint128(slashedPending)); // @audit may be zeroed
    // ...
}
```

Once `allocation.pendingDiff` equals zero, the pending deallocation can be modified as the following check now passes:

## AllocationManager.sol::modifyAllocations()
```solidity
function modifyAllocations(
    address operator,
    AllocateParams[] memory params
) external onlyWhenNotPaused(PAUSED_MODIFY_ALLOCATIONS) {
    // ...
    for (uint256 i = 0; i < params.length; i++) {
        // ...
        for (uint256 j = 0; j < params[i].strategies.length; j++) {
            (StrategyInfo memory info, Allocation memory allocation) =
                _getUpdatedAllocation(operator, operatorSet.key(), strategy);
            // @audit modification no longer counts as pending even though effectBlock has not passed
            require(allocation.pendingDiff == 0, ModificationAlreadyPending());
            // ...
        }
    }
}
```

`allocation.pendingDiff == 0` incorrectly assumes that the allocation has no pending modifications, even though the `allocation.effectBlock` has not passed. Once this allocation is modified, the `allocation.effectBlock` will be set again, resulting in the `deallocationQueue` being unsorted.

An unsorted `deallocationQueue` will result in the `_clearDeallocationQeue()` function not clearing all of the deallocations in the queue. `getAllocatableMagnitude()` will also incorrectly calculate the return value as it discounts deallocations.

## Recommendations
Consider changing the function `modifyAllocations()` to check for pending modifications based on `allocation.effectBlock` instead of `allocation.pendingDiff`.

## Resolution
The EigenLayer team has implemented the recommended fix above. This issue has been resolved in PR #1052.

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

