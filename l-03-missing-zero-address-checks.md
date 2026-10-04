---
# Core Classification
protocol: Tribe
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 4218
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-02-tribe-turbo-contest
source_link: https://code4rena.com/reports/2022-02-tribe-turbo
github_link: #l-03-missing-zero-address-checks

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

protocol_categories:
  - liquid_staking
  - dexes
  - bridge
  - cdp
  - yield

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[L-03] Missing zero address checks

### Overview

See description below for full details.

### Original Finding Content


1.  setBooster, setClerk, setDefaultSafeAuthority at TurboMaster.sol are not checking whether the supplied address!=0



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Tribe |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-02-tribe-turbo
- **GitHub**: #l-03-missing-zero-address-checks
- **Contest**: https://code4rena.com/contests/2022-02-tribe-turbo-contest

### Keywords for Search

`vulnerability`

