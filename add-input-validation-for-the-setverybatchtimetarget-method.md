---
# Core Classification
protocol: Polygon zkEVM Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21450
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/zkEVM-bridge-Spearbit-27-March.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/zkEVM-bridge-Spearbit-27-March.pdf
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

protocol_categories:
  - bridge

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - Xiaoming90
  - Gerard Persoon
  - Pashov Krum
  - 0xLeastwood
  - Csanuragjain
---

## Vulnerability Title

Add input validation for the setVeryBatchTimeTarget method

### Overview

See description below for full details.

### Original Finding Content

## Severity: Low Risk

**Context:** PolygonZkEVM.sol#L1171-L1176

**Description:**  
The `setVeryBatchTimeTarget` method in `PolygonZkEVM` accepts a `uint64` `newVeryBatchTimeTarget` argument to set the `veryBatchTimeTarget`. This variable has a value of 30 minutes in the initialize method, so it is expected that it shouldn’t hold a very big value as it is compared to timestamps difference in `_updateBatchFee`. Since there is no upper bound for the value of the `newVeryBatchTimeTarget` argument, it is possible (for example, due to fat-fingering the call) that an admin passes a big value (up to `type(uint64).max`) which will result in wrong calculation in `_updateBatchFee`.

**Recommendation:**  
Add a sensible upper bound for the value of `newVeryBatchTimeTarget`, for example, 1 day.

**Polygon-Hermez:** Solved in PR 88.  
**Spearbit:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Polygon zkEVM Contracts |
| Report Date | N/A |
| Finders | Xiaoming90, Gerard Persoon, Pashov Krum, 0xLeastwood, Csanuragjain |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/zkEVM-bridge-Spearbit-27-March.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/zkEVM-bridge-Spearbit-27-March.pdf

### Keywords for Search

`vulnerability`

