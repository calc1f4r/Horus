---
# Core Classification
protocol: yAxis
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42361
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-11-yaxis
source_link: https://code4rena.com/reports/2021-11-yaxis
github_link: https://github.com/code-423n4/2021-11-yaxis-findings/issues/31

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

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[H-02] CDP.sol update overwrites user's credit on every positive increment

### Overview


The report highlights a bug in a function called "update" within the CDP.sol file in the Yaxis project. This function is meant to decrease debt and increase credit over time, but due to a mistake in the code, the credit is overwritten each time the function is called instead of being incremented. This means that the credit will never accurately reflect the amount earned over time and will always be overwritten with a small value. The impact of this bug is significant as it affects every user's credit and can lead to incorrect information being displayed. The recommended mitigation step is to change the code to increment the credit instead of overwriting it. There was some discussion and clarification on the issue, and it was ultimately confirmed as a valid bug.

### Original Finding Content

_Submitted by harleythedog_

#### Impact

Within `CDP.sol` (<https://github.com/code-423n4/2021-11-yaxis/blob/main/contracts/v3/alchemix/libraries/alchemist/CDP.sol>) there is a function called update. This function slowly decreases the debt of a position as yield is earned, until the debt is fully paid off, and the idea is then that the credit should begin incrementing as more yield is accumulated. However, the current logic to increment the totalCredit is this line of code (line 39 of `CDP.sol`):

`\_self.totalCredit = \_earnedYield.sub(\_currentTotalDebt);`

Notice that that each time update is called, this overwrites the previous totalCredit with the incremental credit accumulated. The line should instead be:

`\_self.totalCredit = \_self.totalCredit.add(\_earnedYield.sub(\_currentTotalDebt));`

Indeed, look at the function `getUpdatedTotalCredit`, it returns the value:

`\_self.totalCredit + (\_unclaimedYield - \_currentTotalDebt);`

So it is obviously intended that the `totalCredit` should keep increasing over time instead of being overwritten on each update with a small value. The impact of this issue is large - the credit of every position will always be overwritten and the correct information will be lost forever. User's credit should grow over time, but instead it is overwritten with a small value every time update is called.

#### Proof of Concept

See line 39 in `CDP.sol` here: <https://github.com/code-423n4/2021-11-yaxis/blob/main/contracts/v3/alchemix/libraries/alchemist/CDP.sol#:~:text=_self.totalCredit%20%3D%20_earnedYield.sub(_currentTotalDebt)%3B>

#### Tools Used

Manual inspection.

#### Recommended Mitigation Steps

Change code as described above to increment `totalCredit` instead of overwrite it.

**[Xuefeng-Zhu (yAxis) disputed](https://github.com/code-423n4/2021-11-yaxis-findings/issues/31#issuecomment-985278604):**
 > If there is debt, the credit should be zero 

**[0xleastwood (judge) commented](https://github.com/code-423n4/2021-11-yaxis-findings/issues/31#issuecomment-998542307):**
 > It seems like if `_self.totalDebt` is already zero and yield has been earned by the protocol, `_self.totalCredit` will be overwritten. This doesn't seem ideal, could you clarify why the issue is incorrect?

**[0xleastwood (judge) commented](https://github.com/code-423n4/2021-11-yaxis-findings/issues/31#issuecomment-998543262):**
 > If I'm not mistaken, yield can be earned from a positive credit (net 0 debt) position.

**[Xuefeng-Zhu (yAxis) commented](https://github.com/code-423n4/2021-11-yaxis-findings/issues/31#issuecomment-999386020):**
 > @0xleastwood `totalCredit ` is 0 if there is debt

**[0xleastwood (judge) commented](https://github.com/code-423n4/2021-11-yaxis-findings/issues/31#issuecomment-999923125):**
 > After chatting to @Xuefeng-Zhu in Discord, he was able to confirm the issue as valid. So keeping it as is.



 


### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | yAxis |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-11-yaxis
- **GitHub**: https://github.com/code-423n4/2021-11-yaxis-findings/issues/31
- **Contest**: https://code4rena.com/reports/2021-11-yaxis

### Keywords for Search

`vulnerability`

