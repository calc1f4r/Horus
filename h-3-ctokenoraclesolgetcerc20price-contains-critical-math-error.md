---
# Core Classification
protocol: Sentiment
chain: everychain
category: uncategorized
vulnerability_type: decimals

# Attack Vector Details
attack_type: decimals
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3351
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/1
source_link: none
github_link: https://github.com/sherlock-audit/2022-08-sentiment-judging/tree/main/021-H

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 2

# Context Tags
tags:
  - decimals

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - 0x52
---

## Vulnerability Title

H-3: CTokenOracle.sol#getCErc20Price contains critical math error

### Overview


This bug report is about an issue found in the CTokenOracle.sol#getCErc20Price contract. The issue is a math error that immensely overvalues CTokens, which could lead to all lenders being drained of all their funds due to excessive over valuation of CTokens. The math error is in line 74, where IERC20(underlying).decimals() is not raised to the power of 10. The Sentiment Team fixed the issue as recommended by changing line 74 to return cToken.exchangeRateStored().mulDivDown(1e8 , 10 ** IERC20(underlying).decimals()).mulWadDown(oracle.getPrice(underlying)); and Lead Senior Watson confirmed the fix.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-08-sentiment-judging/tree/main/021-H 
## Found by 
0x52

## Summary

CTokenOracle.sol#getCErc20Price contains a math error that immensely overvalues CTokens

## Vulnerability Detail

[CTokenOracle.sol#L66-L76](https://github.com/sentimentxyz/oracle/blob/59b26a3d8c295208437aad36c470386c9729a4bc/src/compound/CTokenOracle.sol#L66-L76)

    function getCErc20Price(ICToken cToken, address underlying) internal view returns (uint) {
        /*
            cToken Exchange rates are scaled by 10^(18 - 8 + underlying token decimals) so to scale
            the exchange rate to 18 decimals we must multiply it by 1e8 and then divide it by the
            number of decimals in the underlying token. Finally to find the price of the cToken we
            must multiply this value with the current price of the underlying token
        */
        return cToken.exchangeRateStored()
        .mulDivDown(1e8 , IERC20(underlying).decimals())
        .mulWadDown(oracle.getPrice(underlying));
    }

In L74, IERC20(underlying).decimals() is not raised to the power of 10. The results in the price of the LP being overvalued by many order of magnitudes. A user could deposit one CToken and drain the reserves of every liquidity pool.

## Impact

All lenders could be drained of all their funds due to excessive over valuation of CTokens cause by this error

## Code Snippet

[CTokenOracle.sol#L66-L76](https://github.com/sentimentxyz/oracle/blob/59b26a3d8c295208437aad36c470386c9729a4bc/src/compound/CTokenOracle.sol#L66-L76)

## Tool used

Manual Review

## Recommendation

Fix the math error by changing L74:

    return cToken.exchangeRateStored()
    .mulDivDown(1e8 , 10 ** IERC20(underlying).decimals())
    .mulWadDown(oracle.getPrice(underlying));
       
## Sentiment Team
Fixed as recommended. PR [here](https://github.com/sentimentxyz/oracle/pull/43).

## Lead Senior Watson
Confirmed fix.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 2/5 |
| Audit Firm | Sherlock |
| Protocol | Sentiment |
| Report Date | N/A |
| Finders | 0x52 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-08-sentiment-judging/tree/main/021-H
- **Contest**: https://app.sherlock.xyz/audits/contests/1

### Keywords for Search

`Decimals`

