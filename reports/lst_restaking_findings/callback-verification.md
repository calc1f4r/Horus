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
solodit_id: 28130
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Lido%20Protocol/README.md#7-callback-verification
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

Callback verification

### Overview


This bug report describes an issue with the Lido Oracle contract. A callback which does not have an implementation of the `processLidoOracleReport()` method can be added to the `OrderedCallbacksArray.sol` line. This causes the execution of the `LidoOracle.sol` line to be reverted. It is recommended to add verification of the existing `processLidoOracleReport()` method in the callback, or to double-check callbacks before adding them. This can be done by following the Ethereum Improvement Proposal (EIP) 165 standard.

### Original Finding Content

##### Description
By mistake a callback which has no implementation of the`processLidoOracleReport()` method can be added at the line:
https://github.com/lidofinance/lido-dao/blob/801d3e854efb33ff33a59fe51187e187047a6be2/contracts/0.8.9/OrderedCallbacksArray.sol#L60
In case you set the `IBeaconReportReceiver`  address, the  execution of the following lines will be reverted.
https://github.com/lidofinance/lido-dao/blob/801d3e854efb33ff33a59fe51187e187047a6be2/contracts/0.4.24/oracle/LidoOracle.sol#L644
##### Recommendation
It is necessary to add verification of the existing `processLidoOracleReport()` method in callback or callbacks should be double-checked before adding.
See this standard: https://eips.ethereum.org/EIPS/eip-165.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Lido%20Protocol/README.md#7-callback-verification
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

