---
# Core Classification
protocol: Symbiosis
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 56377
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-02-08-Symbiosis.md
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

In contract MetaRouterV2, function metaRouteV2, lines 87 & 67, there are some external calls to an arbitrary address with an arbitrary data, an malicious actor could carefully craft the input arguments to call transferFrom function from an ERC20 that was previously approved by the user.

### Overview


This bug report is recommending that all addresses used by metaRouter for external calls should be whitelisted. This includes firstDexRouter, secondDexRouter, and relayRecipient.

### Original Finding Content

**Recommendation**:
Whitelist all the addresses that metaRouter will do external calls to (firstDexRouter,
secondDexRouter, relayRecipient).

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Symbiosis |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-02-08-Symbiosis.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

