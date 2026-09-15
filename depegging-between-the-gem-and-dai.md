---
# Core Classification
protocol: MakerDAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40974
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/53e12fbd-182a-45f9-a115-55fdea33c5c4
source_link: https://cdn.cantina.xyz/reports/cantina_makerdao_dss-lite-psm_oct2023.pdf
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
finders_count: 3
finders:
  - m4rio
  - shung
  - Christoph Michel
---

## Vulnerability Title

Depegging between the GEM and DAI

### Overview

See description below for full details.

### Original Finding Content

## DssLitePsm.sol

## Description
The DssLitePsm assumes that the exchange rate between the GEM and DAI is always 1-1. As this is acceptable during normal market conditions, it can create a good opportunity for MEV during volatile conditions. If a depeg happens, users will start dumping gems into the protocol, gaining more DAI.

## Recommendation
We do not have a recommendation on the current code. We recommend using the Debt Ceiling Instant Access Module (AutoLine) to control the debt ceiling of a gem, which will restrict the maximum growth of the debt ceiling over a certain timeframe. Furthermore, because the AutoLine contains the `exec` function that can be triggered by anyone, it can increase the debt ceiling in a permissionless way. If the depegging lasts for a long period, an emergency spell should be in place to zero the debt ceiling for that specific gem until the depegging starts to heal to an acceptable ratio.

## Acknowledgements
- Maker DAO: Acknowledged. This module is meant to be used with DCIAM.
- Cantina Managed: Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | MakerDAO |
| Report Date | N/A |
| Finders | m4rio, shung, Christoph Michel |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_makerdao_dss-lite-psm_oct2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/53e12fbd-182a-45f9-a115-55fdea33c5c4

### Keywords for Search

`vulnerability`

