---
# Core Classification
protocol: Euler Labs - Euler Price Oracle
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35787
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Euler-Spearbit-Security-Review-Oracle-April-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Euler-Spearbit-Security-Review-Oracle-April-2024.pdf
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
finders_count: 5
finders:
  - Christos Pap
  - M4rio.eth
  - Christoph Michel
  - David Chaparro
  - Emanuele Ricci
---

## Vulnerability Title

Chainlink price feed decimals are cached

### Overview

See description below for full details.

### Original Finding Content

## Security Review Summary

## Severity
**Low Risk**

## Context
- **File**: ChainlinkOracle.sol
- **Lines**: L39-L40
- **Feed**: ETHUSD price feed
- **Source**: Chainlink feeds

## Description
The Chainlink adapter fetches the Chainlink price feed's decimals once in the constructor. As Chainlink price feeds fetch the decimals from the current aggregator and the aggregator can be changed, the decimals could also change. This would lead to incorrect price conversion if the price with the new decimals is used with the old cached decimals. It is unclear if Chainlink would ever update the aggregator to one with different decimals.

## Recommendation
Ideally, the decimals would be fetched every time the `latestRoundData` function is called to get the price.

## Euler Response
Acknowledged, won't fix. We discussed this at length and won't be applying the recommendation due to the following reasons:
- There is no past record of Chainlink changing the decimals of an already live price feed.
- Chainlink oracles secure billions of DeFi value; changing decimals would lead to cataclysmic disruptions in markets. Most consumers assume the 18/8 convention.
- Chainlink has a history of going the extra mile to ensure perfect backward compatibility with their upgrades; the now-ancient rounds system is evidence of that.
- I could not find a recommendation in the Chainlink developer documentation to expect this behavior.

## Spearbit Response
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Euler Labs - Euler Price Oracle |
| Report Date | N/A |
| Finders | Christos Pap, M4rio.eth, Christoph Michel, David Chaparro, Emanuele Ricci |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Euler-Spearbit-Security-Review-Oracle-April-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Euler-Spearbit-Security-Review-Oracle-April-2024.pdf

### Keywords for Search

`vulnerability`

