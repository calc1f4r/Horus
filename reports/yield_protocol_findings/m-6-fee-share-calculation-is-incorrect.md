---
# Core Classification
protocol: Surge
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6708
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/51
source_link: none
github_link: https://github.com/sherlock-audit/2023-02-surge-judging/issues/113

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
  - liquid_staking
  - cdp
  - yield
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - 0x52
  - y1cunhui
  - cccz
  - KingNFT
  - GimelSec
---

## Vulnerability Title

M-6: Fee share calculation is incorrect

### Overview


This bug report is about an issue with the fee share calculation in the Surge protocol. The current equation used to calculate the fees is incorrect and always mints too many shares for the fee recipient, resulting in them receiving more fees than they should. This is demonstrated in the example given, where the current equation yields 2 shares and the revised equation yields 1.852 shares. This results in the fee recipient receiving more fees than intended, resulting in less interest for LPs. The code snippet and recommendation for a modified equation are provided.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-02-surge-judging/issues/113 

## Found by 
y1cunhui, GimelSec, KingNFT, 0x52, cccz

## Summary

Fees are given to the feeRecipient by minting them shares. The current share calculation is incorrect and always mints too many shares the fee recipient, giving them more fees than they should get.

## Vulnerability Detail

The current equation is incorrect and will give too many shares, which is demonstrated in the example below.

Example:

    _supplied = 100
    _totalSupply = 100
    
    _interest = 10
    fee = 2

Calculate the fee with the current equation:

    _accuredFeeShares = fee * _totalSupply / supplied = 2 * 100 / 100 = 2

This yields 2 shares. Next calculate the value of the new shares:

    2 * 110 / 102 = 2.156

The value of these shares yields a larger than expected fee. Using a revised equation gives the correct amount of fees:

    _accuredFeeShares = (_totalSupply * fee) / (_supplied + _interest - fee) = 2 * 100 / (100 + 10 - 2) = 1.852
    
    1.852 * 110 / 101.852 = 2

This new equation yields the proper fee of 2.

## Impact

Fee recipient is given more fees than intended, which results in less interest for LPs

## Code Snippet

https://github.com/sherlock-audit/2023-02-surge/blob/main/surge-protocol-v1/src/Pool.sol#L161-L165

## Tool used

[Solidity YouTube Tutorial](https://www.youtube.com/watch?v=dQw4w9WgXcQ)

## Recommendation

Use the modified equation shown above:

        uint fee = _interest * _feeMantissa / 1e18;
        // 13. Calculate the accrued fee shares
    -   _accruedFeeShares = fee * _totalSupply / _supplied; // if supplied is 0, we will have returned at step 7
    +   _accruedFeeShares = fee * (_totalSupply * fee) / (_supplied + _interest - fee); // if supplied is 0, we will have returned at step 7
        // 14. Update the total supply
        _currentTotalSupply += _accruedFeeShares;

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Surge |
| Report Date | N/A |
| Finders | 0x52, y1cunhui, cccz, KingNFT, GimelSec |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-02-surge-judging/issues/113
- **Contest**: https://app.sherlock.xyz/audits/contests/51

### Keywords for Search

`vulnerability`

