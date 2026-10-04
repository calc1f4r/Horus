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
solodit_id: 49798
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/clo38mm260001la08daw5cbuf
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
finders_count: 1
finders:
  - rvierdiiev
---

## Vulnerability Title

ChainlinkARBOracle.consult will revert phase id was increased for chainlink aggregator

### Overview

See description below for full details.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-10-SteadeFi/blob/main/contracts/oracles/ChainlinkARBOracle.sol#L213-L219">https://github.com/Cyfrin/2023-10-SteadeFi/blob/main/contracts/oracles/ChainlinkARBOracle.sol#L213-L219</a>


## Summary
ChainlinkARBOracle.consult will revert phase id was increased for chainlink aggregator, because wrong round will be requested instead of previous one.
## Vulnerability Details
In order to validate chainlink price ChainlinkARBOracle fetched answer [for current and previous rounds](https://github.com/Cyfrin/2023-10-SteadeFi/blob/main/contracts/oracles/ChainlinkARBOracle.sol#L67-L68).
In order to get the previous round, roundId from current response is used. So just [`roundId - 1` is requested](https://github.com/Cyfrin/2023-10-SteadeFi/blob/main/contracts/oracles/ChainlinkARBOracle.sol#L219). 

Round id in the chainlink [consists of phaseId and aggregatorRoundId](https://docs.chain.link/data-feeds/historical-data#roundid-in-proxy). In case if new aggregator is used, then phaseId is increased.

So the problem occurs when new aggregator is used and it has only the first round. Then `roundId - 1` will not point to the last round of the previous aggregator, but it will be an incorrect round. As a result wrong answer will be returned and the call will likely revert.
## Impact
Call will revert as price will not be validated.
## Tools Used
VsCode
## Recommendations
It can be really complicated fix, where you need to parse roundId to know if phase was changed. I am not sure it worth it.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | SteadeFi |
| Report Date | N/A |
| Finders | rvierdiiev |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-10-SteadeFi
- **Contest**: https://codehawks.cyfrin.io/c/clo38mm260001la08daw5cbuf

### Keywords for Search

`vulnerability`

