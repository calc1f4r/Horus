---
# Core Classification
protocol: LoopFi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49063
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-07-loopfi
source_link: https://code4rena.com/reports/2024-07-loopfi
github_link: https://github.com/code-423n4/2024-07-loopfi-findings/issues/150

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
finders_count: 7
finders:
  - VAD37
  - Trooper
  - 0xpiken
  - 1
  - 2
---

## Vulnerability Title

[M-26] `PoolV3#repayCreditAccount()` use incorrect share converting function to calculate profit and loss

### Overview


The bug report discusses an issue with the calculation of profit and loss in the LoopFi project's PoolV3.sol file. This results in the treasury owning an incorrect balance. The report provides a proof of concept for the issue and recommends a mitigation step to use a different function for share calculation. The type of issue is assessed as a math problem and has been confirmed by the LoopFi team.

### Original Finding Content


<https://github.com/code-423n4/2024-07-loopfi/blob/main/src/PoolV3.sol#L549> 

<https://github.com/code-423n4/2024-07-loopfi/blob/main/src/PoolV3.sol#L553>

### Impact

Either the profit or the loss is calculated incorrectly, resulting in the treasury owns incorrect profit balance.

### Proof of Concept

Anyone can deposit `WETH` for `lpETH` by calling `PoolV3#deposit()` or `PoolV3#mint()`.  The exchange rate of `WETH:lpETH` is `1:1`.
The eligible credit manager can borrow `WETH` by calling `PoolV3#lendCreditAccount()`, and repay the debt and profit lately by calling `PoolV3#repayCreditAccount()`.
The corresponding amount of `lpETH` will be minted to `treasury` if there is profit, and the corresponding amount of `lpETH` should be burned from `treasury` if there is any loss:

```solidity
        if (profit > 0) {
@>          _mint(treasury, convertToShares(profit)); // U:[LP-14B]
        } else if (loss > 0) {
            address treasury_ = treasury;
            uint256 sharesInTreasury = balanceOf(treasury_);
@>          uint256 sharesToBurn = convertToShares(loss);
            if (sharesToBurn > sharesInTreasury) {
                unchecked {
                    emit IncurUncoveredLoss({
                        creditManager: msg.sender,
                        loss: convertToAssets(sharesToBurn - sharesInTreasury)
                    }); // U:[LP-14D]
                }
                sharesToBurn = sharesInTreasury;
            }
            _burn(treasury_, sharesToBurn); // U:[LP-14C,14D]
        }
```

However, `convertToShares()` is used to calculate shares for profit and loss, while  `_convertToShares()` is used to calculate shares in [`PoolV3#deposit()`](https://github.com/code-423n4/2024-07-loopfi/blob/main/src/PoolV3.sol#L243).
`convertToShares()` uses the exchange rate of `E4626` to calculate shares instead of `1:1` exchange rate defined in `PoolV3`.

The incorrect `convertToShares()` call could highly return less shares than expected, resulting in the treasury owning incorrect balance.

### Recommended Mitigation Steps

Use `_convertToShares()` for share calculation:

```diff
        if (profit > 0) {
-           _mint(treasury, convertToShares(profit)); // U:[LP-14B]
+           _mint(treasury, _convertToShares(profit)); 
        } else if (loss > 0) {
            address treasury_ = treasury;
            uint256 sharesInTreasury = balanceOf(treasury_);
-           uint256 sharesToBurn = convertToShares(loss);
+           uint256 sharesToBurn = _convertToShares(loss);
            if (sharesToBurn > sharesInTreasury) {
                unchecked {
                    emit IncurUncoveredLoss({
                        creditManager: msg.sender,
                        loss: convertToAssets(sharesToBurn - sharesInTreasury)
                    }); // U:[LP-14D]
                }
                sharesToBurn = sharesInTreasury;
            }
            _burn(treasury_, sharesToBurn); // U:[LP-14C,14D]
        }
```

### Assessed type

Math

**[0xtj24 (LoopFi) confirmed](https://github.com/code-423n4/2024-07-loopfi-findings/issues/150#event-14198057510)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | LoopFi |
| Report Date | N/A |
| Finders | VAD37, Trooper, 0xpiken, 1, 2, monrel, Agontuk |

### Source Links

- **Source**: https://code4rena.com/reports/2024-07-loopfi
- **GitHub**: https://github.com/code-423n4/2024-07-loopfi-findings/issues/150
- **Contest**: https://code4rena.com/reports/2024-07-loopfi

### Keywords for Search

`vulnerability`

