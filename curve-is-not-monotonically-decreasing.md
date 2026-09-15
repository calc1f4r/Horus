---
# Core Classification
protocol: Subscription Token Protocol V2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59343
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/subscription-token-protocol-v-2/7ef99de3-7f40-434b-9931-cd91a798940b/index.html
source_link: https://certificate.quantstamp.com/full/subscription-token-protocol-v-2/7ef99de3-7f40-434b-9931-cd91a798940b/index.html
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
finders_count: 3
finders:
  - Valerian Callens
  - Jeffrey Kam
  - Jonathan Mevs
---

## Vulnerability Title

Curve Is Not Monotonically Decreasing

### Overview

See description below for full details.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `852c8d49bd21356bdda907ecd4a2a631857a70c9`.

If the calculated curve multiplier is less than the `minMultiplier`, the `minMultiplier` will be used.

**File(s) affected:**`RewardCurveLib.sol`

**Description:** After a certain time (i.e. `periods > curve.numPeriods`), the curve multiplier will be lower bounded by `minMultiplier`, as indicated by `RewardCurveLib.currentMultiplier()`. However, it is possible that for periods before `curve.numPeriods`, the multiplier calculated using `uint256(curve.formulaBase) ** (curve.numPeriods - periods)` is lower than the `minMultiplier`. This means for some misconfigured curves as described above, there may be undesired cases where a user is incentivized to delay purchasing the subscription due to an expected increase in `currentMultiplier()` in later periods (i.e. when `periods > curve.numPeriods`).

**Recommendation:** Consider taking the max of `uint256(curve.formulaBase) ** (curve.numPeriods - periods);` and `minMultiplier` in the returned value of `currentMultiplier()`. Alternatively, further input validation can be included when creating a curve to ensure that the `minMultiplier` is not greater than the last multiplier applied based on the periods.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Subscription Token Protocol V2 |
| Report Date | N/A |
| Finders | Valerian Callens, Jeffrey Kam, Jonathan Mevs |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/subscription-token-protocol-v-2/7ef99de3-7f40-434b-9931-cd91a798940b/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/subscription-token-protocol-v-2/7ef99de3-7f40-434b-9931-cd91a798940b/index.html

### Keywords for Search

`vulnerability`

