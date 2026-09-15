---
# Core Classification
protocol: Beyond
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45759
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-24-Beyond.md
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

Missing Validation for Same Token Addresses in registerToken

### Overview


A bug was found in the registerToken function of the OriginalTokenBridge contract. This can cause problems when using the bridge to transfer tokens between different blockchains. The recommended solution is to add a check to make sure that the localToken and remoteToken addresses are not the same. The client has acknowledged this issue and will work on fixing it.

### Original Finding Content

**Severity**: Medium

**Status**: Acknowledged

**Description**

In the registerToken function of the OriginalTokenBridge contract, there is no validation to ensure that localToken and remoteToken are not the same addresses. Registering the same address for both local and remote tokens could cause unexpected behavior in cross-chain operations or token handling.

**Recommendation**:

Add a validation check to ensure that the localToken and remoteToken addresses are not the same. This will prevent the registration of the same token address on both sides of the bridge.

**Client comment**:

we decided to Acknowledge this finding

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Beyond |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-24-Beyond.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

