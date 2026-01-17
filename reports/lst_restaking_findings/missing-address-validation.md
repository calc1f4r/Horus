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
solodit_id: 28365
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Easy%20Track/README.md#2-missing-address-validation
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

Missing address validation

### Overview


This bug report is about the delegatecall on an callsScript address always returning true if callsScript is a non-contract address. This is due to a line of code in the EvmScriptExecutor.sol file on GitHub. The recommendation is to make the callsScript address constant, or add a check that callsScript is a contract address in the constructor. This would ensure that the delegatecall on an callsScript address only returns true if the callsScript is a contract address.

### Original Finding Content

##### Description
A delegatecall on an callsScript address always returns true if callsScript is non-contract address.
At line https://github.com/lidofinance/easy-track/blob/ec694adb872877db814da960d96ce767ccbdf462/contracts/EvmScriptExecutor.sol#L80
##### Recommendation
We recommend making the callsScript address constant or add check that callsScript is contract address in constructor.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Easy%20Track/README.md#2-missing-address-validation
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

