---
# Core Classification
protocol: Angle
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19196
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/angle/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/angle/review.pdf
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

Suboptimal Search Iteration

### Overview

See description below for full details.

### Original Finding Content

## Description

Contract Core utilises two address lists, namely `stablecoinList` and `governorList`, to store the list of stablecoins and governors, respectively. To track the existence of a stablecoin or a governor in the mentioned lists, the contract iterates through the lists to get the item index.

For example, line [65-69] in function `deployStableMaster()` indicates an iterative process of finding whether a `StableMaster` contract of an `AgToken` contract has been deployed. This iteration can be expensive in terms of gas usage if `stablecoinList` has a large membership.

Similar types of iteration in the contract can be found in the following functions:
- `deployStableMaster()`, line [65-69]
- `addGovernor()`, line [115-117]
- `setGuardian()`, line [167-169]

Consider the following snippet from line [64-70]:

```solidity
uint256 indexMet = 0;
for (uint256 i = 0; i < stablecoinList.length; i++) {
    if (stablecoinList[i] == stableMaster) {
        indexMet = 1;
    }
}
require(indexMet == 0, "stableMaster already deployed");
```

The `for` iteration in the snippet above always conducts a search from index 0 to `stablecoinList.length`, which is suboptimal.

## Recommendations

The testing team recommends inserting a break after the search data is found:

```solidity
uint256 indexMet = 0;
uint256 listLength = stablecoinList.length;
for (uint256 i = 0; i < listLength; i++) {
    if (stablecoinList[i] == stableMaster) {
        indexMet = 1;
        break;
    }
}
require(indexMet == 0, "stableMaster already deployed");
```

## Resolution

This has been resolved in commit `4cd59ce`. Some search functions within the project were optimised by utilising mappings to access the intended item instantly without iteration. The `break` was also introduced to applicable codes to stop an iteration quickly after a condition is met.

---

## AGL-17 Suboptimal Delete Iteration

**Asset:** contracts/  
**Status:** Resolved: See Resolution  
**Rating:** Informational  

## Description

The contracts have several list item deletion operations, which can be found in the following functions:
- `Core.revokeStableMaster()`, line [89-96]
- `Core.removeGovernor()`, line [138-145]
- `PoolManager.revokeStrategy()`, line [301-328]
- `StableMaster.revokeCollateral()`, line [328-369]
- `RewardsDistributor.removeStakingContract()`, line [154-173]

Consider the following snippet from `Core.sol`, line [88-98]:

```solidity
uint256 indexMet = 0;
for (uint256 i = 0; i < stablecoinList.length - 1; i++) {
    if (stablecoinList[i] == stableMaster) {
        indexMet = 1;
    }
    if (indexMet == 1) {
        stablecoinList[i] = stablecoinList[i + 1];
    }
}
require(indexMet == 1 || stablecoinList[stablecoinList.length - 1] == stableMaster, "incorrect stablecoin");
stablecoinList.pop();
```

The `for` iteration in the snippet above always conducts a search from index 0 to `stablecoinList.length`; if an item is found, then the next items are shifted to the left in order not to leave a gap in the list. This operation uses an excessive amount of gas due to numerous SLOAD operations.

## Recommendations

The testing team recommends swapping the deleted item with the last item if item order is not important. Also, consider a gas optimisation where the length of the list (`listLength`) is cached to reduce the number of SLOAD instructions, which can be applied to all array iterations, not just deletions:

```solidity
uint256 indexMet = 0;
uint256 listLength = stablecoinList.length;
for (uint256 i = 0; i < listLength - 1; i++) {
    if (stablecoinList[i] == stableMaster) {
        stablecoinList[i] = stablecoinList[listLength - 1];
        stablecoinList.pop();
        indexMet = 1;
        break;
    }
}
require(indexMet == 1, "incorrect stablecoin");
```

## Resolution

This has been resolved in commit `2848add`. The deleted item is now swapped with the last item, because the development team considers item order as not important. The list length is now cached whenever possible to reduce SLOAD opcode usage.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Angle |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/angle/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/angle/review.pdf

### Keywords for Search

`vulnerability`

