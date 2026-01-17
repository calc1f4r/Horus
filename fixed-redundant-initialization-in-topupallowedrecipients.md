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
solodit_id: 29433
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

[FIXED] Redundant initialization in `TopUpAllowedRecipients`

### Overview

See description below for full details.

### Original Finding Content

##### Location
File | Location | Line
--- | --- | ---
[TopUpAllowedRecipients.sol](https://github.com/lidofinance/easy-track/tree/425f4a254ceb2be389f669580b9dc76618e92756/contracts/EVMScriptFactories/TopUpAllowedRecipients.sol#L131 "/contracts/EVMScriptFactories/TopUpAllowedRecipients.sol") | contract `TopUpAllowedRecipients` > function `_validateEVMScriptCallData` | 131

##### Description
In the function [`_validateEVMScriptCallData`](https://github.com/lidofinance/easy-track/tree/425f4a254ceb2be389f669580b9dc76618e92756/contracts/EVMScriptFactories/TopUpAllowedRecipients.sol#L131 "/contracts/EVMScriptFactories/TopUpAllowedRecipients.sol") of the `TopUpAllowedRecipients` contract the variable `totalAmount` is initialized with 0, which is redundant.
##### Recommendation
We recommend removing redundant initialization to keep the code base clean.
##### Update
Fixed in the commit [`3b718ad094ed54da1d7e216c03b38b856dcac7a6`](https://github.com/lidofinance/easy-track/commit/3b718ad094ed54da1d7e216c03b38b856dcac7a6).

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

