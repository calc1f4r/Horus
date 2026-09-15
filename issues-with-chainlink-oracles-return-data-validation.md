---
# Core Classification
protocol: Tempus Raft
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17570
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-04-tempus-raft-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-04-tempus-raft-securityreview.pdf
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
  - Justin Jacob
  - Michael Colburn
---

## Vulnerability Title

Issues with Chainlink oracle’s return data validation

### Overview

See description below for full details.

### Original Finding Content

## Security Assessment Report

**Difficulty:** High  
**Type:** Configuration  
**Target:** `contracts/Oracles/ChainlinkPriceOracle.sol`  

## Description
Chainlink oracles are used to compute the price of a collateral token throughout the protocol. When validating the oracle's return data, the returned price is compared to the price of the previous round. However, there are a few issues with the validation:

- The increase of the `currentRoundId` value may not be statically increasing across rounds. The only requirement is that the `roundID` increases monotonically.
- The `updatedAt` value in the oracle response is never checked, so potentially stale data could be coming from the `priceAggregator` contract.
- The `roundId` and `answeredInRound` values in the oracle response are not checked for equality, which could indicate that the answer returned by the oracle is fresh.

```solidity
function _badChainlinkResponse(ChainlinkResponse memory response) internal view returns (bool) {
    return !response.success || response.roundId == 0 || response.timestamp == 0 || response.timestamp > block.timestamp || response.answer <= 0;
}
```
*Figure 2.1: The Chainlink oracle response validation logic*

## Exploit Scenario
The Chainlink oracle attempts to compare the current returned price to the price in the previous `roundID`. However, because the `roundID` did not increase by one from the previous round to the current round, the request fails, and the price oracle returns a failure. A stale price is then used by the protocol.

## Recommendations
- **Short term:** Validate that the `timestamp` value is greater than `0` to ensure that the data is fresh. Also, check that the `roundID` and `answeredInRound` values are equal to ensure that the returned answer is not stale. Lastly, ensure that the `timestamp` value is not decreasing from round to round.
  
- **Long term:** Carefully investigate oracle integrations for potential footguns in order to conform to correct API usage.

## References
- The Historical-Price-Feed-Data Project

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Tempus Raft |
| Report Date | N/A |
| Finders | Justin Jacob, Michael Colburn |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2023-04-tempus-raft-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2023-04-tempus-raft-securityreview.pdf

### Keywords for Search

`vulnerability`

