---
# Core Classification
protocol: Licredity
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62351
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-01-cyfrin-licredity-v2.0.md
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4.5

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Immeas
  - Alexzoid
  - ChainDefenders](https://x.com/ChDefendersEth) ([0x539](https://x.com/1337web3) & [PeterSR
---

## Vulnerability Title

Missing Chainlink oracle staleness check

### Overview


This bug report discusses an issue with the `getPrice` function in the `ChainlinkFeedLibrary`. This function fetches the latest price from a Chainlink feed, but does not check if the data is stale. This means that the protocol may use outdated or inaccurate price information, which could be exploited by attackers. The report recommends implementing a staleness check in the function to prevent this issue. The bug has been fixed in the code and verified by Cyfrin.

### Original Finding Content

**Description:** The `getPrice` function in `ChainlinkFeedLibrary` fetches the latest price from a Chainlink feed using `latestRoundData`, but does not check if the returned data is stale. Chainlink feeds can become stale if no new price updates have occurred for a significant period, which may result in outdated or inaccurate price information being used by the protocol. The Chainlink interface provides `updatedAt` and `answeredInRound` fields specifically to help consumers detect stale or incomplete data, but these are ignored in the current implementation.

**Impact:** The protocol may use outdated or stale price data, leading to incorrect valuations, margin calculations, or other critical logic. This can be exploited by attackers if they can manipulate or anticipate periods of feed staleness. Users and integrators may be exposed to increased risk due to reliance on old price information.

**Proof of Concept:** Add a `ChainlinkFeedLibraryTest.t.sol` file in the `./oracle/test/` folder:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "forge-std/Test.sol";
import {ChainlinkFeedLibrary} from "./../src/libraries/ChainlinkFeedLibrary.sol";
import {AggregatorV3Interface} from "./../src/interfaces/external/AggregatorV3Interface.sol";

contract ChainlinkFeedLibraryTest is Test {
    address internal constant MOCK_FEED = address(0xFEED);

    function test_getPrice_acceptsStaleData() public {
        vm.warp(block.timestamp + 10 days); // Set the block timestamp to 10 day in the future

        // Mock the Chainlink feed to return a price but with stale timestamp (e.g., updated 1 day ago)
        // In a secure implementation, this should revert due to staleness, but here it does not
        vm.mockCall(
            MOCK_FEED,
            abi.encodeWithSelector(AggregatorV3Interface.latestRoundData.selector),
            abi.encode(
                uint80(1),                  // roundId
                int256(100e8),              // answer
                uint256(0),                 // startedAt (unused)
                block.timestamp - 1 days,   // updatedAt (stale)
                uint80(1)                   // answeredInRound
            )
        );

        // Call getPrice; it should return the stale price without reverting
        uint256 price = ChainlinkFeedLibrary.getPrice(AggregatorV3Interface(MOCK_FEED));

        // Assert that the stale price is returned
        assertEq(price, 100e8);
    }
}
```

**Recommended Mitigation:** Implement a staleness check in the `getPrice` function. For example, require that `updatedAt` is within an acceptable time window (e.g., not older than a configurable threshold) and that `answeredInRound >= roundId`. If the data is stale, revert or return an error. Example check:

```solidity
(uint80 roundId, int256 answer,, uint256 updatedAt, uint80 answeredInRound) = feed.latestRoundData();
require(updatedAt >= block.timestamp - MAX_STALENESS, "Chainlink: stale price");
require(answeredInRound >= roundId, "Chainlink: incomplete round");
```

Where `MAX_STALENESS` is a reasonable time threshold set by the protocol.

**Licredity:** Fixed in [PR#18](https://github.com/Licredity/licredity-v1-oracle/pull/18/files), commit [`5a615c0`](https://github.com/Licredity/licredity-v1-oracle/commit/5a615c0eabd71597931680c4321eb6209d29eb8c)

**Cyfrin:** Verified. A field `maxStaleness` added to `ChainlinkOracleConfig` which `governor` can update.

\clearpage

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4.5/5 |
| Audit Firm | Cyfrin |
| Protocol | Licredity |
| Report Date | N/A |
| Finders | Immeas, Alexzoid, ChainDefenders](https://x.com/ChDefendersEth) ([0x539](https://x.com/1337web3) & [PeterSR |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-01-cyfrin-licredity-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

