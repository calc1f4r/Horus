---
# Core Classification
protocol: dForce
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34258
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/dForce/Lending%20v2/README.md#1-thecontrollerv2-implementation-can-be-destroyed-by-an-attacker
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

The`ControllerV2` implementation can be destroyed by an attacker

### Overview


The `ControllerV2` implementation code has a vulnerability that allows an attacker to directly call the `initialize` function, which can lead to the destruction of the Controller's implementation contract. This can cause the entire system to freeze until a manual intervention is done by the proxy administrator. This is considered a high severity issue. To fix this, it is recommended to prevent direct calls to `initialize` against the implementation address in the smart contract code.

### Original Finding Content

##### Description
The `ControllerV2` implementation code is vulnerable to a direct call of `initialize`. Since `initialize` executes `delegatecall` to an arbitrary address, an attacker can destroy the Controller's implementation contract, thus freezing the entire system until manual intervention by the proxy administrator occurs. This is accordingly rated as high in severity.

Related code - `delegatecall` to the arbitrary address: https://github.com/dforce-network/LendingContracts/blob/6f3a7b6946d8226b38e7f0d67a50e68a28fe5165/contracts/ControllerV2.sol#L57
##### Recommendation
Although this vulnerability can be hotfixed through an accurate deployment process, we recommend addressing it at the smart contract code level by preventing direct calls to `initialize` against the implementation address.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | dForce |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/dForce/Lending%20v2/README.md#1-thecontrollerv2-implementation-can-be-destroyed-by-an-attacker
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

