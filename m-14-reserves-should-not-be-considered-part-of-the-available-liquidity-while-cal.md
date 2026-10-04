---
# Core Classification
protocol: Sentiment
chain: everychain
category: logic
vulnerability_type: wrong_math

# Attack Vector Details
attack_type: wrong_math
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3370
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/1
source_link: none
github_link: https://github.com/sherlock-audit/2022-08-sentiment-judging/tree/main/266-M

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 3

# Context Tags
tags:
  - wrong_math
  - business_logic

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
  - WATCHPUG
---

## Vulnerability Title

M-14: `Reserves` should not be considered part of the available liquidity while calculating the interest rate

### Overview


This bug report is about the incorrect implementation of the interest rate formula in the protocol. The formula given in the documentation states that the interest rate should be calculated by taking the ratio of borrows to the available liquidity minus reserves. However, the current implementation is using all the balance as the liquidity, resulting in an interest rate that is lower than expected. This discrepancy was found by manual review and a proof of concept was provided to demonstrate the difference between the expected and actual results. The Sentiment team then implemented the recommended changes and pushed a commit to remove a redundant call to the riskEngine. The bug was successfully resolved.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-08-sentiment-judging/tree/main/266-M 
## Found by 
WATCHPUG

## Summary

The implementation is different from the documentation regarding the interest rate formula.

## Vulnerability Detail

The formula given in the [docs](https://docs.sentiment.xyz/protocol/core/rateModel):

> Calculates Borrow rate per second:

> $$
Borrow Rate Per Second = c3 \cdot (util \cdot c1 + util^{32} \cdot c1 + util^{64} \cdot c2) \div secsPerYear
$$

> where, $util = borrows \div (liquidity - reserves + borrows)$

> $$
util=borrows \div (liquidity−reserves+borrows)
$$

https://github.com/sentimentxyz/protocol/blob/4e45871e4540df0f189f6c89deb8d34f24930120/src/tokens/LToken.sol#L217-L227

```solidity
    function getRateFactor() internal view returns (uint) {
        return (block.timestamp == lastUpdated) ?
            0 :
            ((block.timestamp - lastUpdated)*1e18)
            .mulWadUp(
                rateModel.getBorrowRatePerSecond(
                    asset.balanceOf(address(this)),
                    borrows
                )
            );
    }
```

However, the current implementation is taking all the balance as the liquidity:

https://github.com/sentimentxyz/protocol/blob/4e45871e4540df0f189f6c89deb8d34f24930120/src/core/DefaultRateModel.sol#L51-L68

```solidity
    function getBorrowRatePerSecond(
        uint liquidity,
        uint borrows
    )
        external
        view
        returns (uint)
    {
        uint util = _utilization(liquidity, borrows);
        return c3.mulDivDown(
            (
                util.mulWadDown(c1)
                + util.rpow(32, SCALE).mulWadDown(c1)
                + util.rpow(64, SCALE).mulWadDown(c2)
            ),
            secsPerYear
        );
    }
```

https://github.com/sentimentxyz/protocol/blob/4e45871e4540df0f189f6c89deb8d34f24930120/src/core/DefaultRateModel.sol#L70-L77

```solidity
    function _utilization(uint liquidity, uint borrows)
        internal
        pure
        returns (uint)
    {
        uint totalAssets = liquidity + borrows;
        return (totalAssets == 0) ? 0 : borrows.divWadDown(totalAssets);
    }
```

## Impact

Per the docs, when calculating the interest rate, `util` is the ratio of available liquidity to the `borrows`, available liquidity should not include reserves.

The current implementation is using all the balance as the `liquidity`, this will make the interest rate lower than expectation.

### PoC

Given:

- `asset.address(this) + borrows = 10000`
- `reserves = 1500, borrows = 7000`

Expected result:

When calculating `getRateFactor()`, available liquidity should be `asset.balanceOf(address(this)) - reserves = 1500, util = 7000 / 8500 = 0.82`, `getBorrowRatePerSecond() = 9114134329`

Actual result:

When calculating `getRateFactor()`, `asset.balanceOf(address(this)) = 3000, util = 0.7e18`, `getBorrowRatePerSecond() = 7763863430`

The actual interest rate is only `7763863430 / 9114134329 = 85%` of the expected rate.

## Code Snippet

## Tool used

Manual Review

## Recommendation

The implementation of `getRateFactor()` can be updated to:

```solidity
function getRateFactor() internal view returns (uint) {
    return (block.timestamp == lastUpdated) ?
        0 :
        ((block.timestamp - lastUpdated)*1e18)
        .mulWadUp(
            rateModel.getBorrowRatePerSecond(
                asset.balanceOf(address(this)) - reserves,
                borrows
            )
        );
}
```

## Sentiment Team
Removed reserves from LToken and added an alternate mechanism to collect direct fees.

## Lead Senior Watson
originationFee may result in the borrower account becoming liquidatable immediately (aka WP-M2).

## Sentiment Team
Fixed as recommended. PR [here](https://github.com/sentimentxyz/protocol/pull/236). 

## Lead Senior Watson
riskEngine.isBorrowAllowed should be removed as it's no longer needed.

## Sentiment Team
Pushed a commit to remove the redundant call to riskEngine. PR [here](https://github.com/sentimentxyz/protocol/pull/236/commits/bfc445b02784f8130181641ce0054382b4cc3ec5
).

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 3/5 |
| Audit Firm | Sherlock |
| Protocol | Sentiment |
| Report Date | N/A |
| Finders | WATCHPUG |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-08-sentiment-judging/tree/main/266-M
- **Contest**: https://app.sherlock.xyz/audits/contests/1

### Keywords for Search

`Wrong Math, Business Logic`

