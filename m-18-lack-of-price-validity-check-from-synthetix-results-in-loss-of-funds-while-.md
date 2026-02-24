---
# Core Classification
protocol: Polynomial Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20255
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-03-polynomial
source_link: https://code4rena.com/reports/2023-03-polynomial
github_link: https://github.com/code-423n4/2023-03-polynomial-findings/issues/59

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
  - DadeKuma
  - \_\_141345\_\_
  - rbserver
---

## Vulnerability Title

[M-18] Lack of price validity check from Synthetix results in loss of funds while liquidating

### Overview


This bug report is about a lack of a validity check while liquidating, which can lead to the loss of funds. This is because the price could be invalid momentarily from Synthetix due to high volatility or other issues. There is no `isInvalid` check in `getMarkPrice` and `getAssetPrice` functions, which must be false before closing the liquidation. This check is used in other similar functions though. If this isn't the case, liquidation could result in under-liquidation (a loss for the user) or over-liquidation (a loss for the protocol). The same problem is also present in `LiquidityPool` when calculating the `orderFee`.

To mitigate the issue, a check must be added to be sure that `isInvalid` is false in both `markPrice` and `collateralPrice` before liquidating. The severity of the issue was initially disagreed upon, but was later confirmed as Medium.

### Original Finding Content


Lack of a validity check while liquidating results in loss of funds, as the price could be invalid momentarily from Synthetix due to high volatility or other issues.

### Proof of Concept

There isn't a check for `isInvalid` in `getMarkPrice` and `getAssetPrice`, which must be false before closing the liquidation:

```solidity
File: src/ShortCollateral.sol

134:         (uint256 markPrice,) = exchange.getMarkPrice();
135:         (uint256 collateralPrice,) = synthetixAdapter.getAssetPrice(currencyKey);

```

This check is used in other similar functions that fetch the price:

    File: src/ShortCollateral.sol

    194:         (uint256 markPrice, bool isInvalid) = exchange.getMarkPrice();
    195:         require(!isInvalid);

    205:         (collateralPrice, isInvalid) = synthetixAdapter.getAssetPrice(collateralKey);
    206:         require(!isInvalid);

This must be present to ensure that the price fetched from Synthetix is not stale or invalid.

If this isn't the case, a liquidation could result in under-liquidation (a loss for the user) or over-liquidation (a loss for the protocol).

The same problem is also present in `LiquidityPool`:

```solidity
File: src/LiquidityPool.sol

388:         (uint256 markPrice,) = exchange.getMarkPrice();
```

As the `markPrice` is not validated when calculating the `orderFee`.

### Recommended Mitigation Steps

Add a check to be sure that `isInvalid` is false in both `markPrice` and `collateralPrice` before liquidating.

**[rivalq (Polynomial) disagreed with severity](https://github.com/code-423n4/2023-03-polynomial-findings/issues/59#issuecomment-1495749537)**

**[Dravee (judge) commented](https://github.com/code-423n4/2023-03-polynomial-findings/issues/59#issuecomment-1517792823):**
 > Would like @rivalq 's thought on the severity and validity.<br>
> Was there a reason for an absence on these checks? (Like a redundancy because it would revert somewhere on an invalid price).
> 
> It was also raised by the warden that an invalid price could be 0 through these:
> - `PerpsV2MarketViews.sol#L45-L50`
> - `PerpsV2Market.sol#L124-L126`
> 
> How likely is this to happen?

**[mubaris (Polynomial) confirmed and commented](https://github.com/code-423n4/2023-03-polynomial-findings/issues/59#issuecomment-1518535573):**
 > This seems like a miss from our side.

**[Dravee (judge) commented](https://github.com/code-423n4/2023-03-polynomial-findings/issues/59#issuecomment-1521468233):**
 > Agreed on Medium severity.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Polynomial Protocol |
| Report Date | N/A |
| Finders | DadeKuma, \_\_141345\_\_, rbserver |

### Source Links

- **Source**: https://code4rena.com/reports/2023-03-polynomial
- **GitHub**: https://github.com/code-423n4/2023-03-polynomial-findings/issues/59
- **Contest**: https://code4rena.com/reports/2023-03-polynomial

### Keywords for Search

`vulnerability`

