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
solodit_id: 53553
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

Global Deallocation Delay May Not Be Appropriate For Diﬀerent Operator Sets

### Overview

See description below for full details.

### Original Finding Content

## Description
The current implementation of a global `DEALLOCATION_DELAY` in the `AllocationManager` may not adequately address the diverse security requirements of different operator sets. The EigenLayer slashing upgrade introduces the concept of operator sets, which are logical groupings of operators created by AVSs for various tasks and security requirements. Each operator set can have unique slashing conditions and security needs. For instance, an operator set with high-risk, computationally intensive tasks might require a longer deallocation delay compared to a set with simpler, low-risk tasks.

However, the current implementation uses a single, global `DEALLOCATION_DELAY` immutable constant for all operator sets in `AllocationManager`. This may not be appropriate given the varying risk profiles and operational requirements of different sets.

## AllocationManagerStorage.sol
```solidity
/// @notice Delay before deallocations are clearable and can be added back into freeMagnitude
/// In this window, deallocations still remain slashable by the operatorSet they were allocated to.
uint32 public immutable DEALLOCATION_DELAY;
```

## Recommendations
Consider implementing a unique `DEALLOCATION_DELAY` for each operator set to allow for more granular control over security parameters. This can be achieved by extending the `OperatorSet` struct to include a custom `deallocationDelay` field.

## Resolution
The EigenLayer team has acknowledged this issue with the following comment:

> "We agree that a global deallocation delay won’t work for all use-cases. This is a known limitation we’d like to address in a future release."

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

