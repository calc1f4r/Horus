---
# Core Classification
protocol: Retro/Thena Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33072
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/retro-thena-audit
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
  - OpenZeppelin
---

## Vulnerability Title

Whitelist Is Incompatible With Proxies

### Overview


The whitelist feature is meant to prevent harmful contracts from being used on the protocol. However, there is a concern that a previously safe contract could be upgraded into a harmful one and still be whitelisted. To avoid this, it is recommended to not whitelist proxy contracts and to add documentation explaining this in the whitelist code. The Retro-Thena team has acknowledged this issue but it has not been resolved yet. They are currently in communication with the projects that require proxy contracts, such as USDC.

### Original Finding Content

The intention of the whitelist is to keep malicious contracts off of the protocol. When whitelisting upgradable contracts, it is possible for a formerly benign whitelisted contract to eventually upgrade into a malicious contract. Because of this, proxy contracts should never be whitelisted.


Consider removing any proxy contracts from the whitelist and introducing documentation around proxies in the whitelist code to avoid future proxies from being whitelisted.


***Update:** Acknowledged, not resolved. The Retro-Thena team stated:*



> *We do due diligence on the whitelisted projects and we are in contact with them. Some projects (e.g., USDC) need a proxy.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Retro/Thena Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/retro-thena-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

