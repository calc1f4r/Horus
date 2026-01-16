---
# Core Classification
protocol: Vaultka
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44898
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-08-30-Vaultka.md
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

Water deposit is exposed to inflation attack

### Overview


This bug report is about a security issue in a code called Water.sol. The problem is that the code is using a version of ERC4626 that is vulnerable to an attack. This allows attackers to use the "deposit()" function in the contract to gain money illegally. The report recommends following the instructions in a link to fix the issue. The status of the bug is marked as resolved.

### Original Finding Content

**Severity**: High

**Status**: Resolved

**Description**

Water.sol - The ERC4626 version used is exposed to inflation attack. That leads to having function deposit() in the water contract to be exploited by attackers to achieve illegitimate gains. The description of the attack scenario as well as the mitigation is described: https://docs.openzeppelin.com/contracts/4.x/erc4626.

**Recommendation** 

Follow the mitigation suggested in the link.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Vaultka |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-08-30-Vaultka.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

