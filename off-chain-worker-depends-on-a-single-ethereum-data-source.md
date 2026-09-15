---
# Core Classification
protocol: Polkaswap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48897
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2021-08-soramitsu-polkaswap-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2021-08-soramitsu-polkaswap-securityreview.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Dominik Czarnota
  - Artur Cygan
---

## Vulnerability Title

Off-chain worker depends on a single Ethereum data source

### Overview


This bug report is about a potential vulnerability in the Sorascan system, specifically in the Auditing and Logging feature. The report states that the system only uses one source of information from Ethereum, which could cause problems if that source is compromised or unavailable. This could lead to an attacker manipulating the events provided to the system and stealing funds. The report recommends implementing a system that uses multiple sources of information and validating the data returned. In the long term, it suggests not relying on a single third-party source for important data. 

### Original Finding Content

## Type: Auditing and Logging
**Target:** Sorascan

**Difficulty:** High

## Description
The Polkaswap system uses a single source of truth to fetch Ethereum events from the Ethereum bridge contract. There is no mechanism for including additional Ethereum data sources. If this Ethereum data source experienced an outage, the Polkaswap system would also be at risk of an outage; if an attacker hacked the API, the attacker could manipulate the events provided to the system in an attempt to steal funds from it.

## Exploit Scenario
An attacker finds a way to hack the Ethereum data source used by the Polkaswap system. The attacker then modifies the API to serve bogus events to the Polkaswap off-chain worker, changing the chain state to his benefit.

## Recommendations
**Short term:** Enable the off-chain worker to fetch Ethereum events from multiple sources, and cross-validate the values it returns. Then require validators to use at least two Ethereum sources, including one self-hosted Ethereum node. Finally, document the process of adding additional sources. These steps will mitigate the risk of system outages or theft in the event that the Ethereum source to which the off-chain worker connects becomes malicious or unavailable.

**Long term:** Avoid relying on a single third-party source when fetching data that influences the chain state.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Polkaswap |
| Report Date | N/A |
| Finders | Dominik Czarnota, Artur Cygan |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2021-08-soramitsu-polkaswap-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2021-08-soramitsu-polkaswap-securityreview.pdf

### Keywords for Search

`vulnerability`

