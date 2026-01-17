---
# Core Classification
protocol: Cap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62168
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/990
source_link: none
github_link: https://github.com/sherlock-audit/2025-07-cap-judging/issues/396

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
finders_count: 3
finders:
  - montecristo
  - HeckerTrieuTien
  - magiccentaur
---

## Vulnerability Title

M-6: VaultAdapter::multiplier not initialized can  lead first borrows to have `utilizationRate` = 0

### Overview


This bug report discusses an issue with the InterestRate calculation in the DebtToken::_nextInterestRate() function. The problem occurs when the utilizationRate for the first borrowers is 0, resulting in a lower cost for users and a loss of yield for the protocol. The root cause of this issue is a function that changes the storage and retrieves the utilizationRate under different cases. This leads to a situation where the multiplier is set to 0, causing the final interest rate to also be 0. This issue can only occur if the first borrower borrows a large amount of tokens, leading to a utilizationRate above a certain threshold. This bug allows early borrowers to borrow at a lower interest rate than expected, resulting in less interest being received by the protocol. The mitigation suggested is to initialize the multiplier at a neutral value.

### Original Finding Content


Source: https://github.com/sherlock-audit/2025-07-cap-judging/issues/396 

## Found by 
HeckerTrieuTien, magiccentaur, montecristo

### Summary

InterestRate calculted in `DebtToken::_nextInterestRate()`  is composed of 2 value:  rate (marketRate or benchmarkRate)  plus an `utilizationRate`.  For an issue in `VaultAdapter` the utilizationRate for the first borrowers can be 0, leading to a lower cost for the users and a loss of yield for protocol. 

### Root Cause

https://github.com/sherlock-audit/2025-07-cap/blob/main/cap-contracts/contracts/oracle/libraries/VaultAdapter.sol#L27-L50

Rate is a function that changes the storage.  `utilization` value is retrieved by `rate` under different cases.


https://github.com/sherlock-audit/2025-07-cap/blob/main/cap-contracts/contracts/oracle/libraries/VaultAdapter.sol#L79-L95

`multiplier` is a storage variable auto-initialized to 0. In `_applySlopes` if the first user borrows a large amount of tokens such that `_utilization > slopes.kink` we have this formula:

```solidity
 utilizationData.multiplier = utilizationData.multiplier
                * (1e27 + (1e27 * excess / (1e27 - slopes.kink)) * (_elapsed * $.rate / 1e27)) / 1e27;
```
utilizationData.multiplier will be multiplied for a number, but is 0 so final `multiplier` will be 0:

```solidity
 utilizationData.multiplier= 0 * (1e27 + (1e27 * excess / (1e27 - slopes.kink)) * (_elapsed * $.rate / 1e27)) / 1e27 = 0
```
So: 

```solidity

            interestRate = (slopes.slope0 + (slopes.slope1 * excess / 1e27)) * utilizationData.multiplier / 1e27;

```
```solidity
interestRate = (slopes.slope0 + (slopes.slope1 * excess / 1e27)) * 0 / 1e27 = 0
```
The final `interestRate` will be 0 too.  New ` utilizationData.multiplier` is stored as 0. 
For a second borrower (if  remains `utilization > slopes.kink` ) will have the same situation, and so on.

Series will be interrupted when, after some operations, we will have `utilization < slopes.kink`. Entering the `else`  will set at least the multiplier to `minMultiplier` for:

```solidity
 if (utilizationData.multiplier < $.minMultiplier) {
utilizationData.multiplier = $.minMultiplier;
}
```

At that point, the storage will contain a number != 0.

### Internal Pre-conditions

amount borrowed by first user must lead to `utilization > slopes.kink`.

### External Pre-conditions

--

### Attack Path

1. First agent borrows a large amount of tokens such that: `utilization > slopes.kink `.
2. New value stored as multiplier: 0.
3.  InterestRate (from utilization) is 0.
4.  As long as the condition `utilization > slopes.kink ` remains valid other agents can borrow at the basic condition interest because  the new multiplier that should be used is always multiplied by the old one which is 0 (and the new value will be too).


### Impact

Under the conditions, early borrowers borrow with a interest rate lower than expected. The protocol will receive less interests than it should. The higher the usage, the higher the interest to be paid should be, instead it is 0 (only the base interest will be paid).

### PoC

--

### Mitigation

Consider the initialization of `multiplier` at the neutral value.



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Cap |
| Report Date | N/A |
| Finders | montecristo, HeckerTrieuTien, magiccentaur |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-07-cap-judging/issues/396
- **Contest**: https://app.sherlock.xyz/audits/contests/990

### Keywords for Search

`vulnerability`

