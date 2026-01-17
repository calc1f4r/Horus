---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19461
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/lido/lido-easy-track/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/lido/lido-easy-track/review.pdf
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

EasyTrack Gas Saving Considerations

### Overview

See description below for full details.

### Original Finding Content

## Description

This section details findings relating to gas savings or optimizations which do not have direct security implications:

1. There is on-chain reason for `objectionsAmountPct` to be saved to storage (it’s recalculated each time, and the stored value is never used).  
   Though it may be useful to off-chain users via `getMotion`. Consider removing it from the Motion struct to save on storage gas fees.

2. It is possible to make large storage cost savings by storing the majority of the Motion struct on-chain as a hash only. While `objectionsAmount` changes regularly and should be stored on-chain, the remaining fields are immutable (not changing for the life of the motion) and could feasibly be condensed into a hash.  
   These values would need to be passed as parameters during relevant function calls, and compared against the stored hash to verify them.  
   While this would save on gas, it may be a problematic user experience for those now needing knowledge of the historical state in order to object. Data availability issues may also be a consideration.  
   A middle ground could also be considered, where some values are stored on-chain for improved data availability and user experience, but others are kept only in the hash.

3. It is unnecessary to create the EVM script during `enactMotion()`. It may be preferable and cheaper to pass the entire script as a parameter and validate it against the stored hash.  
   Note that an external call to the factory may still be needed if it’s possible for the creator to no longer be authorized by the factory (where it was allowed to create a script at the time of `createMotion()` but not later).

4. It would be more gas efficient to avoid checking the permissions for an EVM script in `enactMotion()`, and instead simply check the script against the stored hash (a hash collision should be infeasible).  
   There would be some complications, however, in safely handling factories that have been removed (or removed and re-added with different permissions) since the motion was created. This may be possible by storing with each factory the timestamp or block number when it was added (or its permissions had last changed).

5. Depending on how gas-expensive `totalSupplyAt(snapshotBlock)` is, it may be desirable to cache this in storage.  
   A negative is that the entity saving it to the cache would incur higher gas costs (either the proposer in `createMotion()` or the first objector).  
   Saving it during `createMotion()` also incurs extra gas costs in the common, “happy” scenario in which no objections are raised.

## Recommendations

Ensure that the comments are understood and acknowledged, and consider implementing the suggestions above.

## Resolution

The above comments have been considered and relevant fixes were introduced in PR #6.  
The Lido team have addressed these comments as follows:

1. The `objectionsAmountPct` is no longer saved to storage in the Motion struct.
   
2. This involves large changes to the existing UI, and is inconvenient from a UX perspective. The team will consider relevant changes in more detail in subsequent upgrades.

3. It is important that a factory can validate the script at the point of execution/enactment (as well as when created), to account for state changes such that the script is no longer valid.  
   As an example, “a motion to increase the node operator staking limit might become non-executable if the node operator who created it was removed from the node operators registry after the creation of the motion.”  
   The suggestion to pass the EVMScript as a parameter greatly complicates this validation (and likely makes it infeasible, such that no gas is saved).

4. This has been considered, and the increased logical complexity was deemed to outweigh the potential gas savings.  
   The testing team concurs that a simple implementation is less likely to contain bugs and more easily understood by third parties.

5. The development team intends to design EasyTrack to be used by common, non-controversial proposals which, in the usual “happy” scenario, should have no objections.  
   As such, they prioritize the gas efficiency of motion creation over objection. Similarly, making the first objection more expensive than subsequent ones may introduce minor but undesirable incentives.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Lido |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/lido/lido-easy-track/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/lido/lido-easy-track/review.pdf

### Keywords for Search

`vulnerability`

