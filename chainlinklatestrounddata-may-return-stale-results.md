---
# Core Classification
protocol: SteadeFi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27645
audit_firm: Codehawks
contest_link: https://www.codehawks.com/contests/clo38mm260001la08daw5cbuf
source_link: none
github_link: https://github.com/Cyfrin/2023-10-SteadeFi

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
  - Bauer
  - mylifechangefast
---

## Vulnerability Title

`Chainlink.latestRoundData()` may return stale results

### Overview

See description below for full details.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-10-SteadeFi/blob/main/contracts/oracles/ChainlinkOracle.sol#L151-L170">https://github.com/Cyfrin/2023-10-SteadeFi/blob/main/contracts/oracles/ChainlinkOracle.sol#L151-L170</a>


## Summary
The `_getChainlinkResponse()` function is used to get the price of tokens, the problem is that the function does not check for stale results.

## Vulnerability Details
The `ChainlinkOracle._getChainlinkResponse()` function is used to get latest Chainlink response.
```solidity
function _getChainlinkResponse(address _feed) internal view returns (ChainlinkResponse memory) {
    ChainlinkResponse memory _chainlinkResponse;

    _chainlinkResponse.decimals = AggregatorV3Interface(_feed).decimals();

    (
      uint80 _latestRoundId,
      int256 _latestAnswer,
      /* uint256 _startedAt */,
      uint256 _latestTimestamp,
      /* uint80 _answeredInRound */
    ) = AggregatorV3Interface(_feed).latestRoundData();

    _chainlinkResponse.roundId = _latestRoundId;
    _chainlinkResponse.answer = _latestAnswer;
    _chainlinkResponse.timestamp = _latestTimestamp;
    _chainlinkResponse.success = true;

    return _chainlinkResponse;
  }

```

The problem is that there is not check for stale data. There are some reasons that the price feed can become stale.
## Impact
Since the token prices are used in many contracts, stale data could be catastrophic for the project.


## Tools Used

## Recommendations
Read the updatedAt return value from the `Chainlink.latestRoundData()` function and verify that is not older than than specific time tolerance.
```solidity
require(block.timestamp - udpatedData < toleranceTime, "stale price");
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | SteadeFi |
| Report Date | N/A |
| Finders | Bauer, mylifechangefast |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-10-SteadeFi
- **Contest**: https://www.codehawks.com/contests/clo38mm260001la08daw5cbuf

### Keywords for Search

`vulnerability`

