---
# Core Classification
protocol: Zap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35719
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-26-zap.md
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
  - Zokyo
---

## Vulnerability Title

Centralization Risk Due to Overpowered Owner

### Overview


This bug report describes a critical issue where an attacker can exploit a function in the system to allocate themselves an excessive number of vaults without any payment. This can lead to a significant loss of funds and trust. The report recommends using a multi-signature wallet for executing critical actions to reduce the risk of a single point of failure. However, the client has commented that it is not their responsibility to ensure wallet security. 

### Original Finding Content

**Severity**: Critical

**Status**: Acknowledged

**Description**

An admin calls `setNumberOfVaults(accountAddress, value)` to set the number of vaults for an account to any desired amount without any payment. This can be done without any checks for the `MAX_ALLOWED_VAULTS` constraint.  If an attacker gains control of the admin account, they can allocate themselves an excessive number of vaults without any payment, leading to a significant loss of funds and trust. An admin can use `addMultipleVaults(accountAddress, numberOfVaults)` to increase the number of vaults for any account without requiring any funds. This can lead to an inflation of the total number of vaults beyond the intended cap, disrupting the vault pricing mechanism and the overall supply.

**Recommendation**: 
Use a multi-signature wallet for executing onlyOwner functions. This requires multiple authorized signatures to approve critical actions, reducing the risk of a single point of failure. 
**Client comment**: A wallet with admin authorization should be able to do this. It is not our responsibility whether they ensure wallet security or not.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Zap |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-26-zap.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

