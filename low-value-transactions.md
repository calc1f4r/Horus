---
# Core Classification
protocol: Resolv
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43609
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Resolv/Treasury/README.md#4-low-value-transactions
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

Low-value transactions

### Overview

See description below for full details.

### Original Finding Content

##### Description

* https://github.com/resolv-im/resolv-contracts/blob/2e24f0e76525a663e222530a88bdd968e5e818eb/contracts/LPExternalRequestsManager.sol#L144
* https://github.com/resolv-im/resolv-contracts/blob/2e24f0e76525a663e222530a88bdd968e5e818eb/contracts/LPExternalRequestsManager.sol#L215
* https://github.com/resolv-im/resolv-contracts/blob/2e24f0e76525a663e222530a88bdd968e5e818eb/contracts/ExternalRequestsManager.sol#L121
* https://github.com/resolv-im/resolv-contracts/blob/2e24f0e76525a663e222530a88bdd968e5e818eb/contracts/ExternalRequestsManager.sol#L192

The provider may execute transactions to mint or burn small amounts of funds, resulting in a value that is lower than the profit generated for the protocol, or even negative if the gas fees are higher.

This can lead to some provider requests remaining unfulfilled or cause losses to the protocol.

##### Recommendation
We recommend implementing a minimum threshold for minting and burning stablecoins.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Resolv |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Resolv/Treasury/README.md#4-low-value-transactions
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

