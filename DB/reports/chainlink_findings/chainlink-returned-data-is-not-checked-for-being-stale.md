---
# Core Classification
protocol: MetaLeX
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43442
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/MetaLeX/Borg/README.md#6-chainlink-returned-data-is-not-checked-for-being-stale
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

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

Chainlink returned data is not checked for being stale

### Overview


The bug report is about a call to the Chainlink price feed function `latestRoundData` that can return an outdated price. This is because Chainlink may take some time to deliver the most recent data. The recommendation is to add a call to the `updatedAt` function to ensure that the data being returned is up-to-date.

### Original Finding Content

##### Description
There is a call to the Chainlink price feed `latestRoundData` at line https://github.com/MetaLex-Tech/borg-core/blob/67e3131f9ea7daafa7e98b5fb6892a122516fe2a/src/libs/conditions/chainlinkOracleCondition.sol#L53. It can return a stale price due to Chainlink lagging in delivering actual data.

##### Recommendation
We recommend adding a call to the price feed function `updatedAt` to check if the returned data is not stale.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | MetaLeX |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/MetaLeX/Borg/README.md#6-chainlink-returned-data-is-not-checked-for-being-stale
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

