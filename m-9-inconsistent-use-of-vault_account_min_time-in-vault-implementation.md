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
solodit_id: 18587
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/59
source_link: none
github_link: https://github.com/sherlock-audit/2023-03-notional-judging/issues/179

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

M-9: Inconsistent use of `VAULT_ACCOUNT_MIN_TIME` in vault implementation

### Overview


This bug report is about an issue with the `VAULT_ACCOUNT_MIN_TIME` variable in the vault implementation. It was discovered by xiaoming90 and the vulnerability detail is that there is a considerable difference in implementation behaviour when a vault has yet to mature compared to after vault settlement. The code snippet in the report shows that the variable is updated in two cases; when a user enters a vault position, and when the vault has matured. The impact of this is that the `exitVault()` function will affect prime and non-prime vault users differently. The recommendation given is to add an exception to the `VaultConfiguration.settleAccountOrAccruePrimeCashFees()` so that when vault fees are calculated, `lastUpdatedBlockTime` is not updated to `block.timestamp`. Jeffywu commented that the exit time is 1 minute and marked the issue as "Won't Fix" as the change would be complex.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-03-notional-judging/issues/179 

## Found by 
xiaoming90
## Summary

There is a considerable difference in implementation behaviour when a vault has yet to mature compared to after vault settlement.

## Vulnerability Detail

There is some questionable functionality with the following `require` statement:

https://github.com/sherlock-audit/2023-03-notional-0xleastwood/blob/main/contracts-v2/contracts/external/actions/VaultAccountAction.sol#L242

```solidity
File: VaultAccountAction.sol
242:     require(vaultAccount.lastUpdateBlockTime + Constants.VAULT_ACCOUNT_MIN_TIME <= block.timestamp)
```

The `lastUpdateBlockTime` variable is updated in _two_ cases:
 - A user enters a vault position, updating the vault state; including `lastUpdateBlockTime`. This is a proactive measure to prevent users from quickly entering and exiting the vault.
 - The vault has matured and as a result, each time vault fees are assessed for a given vault account, `lastUpdateBlockTime` is updated to `block.timestamp` after calculating the pro-rated fee for the prime cash vault.

Therefore, before a vault has matured, it is not possible to quickly enter and exit a vault. But after `Constants.VAULT_ACCOUNT_MIN_TIME` has passed, the user can exit the vault as many times as they like. However, the same does not hold true once a vault has matured. Each time a user exits the vault, they must wait `Constants.VAULT_ACCOUNT_MIN_TIME` time again to re-exit. This seems like inconsistent behaviour.

## Impact

The `exitVault()` function will ultimately affect prime and non-prime vault users differently. It makes sense for the codebase to be written in such a way that functions execute in-line with user expectations.

## Code Snippet

https://github.com/sherlock-audit/2023-03-notional-0xleastwood/blob/main/contracts-v2/contracts/external/actions/VaultAccountAction.sol#L242

https://github.com/sherlock-audit/2023-03-notional-0xleastwood/blob/main/contracts-v2/contracts/internal/vaults/VaultAccount.sol#L487-L506

https://github.com/sherlock-audit/2023-03-notional-0xleastwood/blob/main/contracts-v2/contracts/internal/vaults/VaultConfiguration.sol#L284

https://github.com/sherlock-audit/2023-03-notional-0xleastwood/blob/main/contracts-v2/contracts/internal/vaults/VaultConfiguration.sol#L257

## Tool used

Manual Review

## Recommendation

It might be worth adding an exception to `VaultConfiguration.settleAccountOrAccruePrimeCashFees()` so that when vault fees are calculated, `lastUpdatedBlockTime` is not updated to `block.timestamp`.



## Discussion

**jeffywu**

Given how storage is structured, if we do not set lastUpdatedBlockTime then the prime vault account will end up paying fees on the same time portion twice. This is probably worse than not being able to exit the position twice in succession.

Although this issue is correct, the exit time is 1 minute. Will mark this as Won't Fix as the change will probably more complex than the benefit to UX.

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
- **GitHub**: https://github.com/sherlock-audit/2023-03-notional-judging/issues/179
- **Contest**: https://app.sherlock.xyz/audits/contests/59

### Keywords for Search

`vulnerability`

