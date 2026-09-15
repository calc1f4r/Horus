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
solodit_id: 18569
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/59
source_link: none
github_link: https://github.com/sherlock-audit/2023-03-notional-judging/issues/172

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
  - liquid_staking
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - bin2chen
  - xiaoming90
---

## Vulnerability Title

H-2: repayAccountPrimeDebtAtSettlement() user lost residual cash

### Overview


This bug report is about an issue found in the `repayAccountPrimeDebtAtSettlement()` method in the VaultAccount.sol file. The incorrect calculation of the `primeCashRefund` value (always == 0) resulted in the user losing their residual cash. This was found by bin2chen and xiaoming90 during a manual review. 

The code snippet of the issue is as follows.

```solidity
    function repayAccountPrimeDebtAtSettlement(
        PrimeRate memory pr,
        VaultStateStorage storage primeVaultState,
        uint16 currencyId,
        address vault,
        address account,
        int256 accountPrimeCash,
        int256 accountPrimeStorageValue
    ) internal returns (int256 finalPrimeDebtStorageValue, bool didTransfer) {
...

            if (netPrimeDebtRepaid < accountPrimeStorageValue) {
                // If the net debt change is greater than the debt held by the account, then only
                // decrease the total prime debt by what is held by the account. The residual amount
                // will be refunded to the account via a direct transfer.
                netPrimeDebtChange = accountPrimeStorageValue;
                finalPrimeDebtStorageValue = 0;

                int256 primeCashRefund = pr.convertFromUnderlying(
                    pr.convertDebtStorageToUnderlying(netPrimeDebtChange.sub(accountPrimeStorageValue)) //<--------@audit always ==0
                );
                TokenHandler.withdrawPrimeCash(
                    account, currencyId, primeCashRefund, pr, false // ETH will be transferred natively
                );
                didTransfer = true;
            } else {
```

The issue is caused by a spelling error, where `netPrimeDebtChange = accountPrimeStorageValue` should be `primeCashRefund = netPrimeDebtRepaid - accountPrimeStorageValue`. This resulted in the `primeCashRefund` value always being 0, leading to the user losing their residual cash.

The recommendation to fix this issue is to change the code to:

```solidity
    function repayAccountPrimeDebtAtSettlement(
        PrimeRate memory pr,
        VaultStateStorage storage primeVaultState,
       

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-03-notional-judging/issues/172 

## Found by 
bin2chen, xiaoming90
## Summary

in `repayAccountPrimeDebtAtSettlement() `
Incorrect calculation of `primeCashRefund` value (always == 0)
Resulting in the loss of the user's residual  cash

## Vulnerability Detail

when settle Vault Account 
will execute `settleVaultAccount()`->`repayAccountPrimeDebtAtSettlement()`
In the `repayAccountPrimeDebtAtSettlement()` method the residual amount will be refunded to the user
The code is as follows.
```solidity
    function repayAccountPrimeDebtAtSettlement(
        PrimeRate memory pr,
        VaultStateStorage storage primeVaultState,
        uint16 currencyId,
        address vault,
        address account,
        int256 accountPrimeCash,
        int256 accountPrimeStorageValue
    ) internal returns (int256 finalPrimeDebtStorageValue, bool didTransfer) {
...

            if (netPrimeDebtRepaid < accountPrimeStorageValue) {
                // If the net debt change is greater than the debt held by the account, then only
                // decrease the total prime debt by what is held by the account. The residual amount
                // will be refunded to the account via a direct transfer.
                netPrimeDebtChange = accountPrimeStorageValue;
                finalPrimeDebtStorageValue = 0;

                int256 primeCashRefund = pr.convertFromUnderlying(
                    pr.convertDebtStorageToUnderlying(netPrimeDebtChange.sub(accountPrimeStorageValue)) //<--------@audit always ==0
                );
                TokenHandler.withdrawPrimeCash(
                    account, currencyId, primeCashRefund, pr, false // ETH will be transferred natively
                );
                didTransfer = true;
            } else {
```

From the above code we can see that there is a spelling error

1. netPrimeDebtChange = accountPrimeStorageValue;
2. primeCashRefund = netPrimeDebtChange.sub(accountPrimeStorageValue)
so primeCashRefund always ==0

should be `primeCashRefund = netPrimeDebtRepaid - accountPrimeStorageValue`


## Impact

`primeCashRefund` always == 0 ,  user lost residual cash

## Code Snippet

https://github.com/sherlock-audit/2023-03-notional/blob/main/contracts-v2/contracts/internal/vaults/VaultAccount.sol#L575


## Tool used

Manual Review

## Recommendation

```solidity
    function repayAccountPrimeDebtAtSettlement(
        PrimeRate memory pr,
        VaultStateStorage storage primeVaultState,
        uint16 currencyId,
        address vault,
        address account,
        int256 accountPrimeCash,
        int256 accountPrimeStorageValue
    ) internal returns (int256 finalPrimeDebtStorageValue, bool didTransfer) {
...

            if (netPrimeDebtRepaid < accountPrimeStorageValue) {
                // If the net debt change is greater than the debt held by the account, then only
                // decrease the total prime debt by what is held by the account. The residual amount
                // will be refunded to the account via a direct transfer.
                netPrimeDebtChange = accountPrimeStorageValue;
                finalPrimeDebtStorageValue = 0;

                int256 primeCashRefund = pr.convertFromUnderlying(
-                   pr.convertDebtStorageToUnderlying(netPrimeDebtChange.sub(accountPrimeStorageValue))
+                   pr.convertDebtStorageToUnderlying(netPrimeDebtRepaid.sub(accountPrimeStorageValue)) 
                );
                TokenHandler.withdrawPrimeCash(
                    account, currencyId, primeCashRefund, pr, false // ETH will be transferred natively
                );
                didTransfer = true;
            } else {
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Notional V3 |
| Report Date | N/A |
| Finders | bin2chen, xiaoming90 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-03-notional-judging/issues/172
- **Contest**: https://app.sherlock.xyz/audits/contests/59

### Keywords for Search

`vulnerability`

