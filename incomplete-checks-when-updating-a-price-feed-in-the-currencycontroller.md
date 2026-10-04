---
# Core Classification
protocol: Secured Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59985
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/secured-finance/20cad24f-5901-4107-9509-e3d5ad3acc7c/index.html
source_link: https://certificate.quantstamp.com/full/secured-finance/20cad24f-5901-4107-9509-e3d5ad3acc7c/index.html
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
finders_count: 3
finders:
  - Mustafa Hasan
  - Valerian Callens
  - Guillermo Escobero
---

## Vulnerability Title

Incomplete Checks when Updating a Price Feed in the `CurrencyController`

### Overview

See description below for full details.

### Original Finding Content

**Update**
Addressed in: `b5c21d6865e06e223faef7150739b3d9d8bbf330` and `77549829f7406112d856451058f2e1d7fe1fdb8a`.

**File(s) affected:**`CurrencyController.sol`

**Description:** The system gets prices for a given pair of tokens (A, B) (price of one token A in token B) by using functions of the contract `CurrencyController` that fetch data from Oracle price feeds implementing the interface `AggregatorV3Interface`. When no price feed exists to directly provide the price of A in the base currency used by the protocol, a sequence of price feeds is stored in a struct `CurrencyControllerStorage.PriceFeed` that has two attributes:

*   `AggregatorV3Interface[] instances` representing the sequence of price feeds to call consecutively;
*   `uint256 heartbeat` representing the update frequency of an oracle; In addition, the mapping `decimalsCaches` stores the sum of the decimals used by the instances of the price feed.

A price feed can be updated via the function `updatePriceFeed()`. However, some aspects are not checked during this update:

1.   A single `heartbeat` value is provided to apply for all items of `_priceFeeds`. However, these price feeds can have different heartbeat values, leading to possible reverts or stale data if the expected unique heartbeat does not match with the rest of the price feeds' heartbeats. Add individual heartbeat limits for each price feed.
2.   No check makes sure that the value of `_decimals` matches the sum of the decimals of each item of `_priceFeeds`
3.   No check makes sure that `heartbeat` is respected for the last price returned by the price feed
4.   No check makes sure that the last item of `_priceFeeds` returns a price in base currency. A check could at least make sure that the number of decimals matches the number of decimals of the base currency
5.   The `_updatePriceFeed()` function calls `latestRoundData()` on the provided price feeds and uses the returned price information without checking the `updatedAt` against a time limit. Perform the same checks on the `updatedAt` result value as in `_getAggregatedLastPrice()`.

**Recommendation:** Consider implementing the mentioned validations.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Secured Finance |
| Report Date | N/A |
| Finders | Mustafa Hasan, Valerian Callens, Guillermo Escobero |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/secured-finance/20cad24f-5901-4107-9509-e3d5ad3acc7c/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/secured-finance/20cad24f-5901-4107-9509-e3d5ad3acc7c/index.html

### Keywords for Search

`vulnerability`

