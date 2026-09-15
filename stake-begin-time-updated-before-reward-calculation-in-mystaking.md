---
# Core Classification
protocol: Magic Yearn
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57531
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-08-17-Magic Yearn.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - zokyo
---

## Vulnerability Title

Stake begin time updated before reward calculation in MyStaking.

### Overview


The bug report describes an issue with a function called "stake" in a file called "MyStaking.sol". This function uses another function called "getDivisorByTime" to calculate the amount that can be claimed. However, there is a problem with the variable "stakeBegin" which is used in this calculation. The function "setTimer" is called before the rewards are calculated, which means that "stakeBegin" will be the same for everyone and the commission for users will always be calculated with the maximum fee. 

The recommendation is to update the variable "stakeBegin" after the rewards are calculated. This will ensure that the commission is calculated correctly for each user. The re-audit comment confirms that this issue has been verified. The client also notes that the rewards are saved in a variable called "unclaimedAmount" without the fee subtracted, so users will not lose any funds but they will receive a higher fee than intended.

### Original Finding Content

**Description**

MyStaking.sol: function_stake(). "stakeBegin" is used within the function getDivisorByTime() during the calculation of the claimable amount. Since_setTimer() is called before rewards are calculated (Lines 243-244), "stakeBegin" will be equal for msg.sender and the commission for the user will always be calculated with maximum fee.

**Recommendation**

Update "stakeBegin" after rewards are calculated.

**Re-audit comment**

Verified.

From the client:

The calculated rewards in_stake() are saved in userInfo[msg.sender].unclaimedAmount without the fee subtracted, so the user does not lose funds but the "fee-advantage".

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Magic Yearn |
| Report Date | N/A |
| Finders | zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-08-17-Magic Yearn.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

