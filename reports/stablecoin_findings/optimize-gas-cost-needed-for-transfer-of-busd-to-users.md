---
# Core Classification
protocol: Dpnmdefi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44547
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-03-13-DPNMDEFI.md
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

Optimize gas cost needed for transfer of busd to users

### Overview

See description below for full details.

### Original Finding Content

**Severity**: Low

**Status**: Acknowledged

**Description**

dpnm_sc.sol - in depositBonus Issue is similar to Transfer of busd to same recipient is unnecessarily repeated in loops, but it is dealt with in a different way. Method depositBonus includes busd.safeTransfer(userAddress, ...). Mehtod depositBonus is repeated in loops in the implementations of _TreePayment and depositBonusFordPNMBuy.

**Recommendation** 

This kind of use case is mostly implemented in the following way in DeFi:
Instead of transferring the busd right away, add the amount of reward to be paid for the users in a mapping state variable like:
mapping(address => uint256) bonusToBePaid;

while the actual busd rewards (i.e., bonuses) are sent as a whole to a reward pool (or the same contract). Users later claim their rewards from the reward pool in a separate transaction triggered by them, like this:
bonusToBePaid[userAddress] -= amount;
rewardPool.safeTransferBUSDBonusTo(userAddress, amount);

**Fix**: Developers acknowledged the issue and they showed their awareness about it. They preferred accessibility for users (i.e. simplicity to deal with their ecosystem) than following the more common practice.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Dpnmdefi |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-03-13-DPNMDEFI.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

