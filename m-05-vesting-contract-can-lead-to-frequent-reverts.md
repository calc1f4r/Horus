---
# Core Classification
protocol: Subsquid
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58253
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Subsquid-security-review.md
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
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

[M-05] Vesting contract can lead to frequent reverts

### Overview


This bug report discusses an issue with the `Vesting` contract, which is used to lock funds for users while allowing them to participate in the protocol. The problem occurs when users try to release their vested funds, as the contract uses the `erc20.balanceOf` function to track the amount of tokens available. However, if the user has allocated some of their vested amount to staking or registering workers and gateways, this can cause an underflow and revert the function. This results in a temporary denial of service for users, as they are unable to release their funds until their stake or registration is paid out. To fix this issue, the report recommends adding a `depositForVesting` function and tracking the amount with a storage variable to correctly calculate the vested amounts. This will prevent the function from reverting even if funds are available.

### Original Finding Content

## Severity

**Impact**: Medium, temporary DOS of funds

**Likelihood**: Medium, occurs when funds are staked / used in the protocol

## Description

The `Vesting` is used to lock funds on behalf of a user while giving them the ability to participate in the protocol. The idea behind the contract is that the amount of funds in the contract will gradually be unlocked over time, while giving the owner the ability to use those tokens to stake or register workers and gateways with. This allows the users to use the tokens in the ecosystem, without having the option to withdraw them all at once.

The `VestingWallet` OpenZeppelin contract tracks a `_erc20Released` variable which keeps track of the tokens already paid out. When trigerring a new payout, the amount of tokens available is calculated as shown below.

```solidity
function releasable() public view virtual returns (uint256) {
    return vestedAmount(uint64(block.timestamp)) - released();
}
```

The issue is that since the contract uses the `erc20.balanceOf` function to track the vesting amounts, this above expression can underflow and revert. This is because the balance in the contract can decrease if the user wishes to allocate some of the vested amount to staking or registering workers and gateways.

This is best demonstrated in the POC below.

The issue is recreated in the following steps

1. The vesting contract is transferred in 8 eth of tokens.
2. At the midpoint, half (4 eth) tokens have been vested out. These tokens are collected by calling `release`. Thus `_erc20Released` is set to 4 eth for the token.
3. Of the remaining 4 eth in the contract, 2 eth is allocated to staking.
4. After some time, more tokens are vested out.
5. Now when `release` is called, the function reverts. This is because `vestedAmount()` returns a value less than 4 eth, and `_erc20Released` is 4 eth. This causes the `releasable` function to underflow and revert.

So even though the contract has funds and can afford to pay out some vested rewards, this function reverts.

```solidity
function test_AttackVesting() public {
    token.transfer(address(vesting), 8 ether);

    // Half (4 eth) is vested out
    vm.warp(vesting.start() + vesting.duration() / 2);
    vesting.release();
    assert(vesting.released(address(token)) == 4 ether);

    // Stake half of rest (2 ETH)
    bytes memory call = abi.encodeWithSelector(
        Staking.deposit.selector,
        0,
        2 ether
    );
    vesting.execute(address(router.staking()), call, 2 ether);

    // pass some time
    vm.warp(vesting.start() + (vesting.duration() * 60) / 100);
    // check rewards
    vm.expectRevert();
    vesting.release();
}
```

This causes a temporary DOS, and users are unable to release vested tokens until their stake or registration is paid out.

Since users lose access to part of the funds they deserve, this is a medium severity issue.

## Recommendations

Consider adding a `depositForVesting(unit amount)` function, and tracking the amount with a storage variable `baseAmount` updated in this function. This way, the vesting rewards will calculate rewards based on this and not the `erc20.balanceOf` value. The result is that we need not decrease the `baseAmount` when tokens are sent out for staking, and then the vested amounts will be correctly calculated based on the value of the contract, instead of just the balances. This will prevent scenarios where claiming can revert even if funds are available.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Subsquid |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Subsquid-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

