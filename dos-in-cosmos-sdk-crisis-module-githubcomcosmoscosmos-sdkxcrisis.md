---
# Core Classification
protocol: Shido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37656
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-30-Shido.md
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

DoS in Cosmos SDK Crisis Module (github.com/cosmos/cosmos-sdk/x/crisis)

### Overview


This bug report is about a problem in the Cosmos SDK network where the chain does not stop when a certain check fails. This can be used by attackers to disrupt the network, which is called a denial-of-service attack. The chances of this happening are moderate, as it requires specific knowledge and skills. The recommendation is to create a custom solution to handle these failures, such as logging the error and alerting administrators. There is currently no fixed version for this issue.

### Original Finding Content

**Severity:** Medium

**Status**: Acknowledged

**Description:** 

The chain does not halt when an invariant check fails on a Cosmos SDK network, and a transaction is sent to the x/crisis module.

**Impact**: 

This can lead to a denial-of-service (DoS) attack, in which an attacker repeatedly triggers invariant failures to disrupt the network.

**Likelihood:** 

Moderate, as it requires knowledge of the invariant checks and the ability to craft malicious transactions.

**Recommendation:** 

There is no fixed version for github.com/cosmos/cosmos-sdk/x/crisis. Consider implementing a custom solution to handle invariant failures gracefully, such as logging the error, notifying administrators, and potentially pausing block production until the issue is resolved.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Shido |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-30-Shido.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

