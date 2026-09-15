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
solodit_id: 28152
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Deposit%20Security%20Module/README.md#12-using-unchecked-address
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

Using unchecked address

### Overview


This bug report is about a security issue in the Lido DAO code. The code in question is found at two lines in the DepositSecurityModule.sol file: 77 and 78. The issue is that the address is not being checked for zeros before it is used. It is recommended that the address should be checked for zeros before being used.

### Original Finding Content

##### Description
At the lines:
https://github.com/lidofinance/lido-dao/blob/5b449b740cddfbef5c107505677e6a576e2c2b69/contracts/0.8.9/DepositSecurityModule.sol#L77
https://github.com/lidofinance/lido-dao/blob/5b449b740cddfbef5c107505677e6a576e2c2b69/contracts/0.8.9/DepositSecurityModule.sol#L78
address is not checked before using.
##### Recommendation
It is recommended to check address for zeros.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Deposit%20Security%20Module/README.md#12-using-unchecked-address
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

