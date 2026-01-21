---
# Core Classification
protocol: Enso
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61933
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Enso/Enso%20Wallet/README.md#1-destruction-of-the-ensowallet-implementation-contract
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

Destruction of the EnsoWallet implementation contract

### Overview

The bug report describes a vulnerability in the EnsoWallet contract that could allow an attacker to destroy the contract and freeze all user funds. This can happen if the attacker makes a direct call to the EnsoWallet.initialize() function or specifies themselves as the executor and later executes the SELFDESTRUCT opcode. To prevent this, it is recommended to disallow direct calls to the EnsoWallet.initialize() function.

### Original Finding Content

##### Description
An attacker can make a direct call (not via proxy) to [EnsoWallet.initialize()](https://github.com/EnsoFinance/shortcuts-contracts/blob/4902e55608f975f73772310955444110b1cfc4fc/contracts/EnsoWallet.sol#L24) and execute the SELFDESTRUCT opcode or specify themself as EXECUTOR and gain the ability to execute SELFDESTRUCT later. Consequently, the current implementation contract will be destroyed, and all users' wallet functionality will be inaccessible until the core upgrade. The worst case occurs if an attack happens after EnsoBeacon.renounceAdministration(), and all users' funds will be frozen.
##### Recommendation
We recommend disallowing direct calls to EnsoWallet.initialize().




### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Enso |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Enso/Enso%20Wallet/README.md#1-destruction-of-the-ensowallet-implementation-contract
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

