---
# Core Classification
protocol: Merit Circle
chain: everychain
category: logic
vulnerability_type: business_logic

# Attack Vector Details
attack_type: business_logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3471
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/9
source_link: none
github_link: https://github.com/sherlock-audit/2022-10-merit-circle-judging/issues/108

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:
  - business_logic
  - vecrv
  - change_validation

protocol_categories:
  - dexes
  - cdp
  - cross_chain
  - rwa
  - payments

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - WATCHPUG
---

## Vulnerability Title

M-2: Expired locks should not continue to earn rewards at the original high multiplier rate

### Overview


This bug report is about an issue in the Merit Circle Liquidity Mining System which allows users with expired locks to continue to enjoy the original high multiplier rate, while they can withdraw anytime they want. This means that users with expired locks will take more rewards than expected, which means fewer rewards for other users. A solution to this issue is to add a function called `kick()` which allows the expired (zeroed) veCRV users to be kicked from the rewards. This function can be called by anyone and shares will go back to a 1:1 ratio. A PR (pull request) from this issue has been submitted and agreed on.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-10-merit-circle-judging/issues/108 

## Found by 
WATCHPUG

## Summary

Expired locks should be considered as same as the deposits with no lock.

## Vulnerability Detail

The current implementation allows the deposits with expired locks to continue to enjoy the original high multiplier rate, while they can withdraw anytime they want.

The multiplier of shares amount is essentially a higher reward rate (APR) for longer period of locks.

For example:

If the regular APR is 2%; Locking for 4 years will boost the APR to 10%.

- Alice deposited 1M $MC tokens and got 10% APR;
- 4 years later, Alice's deposit's lock was expired.

Expected result:

The new APR for Alice's deposit is 2%;

Actual result:

Alice can continue to enjoy a 10% APR while she can withdraw anytime.

## Impact

Users with expired locks will take more rewards than expected, which means fewer rewards for other users.

## Code Snippet

https://github.com/Merit-Circle/merit-liquidity-mining/blob/ce5feaae19126079d309ac8dd9a81372648437f1/contracts/TimeLockPool.sol#L116-L135

## Tool used

Manual Review

## Recommendation

Curve's Gauge system introduced a method called `kick()` which allows the expired (zeroed) veCRV users to be kicked from the rewards.

See: https://github.com/curvefi/curve-dao-contracts/blob/master/contracts/gauges/LiquidityGaugeV5.vy#L430-L446

A similar method can be added to solve this issue:

```solidity
function kick(uint256 _depositId, address _user) external {
    if (_depositId >= depositsOf[_user].length) {
        revert NonExistingDepositError();
    }
    Deposit memory userDeposit = depositsOf[_user][_depositId];
    if (block.timestamp < userDeposit.end) {
        revert TooSoonError();
    }

    // burn pool shares
    _burn(_user, userDeposit.shareAmount - userDeposit.amount);
}
```

## Discussion

**federava**

Agree on the recommendation, will implement kick function. Noticing that shares go back to a 1:1 ratio and that the function can be called by anyone is a good design choice.

**federava**

[PR](https://github.com/Merit-Circle/merit-liquidity-mining/pull/16) from this issue

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Sherlock |
| Protocol | Merit Circle |
| Report Date | N/A |
| Finders | WATCHPUG |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-10-merit-circle-judging/issues/108
- **Contest**: https://app.sherlock.xyz/audits/contests/9

### Keywords for Search

`Business Logic, veCRV, Change Validation`

