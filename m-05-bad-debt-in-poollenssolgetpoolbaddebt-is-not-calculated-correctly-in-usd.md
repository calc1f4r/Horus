---
# Core Classification
protocol: Venus Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20774
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-05-venus
source_link: https://code4rena.com/reports/2023-05-venus
github_link: https://github.com/code-423n4/2023-05-venus-findings/issues/316

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
finders_count: 4
finders:
  - 0xStalin
  - volodya
  - peanuts
  - jasonxiale
---

## Vulnerability Title

[M-05] Bad Debt in PoolLens.sol#getPoolBadDebt() is not calculated correctly in USD

### Overview


A bug has been identified in the code of two Ethereum smart contracts, PoolLens.sol and Shortfall.sol. The bug is related to the calculation of bad debt in USD. In PoolLens.sol, bad debt in USD is calculated by multiplying the bad debt of the VToken market by the underlying price. However, in Shortfall, bad debt in USD is calculated by the bad debt of the VToken market by the underlying price and divided by 1e18. This causes the badDebt in USD in PoolLens.sol to be massively inflated.

The recommended mitigation step is to normalize the decimals of the bad debt calculation in getPoolBadDebt(). This will ensure that the pool debt is calculated correctly. The assessed type of the bug is Decimal.

### Original Finding Content


### Proof of Concept

In `PoolLens.sol#getPoolBadDebt()`, bad debt is calculated as such:

                badDebt.badDebtUsd =
                    VToken(address(markets[i])).badDebt() *
                    priceOracle.getUnderlyingPrice(address(markets[i]));
                badDebtSummary.badDebts[i] = badDebt;
                totalBadDebtUsd = totalBadDebtUsd + badDebt.badDebtUsd;

In `Shortfall.sol#\_startAuction()`, bad debt is calculated as such:

            uint256[] memory marketsDebt = new uint256[](marketsCount);
            auction.markets = new VToken[](marketsCount);

            for (uint256 i; i < marketsCount; ++i) {
                uint256 marketBadDebt = vTokens[i].badDebt();

                priceOracle.updatePrice(address(vTokens[i]));
                uint256 usdValue = (priceOracle.getUnderlyingPrice(address(vTokens[i])) * marketBadDebt) / 1e18;

                poolBadDebt = poolBadDebt + usdValue;

Focus on the line with the `priceOracle.getUnderlyingPrice`. In `PoolLens.sol#getPoolBadDebt`, `badDebt` in USD is calculated by multiplying the bad debt of the VToken market by the underlying price. However, in `Shortfall`, `badDebt` in USD is calculated by the bad debt of the VToken market by the underlying price and divided by 1e18.

The `PoolLens#getPoolBadDebt()` function doesn't divide the debt in USD by 1e18.

This is what the function is actually counting:

Let's say that the VToken market has a `badDebt` of 1.3 ETH (1e18 ETH). The pool intends to calculate 1.3 ETH in terms of USD, so it calls the oracle to determine the price of ETH. Let's say the price of ETH is 1500 USD. The total pool debt should be 1.3 &ast; 1500 = 1950 USD. In decimal calculation, the pool debt should be 1.3e18 &ast; 1500e18 (if oracle returns in 18 decimal places) / 1e18 = 1950e18.

The badDebt in USD in `PoolLens.sol#getPoolBadDebt()` will be massively inflated.

### Tools Used

VSCode

### Recommended Mitigation Steps

Normalize the decimals of the bad debt calculation in `getPoolBadDebt()`.

                badDebt.badDebtUsd =
                    VToken(address(markets[i])).badDebt() *
    +               priceOracle.getUnderlyingPrice(address(markets[i])) / 1e18;
                badDebtSummary.badDebts[i] = badDebt;
                totalBadDebtUsd = totalBadDebtUsd + badDebt.badDebtUsd;

### Assessed type

Decimal

**[chechu (Venus) confirmed](https://github.com/code-423n4/2023-05-venus-findings/issues/316#issuecomment-1560138640)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Venus Protocol |
| Report Date | N/A |
| Finders | 0xStalin, volodya, peanuts, jasonxiale |

### Source Links

- **Source**: https://code4rena.com/reports/2023-05-venus
- **GitHub**: https://github.com/code-423n4/2023-05-venus-findings/issues/316
- **Contest**: https://code4rena.com/reports/2023-05-venus

### Keywords for Search

`vulnerability`

