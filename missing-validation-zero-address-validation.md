---
# Core Classification
protocol: Narwhal Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44711
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal Finance.md
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
  - Zokyo
---

## Vulnerability Title

Missing Validation Zero address validation

### Overview

See description below for full details.

### Original Finding Content

**Severity** : Low

**Status**: Resolved

**Description**:

The setManager function in the PairInfos contract allows the gov address to set a new manager address. However, this function does not include a check to ensure that the new manager address is not a zero address. This can lead to unexpected behavior or unintended consequences.


If the manager address is set to the zero address, it can cause issues with the functionality of the contract. For example, if the manager address is used to interact with external contracts or services, then the contract may fail to interact properly or lose access to critical functionality if the manager address is set to zero. Additionally, if the manager address is used to control access to the contract, then setting the address to zero could potentially allow unauthorized users to interact with the contract.

**Recommendation**:

To mitigate this vulnerability, a check should be added to the setManager function to ensure that the new manager address is not a zero address. This can be accomplished by adding an if statement that checks if the new address is zero, and if so, reverts the transaction.

**Fixed**: Issue fixed in commit a72e06b

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Narwhal Finance |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal Finance.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

