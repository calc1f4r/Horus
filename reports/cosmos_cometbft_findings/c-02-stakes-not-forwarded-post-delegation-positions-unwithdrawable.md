---
# Core Classification
protocol: BOB-Staking_2025-10-18
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63718
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/BOB-Staking-security-review_2025-10-18.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[C-02] Stakes not forwarded post-delegation, positions unwithdrawable

### Overview


The bug report describes a problem in the 'BobStaking' smart contract where users who delegate governance are unable to withdraw their staked tokens. This is because when a user delegates governance, their tokens are moved to a 'DelegationSurrogate' contract. However, later calls to stake more tokens do not transfer these tokens to the DelegationSurrogate, causing a mismatch in the amount of tokens available for withdrawal. The report recommends enforcing a single custody location for delegated tokens to prevent this issue. 

### Original Finding Content


_Resolved_

## Severity

**Impact:** High

**Likelihood:** High

## Description

In `BobStaking`, once a user delegates governance via `alterGovernanceDelegatee`, their existing stake is moved to a `DelegationSurrogate`.
However, later calls to `stake(_amount, receiver, lockPeriod)` **keep new tokens in the staking contract**:

```solidity
IERC20(_stakingToken).safeTransferFrom(_stakeMsgSender(), address(this), _amount);
stakers[receiver].amountStaked += _amount;
```

No forwarding occurs when `stakers[receiver].governanceDelegatee != address(0)`.
Exit paths then **assume all** `amountStaked` sits in the surrogate:

* `unbond()` tries `safeTransferFrom(surrogate, this, amountStaked);`
* `instantWithdraw()` tries `safeTransferFrom(surrogate, _receiver, _amountForUser);`

If part of the stake stayed in this contract (common after re-staking), the surrogate **doesn’t hold enough** (and hasn’t approved), so these calls **revert**. The user cannot unbond or instant-withdraw → funds are effectively stuck.

**Minimal repro**

1. Stake 100 → delegate → 100 moved to surrogate.
2. Stake 50 again → 50 remains in staking contract; `amountStaked = 150`.
3. Call `unbond()` or `instantWithdraw()` → contract tries to pull 150 from surrogate → **revert**.

## Recommendations

* **Enforce a single custody location when delegated (preferred):**
  In `stake()`, if `governanceDelegatee != 0`, immediately forward `_amount` to the user’s surrogate:

  ```solidity
  if (stakers[receiver].governanceDelegatee != address(0)) {
      DelegationSurrogate s = storedSurrogates[stakers[receiver].governanceDelegatee];
      IERC20(stakingToken).safeTransfer(address(s), _amount);
  }
  ```





### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | BOB-Staking_2025-10-18 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/BOB-Staking-security-review_2025-10-18.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

