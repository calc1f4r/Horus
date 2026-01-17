---
# Core Classification
protocol: Inverse Finance
chain: everychain
category: oracle
vulnerability_type: oracle

# Attack Vector Details
attack_type: oracle
affected_component: oracle

# Source Information
source: solodit
solodit_id: 5740
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-10-inverse-finance-contest
source_link: https://code4rena.com/reports/2022-10-inverse
github_link: https://github.com/code-423n4/2022-10-inverse-findings/issues/404

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
  - oracle

protocol_categories:
  - liquid_staking
  - cdp
  - services
  - synthetics

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Jeiwan
---

## Vulnerability Title

[M-11] viewPrice doesn’t always report dampened price

### Overview


This bug report is about a vulnerability in Oracle's `viewPrice` function in the code-423n4/2022-10-inverse repository on GitHub. The vulnerability impacts the public read-only functions that call it, which are used to get on-chain state and prepare values for write calls. This can cause withdrawal of a wrong amount or liquidation of a wrong debt or cause reverts.

The proof of concept was a manual review of the code, and the recommended mitigation step is to consider the change in the code provided. This change will ensure that the viewPrice is dampened until the getPrice function is called and today's price is updated.

In conclusion, this bug report is about a vulnerability in the code-423n4/2022-10-inverse repository on GitHub that impacts the public read-only functions that call it. The proof of concept was a manual review of the code, and the recommended mitigation step is to consider the change in the code provided.

### Original Finding Content

## Lines of code

https://github.com/code-423n4/2022-10-inverse/blob/3e81f0f5908ea99b36e6ab72f13488bbfe622183/src/Oracle.sol#L91


## Vulnerability details

## Impact
Oracle's `viewPrice` function doesn't report a dampened price until `getPrice` is called and today's price is updated. This will impact the public read-only functions that call it:
- [getCollateralValue](https://github.com/code-423n4/2022-10-inverse/blob/3e81f0f5908ea99b36e6ab72f13488bbfe622183/src/Market.sol#L312);
- [getCreditLimit](https://github.com/code-423n4/2022-10-inverse/blob/3e81f0f5908ea99b36e6ab72f13488bbfe622183/src/Market.sol#L334) (calls `getCollateralValue`);
- [getLiquidatableDebt](https://github.com/code-423n4/2022-10-inverse/blob/3e81f0f5908ea99b36e6ab72f13488bbfe622183/src/Market.sol#L578) (calls `getCreditLimit`);
- [getWithdrawalLimit](https://github.com/code-423n4/2022-10-inverse/blob/3e81f0f5908ea99b36e6ab72f13488bbfe622183/src/Market.sol#L370).

These functions are used to get on-chain state and prepare values for write calls (e.g. calculate withdrawal amount before withdrawing or calculate a user's debt that can be liquidated before liquidating it). Thus, wrong values returned by these functions can cause withdrawal of a wrong amount or liquidation of a wrong debt or cause reverts.
## Proof of Concept
```solidity
// src/test/Oracle.t.sol
function test_viewPriceNoDampenedPrice_AUDIT() public {
    uint collateralFactor = market.collateralFactorBps();
    uint day = block.timestamp / 1 days;
    uint feedPrice = ethFeed.latestAnswer();

    //1600e18 price saved as daily low
    oracle.getPrice(address(WETH), collateralFactor);
    assertEq(oracle.dailyLows(address(WETH), day), feedPrice);

    vm.warp(block.timestamp + 1 days);
    uint newPrice = 1200e18;
    ethFeed.changeAnswer(newPrice);
    //1200e18 price saved as daily low
    oracle.getPrice(address(WETH), collateralFactor);
    assertEq(oracle.dailyLows(address(WETH), ++day), newPrice);

    vm.warp(block.timestamp + 1 days);
    newPrice = 3000e18;
    ethFeed.changeAnswer(newPrice);

    //1200e18 should be twoDayLow, 3000e18 is current price. We should receive dampened price here.
    // Notice that viewPrice is called before getPrice.
    uint viewPrice = oracle.viewPrice(address(WETH), collateralFactor);
    uint price = oracle.getPrice(address(WETH), collateralFactor);
    assertEq(oracle.dailyLows(address(WETH), ++day), newPrice);

    assertEq(price, 1200e18 * 10_000 / collateralFactor);

    // View price wasn't dampened.
    assertEq(viewPrice, 3000e18);
}
```
## Tools Used
Manual review
## Recommended Mitigation Steps
Consider this change:
```diff
--- a/src/Oracle.sol
+++ b/src/Oracle.sol
@@ -89,6 +89,9 @@ contract Oracle {
             uint day = block.timestamp / 1 days;
             // get today's low
             uint todaysLow = dailyLows[token][day];
+            if(todaysLow == 0 || normalizedPrice < todaysLow) {
+                todaysLow = normalizedPrice;
+            }
             // get yesterday's low
             uint yesterdaysLow = dailyLows[token][day - 1];
             // calculate new borrowing power based on collateral factor
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Inverse Finance |
| Report Date | N/A |
| Finders | Jeiwan |

### Source Links

- **Source**: https://code4rena.com/reports/2022-10-inverse
- **GitHub**: https://github.com/code-423n4/2022-10-inverse-findings/issues/404
- **Contest**: https://code4rena.com/contests/2022-10-inverse-finance-contest

### Keywords for Search

`Oracle`

