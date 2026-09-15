---
# Core Classification
protocol: Zaros
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 38004
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/clyg8slke0001bvhpwszwjr7z
source_link: none
github_link: https://github.com/Cyfrin/2024-07-zaros

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
  - h2134
---

## Vulnerability Title

User might be unfairly liquidated after L2 Sequencer grace period

### Overview


This bug report discusses a potential issue with the protocol that could result in users being unfairly liquidated after a certain period of time. The severity of this bug is considered to be medium risk. The report recommends allowing users to create and fill orders during this grace period to prevent unfair liquidations. The impact of this bug is that users may lose their assets without being given a fair chance to react to price changes. The tools used to identify this bug were manual review. The recommendation is to skip the grace period check to allow for order creation and filling during this time.

### Original Finding Content

## Summary

User might be unfairly liquidated after L2 Sequencer grace period.

## Vulnerability Details

The protocol implements a L2 sequencer downtime check in the [ChainlinkUtil](https://github.com/Cyfrin/2024-07-zaros/blob/d687fe96bb7ace8652778797052a38763fbcbb1b/src/external/chainlink/ChainlinkUtil.sol#L41-L57). In the event of sequencer downtime (as well as a grace period following recovery), liquidations are disabled for the rightful reasons.

```Solidity
        if (address(sequencerUptimeFeed) != address(0)) {
            try sequencerUptimeFeed.latestRoundData() returns (
                uint80, int256 answer, uint256 startedAt, uint256, uint80
            ) {
                bool isSequencerUp = answer == 0;
                if (!isSequencerUp) {
@>                  revert Errors.OracleSequencerUptimeFeedIsDown(address(sequencerUptimeFeed));
                }

                uint256 timeSinceUp = block.timestamp - startedAt;
                if (timeSinceUp <= Constants.SEQUENCER_GRACE_PERIOD_TIME) {
@>                  revert Errors.GracePeriodNotOver();
                }
            } catch {
                revert Errors.InvalidSequencerUptimeFeedReturn();
            }
        }
```

At the same time, user won't be able to create order nor any order can be filled. This is problematic because when the Arbitrum sequencer is down and then comes back up, all Chainlink price updates will become available on Arbitrum within a very short time. This leaves users no time to react to the price changes which can lead to unfair liquidations.

Even if deposit is still allowed during the grace period, it is unfair to the user as they are forced to do so, not to mention that some users may not have enough funds to deposit.

## Impact

User might be unfairly liquidated after L2 Sequencer grace period.

## Tools Used

Manual Review

## Recommendations

Order should be allowed to be created and filled during sequencer grace period, this can be achieved by skipping `SEQUENCER_GRACE_PERIOD_TIME` checking.

```diff
    function getPrice(
        IAggregatorV3 priceFeed,
        uint32 priceFeedHeartbeatSeconds,
        IAggregatorV3 sequencerUptimeFeed,
+       bool skipGracePeriodChecking
    )
        internal
        view
        returns (UD60x18 price)
    {
        ...

        if (address(sequencerUptimeFeed) != address(0)) {
            try sequencerUptimeFeed.latestRoundData() returns (
                uint80, int256 answer, uint256 startedAt, uint256, uint80
            ) {
                bool isSequencerUp = answer == 0;
                if (!isSequencerUp) {
                    revert Errors.OracleSequencerUptimeFeedIsDown(address(sequencerUptimeFeed));
                }

                uint256 timeSinceUp = block.timestamp - startedAt;
-                if (timeSinceUp <= Constants.SEQUENCER_GRACE_PERIOD_TIME) {
+                if (!skipGracePeriodChecking && timeSinceUp <= Constants.SEQUENCER_GRACE_PERIOD_TIME) {
                    revert Errors.GracePeriodNotOver();
                }
            } catch {
                revert Errors.InvalidSequencerUptimeFeedReturn();
            }
        }

        ...
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Zaros |
| Report Date | N/A |
| Finders | h2134 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2024-07-zaros
- **Contest**: https://codehawks.cyfrin.io/c/clyg8slke0001bvhpwszwjr7z

### Keywords for Search

`vulnerability`

