---
# Core Classification
protocol: Concur Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1401
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-02-concur-finance-contest
source_link: https://code4rena.com/reports/2022-02-concur
github_link: https://github.com/code-423n4/2022-02-concur-findings/issues/138

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
  - liquid_staking
  - cdp
  - yield
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - leastwood
  - hickuphh3
---

## Vulnerability Title

[H-02] Masterchef: Improper handling of deposit fee

### Overview


A bug has been identified in the MasterChef.sol contract, which is used to manage liquidity pools in the Concur protocol. The bug results in permanent lockups of deposit fees in the relevant depositor contracts (StakingRewards and ConvexStakingWrapper for now). 

The bug occurs when a pool’s deposit fee is non-zero. In this case, the deposit fee is subtracted from the amount to be credited to the user. However, the deposit fee is not credited to anyone, leading to permanent lockups of deposit fees in the relevant depositor contracts.

Two examples have been provided to demonstrate the bug. In the first example, Alice deposits 1000 LP tokens via the ConvexStakingWrapper contract and a deposit fee of 100 LP tokens is charged. However, Alice will only be able to withdraw 900 LP tokens. The 100 LP tokens is not credited to any party, and is therefore locked up permanently. In the second example, Alice deposits 1000 CRV into the StakingRewards contract and a deposit fee of 100 CRV is charged. Again, Alice is only able to withdraw 900 CRV tokens, while the 100 CRV is not credited to any party, and is therefore locked up permanently.

It is recommended that the deposit fee logic be shifted out of the masterchef contract into the depositor contracts themselves. This would ensure that the fee recipient is credited with the deposit fee and any additional logic to update the fee recipient’s state can be added in the masterchef contract.

### Original Finding Content

_Submitted by hickuphh3, also found by leastwood_

[MasterChef.sol#L170-L172](https://github.com/code-423n4/2022-02-concur/blob/main/contracts/MasterChef.sol#L170-L172)<br>

If a pool’s deposit fee is non-zero, it is subtracted from the amount to be credited to the user.

```jsx
if (pool.depositFeeBP > 0) {
  uint depositFee = _amount.mul(pool.depositFeeBP).div(_perMille);
  user.amount = SafeCast.toUint128(user.amount + _amount - depositFee);
}
```

However, the deposit fee is not credited to anyone, leading to permanent lockups of deposit fees in the relevant depositor contracts (StakingRewards and ConvexStakingWrapper for now).

### Proof of Concept

#### Example 1: ConvexStakingWrapper

Assume the following

*   The [curve cDai / cUSDC / cUSDT LP token](https://etherscan.io/address/0x9fC689CCaDa600B6DF723D9E47D84d76664a1F23) corresponds to `pid = 1` in the convex booster contract.
*   Pool is added in Masterchef with `depositFeeBP = 100 (10%)`.

1.  Alice deposits 1000 LP tokens via the ConvexStakingWrapper contract. A deposit fee of 100 LP tokens is charged. Note that the `deposits` mapping of the ConvexStakingWrapper contract credits 1000 LP tokens to her.
2.  However, Alice will only be able to withdraw 900 LP tokens. The 100 LP tokens is not credited to any party, and is therefore locked up permanently (essentially becomes protocol-owned liquidity). While she is able to do `requestWithdraw()` for 1000 LP tokens, attempts to execute `withdraw()` with amount = 1000 will revert because she is only credited 900 LP tokens in the Masterchef contract.

#### Example 2: StakingRewards

*   CRV pool is added in Masterchef with `depositFeeBP = 100 (10%)`.

1.  Alice deposits 1000 CRV into the StakingRewards contract. A deposit fee of 100 CRV is charged.
2.  Alice is only able to withdraw 900 CRV tokens, while the 100 CRV is not credited to any party, and is therefore locked up permanently.

These examples are non-exhaustive as more depositors can be added / removed from the Masterchef contract.

### Recommended Mitigation Steps

I recommend shifting the deposit fee logic out of the masterchef contract into the depositor contracts themselves, as additional logic would have to be added in the masterchef to update the fee recipient’s state (rewardDebt, send pending concur rewards, update amount), which further complicates matters. As the fee recipient is likely to be the treasury, it is also not desirable for it to accrue concur rewards.

```jsx
if (pool.depositFeeBP > 0) {
  uint depositFee = _amount.mul(pool.depositFeeBP).div(_perMille);
  user.amount = SafeCast.toUint128(user.amount + _amount - depositFee);
  UserInfo storage feeRecipient = userInfo[_pid][feeRecipient];
  // TODO: update and send feeRecipient pending concur rewards
  feeRecipient.amount = SafeCast.toUint128(feeRecipient.amount + depositFee);
  // TODO: update fee recipient's rewardDebt
}
```

**[ryuheimat (Concur) confirmed](https://github.com/code-423n4/2022-02-concur-findings/issues/138)**

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2022-02-concur-findings/issues/138#issuecomment-1092873088):**
 > The warden has identified a way for funds to be forever lost, because of that reason I believe High Severity to be appropriate.
> 
> Mitigation could be as simple as transferring the fee to a `feeReceiver` or adding a way to pull those fees.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Concur Finance |
| Report Date | N/A |
| Finders | leastwood, hickuphh3 |

### Source Links

- **Source**: https://code4rena.com/reports/2022-02-concur
- **GitHub**: https://github.com/code-423n4/2022-02-concur-findings/issues/138
- **Contest**: https://code4rena.com/contests/2022-02-concur-finance-contest

### Keywords for Search

`vulnerability`

