---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41212
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Lido%20Oracle/README.md#3-incorrect-calculation-of-finalized_epoch-in-csoraclecollect_data
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
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Incorrect Calculation of `finalized_epoch` in `CSOracle.collect_data()`

### Overview

See description below for full details.

### Original Finding Content

##### Description
When calculating the last finalized epoch, [it is assumed](https://github.com/lidofinance/lido-oracle/blob/4e1e2210483fb44926d751049ea2d21561779dc8/src/modules/csm/csm.py#L180) that `blockstamp.slot_number` is the first slot of the justifying epoch. However, if the first slot of the justifying epoch is empty, `blockstamp.slot_number` [will point](https://github.com/lidofinance/lido-oracle/blob/4e1e2210483fb44926d751049ea2d21561779dc8/src/modules/submodules/oracle_module.py#L81-L88) to the slot where the last finalized block was created. As a result, `finalized_epoch` in this case will be less than the actual number of the last finalized epoch.

##### Recommendation
We recommend considering the case when the first slot of the justifying epoch is empty.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Lido%20Oracle/README.md#3-incorrect-calculation-of-finalized_epoch-in-csoraclecollect_data
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

