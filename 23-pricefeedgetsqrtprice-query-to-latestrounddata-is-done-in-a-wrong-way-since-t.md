---
# Core Classification
protocol: Predy
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34917
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-05-predy
source_link: https://code4rena.com/reports/2024-05-predy
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

protocol_categories:
  - dexes

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[23] `PriceFeed#getSqrtPrice()` query to `latestRoundData()` is done in a wrong way since there is no check first to see if the sequencer is down

### Overview

See description below for full details.

### Original Finding Content


https://github.com/code-423n4/2024-05-predy/blob/a9246db5f874a91fb71c296aac6a66902289306a/src/PriceFeed.sol#L45-L58

```solidity
    function getSqrtPrice() external view returns (uint256 sqrtPrice) {
        (, int256 quoteAnswer,,,) = AggregatorV3Interface(_quotePriceFeed).latestRoundData(); //@audit
        IPyth.Price memory basePrice = IPyth(_pyth).getPriceNoOlderThan(_priceId, VALID_TIME_PERIOD);

        require(basePrice.expo == -8, "INVALID_EXP");

        require(quoteAnswer > 0 && basePrice.price > 0);

        uint256 price = uint256(int256(basePrice.price)) * Constants.Q96 / uint256(quoteAnswer);
        price = price * Constants.Q96 / _decimalsDiff;

        sqrtPrice = FixedPointMathLib.sqrt(price);
    }
```

This function returns the square root of the `baseToken` price quoted in `quoteToken`, and this data is queried when [checking if the vault is in danger](https://github.com/code-423n4/2024-05-predy/blob/a9246db5f874a91fb71c296aac6a66902289306a/src/libraries/logic/LiquidationLogic.sol#L129) in order to liquidate it, with needing a confirmation via `PositionCalculator.isLiquidatable()`.

The problem is that unlike the way Pyth is being queried which includes a `VALID_TIME_PERIOD` to act as a stale check for Pyth's `getPriceNoOlderThan()`. In the case of Chainlink, the protocol just ingests whatever price is returned from the feed even though it might be stale/not safe.

One thing with using Chainlink on L2 chains is that there is a need to check if the sequencer is down to avoid prices from looking like they are fresh although they are not. The bug could then be leveraged by malicious actors to take advantage of the sequencer downtime.

### Impact

Core functionalities across protocol would be somewhat broken on L2 chains where the networks could be down for a while.

As this, in it's sense, is like a `pausing` functionality on the chain and any action that's time-restricted has a potential of been flawly finalized, popular bug ideas include users not being able say add collateral if they had borrowed a position making them immediately liquidatable when the sequencer comes back on, etc. This could be coined to fit into any time-restricted logic.

If the sequencer goes down, the protocol will allow users to continue to operate at the previous (stale) prices.

### Recommended Mitigation Steps

Consider reimplementing the timing logics on the L2 side of the protocol to take the fact that the sequencer could indeed be down into account.

Additionally, since Chainlink recommends that all Optimistic L2 oracles consult the Sequencer Uptime Feed to ensure that the sequencer is live before trusting the data returned by the oracle introduce a seqeuncer check to ensure that the sequencer is active and prices returned are accurate.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Predy |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2024-05-predy
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2024-05-predy

### Keywords for Search

`vulnerability`

