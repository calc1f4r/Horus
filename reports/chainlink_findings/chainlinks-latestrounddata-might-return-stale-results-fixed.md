---
# Core Classification
protocol: USDi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55395
audit_firm: ConsenSys
contest_link: none
source_link: https://diligence.consensys.io/audits/2025/04/usdi/
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
finders_count: 2
finders:
  - George Kobakhidze
  -  Vladislav Yaroshuk
                        
---

## Vulnerability Title

Chainlink’s latestRoundData Might Return Stale Results ✓ Fixed

### Overview

See description below for full details.

### Original Finding Content

...

Export to GitHub ...

Set external GitHub Repo ...

Export to Clipboard (json)

Export to Clipboard (text)

#### Resolution

Addressed in commit `45181fbc99153658f32fd6202bd0604e3e80d588` by removing the price oracle altogether as well as the associated functions for checking that the `backingToken` price is within acceptable range of the peg. The USDi team acknowledges that the token can be off peg at specific times and accepts that risk as the `backingToken` conversion will happen offchain after they receive mint and withdrawal requests from their clients, and the price oracle in the smart contract does not define any price or conversion logic for `USDi`. Specifically, since the intended `backingToken` is `USDC`, the USDi team feels comfortable with accepting the off-peg risk.

#### Description

The `_getBackingTokenPriceInUsd` function fetches the latest price from the oracle without verifying the freshness of the data. Without a freshness check, the contract could rely on outdated price data, potentially exposing the protocol to price manipulation attacks or significant economic inaccuracies.

#### Examples

**contracts/USDiCoin.sol:L168-L198**

```
/// @notice Internal helper to get the backing token’s price in USD from the oracle
/// Typically scaled by 1e8 if we’re using a standard Chainlink feed.
function _getBackingTokenPriceInUsd() internal view returns (uint256) {
    (
        /* uint80 roundID */,
        int256 answer,
        /* uint256 startedAt */,
        /* uint256 updatedAt */,
        /* uint80 answeredInRound */
    ) = backingTokenPriceOracle.latestRoundData();
    require(answer > 0, "Invalid price from oracle");
    return uint256(answer); // e.g. 100000000 => $1.00
}

/// @notice Ensures the backing token’s price is within an acceptable range around $1.00
function _requireBackingTokenPegInRange() internal view {
    // 1 USD in 1e8 is 100000000
    uint256 oneUsd = 100000000;

    // offset = (oneUsd * maxDeviationBps) / 10000
    // e.g. if maxDeviationBps=200 => offset=2% of oneUsd => 2000000 => $0.02
    uint256 offset = (oneUsd * maxDeviationBps) / 10000;
    uint256 lowerBound = oneUsd - offset;
    uint256 upperBound = oneUsd + offset;

    uint256 currentPrice = _getBackingTokenPriceInUsd();
    require(
        currentPrice >= lowerBound && currentPrice <= upperBound,
        "Backing token price out of range"
    );
}

```

#### Recommendation

We recommend implementing a freshness check by validating the `updatedAt` timestamp returned by the oracle. Ensure the data retrieved is within a reasonable timeframe (e.g., not older than several hours, depending on protocol needs) before using it within the contract logic.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | USDi |
| Report Date | N/A |
| Finders | George Kobakhidze,  Vladislav Yaroshuk
                         |

### Source Links

- **Source**: https://diligence.consensys.io/audits/2025/04/usdi/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

