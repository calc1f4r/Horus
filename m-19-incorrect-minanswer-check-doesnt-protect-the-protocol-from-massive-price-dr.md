---
# Core Classification
protocol: Peapods
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52771
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/749
source_link: none
github_link: https://github.com/sherlock-audit/2025-01-peapods-finance-judging/issues/426

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
  - pkqs90
  - X77
  - TessKimy
---

## Vulnerability Title

M-19: Incorrect `minAnswer` check doesn't protect the protocol from massive price drops

### Overview


Bug Report Summary:

The Chainlink Single Price Oracle has an incorrect `minAnswer` check that can lead to issues with the protocol. This check is not triggered correctly and can result in incorrect price information being used. This has a low likelihood of occurring but has happened before with LUNA. The impact of this bug is that users can buy assets at inflated prices and use them as collateral, leading to borrowing of assets at an inflated price. To mitigate this issue, a reasonable gap should be decided for the `minAnswer` check.

### Original Finding Content

Source: https://github.com/sherlock-audit/2025-01-peapods-finance-judging/issues/426 

## Found by 
TessKimy, X77, pkqs90

### Summary

Incorrect `minAnswer` check doesn't protect the protocol from massive price drops

### Root Cause

In [Chainlink Single Price Oracle](https://github.com/sherlock-audit/2025-01-peapods-finance/blob/main/contracts/contracts/oracle/ChainlinkSinglePriceOracle.sol#L117), `minAnswer` and  `maxAnswer` checks are handled incorrectly. Let say Chainlink returns 1e17 `minAnswer` value for ETH/USD pair. It means aggregator will never return lesser this value. But single price oracle checks it's lower than that value or not.

```solidity
        if (_answer > _max || _answer < _min) {
            _isValid = false;
        }
```

In conclusion, this if check will never triggered in time correctly.

### Internal Pre-conditions

No need

### External Pre-conditions

1. Actual price of the assets should be lower than `minAnswer` or higher than `maxAnswer`

### Attack Path

1. I can give an example from LUNA's massive price drop
2. LUNA's price drops through zero
3. Chainlink won't return lower than `minAnswer` value
4. Protocol will use wrong price information and it can't even detect it as bad data

### Impact

This is low likelihood issue but it's happened before in history ( LUNA ). Users can buy from real price in external pools and they can use it as collateral by pairing it with pTKN and then they can borrow asset using this inflated price.

### Mitigation

Decide a reasonable gap for it. Because Chainlink won't update the price of the asset's price is lower than min answer and the last answer doesn't have to be equal to minAnswer value.

minAnswer + gap > returned value

This check is much better than just checking minimum answer

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Peapods |
| Report Date | N/A |
| Finders | pkqs90, X77, TessKimy |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-01-peapods-finance-judging/issues/426
- **Contest**: https://app.sherlock.xyz/audits/contests/749

### Keywords for Search

`vulnerability`

