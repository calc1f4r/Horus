---
# Core Classification
protocol: Yield
chain: everychain
category: oracle
vulnerability_type: stale_price

# Attack Vector Details
attack_type: stale_price
affected_component: oracle

# Source Information
source: solodit
solodit_id: 1351
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-01-yield-convex-contest
source_link: https://code4rena.com/reports/2022-01-yield
github_link: https://github.com/code-423n4/2022-01-yield-findings/issues/136

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 4

# Context Tags
tags:
  - stale_price
  - oracle
  - chainlink

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - yield
  - services

# Audit Details
report_date: unknown
finders_count: 12
finders:
  - hack3r-0m
  - sirhashalot
  - cccz
  - leastwood
  - throttle
---

## Vulnerability Title

[M-01] Oracle data feed is insufficiently validated

### Overview


This bug report is about the 'throttle' handle. The vulnerability in this handle is that the Oracle data feed is insufficiently validated, which can lead to a stale price and wrong return value. The proof of concept is that there is no check for stale price and round completeness, and the impact of this is that the quoteAmount return value can be wrong. The tool used for this bug report is manual review. The recommended mitigation steps are to validate the data feed, which can be done by adding code to the _peek() function to check for stale prices and round completeness. This code will require the prices to be greater than zero, and the round to be complete.

### Original Finding Content

_Submitted by throttle, also found by 0x1f8b, cccz, defsec, hack3r-0m, hyh, kenzo, leastwood, sirhashalot, TomFrenchBlockchain, WatchPug, and ye0lde_

Price can be stale and can lead to wrong `quoteAmount` return value

#### Proof of Concept

Oracle data feed is insufficiently validated. There is no check for stale price and round completeness.
Price can be stale and can lead to wrong `quoteAmount` return value

```javascript
function _peek(
    bytes6 base,
    bytes6 quote,
    uint256 baseAmount
) private view returns (uint256 quoteAmount, uint256 updateTime) {
    ...

    (, int256 daiPrice, , , ) = DAI.latestRoundData();
    (, int256 usdcPrice, , , ) = USDC.latestRoundData();
    (, int256 usdtPrice, , , ) = USDT.latestRoundData();

    require(
        daiPrice > 0 && usdcPrice > 0 && usdtPrice > 0,
        "Chainlink pricefeed reporting 0"
    );

    ...
}
```

#### Recommended Mitigation Steps

Validate data feed

```javascript
function _peek(
    bytes6 base,
    bytes6 quote,
    uint256 baseAmount
) private view returns (uint256 quoteAmount, uint256 updateTime) {
    ...
    (uint80 roundID, int256 daiPrice, , uint256 timestamp, uint80 answeredInRound) = DAI.latestRoundData();
    require(daiPrice > 0, "ChainLink: DAI price <= 0");
    require(answeredInRound >= roundID, "ChainLink: Stale price");
    require(timestamp > 0, "ChainLink: Round not complete");

    (roundID, int256 usdcPrice, , timestamp, answeredInRound) = USDC.latestRoundData();
    require(usdcPrice > 0, "ChainLink: USDC price <= 0");
    require(answeredInRound >= roundID, "ChainLink: Stale USDC price");
    require(timestamp > 0, "ChainLink: USDC round not complete");

    (roundID, int256 usdtPrice, , timestamp, answeredInRound) = USDT.latestRoundData();
    require(usdtPrice > 0, "ChainLink: USDT price <= 0");
    require(answeredInRound >= roundID, "ChainLink: Stale USDT price");
    require(timestamp > 0, "ChainLink: USDT round not complete");

    ...
}
```

**[iamsahu (Yield) confirmed and resolved](https://github.com/code-423n4/2022-01-yield-findings/issues/136)**

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2022-01-yield-findings/issues/136#issuecomment-1039639929):**
 > When using Chainlink Price feeds it is important to ensure the price feed data was updated recently.
> While getting started with chainlink requires just one line of code, it is best to add additional checks for in production environments.
> 
> I believe the finding to be valid and Medium severity to be appropriate.
> 
> The sponsor has mitigated in a subsequent PR.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Yield |
| Report Date | N/A |
| Finders | hack3r-0m, sirhashalot, cccz, leastwood, throttle, WatchPug, TomFrenchBlockchain, 0x1f8b, ye0lde, hyh, kenzo, defsec |

### Source Links

- **Source**: https://code4rena.com/reports/2022-01-yield
- **GitHub**: https://github.com/code-423n4/2022-01-yield-findings/issues/136
- **Contest**: https://code4rena.com/contests/2022-01-yield-convex-contest

### Keywords for Search

`Stale Price, Oracle, Chainlink`

