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
solodit_id: 56378
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

In contract MetaRouterV2, function metaMintSwap, line 106 & 129, there is an external call to an arbitrary address with an arbitrary data, made through the swap function, an malicious actor could carefully craft the input arguments to call transferFrom function from an ERC20 that was previously approved by the user.

### Overview


The bug report suggests that the address "router" should be whitelisted in the "_swap" function.

### Original Finding Content

**Recommendation**:
Whitelist the address _router from the _swap function.

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

