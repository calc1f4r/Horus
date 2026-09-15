---
# Core Classification
protocol: Olympusdao
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6684
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/50
source_link: none
github_link: https://github.com/sherlock-audit/2023-02-olympus-judging/issues/102

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - liquid_staking
  - cdp
  - services
  - cross_chain
  - payments

# Audit Details
report_date: unknown
finders_count: 8
finders:
  - Bobface
  - psy4n0n
  - immeas
  - cccz
  - joestakey
---

## Vulnerability Title

M-8: SingleSidedLiquidityVault.withdraw will decreases ohmMinted, which will make the calculation involving ohmMinted incorrect

### Overview


This bug report relates to the SingleSidedLiquidityVault.withdraw function, which decreases ohmMinted, making the calculation involving ohmMinted incorrect. This bug was found by joestakey, cccz, psy4n0n, Bobface, jonatascm, immeas, favelanky, and rvierdiiev. 

ohmMinted indicates the number of ohm minted in the contract, and ohmRemoved indicates the number of ohm burned in the contract. The contract should increase ohmMinted in deposit() and increase ohmRemoved in withdraw(). However, withdraw() decreases ohmMinted, which makes the calculation involving ohmMinted incorrect. 

For example, if a user mints 100 ohm in deposit() and immediately burns 100 ohm in withdraw(), \_canDeposit will return an amount_ less than LIMIT + 1000 instead of LIMIT, and getOhmEmissions() will return 1000 instead of 0. 

This bug impacts the calculation involving ohmMinted and could lead to incorrect results. The code snippets provided can be found at the following links: https://github.com/sherlock-audit/2023-02-olympus/blob/main/src/policies/lending/abstracts/SingleSidedLiquidityVault.sol#L276-L277, https://github.com/sherlock-audit/2023-02-olympus/blob/main/src/policies/lending/abstracts/SingleSidedLiquidityVault.sol#L392-L409. The recommendation to fix this bug is provided in the code snippet.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-02-olympus-judging/issues/102 

## Found by 
joestakey, cccz, psy4n0n, Bobface, jonatascm, immeas, favelanky, rvierdiiev

## Summary
SingleSidedLiquidityVault.withdraw will decreases ohmMinted, which will make the calculation involving ohmMinted incorrect.
## Vulnerability Detail
In SingleSidedLiquidityVault, ohmMinted indicates the number of ohm minted in the contract, and ohmRemoved indicates the number of ohm burned in the contract.
So the contract just needs to increase ohmMinted in deposit() and increase ohmRemoved in withdraw().
But withdraw() decreases ohmMinted, which makes the calculation involving ohmMinted incorrect.
```solidity
        ohmMinted -= ohmReceived > ohmMinted ? ohmMinted : ohmReceived;
        ohmRemoved += ohmReceived > ohmMinted ? ohmReceived - ohmMinted : 0;
```
Consider that a user minted 100 ohm in deposit() and immediately burned 100 ohm in withdraw().

In \_canDeposit, the amount_ is less than LIMIT + 1000 instead of LIMIT 
```solidity
    function _canDeposit(uint256 amount_) internal view virtual returns (bool) {
        if (amount_ + ohmMinted > LIMIT + ohmRemoved) revert LiquidityVault_LimitViolation();
        return true;
    }

```
getOhmEmissions() returns 1000 instead of 0
```solidity
    function getOhmEmissions() external view returns (uint256 emitted, uint256 removed) {
        uint256 currentPoolOhmShare = _getPoolOhmShare();

        if (ohmMinted > currentPoolOhmShare + ohmRemoved)
            emitted = ohmMinted - currentPoolOhmShare - ohmRemoved;
        else removed = currentPoolOhmShare + ohmRemoved - ohmMinted;
    }
```
## Impact
It will make the calculation involving ohmMinted incorrect.
## Code Snippet
https://github.com/sherlock-audit/2023-02-olympus/blob/main/src/policies/lending/abstracts/SingleSidedLiquidityVault.sol#L276-L277
https://github.com/sherlock-audit/2023-02-olympus/blob/main/src/policies/lending/abstracts/SingleSidedLiquidityVault.sol#L392-L409
## Tool used

Manual Review

## Recommendation
```diff
    function withdraw(
        uint256 lpAmount_,
        uint256[] calldata minTokenAmounts_,
        bool claim_
    ) external onlyWhileActive nonReentrant returns (uint256) {
        // Liquidity vaults should always be built around a two token pool so we can assume
        // the array will always have two elements
        if (lpAmount_ == 0 || minTokenAmounts_[0] == 0 || minTokenAmounts_[1] == 0)
            revert LiquidityVault_InvalidParams();
        if (!_isPoolSafe()) revert LiquidityVault_PoolImbalanced();

        _withdrawUpdateRewardState(lpAmount_, claim_);

        totalLP -= lpAmount_;
        lpPositions[msg.sender] -= lpAmount_;

        // Withdraw OHM and pairToken from LP
        (uint256 ohmReceived, uint256 pairTokenReceived) = _withdraw(lpAmount_, minTokenAmounts_);

        // Reduce deposit values
        uint256 userDeposit = pairTokenDeposits[msg.sender];
        pairTokenDeposits[msg.sender] -= pairTokenReceived > userDeposit
            ? userDeposit
            : pairTokenReceived;
-       ohmMinted -= ohmReceived > ohmMinted ? ohmMinted : ohmReceived;
        ohmRemoved += ohmReceived > ohmMinted ? ohmReceived - ohmMinted : 0;
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Olympusdao |
| Report Date | N/A |
| Finders | Bobface, psy4n0n, immeas, cccz, joestakey, rvierdiiev, favelanky, jonatascm |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-02-olympus-judging/issues/102
- **Contest**: https://app.sherlock.xyz/audits/contests/50

### Keywords for Search

`vulnerability`

