---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29435
audit_firm: Oxorio
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2023-10-18-Lido.md
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
  - Oxorio
---

## Vulnerability Title

[FIXED] Missing spec in `TopUpAllowedRecipients`

### Overview

See description below for full details.

### Original Finding Content

##### Location
File | Location | Line
--- | --- | ---
[TopUpAllowedRecipients.sol](https://github.com/lidofinance/easy-track/tree/425f4a254ceb2be389f669580b9dc76618e92756/contracts/EVMScriptFactories/TopUpAllowedRecipients.sol#L48 "/contracts/EVMScriptFactories/TopUpAllowedRecipients.sol") | contract `TopUpAllowedRecipients` > `constructor` | 48

##### Description
In the [`constructor`](https://github.com/lidofinance/easy-track/tree/425f4a254ceb2be389f669580b9dc76618e92756/contracts/EVMScriptFactories/TopUpAllowedRecipients.sol#L48) of the `TopUpAllowedRecipients` contract the `_allowedTokensRegistry` parameter and its description are missing in the NatSpec comment of the constructor method.
##### Recommendation
We recommend adding the missing description of the variable to the NatSpec comment in the constructor method. This will improve the clarity and understanding of the code.
##### Update
Fixed in the commit [`feb440dbe79031ca75d6956c08ce0c7d7f376ff7`](https://github.com/lidofinance/easy-track/commit/feb440dbe79031ca75d6956c08ce0c7d7f376ff7).

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Oxorio |
| Protocol | Lido |
| Report Date | N/A |
| Finders | Oxorio |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2023-10-18-Lido.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

