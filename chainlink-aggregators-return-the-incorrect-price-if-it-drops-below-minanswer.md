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
solodit_id: 27617
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
finders_count: 4
finders:
  - hunterw3b
  - ZedBlockchain
  - Madalad
  - MaanVader
---

## Vulnerability Title

Chainlink aggregators return the incorrect price if it drops below `minAnswer`

### Overview

See description below for full details.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-10-SteadeFi/blob/main/contracts/oracles/ChainlinkARBOracle.sol#L188">https://github.com/Cyfrin/2023-10-SteadeFi/blob/main/contracts/oracles/ChainlinkARBOracle.sol#L188</a>


## Summary

Chainlink aggregators have a built in circuit breaker if the price of an asset goes outside of a predetermined price band. The result is that if an asset experiences a huge drop in value (i.e. LUNA crash) the price of the oracle will continue to return the `minAnswer` instead of the actual price of the asset.

## Vulnerability Details

Chainlink's `latestRoundData` pulls the associated aggregator and requests round data from it. ChainlinkAggregators have `minAnswer` and `maxAnswer` circuit breakers built into them. This means that if the price of the asset drops below the `minAnswer`, the protocol will continue to value the token at `minAnswer` instead of it's actual value. This will result in the asset being priced incorrectly, allowing exploitation such as undercollateralized loans or unfair liquidations.

## Impact

This discrepency could cause major issues within the protocol and potentially lead to loss of funds. This is exactly what happened to [Venus on BSC when LUNA imploded](https://rekt.news/venus-blizz-rekt/).

## Tools Used

Manual review

## Recommendations

Add a check that reverts if the price received from the oracle is out of bounds, as is recommended in Chainlink's [documentation](https://docs.chain.link/data-feeds#check-the-latest-answer-against-reasonable-limits).

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | SteadeFi |
| Report Date | N/A |
| Finders | hunterw3b, ZedBlockchain, Madalad, MaanVader |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-10-SteadeFi
- **Contest**: https://www.codehawks.com/contests/clo38mm260001la08daw5cbuf

### Keywords for Search

`vulnerability`

