---
# Core Classification
protocol: Beraji Ko
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49513
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Beraji-KO-Security-Review.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.20
financial_impact: high

# Scoring
quality_score: 1
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Shieldify Security
---

## Vulnerability Title

[H-01] Attacker Can Redirect Funds To Staking Via Allowances

### Overview

The bug report is a high risk severity issue that is present in the StakingKo contract. The `deligateStake()` function uses an arbitrary address for the `from` parameter when calling the `transferFrom()` function. This allows an attacker to front run the next call and stake funds on behalf of the owner. The attacker can also change the settings of the stake for users attempting to stake in `lockId` 0. The recommendation is to use the funds of the caller instead when staking on behalf of someone and to use `msg.value` instead of an arbitrary address in the `transferFrom()` function. The team has responded that the issue has been fixed.

### Original Finding Content

## Severity

High Risk

## Description

In `deligateStake()` the `transferFrom()` function uses an arbitrary value for the `from` address. Before users or owner call `stake()`, `deligateStake()`, `createReward()`, `repayment()` or `depositRewardAmount()` they first approve the StakingKo contract. Once this is done the attacker can frontrun their next call and call `deligateStake()` on their behalf.

This way funds that were intended to be added by the owner as rewards will be staked on behalf of the owner. The owner will then need to wait for the lock to expire and try again.

In the case of users that try to stake in `lockId` 0, this lock can be changed to any other lock when the attacker stakes on behalf of the user.

## Location of Affected Code

File: [contracts/StakingKo.sol](https://github.com/Beraji-Labs/staking-ko/blob/290103f27365cc419fe0a934feaf5f18e6e12d3a/contracts/StakingKo.sol)

```solidity
function deligateStake(
    address _account,
    uint256 _poolId,
    uint256 _lockId,
    uint256 _amount,
    // aSugar printer
    uint256 _stPrice,
    uint256 _expriedTime,
    bytes memory _sig
)
    public
    payable
    validPool(_poolId)
    poolIsActive(_poolId)
    validPoolLock(_poolId, _lockId)
    updatePoolPrice(_poolId, _stPrice, _expriedTime, _sig)
    updateReward(_poolId, _account)
    payNativeFee
    whenNotPaused
{
    require(_amount != 0, "amount = 0");
    Pool storage pool = pools[_poolId];

@>  pool.stakingToken.safeTransferFrom(_account, address(this), _amount);

    // code

    emit Staked(_poolId, _account, stakeAmount, _stPrice);
}
```

## Impact

The attacker can redirect funds intended for rewards and stake them instead + he can change the settings of the stake for the users who try to stake.

## Recommendation

When staking on behalf of somebody use the funds of the caller instead. Use TransferFrom with `msg.value` instead of with arbitrary address.

## Team Response

Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 1/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Beraji Ko |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Beraji-KO-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

