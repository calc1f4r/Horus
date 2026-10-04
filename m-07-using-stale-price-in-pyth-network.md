---
# Core Classification
protocol: Astrolab
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58111
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Astrolab-security-review.md
github_link: none

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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-07] Using stale price in Pyth Network

### Overview


This bug report discusses a problem with the `StrategyV5Pyth` function, which is used to calculate asset values and share prices. The report states that the function uses `pyth.getPriceUnsafe` to obtain price feeds, but this can lead to inaccurate calculations if the price is not updated. The report recommends using `pyth.updatePriceFeeds` and `pyth.getPrice` instead, and provides an example for how to do so. This bug has a high impact on accuracy, but a low likelihood of occurring.

### Original Finding Content

## Severity

**Impact:** High - Using stale prices leads to inaccurate calculations of total asset values and share prices.

**Likelihood:** Low - Price can be stale frequently if there is no update

## Description

The `StrategyV5Pyth` uses `pyth.getPriceUnsafe` for obtaining Pyth oracle price feeds to calculate the asset/input exchange rate.

        function assetExchangeRate(uint8 inputId) public view returns (uint256) {
            if (inputPythIds[inputId] == assetPythId)
                return weiPerShare; // == weiPerUnit of asset == 1:1
            PythStructs.Price memory inputPrice = pyth.getPriceUnsafe(inputPythIds[inputId]);
            PythStructs.Price memory assetPrice = pyth.getPriceUnsafe(assetPythId);
            ...
        }

However, from the Pyth documents, using the getPriceUnsafe can return stale price if the price is not updated.

        /// @notice Returns the price of a price feed without any sanity checks.
        /// @dev This function returns the most recent price update in this contract without any recency checks.
        /// This function is unsafe as the returned price update may be arbitrarily far in the past.
        ///
        /// Users of this function should check the `publishTime` in the price to ensure that the returned price is
        /// sufficiently recent for their application. If you are considering using this function, it may be
        /// safer / easier to use either `getPrice` or `getPriceNoOlderThan`.
        /// @return price - please read the documentation of PythStructs.Price to understand how to use this safely.
        function getPriceUnsafe(
            bytes32 id
        ) external view returns (PythStructs.Price memory price);

The `assetExchangeRate` function doesn't verify `Price.publishTime`, potentially leading to outdated exchange rates, incorrect investment calculations, and distorted total asset values.

## Recommendations

Using `pyth.updatePriceFeeds` for updating prices, followed by `pyth.getPrice` for retrieval.
Following the example in: https://github.com/pyth-network/pyth-sdk-solidity/blob/main/README.md#example-usage

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Astrolab |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Astrolab-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

