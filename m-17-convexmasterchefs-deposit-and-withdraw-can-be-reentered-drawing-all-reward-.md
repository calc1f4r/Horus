---
# Core Classification
protocol: Aura Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25026
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-05-aura
source_link: https://code4rena.com/reports/2022-05-aura
github_link: https://github.com/code-423n4/2022-05-aura-findings/issues/313

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

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - yield
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-17] `ConvexMasterChef`'s deposit and withdraw can be reentered drawing all reward funds from the contract if reward token allows for transfer flow control

### Overview


A bug report has been submitted by hyh which states that the reward token accounting update in deposit() and withdraw() functions of the ConvexMasterChef.sol contract happens after reward transfer. As a result, if the reward token allows for the control of transfer call flow or can be upgraded to allow it in the future, it is possible to drain all the reward token funds of the contract by directly reentering deposit() or withdraw() with tiny amounts. The severity of the bug has been set to medium as it is conditional to transfer flow control assumption, but the impact is the full loss of contract reward token holdings.

Proof of concept has been provided for both the withdraw() and deposit() functions, which have the issue of performing late accounting update and not controlling for reentrancy. Recommended mitigation steps include adding a direct reentrancy control, e.g. nonReentrant modifier, and finishing all internal state updates prior to external calls.

The bug has been confirmed and commented on by 0xMaharishi (Aura Finance) and resolved with the help of two pull requests on code-423n4/2022-05-aura#6 and code4rena aurafinance/aura-contracts#84.

### Original Finding Content

_Submitted by hyh_

Reward token accounting update in deposit() and withdraw() happens after reward transfer. If reward token allows for the control of transfer call flow or can be upgraded to allow it in the future (i.e. have or can introduce the \_beforetokentransfer, \_afterTokenTransfer type of hooks; or, say, can be upgraded to ERC777), the current implementation makes it possible to drain all the reward token funds of the contract by directly reentering deposit() or withdraw() with tiny \_amount.

Setting the severity to medium as this is conditional to transfer flow control assumption, but the impact is the full loss of contract reward token holdings.

### Proof of Concept

Both withdraw() and deposit() have the issue, performing late accounting update and not controlling for reentrancy:

[ConvexMasterChef.sol#L209-L221](https://github.com/code-423n4/2022-05-aura/blob/4989a2077546a5394e3650bf3c224669a0f7e690/convex-platform/contracts/contracts/ConvexMasterChef.sol#L209-L221)<br>

```solidity
    function deposit(uint256 _pid, uint256 _amount) public {
        PoolInfo storage pool = poolInfo[_pid];
        UserInfo storage user = userInfo[_pid][msg.sender];
        updatePool(_pid);
        if (user.amount > 0) {
            uint256 pending = user
                .amount
                .mul(pool.accCvxPerShare)
                .div(1e12)
                .sub(user.rewardDebt);
            safeRewardTransfer(msg.sender, pending);
        }
        pool.lpToken.safeTransferFrom(
```

[ConvexMasterChef.sol#L239-L250](https://github.com/code-423n4/2022-05-aura/blob/4989a2077546a5394e3650bf3c224669a0f7e690/convex-platform/contracts/contracts/ConvexMasterChef.sol#L239-L250)<br>

```solidity
    function withdraw(uint256 _pid, uint256 _amount) public {
        PoolInfo storage pool = poolInfo[_pid];
        UserInfo storage user = userInfo[_pid][msg.sender];
        require(user.amount >= _amount, "withdraw: not good");
        updatePool(_pid);
        uint256 pending = user.amount.mul(pool.accCvxPerShare).div(1e12).sub(
            user.rewardDebt
        );
        safeRewardTransfer(msg.sender, pending);
        user.amount = user.amount.sub(_amount);
        user.rewardDebt = user.amount.mul(pool.accCvxPerShare).div(1e12);
        pool.lpToken.safeTransfer(address(msg.sender), _amount);
```

### Recommended Mitigation Steps

Consider adding a direct reentrancy control, e.g. nonReentrant modifier:

<https://docs.openzeppelin.com/contracts/2.x/api/utils#ReentrancyGuard>

Also, consider finishing all internal state updates prior to external calls:

<https://consensys.github.io/smart-contract-best-practices/attacks/reentrancy/#pitfalls-in-reentrancy-solutions>

**[0xMaharishi (Aura Finance) confirmed and commented](https://github.com/code-423n4/2022-05-aura-findings/issues/313#issuecomment-1140258550):**
 > Protected by governance, but agree could be solved with simple reentrancy guard.

**[0xMaharishi (Aura Finance) resolved](https://github.com/code-423n4/2022-05-aura-findings/issues/313#issuecomment-1141475322):**
 > [code-423n4/2022-05-aura#6](https://github.com/code-423n4/2022-05-aura/pull/6)<br>
 > [code4rena aurafinance/aura-contracts#84](https://github.com/aurafinance/aura-contracts/pull/84)



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Aura Finance |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-05-aura
- **GitHub**: https://github.com/code-423n4/2022-05-aura-findings/issues/313
- **Contest**: https://code4rena.com/reports/2022-05-aura

### Keywords for Search

`vulnerability`

