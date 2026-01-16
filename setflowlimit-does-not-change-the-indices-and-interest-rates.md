---
# Core Classification
protocol: Astera
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62284
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astera-Spearbit-Security-Review-December-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astera-Spearbit-Security-Review-December-2024.pdf
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
finders_count: 3
finders:
  - Saw-mon and Natalie
  - Cergyk
  - Jonatas Martins
---

## Vulnerability Title

setFlowLimit does not change the indices and interest rates

### Overview


This report is about a bug in a code called MiniPoolAddressProvider. The bug is of medium risk and can cause problems with the virtual available liquidity. This means that when the flow limit of a reserve is changed, the interest rates and indices for that reserve in the mini pool should also be updated. However, this is not happening, and it is recommended that when the `setFlowLimit` function is called, the interest rates and indices should be updated as well. The bug has been fixed in a commit called `696a5fa4` and has been verified by a company called Spearbit.

### Original Finding Content

## Security Advisory

## Severity
**Medium Risk**

## Context
`MiniPoolAddressProvider.sol#L349-L355`

## Description
Changing the flow limit of a reserve in a mini pool affects its virtual available liquidity. Therefore, it is essential to update the interest rates and the indices for that reserve in the mini pool. 

Additionally, setting the flow limit to a non-zero value or resetting it to 0 can trigger the calculation of the minimum liquidity rate. This adds another reason why calling `setFlowLimit` should trigger an update of the interest rates and indices.

## Recommendation
Ensure that when `setFlowLimit` is called, the indices and interest rates are updated accordingly.

## Status
- **Astera**: Fixed in commit `696a5fa4`.
- **Spearbit**: Fix verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Astera |
| Report Date | N/A |
| Finders | Saw-mon and Natalie, Cergyk, Jonatas Martins |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astera-Spearbit-Security-Review-December-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astera-Spearbit-Security-Review-December-2024.pdf

### Keywords for Search

`vulnerability`

