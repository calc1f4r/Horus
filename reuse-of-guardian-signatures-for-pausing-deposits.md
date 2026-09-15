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
solodit_id: 41216
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#4-reuse-of-guardian-signatures-for-pausing-deposits
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

Reuse of Guardian Signatures for Pausing Deposits

### Overview


The report describes a problem with the `pauseDeposits` function in the `DepositSecurityModule` contract. This function does not use a nonce system, which means that an old signature could be used to pause the system again. This could lead to disruptions and potential governance issues. The report recommends implementing a nonce system to prevent this issue and improve the security of the contract.

### Original Finding Content

##### Description
The issue is identified within the [pauseDeposits](https://github.com/lidofinance/core/blob/fafa232a7b3522fdee5600c345b5186b4bcb7ada/contracts/0.8.9/DepositSecurityModule.sol#L384) function of the `DepositSecurityModule` contract. This function checks for guardians' signatures to pause deposits but does not utilize a nonce mechanism. Consequently, a previously used signature could potentially be replayed to initiate another pause, leading to abuse or unintended operational disruptions.

The issue is classified as **Medium** severity because it could allow an attacker to repeatedly pause the system by reusing an old, valid signature, thereby disrupting normal operations and potentially causing governance issues.

##### Recommendation
We recommend implementing a nonce system for signing operations. This will prevent the reuse of signatures and enhance the security and robustness of the contract.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#4-reuse-of-guardian-signatures-for-pausing-deposits
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

