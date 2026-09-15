---
# Core Classification
protocol: Isle Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45741
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-16-Isle Finance.md
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
  - Zokyo
---

## Vulnerability Title

Incorrect ReentrancyGuard Version Used in Upgradeable LoanManager Contract

### Overview


This bug report is about a problem in the LoanManager contract, which is supposed to be upgradeable. However, it uses a non-upgradeable version of a library called ReentrancyGuard, which can cause issues with the upgrade process. The recommendation is to replace the non-upgradeable version with the upgradeable version and make sure to call a specific function during the initialization process. The client is considering making these changes to fix the issue.

### Original Finding Content

**Severity**: Low

**Status**: Resolved

**Description**: 

The LoanManager contract is intended to be upgradeable; however, it imports the non-upgradeable version of ReentrancyGuard from OpenZeppelin. This can lead to issues, as the non-upgradeable version does not have the necessary initializers and storage gap reserved for upgradeable contracts, which are essential for proxy-based upgradeability mechanisms.

**Recommendation**: 

To resolve this issue, replace the inheritance of the non-upgradeable ReentrancyGuard with the upgradeable version from OpenZeppelin, i.e., ReentrancyGuardUpgradeable. Make sure to call the __ReentrancyGuard_init function as part of the initialization process in the initializer function of LoanManager. Additionally, ensure that the contract abides by the storage gap requirements to maintain proper alignment and compatibility between contract upgrades.

**Comment**: 

The client is considering updating the library accordingly.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Isle Finance |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-16-Isle Finance.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

