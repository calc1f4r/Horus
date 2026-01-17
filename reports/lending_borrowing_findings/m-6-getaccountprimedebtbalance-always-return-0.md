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
solodit_id: 18584
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/59
source_link: none
github_link: https://github.com/sherlock-audit/2023-03-notional-judging/issues/173

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
  - bin2chen
---

## Vulnerability Title

M-6: getAccountPrimeDebtBalance() always return 0

### Overview


A bug was found in the code of the Notional Protocol by bin2chen. The bug was in the external method `getAccountPrimeDebtBalance()`, which is used to show the current debt. The bug was caused by a spelling error, which made the method always return 0 when it should have returned the actual debt balance. This could cause serious errors in any third-party integrations with the Notional Protocol, as it would not be able to accurately determine a user's debt. The code snippet of the bug can be found at https://github.com/sherlock-audit/2023-03-notional/blob/main/contracts-v2/contracts/external/Views.sol#L496. The bug was found with a manual review. The recommended fix for the bug is to replace the code with ```debtBalance = cashBalance < 0 ? cashBalance : 0;```.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-03-notional-judging/issues/173 

## Found by 
bin2chen
## Summary
Spelling errors that result in `getAccountPrimeDebtBalance()` Always return 0

## Vulnerability Detail

`getAccountPrimeDebtBalance()` use for Show current debt

```solidity
    function getAccountPrimeDebtBalance(uint16 currencyId, address account) external view override returns (
        int256 debtBalance
    ) {
        mapping(address => mapping(uint256 => BalanceStorage)) storage store = LibStorage.getBalanceStorage();
        BalanceStorage storage balanceStorage = store[account][currencyId];
        int256 cashBalance = balanceStorage.cashBalance;

        // Only return cash balances less than zero
        debtBalance = cashBalance < 0 ? debtBalance : 0;   //<------@audit wrong, Always return 0
    }
```

In the above code we can see that due to a spelling error,  `debtBalance` always ==0 
should use `debtBalance = cashBalance < 0 ? cashBalance : 0;`

## Impact

`getAccountPrimeDebtBalance()` is the external method to check the debt
  If a third party integrates with notional protocol, this method will be used to determine whether the user has debt or not and handle it accordingly, which may lead to serious errors in the third party's business

## Code Snippet

https://github.com/sherlock-audit/2023-03-notional/blob/main/contracts-v2/contracts/external/Views.sol#L496

## Tool used

Manual Review

## Recommendation

```solidity
    function getAccountPrimeDebtBalance(uint16 currencyId, address account) external view override returns (
        int256 debtBalance
    ) {
        mapping(address => mapping(uint256 => BalanceStorage)) storage store = LibStorage.getBalanceStorage();
        BalanceStorage storage balanceStorage = store[account][currencyId];
        int256 cashBalance = balanceStorage.cashBalance;

        // Only return cash balances less than zero
-       debtBalance = cashBalance < 0 ? debtBalance : 0;
+       debtBalance = cashBalance < 0 ? cashBalance : 0;
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Notional V3 |
| Report Date | N/A |
| Finders | bin2chen |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-03-notional-judging/issues/173
- **Contest**: https://app.sherlock.xyz/audits/contests/59

### Keywords for Search

`vulnerability`

