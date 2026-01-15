---
# Core Classification
protocol: Blueberry
chain: everychain
category: uncategorized
vulnerability_type: missing-logic

# Attack Vector Details
attack_type: missing-logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6640
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/41
source_link: none
github_link: https://github.com/sherlock-audit/2023-02-blueberry-judging/issues/151

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - missing-logic
  - deposit/reward_tokens

protocol_categories:
  - leveraged_farming
  - dexes
  - cdp
  - yield
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 14
finders:
  - cergyk
  - Bauer
  - 0x52
  - Ch\_301
  - sinarette
---

## Vulnerability Title

H-3: LP tokens are not sent back to withdrawing user

### Overview


This bug report is about an issue where LP tokens are not sent back to withdrawing users when assets are withdrawn from the `IchiVaultSpell.sol` function. This issue was found by a group of people and the vulnerability detail was found by manually reviewing the code. The impact of the issue is that users who close their positions and choose to keep LP tokens will have their LP tokens stuck permanently in the IchiVaultSpell contract.

The code snippet that is relevant to this issue is located at https://github.com/sherlock-audit/2023-02-blueberry/blob/main/contracts/spell/IchiVaultSpell.sol#L276-L330. The recommendation to resolve this issue is to add an additional line to the `withdrawInternal()` function to refund all LP tokens as well.

The discussion section mentions that this issue is a duplicate of issue 34. This means that the same issue has been reported before and the same solution can be used.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-02-blueberry-judging/issues/151 

## Found by 
rvierdiiev, minhtrng, Dug, Jeiwan, obront, chaduke, koxuan, sinarette, Ch\_301, cergyk, evan, berndartmueller, 0x52, Bauer

## Summary

When users withdraw their assets from `IchiVaultSpell.sol`, the function unwinds their position and sends them back their assets, but it never sends them back the amount they requested to withdraw, leaving the tokens stuck in the Spell contract.

## Vulnerability Detail

When a user withdraws from `IchiVaultSpell.sol`, they either call `closePosition()` or `closePositionFarm()`, both of which make an internal call to `withdrawInternal()`.

The following arguments are passed to the function:
- strategyId: an index into the `strategies` array, which specifies the Ichi vault in question
- collToken: the underlying token, which is withdrawn from Compound
- amountShareWithdraw: the number of underlying tokens to withdraw from Compound
- borrowToken: the token that was borrowed from Compound to create the position, one of the underlying tokens of the vault
- amountRepay: the amount of the borrow token to repay to Compound
- amountLpWithdraw: the amount of the LP token to withdraw, rather than trade back into borrow tokens

In order to accomplish these goals, the contract does the following...

1) Removes the LP tokens from the ERC1155 holding them for collateral.
```solidity
doTakeCollateral(strategies[strategyId].vault, lpTakeAmt);
```
2) Calculates the number of LP tokens to withdraw from the vault.
```solidity
uint256 amtLPToRemove = vault.balanceOf(address(this)) - amountLpWithdraw;
vault.withdraw(amtLPToRemove, address(this));
```

3) Converts the non-borrowed token that was withdrawn in the borrowed token (not copying the code in, as it's not relevant to this issue).

4) Withdraw the underlying token from Compound.
```solidity
doWithdraw(collToken, amountShareWithdraw);
```

5) Pay back the borrowed token to Compound.
```solidity
doRepay(borrowToken, amountRepay);
```

6) Validate that this situation does not put us above the maxLTV for our loans.
```solidity
_validateMaxLTV(strategyId);
```

7) Sends the remaining borrow token that weren't paid back and withdrawn underlying tokens to the user.
```solidity
doRefund(borrowToken);
doRefund(collToken);
```

Crucially, the step of sending the remaining LP tokens to the user is skipped, even though the function specifically does the calculations to ensure that `amountLpWithdraw` is held back from being taken out of the vault.

## Impact

Users who close their positions and choose to keep LP tokens (rather than unwinding the position for the constituent tokens) will have their LP tokens stuck permanently in the IchiVaultSpell contract.

## Code Snippet

https://github.com/sherlock-audit/2023-02-blueberry/blob/main/contracts/spell/IchiVaultSpell.sol#L276-L330

## Tool used

Manual Review

## Recommendation

Add an additional line to the `withdrawInternal()` function to refund all LP tokens as well:

```diff
  doRefund(borrowToken);
  doRefund(collToken);
+ doRefund(address(vault));
```

## Discussion

**Gornutz**

duplicate of 34

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Blueberry |
| Report Date | N/A |
| Finders | cergyk, Bauer, 0x52, Ch\_301, sinarette, Jeiwan, Dug, koxuan, berndartmueller, evan, chaduke, rvierdiiev, obront, minhtrng |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-02-blueberry-judging/issues/151
- **Contest**: https://app.sherlock.xyz/audits/contests/41

### Keywords for Search

`Missing-Logic, Deposit/Reward tokens`

