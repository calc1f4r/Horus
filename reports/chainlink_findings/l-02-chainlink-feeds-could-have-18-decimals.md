---
# Core Classification
protocol: GainsNetwork-February
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37807
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/GainsNetwork-security-review-February.md
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[L-02] Chainlink feeds could have 18 decimals

### Overview

See description below for full details.

### Original Finding Content

Multiple places in the code are built with the assumption that all Chainlink USD price feeds have 8 decimals, for example:

```solidity
File: PriceAggregatorUtils.sol
360:     function getLinkFee(
361:         uint8 _collateralIndex,
362:         uint16 _pairIndex,
363:         uint256 _positionSizeCollateral // collateral precision
364:     ) internal view returns (uint256) {
365:         (, int256 linkPriceUsd, , , ) = _getStorage().linkUsdPriceFeed.latestRoundData();
366:
367:         // NOTE: all [token / USD] feeds are 8 decimals
368:         return
369:             (getUsdNormalizedValue(
370:                 _collateralIndex,
371:                 _getMultiCollatDiamond().pairOracleFeeP(_pairIndex) * _positionSizeCollateral
372:             ) * 1e8) /
373:             uint256(linkPriceUsd) /
374:             PRECISION /
375:             100;
376:     }
```

However, there are USD price feeds that have 18 decimals, for example, PEPE/USD on Arbitrum:
[Arbiscan link](https://arbiscan.io/address/0x02DEd5a7EDDA750E3Eb240b54437a54d57b74dBE#readContract#F3)

While this token is not expected as a protocol collateral at this moment, some future tokens with 18 decimal feeds could be, and integration of such tokens would require a protocol upgrade.

Consider saving price feed decimals number per each collateral during its adding and use this value in price calculations.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | GainsNetwork-February |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/GainsNetwork-security-review-February.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

