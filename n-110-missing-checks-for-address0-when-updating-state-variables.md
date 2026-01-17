---
# Core Classification
protocol: Panoptic
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33810
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-04-panoptic
source_link: https://code4rena.com/reports/2024-04-panoptic
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
finders_count: 0
finders:
---

## Vulnerability Title

[N-110] Missing checks for `address(0)` when updating state variables

### Overview

See description below for full details.

### Original Finding Content


Check for zero-address to avoid the risk of setting `address(0)` for state variables after an update.

*There are 20 instances of this issue.*

---

**[Picodes (judge) commented](https://github.com/code-423n4/2024-04-panoptic-findings/issues/568#issuecomment-2096433011):**
 > Flagging as best as this is the best mix of custom issues and automated findings I've seen so to me it brings the most value.
> 
> The following issues from this warden have also been considered in scoring and should be considered valid Low findings:
> - [Median is not updated when burning a position, which can result in an inaccurate solvency check](https://github.com/code-423n4/2024-04-panoptic-findings/issues/540)
> - [`PanopticFactory` can be bricked and become unusable](https://github.com/code-423n4/2024-04-panoptic-findings/issues/523)



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Panoptic |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2024-04-panoptic
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2024-04-panoptic

### Keywords for Search

`vulnerability`

