---
# Core Classification
protocol: Renzo
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33508
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-04-renzo
source_link: https://code4rena.com/reports/2024-04-renzo
github_link: https://github.com/code-423n4/2024-04-renzo-findings/issues/103

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
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 21
finders:
  - 3
  - ZanyBonzy
  - inzinko
  - 0xAadi
  - kennedy1030
---

## Vulnerability Title

[M-13] Pending withdrawals prevent safe removal of collateral assets

### Overview


The report discusses a bug in the `RestakeManager` contract that allows the admin to add and remove collateral tokens used for deposits. However, if a token is removed while there are still pending withdrawals for it, it can cause issues with the accounting in the protocol. This can lead to an incorrect calculation of the total value locked (TVL) and an inflation of the mint and redeem rates for the `ezETH` token. The report recommends implementing a check to prevent removing a token with pending withdrawals or including the balance of the `WithdrawQueue` in the TVL calculation for removed tokens. The team has acknowledged the issue and plans to partially mitigate it by implementing a check and may also add a force `kickOff` in the future. 

### Original Finding Content


<https://github.com/code-423n4/2024-04-renzo/blob/main/contracts/RestakeManager.sol#L316-L321> 

<https://github.com/code-423n4/2024-04-renzo/blob/main/contracts/Withdraw/WithdrawQueue.sol#L279>

### Vulnerability details

The [`RestakeManager`](https://github.com/code-423n4/2024-04-renzo/blob/main/contracts/RestakeManager.sol) contract allows the admin to add and remove collateral tokens that are accepted for deposits into the protocol via the [`addCollateralToken()`](https://github.com/code-423n4/2024-04-renzo/blob/main/contracts/RestakeManager.sol#L220) and [`removeCollateralToken()`](https://github.com/code-423n4/2024-04-renzo/blob/main/contracts/RestakeManager.sol#L244) functions.

From the protocol team:

> (In order to) remove a collateral token we can withdraw full and increase the withdraw buffer to let users withdraw it.

However, since users cannot be forced to claim their withdrawals, it is always possible that a significant amount of the collateral token remains in the `WithdrawQueue` indefinitely in outstanding withdrawals.

In that case, calling `removeCollateralToken()` for that token would break accounting in the protocol. The `ezETH` total supply would still reflect the amounts that were burned to initiate those withdrawals, but the token balance in the `WithdrawQueue` would no longer be counted towards the TVL.

### Impact

The `RestakeManager` admin is unable to safely remove a collateral token. Removing the token anyway would inflate the `ezETH` mint and redeem rate compared to the actual backing collateral value.

### Proof of Concept

Assume `token1` has a balance of `Y` in the `WithdrawQueue` from pending user withdrawals. If `removeCollateralToken(token1)` is called:

1. `token1` is removed from the `collateralTokens` array.
2. `token1` balance of `Y` is still in `WithdrawQueue` but no longer counted in `totalTVL`.
3. Mint rate for `ezETH` increases since `totalTVL` is lower but `ezETH` total supply is unchanged.
4. Redeem rate for `ezETH` also increases since `ezETH` is now redeemable for a larger share of the remaining collateral.

The mint and redeem rates for `ezETH` are now inflated compared to the true value of the collateral backing it, since `Y` worth of `token1` is not accounted for in `totalTVL` but is still effectively backing the `ezETH` that was burned to withdraw it.

### Recommended Mitigation Steps

Consider forcing pending withdrawals of a token to be claimed before that token can be removed as collateral. This could be done by only allowing `removeCollateralToken()` to be called if `claimReserve[token] == 0`.

Alternatively, include the balance of the `WithdrawQueue` in the TVL calculation even for tokens that have been removed, as long as there are still pending withdrawals of that token. This would ensure mint and redeem rates remain correct.

**[jatinj615 (Renzo) acknowledged and commented](https://github.com/code-423n4/2024-04-renzo-findings/issues/103#issuecomment-2142257978):**
 > Will be partially mitigating this by having a sanity check on `removeCollateralToken` to revert if `withdrawQueue` Balance is non zero for the collateral asset getting removed. 
> 
> The force `kickOff` will be implemented later on. 



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Renzo |
| Report Date | N/A |
| Finders | 3, ZanyBonzy, inzinko, 0xAadi, kennedy1030, OMEN, 1, KupiaSec, 14si2o\_Flint, 2, t0x1c, CodeWasp, TECHFUND, golu, 4, Bigsam, LessDupes |

### Source Links

- **Source**: https://code4rena.com/reports/2024-04-renzo
- **GitHub**: https://github.com/code-423n4/2024-04-renzo-findings/issues/103
- **Contest**: https://code4rena.com/reports/2024-04-renzo

### Keywords for Search

`vulnerability`

