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
solodit_id: 29434
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

[FIXED] Redundant asserts in `AllowedRecipientsBuilder`

### Overview

See description below for full details.

### Original Finding Content

##### Location
File | Location | Line
--- | --- | ---
[AllowedRecipientsBuilder.sol](https://github.com/lidofinance/easy-track/tree/425f4a254ceb2be389f669580b9dc76618e92756/contracts/AllowedRecipientsBuilder.sol#L219-L220 "/contracts/AllowedRecipientsBuilder.sol") | contract `AllowedRecipientsBuilder` > function `deployAllowedTokensRegistry` | 219-220

##### Description
In the function [`deployAllowedTokensRegistry`](https://github.com/lidofinance/easy-track/blob/425f4a254ceb2be389f669580b9dc76618e92756/contracts/AllowedRecipientsBuilder.sol#L219-L220) of the `AllowedRecipientsBuilder` contract the following assert statements are redundant:
```soldity
assert(!registry.hasRole(REMOVE_TOKEN_FROM_ALLOWED_LIST_ROLE, address(this)));
assert(!registry.hasRole(DEFAULT_ADMIN_ROLE, address(this)));
```
This is because the `AllowedRecipientsBuilder` contract doesn’t receive `DEFAULT_ADMIN_ROLE` and `REMOVE_TOKEN_FROM_ALLOWED_LIST_ROLE` roles in any previous steps.
##### Recommendation
We recommend removing the redundant assert statements to keep the codebase clean.
##### Update
Fixed in the commit [`52b1b1d99531a7aa46d8474bef56b157b83f318a`](https://github.com/lidofinance/easy-track/commit/52b1b1d99531a7aa46d8474bef56b157b83f318a).

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

