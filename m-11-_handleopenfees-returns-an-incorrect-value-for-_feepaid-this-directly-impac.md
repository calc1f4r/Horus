---
# Core Classification
protocol: Tigris Trade
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6341
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-12-tigris-trade-contest
source_link: https://code4rena.com/reports/2022-12-tigris
github_link: https://github.com/code-423n4/2022-12-tigris-findings/issues/367

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - services
  - derivatives
  - cross_chain
  - algo-stables

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - chaduke
  - 0Kage
---

## Vulnerability Title

[M-11] _handleOpenFees returns an incorrect value for _feePaid. This directly impacts margin calculations

### Overview


This bug report is about the incorrect formula for calculating the 'fee paid' in line 734 of the Trading.sol file in the code-423n4/2022-12-tigris repository. This incorrect formula leads to incorrect margin calculations which directly affects the trader margin and associated fee calculations. This is considered a high risk vulnerability. 

The issue is that the formula for 'fee paid' is missing to account for the '2*referralFee' component when calculating '_feePaid'. The '_feePaid' should be the sum of '_daoFeesPaid', 'burnerFee' and 'botFee'. The '_daoFeesPaid' is calculated from '_fees.daoFees' which itself is calculated by subtracting '2*referralFee' and 'botFee'. When 'burnerFee' and 'botFee' are added back to '_feePaid', the '2*referralFee' is not being added back which results in under calculating the '_feePaid' and affects the rewards paid to the protocol NFT holders. 

The recommended mitigation step is to replace the formula in line 734 with one that adds back the '_fees.RefferalFees*2'. This should resolve the incorrect margin calculations and associated fee calculations.

### Original Finding Content

## Lines of code

https://github.com/code-423n4/2022-12-tigris/blob/588c84b7bb354d20cbca6034544c4faa46e6a80e/contracts/Trading.sol#L178
https://github.com/code-423n4/2022-12-tigris/blob/588c84b7bb354d20cbca6034544c4faa46e6a80e/contracts/Trading.sol#L734


## Vulnerability details

## Impact

Formula for `fee paid` in [Line 734](https://github.com/code-423n4/2022-12-tigris/blob/main/contracts/Trading.sol#L734) is incorrect leading to incorrect margin calculations. Since this directly impacts the trader margin and associated fee calculations, I've marked as HIGH risk

On initiating a market order, `Margin` is adjusted for the `fees` that is charged by protocol. This adjustment is in [Line 178 of Trading](https://github.com/code-423n4/2022-12-tigris/blob/588c84b7bb354d20cbca6034544c4faa46e6a80e/contracts/Trading.sol#L178). Fees computed by `_handleOpenFees ` is deducted from Initial margin posted by user.

formula misses to account the `2*referralFee` component while calculaing `_feePaid`

## Proof of Concept
Note that `_feePaid` as per formula in Line 734 is the sum of `_daoFeesPaid', and sum of `burnerFee` & `botFee`. `_daoFeesPaid` is calculated from `_fees.daoFees` which itself is calculated by subtracting `2*referralFee` and `botFee`. 

So when we add back `burnerFee` and `botFee` to `_feePaid`, we are missing to add back the `2*referralFee`  which was earlier excluded when calculating `_daoFeesPaid`. While `botFee` is added back correctly, same adjustment is not being done viz-a-viz referral fee.

 This results in under calculating the `_feePaid` and impacts the rewards paid to the protocol NFT holders.


## Tools Used

## Recommended Mitigation Steps

Suggest replacing the formula in line 734 with below (adding back _fees.referralFees*2)

```
            _feePaid =
                _positionSize
                * (_fees.burnFees + _fees.botFees + _fees.referralFees*2 ) 
                / DIVISION_CONSTANT // divide by 100%
                + _daoFeesPaid;
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Tigris Trade |
| Report Date | N/A |
| Finders | chaduke, 0Kage |

### Source Links

- **Source**: https://code4rena.com/reports/2022-12-tigris
- **GitHub**: https://github.com/code-423n4/2022-12-tigris-findings/issues/367
- **Contest**: https://code4rena.com/contests/2022-12-tigris-trade-contest

### Keywords for Search

`vulnerability`

