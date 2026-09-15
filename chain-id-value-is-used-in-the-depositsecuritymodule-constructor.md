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
solodit_id: 41252
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#30-chain-id-value-is-used-in-the-depositsecuritymodule-constructor
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

Chain Id Value is Used in the `DepositSecurityModule` Constructor

### Overview

See description below for full details.

### Original Finding Content

##### Description
The issue is identified within the constructor of the contract `DepositSecurityModule`. The immutable variables `ATTEST_MESSAGE_PREFIX`, `PAUSE_MESSAGE_PREFIX`, and `UNVET_MESSAGE_PREFIX` values are calculated using block.chainid. There is a possibility of the chain id value changing due to potential modifications in the Ethereum chain. This may lead to replay attacks using signatures with the mentioned message prefixes.

The issue is classified as **Low** severity because it is unlikely that the chain id would change, and it is still better to follow EIP-712 domainSeparator calculation.

##### Recommendation
We recommend calculating the `ATTEST_MESSAGE_PREFIX`, `PAUSE_MESSAGE_PREFIX`, and `UNVET_MESSAGE_PREFIX` message prefixes at the time when the message hash is calculated. This will ensure the use of the actual chain id.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#30-chain-id-value-is-used-in-the-depositsecuritymodule-constructor
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

