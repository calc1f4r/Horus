---
# Core Classification
protocol: Mochi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 926
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-10-mochi-contest
source_link: https://code4rena.com/reports/2021-10-mochi
github_link: https://github.com/code-423n4/2021-10-mochi-findings/issues/25

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
  - dexes
  - cdp
  - cross_chain
  - rwa
  - options_vault

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - gpersoon
---

## Vulnerability Title

[H-05] debts calculation is not accurate

### Overview


A bug has been reported in the contract MochiVault.sol, which is used to calculate the global variable debts in an inconsistent way. In the function borrow(), the variable debts is increased with a value excluding the fee, while in repay() and liquidate() it is decreased with the same value as details[_id].debt, which is including the fee. This would mean that debts will end up in a negative value when all debts are repay-ed. As a result, the value of debts is not accurate and is used directly or indirectly in various functions, which means the entire debt and claimable calculations are slightly off. 

To mitigate this issue, it is recommended to replace the line 'debts += _amount;' in the borrow() function with 'debts += totalDebt'.

### Original Finding Content

## Handle

gpersoon


## Vulnerability details

## Impact
The value of the global variable debts in the contract MochiVault.sol is calculated in an inconsistent way.

In the function borrow() the variable debts is increased with a value excluding the fee.
However in repay() and liquidate() it is decreased with the same value as details[_id].debt is decreased,, which is including the fee.

This would mean that debts will end up in a negative value when all debts are repay-ed. Luckily the function repay() prevents this from happening.

In the mean time the value of debts isn't accurate.
This value is used directly or indirectly in: 
- utilizationRatio(), stabilityFee() calculateFeeIndex() of MochiProfileV0.sol 
- liveDebtIndex(), accrueDebt(), currentDebt() of MochiVault.sol

This means the entire debt and claimable calculations are slightly off.

## Proof of Concept
https://github.com/code-423n4/2021-10-mochi/blob/main/projects/mochi-core/contracts/vault/MochiVault.sol

function borrow(..)
    details[_id].debt = totalDebt; // includes the fee
    debts += _amount;     // excludes the fee 

function repay(..)
    debts -= _amount;  
    details[_id].debt -= _amount;

function liquidate(..)
   debts -= _usdm;
   details[_id].debt -= _usdm;

https://github.com/code-423n4/2021-10-mochi/blob/main/projects/mochi-core/contracts/vault/MochiVault.sol#L263-L268

https://github.com/code-423n4/2021-10-mochi/blob/806ebf2a364c01ff54d546b07d1bdb0e928f42c6/projects/mochi-core/contracts/profile/MochiProfileV0.sol#L272-L283

https://github.com/code-423n4/2021-10-mochi/blob/806ebf2a364c01ff54d546b07d1bdb0e928f42c6/projects/mochi-core/contracts/profile/MochiProfileV0.sol#L242-L256

https://github.com/code-423n4/2021-10-mochi/blob/806ebf2a364c01ff54d546b07d1bdb0e928f42c6/projects/mochi-core/contracts/profile/MochiProfileV0.sol#L258-L269

https://github.com/code-423n4/2021-10-mochi/blob/806ebf2a364c01ff54d546b07d1bdb0e928f42c6/projects/mochi-core/contracts/vault/MochiVault.sol#L66-L73

https://github.com/code-423n4/2021-10-mochi/blob/806ebf2a364c01ff54d546b07d1bdb0e928f42c6/projects/mochi-core/contracts/vault/MochiVault.sol#L79-L88

## Tools Used

## Recommended Mitigation Steps
In function borrow():
replace
    debts += _amount;
with
    debts += totalDebt

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Mochi |
| Report Date | N/A |
| Finders | gpersoon |

### Source Links

- **Source**: https://code4rena.com/reports/2021-10-mochi
- **GitHub**: https://github.com/code-423n4/2021-10-mochi-findings/issues/25
- **Contest**: https://code4rena.com/contests/2021-10-mochi-contest

### Keywords for Search

`vulnerability`

