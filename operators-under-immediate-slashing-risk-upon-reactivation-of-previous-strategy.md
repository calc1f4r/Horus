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
solodit_id: 53555
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

Operators Under Immediate Slashing Risk Upon Reactivation Of Previous Strategy

### Overview

See description below for full details.

### Original Finding Content

## Description

The current implementation of strategy management in operator sets may expose operators to immediate slashing risk when strategies are removed and subsequently re-added.

In the `AllocationManager`, strategies can be added to or removed from operator sets dynamically. Operators allocate their stake to these strategies, and these allocations are subject to slashing conditions. The protocol implements a delay for new allocations to become effective:

```solidity
AllocationManager.sol::modifyAllocations()
allocation.effectBlock = uint32(block.number) + operatorAllocationDelay;
```

However, when a strategy is removed from an operator set and later re-added, the existing allocations associated with that strategy become immediately slashable upon reactivation. This is because operators maintain historical allocation records even after strategy removal.

The standard allocation delay only applies to new allocations, so this behavior upon reactivation contrasts with the delay applied to new allocations and may not align with operators' expectations, potentially resulting in unfair penalties for operators who may not have had sufficient time to adjust their allocations after a strategy's reactivation.

## Recommendations

Consider a delay mechanism for strategy activation when adding or re-adding strategies to operator sets.

## Resolution

The EigenLayer team has acknowledged this issue with the following comment:

> "We’re aware of this, but feel adding yet another delay mechanism is more trouble than it’s worth. This is documented as expected behavior in our contract docs."

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

