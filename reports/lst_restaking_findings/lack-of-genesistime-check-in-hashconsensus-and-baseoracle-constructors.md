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
solodit_id: 41250
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#28-lack-of-genesistime-check-in-hashconsensus-and-baseoracle-constructors
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

Lack of `genesisTime` Check in `HashConsensus` and `BaseOracle` Constructors

### Overview

See description below for full details.

### Original Finding Content

##### Description
The constructors of `HashConsensus` ([1](https://github.com/lidofinance/core/blob/fafa232a7b3522fdee5600c345b5186b4bcb7ada/contracts/0.8.9/oracle/HashConsensus.sol#L240-L265), [2](https://github.com/lidofinance/community-staking-module/blob/a898d045b63303294752d1a60ad9dfe8d8ba69ca/src/lib/base-oracle/HashConsensus.sol#L269-L299)) and `BaseOracle` ([1](https://github.com/lidofinance/core/blob/fafa232a7b3522fdee5600c345b5186b4bcb7ada/contracts/0.8.9/oracle/BaseOracle.sol#L103-L107), [2](https://github.com/lidofinance/community-staking-module/blob/a898d045b63303294752d1a60ad9dfe8d8ba69ca/src/lib/base-oracle/BaseOracle.sol#L129-L133)) lack a validation check to ensure that `genesisTime` is less than or equal to `block.timestamp`. This omission could allow incorrect values for the `genesisTime` parameter to be passed during the deployment.

##### Recommendation
We recommend adding checks in the `HashConsensus` and `BaseOracle` constructors to ensure that `genesisTime` is less than or equal to `block.timestamp`.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#28-lack-of-genesistime-check-in-hashconsensus-and-baseoracle-constructors
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

