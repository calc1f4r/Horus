---
# Core Classification
protocol: Rubicon
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48976
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-04-rubicon
source_link: https://code4rena.com/reports/2023-04-rubicon
github_link: https://github.com/code-423n4/2023-04-rubicon-findings/issues/670

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
  - dexes
  - cdp
  - yield
  - yield_aggregator
  - rwa

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - rvierdiiev
---

## Vulnerability Title

[M-20] `Position` contract allows to interact with positions that are liquidated

### Overview


This bug report discusses an issue with the `Position` contract, which allows users to interact with positions that have been liquidated. This can result in users losing funds. The report provides a proof of concept, showing how this can happen when a user tries to add collateral to a liquidated position. This can cause the user's collateral to become locked and unable to be withdrawn. The report recommends not allowing users to interact with liquidated positions as a mitigation step. The bug was confirmed by the daoio (Rubicon) team. The report was created using VsCode.

### Original Finding Content


`Position` contract allows to interact with positions that are liquidated. Because of that user can loose funds.

### Proof of Concept

When new position is created, the amount of tokens that were supplied as collateral [are saved](https://github.com/code-423n4/2023-04-rubicon/blob/main/contracts/utilities/poolsUtility/Position.sol#L412) as well.
Later, when the user wants to close position, they will [redeem that amount](https://github.com/code-423n4/2023-04-rubicon/blob/main/contracts/utilities/poolsUtility/Position.sol#L220).
If a user wants to add collateral to avoid liquidation or for any other reason, they can call `increaseMargin`, which will [increase their bath token amount](https://github.com/code-423n4/2023-04-rubicon/blob/main/contracts/utilities/poolsUtility/Position.sol#L238) that is used as collateral for the position.

In this case, if `Position bathToken` collateral is liquidated, that means that their debt becomes 0 and if they call `closePosition`, then the call will revert, as it will need to [`redeem`](https://github.com/code-423n4/2023-04-rubicon/blob/main/contracts/utilities/poolsUtility/Position.sol#L220) `bathToken` amount that the `Position` contract doesn't control anymore.

So in this case, if the user will call `increaseMargin`, just after it was liquidated, then the provided collateral will never be possible to withdraw, as `closePosition` will always revert.

Example:
1. User has open position for bathUSDC, with an amount of 1000 bathUSDC.<br>
2. Their position is under liquidation so they want to `increaseMargin` with 100 USDC more.<br>
3. Liquidation happens before `increaseMargin` was called, so the `Position` contract bathUSDC balance is now 0 and `increaseMargin` mints 100 bathUSDC more.<br>
4. `increaseMargin` increased the position's bath amount to 1100.<br>
5. The user realized that they couldn't save position and now want to get back collateral, they call `closePosition`.<br>
6. `closePosition` reverts when redeeming as a `Position` contract that doesn't have 1100 bathUSDC, only 100 USDC.

As a result, the  user's 100 USDC is locked and can be used only as collateral for borrowing.

### Tools Used

VsCode

### Recommended Mitigation Steps

Do not allow users to interact with liquidated positions.

**[daoio (Rubicon) confirmed](https://github.com/code-423n4/2023-04-rubicon-findings/issues/670#issuecomment-1547180974)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Rubicon |
| Report Date | N/A |
| Finders | rvierdiiev |

### Source Links

- **Source**: https://code4rena.com/reports/2023-04-rubicon
- **GitHub**: https://github.com/code-423n4/2023-04-rubicon-findings/issues/670
- **Contest**: https://code4rena.com/reports/2023-04-rubicon

### Keywords for Search

`vulnerability`

