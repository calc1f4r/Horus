---
# Core Classification
protocol: Heurist
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45799
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-11-04-Heurist.md
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

Missing Validation for Empty Address Inputs (ChestRewards.addRewards() and distribute())

### Overview

See description below for full details.

### Original Finding Content

**Severity**: Low

**Status**: Acknowledged

**Description**: 

In the ChestRewards contract, the addRewards() and distribute() functions do not validate whether the rewardee address is a non-zero address. Adding rewards or distributing them to a zero address will lock the tokens.

**Scenario**: 

The operator accidentally calls addRewards(address(0), 100, RewardType.SILVER), which results in the rewards being assigned to the zero address, effectively locking the tokens and making them unclaimable.

**Recommendation**:

Add a validation check in addRewards(), batchAddRewards(), distribute(), and batchDistribute() to ensure that the rewardee is not a zero address (require(rewardee != address(0), "Invalid rewardee address")).

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Heurist |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-11-04-Heurist.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

