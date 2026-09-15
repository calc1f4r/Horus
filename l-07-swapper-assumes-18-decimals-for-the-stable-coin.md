---
# Core Classification
protocol: Angle Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20831
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-01-dev-test-repo
source_link: https://code4rena.com/reports/2022-01-dev-test-repo
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

[L-07] Swapper assumes 18 decimals for the stable coin

### Overview

See description below for full details.

### Original Finding Content

The `Swapper` contract assumes in multiple places that the stable coin contract has 18 decimals (e.g., [here](https://github.com/AngleProtocol/angle-transmuter/blob/196bf1035154809b1c8f454c17bb45e3745509a6/contracts/transmuter/facets/Swapper.sol#L245)). While this is true for `AgToken`'s, the system is intended to be general and usable with other underlying stablecoins according to the whitepaper. Therefore, making this configurable would make sense in my opinion.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Angle Protocol |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-01-dev-test-repo
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2022-01-dev-test-repo

### Keywords for Search

`vulnerability`

