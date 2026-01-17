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
solodit_id: 28147
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Deposit%20Security%20Module/README.md#7-guardian-zero-address-check
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

Guardian zero address check

### Overview


This bug report is about a problem found in the DepositSecurityModule.sol file of the Lido-Dao project. The issue is that it is possible to add a guardian with a zero address. This could cause problems if the guardian is not a valid address. To fix this issue, it is recommended to add a zero address check. This check would require that the guardian address is not equal to address zero. This would ensure that only valid addresses are used as guardians.

### Original Finding Content

##### Description
It is possible to add guardian with zero address 
https://github.com/lidofinance/lido-dao/blob/5b449b740cddfbef5c107505677e6a576e2c2b69/contracts/0.8.9/DepositSecurityModule.sol#L281.
##### Recommendation
It is recommended to add zero address check
```solidity
require(addr != address(0), "guardian zero address");
```

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Deposit%20Security%20Module/README.md#7-guardian-zero-address-check
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

