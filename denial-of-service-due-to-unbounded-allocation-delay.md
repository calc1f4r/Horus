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
solodit_id: 53554
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

Denial Of Service Due To Unbounded Allocation Delay

### Overview

See description below for full details.

### Original Finding Content

## Description

The `setAllocationDelay()` function does not enforce a maximum delay value, allowing operators to set an extremely long delay that prevents any allocations from being set.

## AllocationManager.sol::_setAllocationDelay()

```solidity
function _setAllocationDelay(address operator, uint32 delay) internal {
    AllocationDelayInfo memory info = _allocationDelayInfo[operator];
    
    // If there is a pending delay that can be applied now, set it
    if (info.effectBlock != 0 && block.number >= info.effectBlock) {
        info.delay = info.pendingDelay;
        info.isSet = true;
    }
    
    info.pendingDelay = delay;
    info.effectBlock = uint32(block.number) + ALLOCATION_CONFIGURATION_DELAY + 1;
    _allocationDelayInfo[operator] = info;
    emit AllocationDelaySet(operator, delay, info.effectBlock);
}
```

An operator could set an extremely large delay (up to `MAX_UINT32` blocks, or 1634 years), which would cause the `allocation.effectBlock` calculation in `modifyAllocations()` to overflow:

## AllocationManager.sol::modifyAllocations()

```solidity
else if (allocation.pendingDiff > 0) {
    // ...
    // @audit allocation.effectBlock is uint32, so this can revert from overflow if the delay is too large
    allocation.effectBlock = uint32(block.number) + operatorAllocationDelay;
}
```

This would cause all allocation increases to the operator to revert from an overflow.

## Recommendations

Add an upper bound check in the `setAllocationDelay()` function to prevent unreasonably large delays.

## Resolution

The EigenLayer team has acknowledged this issue with the following comment:

> "We've deemed adding a reasonable upper bound to be more than it's worth. We expect operators to be responsible about the way they modify their allocations."

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

