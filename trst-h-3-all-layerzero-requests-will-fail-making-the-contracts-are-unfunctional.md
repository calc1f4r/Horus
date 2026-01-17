---
# Core Classification
protocol: Mozaic Archimedes
chain: everychain
category: uncategorized
vulnerability_type: layerzero

# Attack Vector Details
attack_type: layerzero
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18996
audit_firm: Trust Security
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-05-23-Mozaic Archimedes.md
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
  - layerzero

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Trust Security
---

## Vulnerability Title

TRST-H-3 All LayerZero requests will fail, making the contracts are unfunctional

### Overview


This bug report is about the LayerZero architecture not accounting for native tokens when sending messages. This caused the contracts to be completely non-functional. The recommended mitigation was to pass value in each of the functions and perform more meticulous testing. The team response was that the bug was fixed, and the mitigation review was that the Controller and Vault now pass appropriate value in native tokens for messaging, and the contracts can be topped-up with the `receive()` method.

### Original Finding Content

**Description:**
When sending messages using the LayerZero architecture, native tokens must be supplied to 
cover the cost of delivering the message at the receiving chain. However, none of the Mozaic 
contracts account for it. The controller calls the bridge's `requestSnapshot()`, `requestSettle()`, 
`requestExecute()` without passing value. Vault calls `reportSnapshot()`, `reportSettle()` similarly. 
StargatePlugin calls the StargateRouter's swap() which also requires value. As a result, the 
contracts are completely unfunctional.

**Recommended Mitigation:**
Pass value in each of the functions above. Perform more meticulous testing with LayerZero 
endpoints. Contracts should support receiving base tokens with the `receive()` fallback, to pay 
for fees.

**Team response:**
Fixed

**Mitigation Review:**
The Controller and Vault now pass appropriate value in native tokens for messaging. The 
contracts can be topped-up with the `receive()` method.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Trust Security |
| Protocol | Mozaic Archimedes |
| Report Date | N/A |
| Finders | Trust Security |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-05-23-Mozaic Archimedes.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`LayerZero`

