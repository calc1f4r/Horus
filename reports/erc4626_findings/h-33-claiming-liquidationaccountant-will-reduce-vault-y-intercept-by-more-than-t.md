---
# Core Classification
protocol: Astaria
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3671
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/8
source_link: none
github_link: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/48

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
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - obront
---

## Vulnerability Title

H-33: Claiming liquidationAccountant will reduce vault y-intercept by more than the correct amount

### Overview


This bug report is about an issue found in the Liquidation Accountant contract in the Sherlock Audit's 2022-10-astaria-judging repository. The issue was found by obront. When `claim()` is called on the Liquidation Accountant, it decreases the y-intercept based on the balance of the contract after funds have been distributed, rather than before. This causes the y-intercept to be decreased more than it should be, siphoning funds from all users and throwing off the vault's math. This issue can be resolved by calling `PublicVault(VAULT()).decreaseYIntercept(expected - balance)` or by moving the current code above the block of code that transfers funds out.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/48 

## Found by 
obront

## Summary

When `claim()` is called on the Liquidation Accountant, it decreases the y-intercept based on the balance of the contract after funds have been distributed, rather than before. The result is that the y-intercept will be decreased more than it should be, siphoning funds from all users.

## Vulnerability Detail

When `LiquidationAccountant.sol:claim()` is called, it uses its `withdrawRatio` to send some portion of its earnings to the `WITHDRAW_PROXY` and the rest to the vault.

After performing these transfers, it updates the vault's y-intercept, decreasing it by the gap between the expected return from the auction, and the reality of how much was sent back to the vault:

```solidity
PublicVault(VAULT()).decreaseYIntercept(
  (expected - ERC20(underlying()).balanceOf(address(this))).mulDivDown(
    1e18 - withdrawRatio,
    1e18
  )
);
```
This rebalancing uses the balance of the `liquidationAccountant` to perform its calculation, but it is done after the balance has already been distributed, so it will always be 0.

Looking at an example:
- `expected = 1 ether` (meaning the y-intercept is currently based on this value)
- `withdrawRatio = 0` (meaning all funds will go back to the vault)
- The auction sells for exactly 1 ether
- 1 ether is therefore sent directly to the vault
- In this case, the y-intercept should not be updated, as the outcome was equal to the expected outcome
- However, because the calculation above happens after the funds are distributed, the decrease equals `(expected - 0) * 1e18 / 1e18`, which equals `expected`

That decrease should not happen, and causing problems for the protocol's accounting. For example, when `withdraw()` is called, it uses the y-intercept in its calculation of the `totalAssets()` held by the vault, creating artificially low asset values for a given number of shares.

## Impact

Every time the liquidation accountant is used, the vault's math will be thrown off and user shares will be falsely diluted.

## Code Snippet

https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/LiquidationAccountant.sol#L62-L97

## Tool used

Manual Review

## Recommendation

The amount of assets sent to the vault has already been calculated, as we've already sent it. Therefore, rather than the full existing formula, we can simply call:

```solidity
PublicVault(VAULT()).decreaseYIntercept(expected - balance)
```

Alternatively, we can move the current code above the block of code that transfers funds out (L73).

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | obront |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/48
- **Contest**: https://app.sherlock.xyz/audits/contests/8

### Keywords for Search

`vulnerability`

