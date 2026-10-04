---
# Core Classification
protocol: Voltz Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60618
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/voltz-protocol/8d0969db-1d24-4744-b1a7-789701ce2c0e/index.html
source_link: https://certificate.quantstamp.com/full/voltz-protocol/8d0969db-1d24-4744-b1a7-789701ce2c0e/index.html
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
  - Poming Lee
  - Roman Rohleder
  - Kacper Bąk
---

## Vulnerability Title

Incorrect Trigger Condition for `checkPositionMarginAboveRequirement()`

### Overview


The bug report is about a function called `checkPositionMarginAboveRequirement()` in the `MarginEngine.sol` file. This function is supposed to check the required margin when a user adds or removes liquidity from their position. However, the function is currently only checking when liquidity is added, and not when it is removed. This could lead to a loss of funds on the platform. The team has recommended changing the condition to ensure that the required margin is checked in both scenarios.

### Original Finding Content

**Update**
The team explained that they want to check the position margin requirement only after a mint (scenario where the liquidity delta is positive) since in that scenario the LP is effectively agreeing to enter into future swaps that cross their active tick range. Burning liquidity means the position will not enter into future swaps (will have no active liquidity in the respective tick range), however their past positions will still mean that they need to have sufficient margin to support them.

**File(s) affected:**`MarginEngine.sol`

**Description:** On `L409` in `MarginEngine.sol`, the function `checkPositionMarginAboveRequirement()` is invoked when the caller is trying to add some liquidity (i.e., when `params.liquidityDelta > 0`) to their `position` instead of when the liquidity gets removed (i.e., when `params.liquidityDelta < 0`). Failing to correctly check the required margin could lead to un-recoverable fund loss on the platform.

**Recommendation:** We recommend changing the condition.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Voltz Protocol |
| Report Date | N/A |
| Finders | Poming Lee, Roman Rohleder, Kacper Bąk |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/voltz-protocol/8d0969db-1d24-4744-b1a7-789701ce2c0e/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/voltz-protocol/8d0969db-1d24-4744-b1a7-789701ce2c0e/index.html

### Keywords for Search

`vulnerability`

