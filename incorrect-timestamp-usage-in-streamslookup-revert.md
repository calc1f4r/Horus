---
# Core Classification
protocol: Part 2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49976
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/cm60h7a380000k66h6knt2vtl
source_link: none
github_link: https://github.com/Cyfrin/2025-01-zaros-part-2

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
finders_count: 2
finders:
  - 0xshoonya
  - 0xexploud
---

## Vulnerability Title

Incorrect Timestamp Usage in `StreamsLookup Revert`

### Overview


This bug report is about a mistake in the code that could lead to incorrect pricing and unfair swaps. The problem is in a function called `checkLog` in a contract called `UsdTokenSwapKeeper`. This function is supposed to use a specific time to get price data, but it uses the wrong time, causing issues with the swap execution. The bug was found through a manual review and the recommendation is to fix the code by using the correct time.

### Original Finding Content

## Summary

`checkLog` function in `UsdTokenSwapKeeper` contract uses `block.timestamp` (current time) instead of `log.timestamp` (event emission time) to query historical price data, leading to incorrect swap executions that violate user expectations and protocol integrity.

## Vulnerability Details

When a user submits a swap request via `MarketMakingEngine`, an event is emitted with a specific timestamp (stored in `log.timestamp`). Chainlink Automation Network detects this event and calls `checkLog` on `UsdTokenSwapKeeper`.The checkLog function is designed to fetch the price at the time of the event using Chainlink Data Streams. However, the code incorrectly uses `block.timestamp` (the current block time) to query the price feed:
[UsdTokenSwapKeeper.sol#L117](https://github.com/Cyfrin/2025-01-zaros-part-2/blob/35deb3e92b2a32cd304bf61d27e6071ef36e446d/src/external/chainlink/keepers/usd-token-swap-keeper/UsdTokenSwapKeeper.sol#L117)

```js
 function checkLog(
        AutomationLog calldata log,
        bytes memory
    )
        external
        view
        returns (bool upkeepNeeded, bytes memory performData)
    {

        string[] memory streams = new string[](1);
        streams[0] = self.streamId;


        // encode perform data
        bytes memory extraData = abi.encode(caller, requestId);

        revert StreamsLookup(
        DATA_STREAMS_FEED_LABEL,
        streams,
        DATA_STREAMS_QUERY_LABEL,
@>      block.timestamp, // BUG: Uses current time instead of event time
        extraData
    );
  }  
```

The `log.timestamp` is the time when the log was emitted, which corresponds to the block time when the event happened. On the other hand, `block.timestamp` is the current block's timestamp when the checkLog function is executed. These might not be the same if there's a delay between the event emission and the `checkLog` call.

In the context of fulfilling a swap request, the price data needed is the one at the time the request was made (`log.timestamp`), not the current time. If `block.timestamp` is used, the price might have changed, leading to incorrect fulfillment. This could cause issues like using outdated or incorrect prices, affecting the swap's execution.

[Chainlink's documentation](https://docs.chain.link/data-streams/reference/interfaces) example itself use `log.timestamp` for the Streams lookup in `checkLog`:

```js
  // This function uses revert to convey call information.
    // See https://eips.ethereum.org/EIPS/eip-3668#rationale for details.
    function checkLog(
        Log calldata log,
        bytes memory
    ) external returns (bool upkeepNeeded, bytes memory performData) {
        revert StreamsLookup(
            DATASTREAMS_FEEDLABEL,
            feedIds,
            DATASTREAMS_QUERYLABEL,
@>          log.timestamp,
            ""
        );
    }
```

## Impact

Using an incorrect timestamp could result in fetching price data from a different time than when the swap was actually requested, potentially leading to unfair pricing.

## Tools Used

Manual Review

## Recommendations

The correct approach should be to use `log.timestamp` to ensure the data corresponds to the event's time:

```diff
revert StreamsLookup(
    DATA_STREAMS_FEED_LABEL,
    streams,
    DATA_STREAMS_QUERY_LABEL,
-   block.timestamp,
+   log.timestamp
    extraData
);
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Part 2 |
| Report Date | N/A |
| Finders | 0xshoonya, 0xexploud |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2025-01-zaros-part-2
- **Contest**: https://codehawks.cyfrin.io/c/cm60h7a380000k66h6knt2vtl

### Keywords for Search

`vulnerability`

