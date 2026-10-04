---
# Core Classification
protocol: Divergence Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29442
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Divergence%20Protocol/README.md#3-price-manipulation-by-calling-updatephase-with-different-symbols
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
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Price manipulation by calling `updatePhase` with different symbols

### Overview


This bug report details a critical flaw in the audited commit `29a0ccb5fc7ac838bd44c75c0afc398b84be267a` in which the `endRoundId` value is not dependent on the asset symbol. An attacker could exploit this vulnerability to manipulate the `endRoundId` values, which would lead to incorrect battle income and violate the correctness of the price calculation algorithm. 

The issue is considered to be of HIGH severity due to its critical impact, but it is only exploitable during a 1-hour period after a Chainlink phase has been changed. As a result, the recommendation is to rework the entire algorithm of interaction with Chainlink to make it more tolerant to manipulations.

### Original Finding Content

##### Description
In the audited commit `29a0ccb5fc7ac838bd44c75c0afc398b84be267a`, the `endRoundId` value is not dependent on the asset symbol. By calling the `updatePhase` function with a different `symbol` argument, an attacker may manipulate the `endRoundId` values. This could violate the correctness of the price calculation algorithm, leading to incorrect battle income.

Although this is a critical flaw, it is only exploitable during a 1-hour period after a Chainlink phase has been changed. Given its critical impact but low likelihood, this issue is assigned a HIGH severity rating.

Related code - the declaration of the `endRoundId`: https://github.com/DivergenceProtocol/diver-contracts/blob/29a0ccb5fc7ac838bd44c75c0afc398b84be267a/src/core/Oracle.sol#L17

##### Recommendation
We recommend reworking the entire algorithm of interaction with Chainlink to render it more tolerant to manipulations.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Divergence Protocol |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Divergence%20Protocol/README.md#3-price-manipulation-by-calling-updatephase-with-different-symbols
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

