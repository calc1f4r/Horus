---
# Core Classification
protocol: Connext
chain: everychain
category: oracle
vulnerability_type: stale_price

# Attack Vector Details
attack_type: stale_price
affected_component: oracle

# Source Information
source: solodit
solodit_id: 7239
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:
  - stale_price
  - oracle
  - chainlink

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - 0xLeastwood
  - Jonah1005
---

## Vulnerability Title

Missing checks for Chainlink oracle

### Overview


This report is about a bug found in the ConnextPriceOracle.sol file at lines 98 and 153. The bug is related to the getTokenPrice() function which goes through a series of oracles and returns a non-zero oracle price if all validations succeed. The bug is that the updateAt value, which is the timestamp of the round, is not checked to make sure it is recent. Additionally, the minAnswer and maxAnswer of the Chainlink oracle are not checked to make sure they are not reached or surpassed. 

The recommendation is to determine the tolerance threshold for updateAt and if the block.timestamp - updateAt exceeds that threshold, return 0. Additionally, consider having off-chain monitoring to identify when the market price moves out of the [minAnswer, maxAnswer] range. Connext has implemented a recency check in PR 1602 and will consider off-chain monitoring. Spearbit has verified and acknowledged this report.

### Original Finding Content

## Severity: Medium Risk

## Context
- ConnextPriceOracle.sol#L98
- ConnextPriceOracle.sol#L153

## Description
The `ConnextPriceOracle.getTokenPrice()` function goes through a series of oracles. At each step, it has a few validations to avoid incorrect prices. If such validations succeed, the function returns the non-zero oracle price. 

For the Chainlink oracle, `getTokenPrice()` ultimately calls `getPriceFromChainlink()`, which has the following validation:

```solidity
if (answer == 0 || answeredInRound < roundId || updateAt == 0) {
    // answeredInRound > roundId ===> ChainLink Error: Stale price
    // updatedAt = 0 ===> ChainLink Error: Round not complete
    return 0;
}
```

`updateAt` refers to the timestamp of the round. This value isn’t checked to ensure it is recent. Additionally, it is important to be aware of the `minAnswer` and `maxAnswer` of the Chainlink oracle; these values are not allowed to be reached or surpassed. See the Chainlink API reference for documentation on `minAnswer` and `maxAnswer`, as well as this piece of code: `OffchainAggregator.sol`.

## Recommendation
- Determine the tolerance threshold for `updateAt`. If `block.timestamp - updateAt` exceeds that threshold, return 0, which is consistent with how the current validations are handled.
- Consider having off-chain monitoring to identify when the market price moves out of `[minAnswer, maxAnswer]` range.

## Connext
Recency check is implemented in PR 1602. Off-chain monitoring will be considered.

## Spearbit
Verified and acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Spearbit |
| Protocol | Connext |
| Report Date | N/A |
| Finders | 0xLeastwood, Jonah1005 |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf

### Keywords for Search

`Stale Price, Oracle, Chainlink`

