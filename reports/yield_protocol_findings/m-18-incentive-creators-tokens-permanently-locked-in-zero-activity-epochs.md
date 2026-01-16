---
# Core Classification
protocol: Debita Finance V3
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44246
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/627
source_link: none
github_link: https://github.com/sherlock-audit/2024-10-debita-judging/issues/616

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
finders_count: 9
finders:
  - newspacexyz
  - h4rs0n
  - dimulski
  - jo13
  - KaplanLabs
---

## Vulnerability Title

M-18: Incentive Creator's Tokens Permanently Locked in Zero-Activity Epochs

### Overview


This bug report discusses an issue with the DebitaIncentives.sol contract where incentive tokens deposited for future epochs can become permanently locked in the contract if there is no lending or borrowing activity during that epoch. This is a serious design flaw that can result in significant financial losses for incentive creators. The root cause of this issue is the lack of a recovery mechanism in the contract. The report also outlines the internal and external pre-conditions for this bug to occur and suggests adding a recovery mechanism as a mitigation strategy. 

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-10-debita-judging/issues/616 

## Found by 
0x37, BengalCatBalu, KaplanLabs, dimulski, h4rs0n, jo13, newspacexyz, t.aksoy, xiaoming90
### Summary

The lack of token recovery mechanism in DebitaIncentives.sol will cause permanent loss of incentive tokens for incentive creators as tokens remain locked in the contract during epochs with zero lending/borrowing activity.

### Root Cause

In DebitaIncentives.sol, the incentivizePair function transfers tokens to the contract without any recovery mechanism:

```solidity
// transfer the tokens
IERC20(incentivizeToken).transferFrom(
    msg.sender,
    address(this),
    amount
);

// add the amount to the total amount of incentives
if (lendIncentivize[i]) {
    lentIncentivesPerTokenPerEpoch[principle][
        hashVariables(incentivizeToken, epoch)
    ] += amount;
} else {
    borrowedIncentivesPerTokenPerEpoch[principle][
        hashVariables(incentivizeToken, epoch)
    ] += amount;
}
```

This means that incentive creators can only deposit incentives for epochs that haven't started yet, and the incentives are locked in the contract until the epoch ends. Once tokens are transferred, they become permanently locked if no activity occurs in that epoch. This is a serious design flaw since market conditions are unpredictable and zero-activity epochs are likely to occur.

### Internal pre-conditions

1. Incentive creator needs to call `incentivizePair()` to deposit incentive tokens for a future epoch
2. `totalUsedTokenPerEpoch[principle][epoch]` needs to be exactly 0
3. No users perform any lending or borrowing actions during the specified epoch


### External pre-conditions

1. Market conditions lead to zero lending/borrowing activity during the incentivized epoch

### Attack Path

1. Incentive creator calls `incentivizePair()` to set up incentives for a future epoch, transferring tokens to the contract
2. The epoch passes with no lending or borrowing activity
3. No users can claim the incentives as there are no qualifying actions (`lentAmountPerUserPerEpoch` and `borrowAmountPerEpoch` remain 0)
4. The tokens remain permanently locked in the contract as there is no withdrawal or recovery mechanism

### Impact

The incentive creators suffer a complete loss of their deposited tokens for that epoch. The tokens become permanently locked in the contract with no mechanism for recovery or redistribution to future epochs. This could lead to significant financial losses.

### PoC

_No response_

### Mitigation

 Add a recovery mechanism that allows incentive creators to withdraw unclaimed tokens after an epoch ends. This should only be possible if the epoch had zero activity.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Debita Finance V3 |
| Report Date | N/A |
| Finders | newspacexyz, h4rs0n, dimulski, jo13, KaplanLabs, xiaoming90, BengalCatBalu, 0x37, t.aksoy |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-10-debita-judging/issues/616
- **Contest**: https://app.sherlock.xyz/audits/contests/627

### Keywords for Search

`vulnerability`

