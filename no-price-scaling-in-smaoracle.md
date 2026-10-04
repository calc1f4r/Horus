---
# Core Classification
protocol: Tracer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6739
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Tracer-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Tracer-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - yield
  - services
  - derivatives

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Emanuele Ricci
  - Christoph Michel
  - Rusty (f7dd60e9cfad19996d73)
  - Gerard Persoon
---

## Vulnerability Title

No price scaling in SMAOracle

### Overview


This bug report is about the SMAOracle and ChainlinkOracleWrapper contracts. The update() function of the SMAOracle contract does not scale the latestPrice variable, while the _latestRoundData() function of the ChainlinkOracleWrapper contract does scale via toWad(). The recommendation is to scale the latestPrice variable in the SMAOracle contract, and reintroduce the toWad() function. If the SMAOracle is only used with WAD based spot oracles, then _spotDecimals == 18 must be enforced. A PR (406) is being submitted as a mitigation for this.

### Original Finding Content

## Severity: High Risk

## Context
- `SMAOracle.sol#L82-L96`
- `ChainlinkOracleWrapper.sol#L36-L60`

## Description
The `update()` function of the `SMAOracle` contract doesn’t scale the `latestPrice` although a scaler is set in the constructor. On the other hand, the `_latestRoundData()` function of the `ChainlinkOracleWrapper` contract does scale via `toWad()`.

```solidity
contract SMAOracle is IOracleWrapper {
    constructor(..., uint256 _spotDecimals, ...) {
        ...
        require(_spotDecimals <= MAX_DECIMALS, "SMA: Decimal precision too high");
        ...
        /* `scaler ` is always <= 10^18 and >= 1 so this cast is safe */
        scaler = int256(10**(MAX_DECIMALS - _spotDecimals));
        ...
    }

    function update() internal returns (int256) {
        /* query the underlying spot price oracle */
        IOracleWrapper spotOracle = IOracleWrapper(oracle);
        int256 latestPrice = spotOracle.getPrice();
        ...
        priceObserver.add(latestPrice); // doesn 't scale latestPrice
        ...
    }
}
```

```solidity
contract ChainlinkOracleWrapper is IOracleWrapper {
    function getPrice() external view override returns (int256) {
        (int256 _price, ) = _latestRoundData();
        return _price;
    }

    function _latestRoundData() internal view returns (int256, uint80) {
        (..., int256 price, ..) = AggregatorV2V3Interface(oracle).latestRoundData();
        ...
        return (toWad(price), ...);
    }
}
```

## Recommendation
The `latestPrice` variable in the `SMAOracle` contract should be scaled, and the `toWad()` function should be re-introduced. 

**Note:** If the `SMAOracle` is only used with WAD-based spot oracles, then `_spotDecimals == 18` must be enforced.

## Tracer
We are submitting PR 406 as a mitigation for this. It is a slightly larger PR than we originally intended so as a result it will likely be submitted for several defects here. We would appreciate if each defect could be assessed against it.

## Spearbit
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Tracer |
| Report Date | N/A |
| Finders | Emanuele Ricci, Christoph Michel, Rusty (f7dd60e9cfad19996d73), Gerard Persoon |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Tracer-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Tracer-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

