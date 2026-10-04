---
# Core Classification
protocol: Snailbrook
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35394
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-04-08-SnailBrook.md
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
  - Zokyo
---

## Vulnerability Title

Missing zero address check for the constructor of `PearlPointsCalculator` & `StakingReardsManager`

### Overview

See description below for full details.

### Original Finding Content

**Severity**: Low

**Status**: Resolved

**Description**

In the contract PearlPointsCalculator.sol, there is missing zero address check for `stakingManager` in constructor. Given that `stakingManager` is immutable, if it is accidentally set to zero address, it cannot be changed again.

Similarly, in `StakingRewardsManager.sol`, there is missing zero address check for token & configurator in the constructor. This can lead to token and configurator accidentally set to zero address as well, and cannot be set again.

**Recommendation**: 

It is advised to add a zero address check for 
1) stakingManager in the constructor() of PearlPointsCalculator.sol 
2) token & configurator in the constructor() of StakingRewardsManager.sol

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Snailbrook |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-04-08-SnailBrook.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

