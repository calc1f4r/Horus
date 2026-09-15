---
# Core Classification
protocol: Reserve
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57075
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2022-08-reserve-protocol-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2022-08-reserve-protocol-securityreview.pdf
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
  - liquid_staking
  - cdp
  - yield
  - launchpad
  - privacy

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Felipe Manzano
  - Anish Naik
---

## Vulnerability Title

Inability to validate the recency of Aave and Compound oracle data

### Overview

See description below for full details.

### Original Finding Content

## Reserve Protocol Security Assessment

## Difficulty: High

## Type: Data Validation

### File Path
`contracts/plugins/assets/abstract/CompoundOracleMixin.sol`

### Description
The Aave and Compound oracle systems do not provide timestamps or round data. Thus, the Reserve protocol cannot validate the recency of the pricing data they provide. The Reserve protocol obtains pricing data for collateral and RSR tokens from the Aave and Compound oracle systems. Each oracle system relies on a Chainlink price feed as its underlying data feed. However, unlike Chainlink, Aave and Compound do not provide information on when a price was last updated. Thus, the pricing data reported to the Reserve protocol could be stale or invalid, exposing the protocol to risk. Additionally, in extreme market conditions, Chainlink may pause its oracle systems, which can increase the risk of undefined behavior.

### Exploit Scenario
The Chainlink system experiences an outage that prevents price feeds from being updated for an extended period of time. The Aave and Compound oracle systems continue reporting pricing data from the outdated feeds. During the outage, the status of a collateral token changes from SOUND to IFFY, but the change is not reflected on-chain. Eve is monitoring the prices off-chain and purchases RTokens during the outage, before an update causes the price to increase.

### Recommendations
- **Short term**: Consider obtaining pricing data from Chainlink, which enables a protocol to validate the recency of its data.
- **Long term**: Consider using an off-monitoring solution to track extreme market conditions and to ensure that the Chainlink oracle system is live.

### References
- Chainlink: Risk Mitigation
- Chainlink: Monitoring Data Feeds

Trail of Bits  
Reserve Protocol Security Assessment  
PUBLIC

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Reserve |
| Report Date | N/A |
| Finders | Felipe Manzano, Anish Naik |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2022-08-reserve-protocol-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2022-08-reserve-protocol-securityreview.pdf

### Keywords for Search

`vulnerability`

