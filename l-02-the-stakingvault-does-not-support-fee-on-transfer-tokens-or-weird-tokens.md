---
# Core Classification
protocol: Surge
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55147
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Surge-Security-Review.md
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

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
finders_count: 1
finders:
  - Shieldify Security
---

## Vulnerability Title

[L-02] The `StakingVault` Does Not Support Fee-On-Transfer Tokens (or Weird Tokens)

### Overview

See description below for full details.

### Original Finding Content

## Severity

Low Risk

## Description

The `StakingVault` does not support fee-on-transfer tokens because the `stake()` function records the amount specified as an argument in `_userStakeInfo[user]`, rather than the actual amount of tokens received.

This will inflate the bonus of shares that the user will get and the last couple of users (or the last user depending on the number of users and the amounts they have staked) will not be able to unstake since the StakingVault will have less balance of staking token than the recorded amount in storage.

## Location of Affected Code

File: [StakingVault.sol]()

```solidity
function _stake(address user, uint256 amount, uint16 periodInDays) internal returns (StakeInfo memory) {
function _restake(address user, uint256 amountToAdd, uint16 periodInDays) internal returns (StakeInfo memory) {
function acceptPositionManagerRewards(address manager, uint256 allowedAmount) external returns (uint256 amount) {
```

## Impact

Some users will experience loss of funds and bonus shares will be a bit inflated.

## Recommendation

Record the token balance `StakingVault` before and after the transfer of the tokens to determine the actual received amount.

In general, before setting the staking and the reward tokens for the contract check whether these tokens have any weird functionalities such as reentrancy, fee on transfer, rebasing, reverting on transfer or approval and etc. Here is a list for a [basic reference](https://github.com/d-xo/weird-erc20).

## Team Response

Acknowledged.

## [I-01] Outstanding Allowances and Max Approvals Could Cause Loss of Funds in Multiple Scenarios

## Severity

Informational

## Description

`PositionManager` uses `_setAllowanceMaxIfNeeded()` in multiple places. If the allowances towards the staking contract or a router are not enough, this function will max out the allowance.

## Location of Affected Code

File: [PositionManager.sol]()

```solidity
function _setAllowanceMaxIfNeeded(IERC20 token, uint256 amount, address spender) internal {
    uint256 allowance = token.allowance(address(this), spender);
    if (allowance >= amount) return;
    token.approve(spender, type(uint256).max); // @audit not all tokens allow that I think
}
```

## Impact

This is considered bad practice because if any approved contract is compromised or a vulnerability is discovered, the `PositionManager`'s tokens could be at risk of being stolen.

Furthermore, some tokens such as `UNI` and `COMP` will revert if you attempt to approve them for more than `type(uint96).max` which will revert the swaps to $VOLT or the `increaseLiquidity()` function for these tokens.

The tokens will be effectively blocked inside the `PositionManager` forever.

## Recommendation

Consider approving entities only for the exact amount needed. This approach minimizes outstanding allowances, reducing the risk while still allowing necessary transactions.

If you plan to reset allowances to 0 after the main operation, be aware that certain tokens, like BNB, may revert when doing so.

## Team Response

Fixed.

## [I-02] The `userShares()` Does Not Show the Shares of the User Until the User Unstakes

## Severity

Informational

## Description

Users are not able to see how many shares they have in a pool until they unstakes.

## Location of Affected Code

File: [StakingVault.sol]()

```solidity
function userShares(address user, uint256 poolId, uint256 cycleId) external view returns (uint256) {
    ClaimableReward memory r = _userRewardPoolClaimableReward[user][poolId];
    if (r.cycleStart == 0) return 0;
    if (r.cycleStart > cycleId) return 0;
@>  if (r.cycleEnd < cycleId) return 0;
    return r.shares;
}
```

## Recommendation

Consider applying the following changes:

```diff
- if (r.cycleEnd < cycleId) return 0;
+ if (cycleId > currentPoolCycleId) return 0;
+ if (r.cycleEnd != 0 && r.cycleEnd < cycleId) return 0;
```

## Team Response

Fixed.

## [I-03] Use `safeERC20` in Order to Support Tokens Such as USDT

## Severity

Informational

## Description

USDT does not return a boolean on transfer which makes `StakingVault` revert on all transfer operations with it.

## Location of Affected Code

All transfers in `StakingVault`

## Impact

USDT cannot be used as a staking or reward token resulting in DOS.

## Recommendation

Consider implementing `SafeERC20` if you want to support such weird tokens.

## Team Response

Acknowledged.

## [I-04] Typography

## Severity

Informational

## Description

- Use custom errors with if statements instead of require with string errors to save gas
- Use fixed solidity versions
- Remove console and `TransferHelper` imports in `PositionManager.sol` as they are not used
- Add NatSpec comments to all functions
- No need to use return in `_swapToVolt()`
- Emit events on every state-changing function

## Recommendation

Consider implementing the recommendations above.

## Team Response

Fixed.

## [I-05] The `collectFees()` in `PositionManager.sol` Might Revert

## Severity

Informational

## Description

Fees in `UniV3` are gathered from the input token of a swap. There might be cases where for a period of time only swaps from token A to token B were made. This would mean that amount1 in this specific scenario is going to be 0 which will make `_swapToVolt()` revert and force the admin to use `collectFeesOnly()` instead.

## Location of Affected Code

File: [PositionManager.sol]()

```solidity
function collectFees(uint256[] calldata tokenIds) external {
    require(tokenIds.length <= MAX_COLLECT_FEES_BATCH_SIZE, "tokenIds array too long");

    for (uint256 i = 0; i < tokenIds.length; i++) {
        uint256 tokenId = tokenIds[i];

        (uint256 amount0, uint256 amount1) = _collectFeesUniV3(tokenId);
        UniV3Nft memory nft = _getNftUniV3(tokenId);

@>      if (nft.token0 != address(voltToken)) {
            _swapToVolt(nft.token0, amount0);
        }

@>      if (nft.token1 != address(voltToken)) {
            _swapToVolt(nft.token1, amount1);
        }
    }

    _transferVoltToStakingVault();
}
```

## Impact

The `collectFees()` in `PositionManager` might revert when only one of the tokens has accrued fees.

## Recommendation

Consider applying the following changes:

```diff
-   if (nft.token0 != address(voltToken)) {
+   if (nft.token0 != address(voltToken) && amount0 != 0) {
    _swapToVolt(nft.token0, amount0);
}

-   if (nft.token1 != address(voltToken)) {
+   if (nft.token1 != address(voltToken) && amount1 != 0) {
    _swapToVolt(nft.token1, amount1);
}
```

## Team Response

Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Surge |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Surge-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

