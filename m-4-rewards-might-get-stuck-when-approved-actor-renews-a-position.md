---
# Core Classification
protocol: MagicSea - the native DEX on the IotaEVM
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36688
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/437
source_link: none
github_link: https://github.com/sherlock-audit/2024-06-magicsea-judging/issues/207

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
finders_count: 5
finders:
  - ydlee
  - ChinmayF
  - BlockBusters
  - HonorLt
  - 0xAnmol
---

## Vulnerability Title

M-4: Rewards might get stuck when approved actor renews a position

### Overview


This bug report discusses an issue with rewards getting stuck when an approved actor renews a position on the Magicsea platform. The bug occurs when an approved actor, such as a smart contract, calls the `renewLockPosition` or `extendLockPosition` functions, causing the rewards to be sent to the wrong user. This can result in a loss of reward tokens. The vulnerability has been identified by a group of researchers and has been confirmed through manual review and the use of the Foundry tool. The recommended solution is to change the `_lockPosition` function in `MlumStaking.sol` to use the owner of the position instead of `msg.sender`. The issue has been fixed by the protocol team in the latest PRs/commits. 

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-06-magicsea-judging/issues/207 

## Found by 
0xAnmol, BlockBusters, ChinmayF, HonorLt, ydlee
## Summary

When an approved actor calls the harvest function, the rewards get sent to the user (staker). However, when the approved actor renews the user’s position, they receive the rewards instead.

If the approved actor is a smart contract (e.g., a keeper), the funds might get stuck forever or go to the wrong user, such as a Chainlink keeper.

## Vulnerability Detail

Suppose Alice mints an NFT by creating a position and approves Bob to use it.

- When Bob calls `harvestPosition` with Alice’s `tokenId`, Alice will receive the rewards (as intended)
- When Bob calls `renewLockPosition` with Alice’s `tokenId`, Bob will receive the rewards. The internal function `_lockPosition`, which is called by `renewLockPosition`, also harvests the position before updating the lock duration. Unlike the harvest function, `_lockPosition` [sends the rewards to `msg.sender`](https://github.com/sherlock-audit/2024-06-magicsea/blob/main/magicsea-staking/src/MlumStaking.sol#L710) instead of the token owner.

This bug exists in both `renewLockPosition` and `extendLockPosition`, as they both call `_lockPosition`, which includes the wrong receiver.

### PoC

To run this test, add it into `MlumStaking.t.sol`.

```solidity
function testVuln_ApprovedActorReceivesRewardsWhenRenewingPosition() public {
    // setup pool
    uint256 _amount = 100e18;
    uint256 lockTime = 1 days;

    _rewardToken.mint(address(_pool), 100_000e6);
    _stakingToken.mint(ALICE, _amount);

    // alice creates new position
    vm.startPrank(ALICE);
    _stakingToken.approve(address(_pool), _amount);
    _pool.createPosition(_amount, lockTime);
    vm.stopPrank();

    // alice approves bob
    vm.prank(ALICE);
    _pool.approve(BOB, 1);

    skip(1 hours);

    // for simplicity of the PoC we use a static call
    // IMlumStaking doesn't include `renewLockPosition(uint256)`
    uint256 bobBefore = _rewardToken.balanceOf(BOB);
    vm.prank(BOB);
    address(_pool).call(abi.encodeWithSignature("renewLockPosition(uint256)", 1));

    // Bob receivew the rewards, instead of alice
    assertGt(_rewardToken.balanceOf(BOB), bobBefore);
}
```

## Impact

Possible loss of reward tokens

## Code Snippet

https://github.com/sherlock-audit/2024-06-magicsea/blob/main/magicsea-staking/src/MlumStaking.sol#L710

## Tool used

Manual Review, Foundry

## Recommendation

Change `_lockPosition()` in `MlumStaking.sol`  to use the owner of the position instead of `msg.sender`.

```solidity
function _lockPosition(uint256 tokenId, uint256 lockDuration, bool resetInitial) internal {
    ...
-   _harvestPosition(tokenId, msg.sender);
+   _harvestPosition(tokenId, _ownerOf(tokenId));
    ...
}
```



## Discussion

**0xSmartContract**

Calling the `renewLockPosition` and `extendLockPosition` functions may result in rewards being sent to the wrong address.

When an approved actor calls the `renewLockPosition` or `extendLockPosition` functions, the rewards go to the approved actor who made the call, not the Position Owner.

**0xHans1**

PR: https://github.com/metropolis-exchange/magicsea-staking/pull/8


**sherlock-admin2**

The protocol team fixed this issue in the following PRs/commits:
https://github.com/metropolis-exchange/magicsea-staking/pull/8

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | MagicSea - the native DEX on the IotaEVM |
| Report Date | N/A |
| Finders | ydlee, ChinmayF, BlockBusters, HonorLt, 0xAnmol |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-06-magicsea-judging/issues/207
- **Contest**: https://app.sherlock.xyz/audits/contests/437

### Keywords for Search

`vulnerability`

