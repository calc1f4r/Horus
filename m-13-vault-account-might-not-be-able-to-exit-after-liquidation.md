---
# Core Classification
protocol: Notional V3
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18591
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/59
source_link: none
github_link: https://github.com/sherlock-audit/2023-03-notional-judging/issues/192

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
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - xiaoming90
---

## Vulnerability Title

M-13: Vault account might not be able to exit after liquidation

### Overview


A bug report has been identified by xiaoming90 where vault accounts might not be able to exit after liquidation events. This is due to a positive `vaultAccount.tempCashBalance` after a liquidation event and interest accrual. This is because the `updateAccountDebt` function is called, and the `vaultAccount.tempCashBalance` is updated to $x - y$ where $x$ is the `primaryCash` of the vault account and $y$ is the cost in prime cash terms to lend an offsetting fCash position. If $x > y$, then the new `vaultAccount.tempCashBalance` will be more than zero. As a result, the `redeemWithDebtRepayment` function will be reverted and the owner cannot exit the vault. This means that the owner of the vault account would not be able to exit the vault and their assets would be stuck within the protocol. 

The recommendation to resolve this issue is to refund the excess positive `vaultAccount.tempCashBalance` to the users so that `vaultAccount.tempCashBalance` will be cleared (set to zero) before calling the `redeemWithDebtRepayment` function. The code snippet related to this issue can be found at https://github.com/sherlock-audit/2023-03-notional/blob/main/contracts-v2/contracts/internal/vaults/VaultConfiguration.sol#L429. The tool used to identify this issue was Manual Review.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-03-notional-judging/issues/192 

## Found by 
xiaoming90
## Summary

The vault exit might fail after a liquidation event, leading to users being unable to main their positions.

## Vulnerability Detail

Assume that a large portion of the vault account gets liquidated which results in a large amount of cash deposited into the vault account's cash balance. In addition, interest will also start accruing within the vault account's cash balance. 

Let $x$ be the `primaryCash` of a vault account after a liquidation event and interest accrual.

The owner of the vault account decided to exit the vault by calling `exitVault`. Within the `exitVault` function, the `vaultAccount.tempCashBalance` will be set to $x$. 

Next, the `lendToExitVault` function is called. Assume that the cost in prime cash terms to lend an offsetting fCash position is $-y$ (`primeCashCostToLend`). The `updateAccountDebt` function will be called, and the `vaultAccount.tempCashBalance` will be updated to $x + (-y) \Rightarrow x - y$. If $x > y$, then the new `vaultAccount.tempCashBalance` will be more than zero.

Subsequently, the `redeemWithDebtRepayment` function will be called. However, since `vaultAccount.tempCashBalance` is larger than zero, the transaction will revert, and the owner cannot exit the vault.

https://github.com/sherlock-audit/2023-03-notional/blob/main/contracts-v2/contracts/internal/vaults/VaultConfiguration.sol#L429

```solidity
File: VaultConfiguration.sol
424:             if (vaultAccount.tempCashBalance < 0) {
425:                 int256 x = vaultConfig.primeRate.convertToUnderlying(vaultAccount.tempCashBalance).neg();
426:                 underlyingExternalToRepay = underlyingToken.convertToUnderlyingExternalWithAdjustment(x).toUint();
427:             } else {
428:                 // Otherwise require that cash balance is zero. Cannot have a positive cash balance in this method
429:                 require(vaultAccount.tempCashBalance == 0);
430:             }
```

## Impact

The owner of the vault account would not be able to exit the vault to main their position. As such, their assets are stuck within the protocol.

## Code Snippet

https://github.com/sherlock-audit/2023-03-notional/blob/main/contracts-v2/contracts/internal/vaults/VaultConfiguration.sol#L429

## Tool used

Manual Review

## Recommendation

Consider refunding the excess positive `vaultAccount.tempCashBalance` to the users so that `vaultAccount.tempCashBalance` will be cleared (set to zero) before calling the `redeemWithDebtRepayment` function.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Notional V3 |
| Report Date | N/A |
| Finders | xiaoming90 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-03-notional-judging/issues/192
- **Contest**: https://app.sherlock.xyz/audits/contests/59

### Keywords for Search

`vulnerability`

