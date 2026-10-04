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
solodit_id: 18597
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/59
source_link: none
github_link: https://github.com/sherlock-audit/2023-03-notional-judging/issues/210

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

M-19: Secondary debt dust balances are not truncated

### Overview


This bug report is about an inconsistency in the handling of dust balances in primary and secondary debt within the protocol. The function `updateAccountDebt` truncates any dust balance in the `vaultState.totalDebtUnderlying` towards zero, however, this truncation was not applied to secondary debt in the `_updateTotalSecondaryDebt` function. This inconsistency could lead to discrepancies in debt accounting, accumulation of dust, and unforeseen consequences. The code snippet provided in the report is from the `_updateTotalSecondaryDebt` function. The tool used to find this bug was manual review. The recommendation is to truncate dust balance in secondary debt similar to what is done for primary debt. The report was validated by jeffywu who labeled it as a valid bug of medium severity.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-03-notional-judging/issues/210 

## Found by 
xiaoming90
## Summary

Dust balances in primary debt are truncated toward zero. However, this truncation was not performed against secondary debts.

## Vulnerability Detail

https://github.com/sherlock-audit/2023-03-notional-0xleastwood/blob/main/contracts-v2/contracts/internal/vaults/VaultAccount.sol#L231

```solidity
File: VaultAccount.sol
212:     function updateAccountDebt(
..SNIP..
230:         // Truncate dust balances towards zero
231:         if (0 < vaultState.totalDebtUnderlying && vaultState.totalDebtUnderlying < 10) vaultState.totalDebtUnderlying = 0;
..SNIP..
233:     }
```

`vaultState.totalDebtUnderlying` is primarily used to track the total debt of primary currency. Within the `updateAccountDebt` function, any dust balance in the `vaultState.totalDebtUnderlying` is truncated towards zero at the end of the function as shown above.

https://github.com/sherlock-audit/2023-03-notional-0xleastwood/blob/main/contracts-v2/contracts/internal/vaults/VaultSecondaryBorrow.sol#L304

```solidity
File: VaultSecondaryBorrow.sol
304:     function _updateTotalSecondaryDebt(
305:         VaultConfig memory vaultConfig,
306:         address account,
307:         uint16 currencyId,
308:         uint256 maturity,
309:         int256 netUnderlyingDebt,
310:         PrimeRate memory pr
311:     ) private {
312:         VaultStateStorage storage balance = LibStorage.getVaultSecondaryBorrow()
313:             [vaultConfig.vault][maturity][currencyId];
314:         int256 totalDebtUnderlying = VaultStateLib.readDebtStorageToUnderlying(pr, maturity, balance.totalDebt);
315:         
316:         // Set the new debt underlying to storage
317:         totalDebtUnderlying = totalDebtUnderlying.add(netUnderlyingDebt);
318:         VaultStateLib.setTotalDebtStorage(
319:             balance, pr, vaultConfig, currencyId, maturity, totalDebtUnderlying, false // not settled
320:         );
```

However, this approach was not consistently applied when handling dust balance in secondary debt within the `_updateTotalSecondaryDebt` function. Within the `_updateTotalSecondaryDebt` function, the dust balance in secondary debts is not truncated.

## Impact

The inconsistency in handling dust balances in primary and secondary debt could potentially lead to discrepancies in debt accounting within the protocol, accumulation of dust, and result in unforeseen consequences.

## Code Snippet

https://github.com/sherlock-audit/2023-03-notional-0xleastwood/blob/main/contracts-v2/contracts/internal/vaults/VaultSecondaryBorrow.sol#L304

## Tool used

Manual Review

## Recommendation

Consider truncating dust balance in secondary debt within the `_updateTotalSecondaryDebt` function similar to what has been done for primary debt.



## Discussion

**jeffywu**

Valid, medium severity looks good

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
- **GitHub**: https://github.com/sherlock-audit/2023-03-notional-judging/issues/210
- **Contest**: https://app.sherlock.xyz/audits/contests/59

### Keywords for Search

`vulnerability`

