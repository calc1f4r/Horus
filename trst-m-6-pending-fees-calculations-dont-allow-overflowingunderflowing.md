---
# Core Classification
protocol: Stella
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19058
audit_firm: Trust Security
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-05-29-Stella.md
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

protocol_categories:
  - lending

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Trust Security
---

## Vulnerability Title

TRST-M-6 Pending fees calculations don’t allow overflowing/underflowing

### Overview


This bug report is about the UniswapV3PositionViewer, which is a tool used to compute pending fees. The calculations of **feeGrowthBelowX128**, **feeGrowthAboveX128**, and **feeGrowthInsideX128** in the `_computePendingFeesToBeEarned()` function do not allow under- and overflowing. This can cause transaction reverts.

The recommended mitigation was to wrap the fee growth calculations in **unchecked**, which is what Uniswap does in the 0.8 branch. The team fixed the issue by implementing this mitigation.

In summary, this bug report was about a problem with the UniswapV3PositionViewer, where the calculations of **feeGrowthBelowX128**, **feeGrowthAboveX128**, and **feeGrowthInsideX128** in the `_computePendingFeesToBeEarned()` function did not allow under- and overflowing. This could cause transaction reverts. The team fixed the issue by wrapping the fee growth calculations in **unchecked**.

### Original Finding Content

**Description:**
When computing pending fees in the UniswapV3PositionViewer. 
`_computePendingFeesToBeEarned()` function, the calculations of **feeGrowthBelowX128**, 
**feeGrowthAboveX128**, and **feeGrowthInsideX128** don’t allow under- and overflowing. 
However, the respective calculations in Uniswap V3 are designed to underflow and overflow 
(for more information, refer to https://github.com/Uniswap/v3-core/issues/573 issue and this https://github.com/Jeiwan/uniswapv3-book/issues/45). As a result, executing 
_computePendingFeesToBeEarned() can revert in some situations, causing transaction 
reverts.

**Recommended Mitigation:**
In the `_computePendingFeesToBeEarned()` function, consider wrapping the fee growth 
calculations in **unchecked**. This is what Uniswap does in the 0.8 branch(https://github.com/Uniswap/v3-core/blob/0.8/contracts/libraries/Tick.sol#L69-L97).

**Team response:**
Fixed

**Mitigation Review:**
The team addressed this issue by wrapping the fee growth calculations in **unchecked** in 
`_computePendingFeesToBeEarned()`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Trust Security |
| Protocol | Stella |
| Report Date | N/A |
| Finders | Trust Security |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-05-29-Stella.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

