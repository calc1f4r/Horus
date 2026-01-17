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
solodit_id: 45801
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

Missing Validation for Claiming More than Available Balance (ChestRewards.claimRewards())

### Overview

See description below for full details.

### Original Finding Content

**Severity**: Low

**Status**: Acknowledged

**Description**: 

In the ChestRewards contract, the claimRewards() function does not verify that the contract has enough balance to fulfill the user’s reward claim. The function calls safeTransfer() directly, which may fail if the contract holds insufficient tokens.

**Scenario**: 

Multiple users attempt to claim their rewards, but the contract's balance is insufficient. Users experience transaction failures and incur gas fees without receiving any rewards.

**Recommendation**: 

Before executing safeTransfer(), add a check to ensure the contract holds enough tokens to fulfill the claim (require(goldRewardToken.balanceOf(address(this)) >= rewards, "Not enough tokens to fulfill claim")).

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

