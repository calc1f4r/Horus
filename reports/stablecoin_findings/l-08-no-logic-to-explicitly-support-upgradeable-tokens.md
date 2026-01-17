---
# Core Classification
protocol: Olas
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34949
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-05-olas
source_link: https://code4rena.com/reports/2024-05-olas
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

[L-08] No logic to explicitly support upgradeable tokens

### Overview

See description below for full details.

### Original Finding Content


As per the README, the protocol intends to support upgradeable tokens. However, there exists no logic to explicitly support such tokens in any way that would differ from non-upgradeable ones.

A change to the token semantics could break the staking contracts if they rely on past beheaviour (e.g. a token introducing rebasing logic), let alone a malicious upgrade.

As per the `weird-erc20` [docs](https://github.com/d-xo/weird-erc20#upgradable-tokens):

> Developers integrating with upgradable tokens should consider introducing logic that will freeze interactions with the token in question if an upgrade is detected. (e.g. the [`TUSD` adapter](https://github.com/makerdao/dss-deploy/blob/7394f6555daf5747686a1b29b2f46c6b2c64b061/src/join.sol#L321) used by MakerDAO).



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Olas |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2024-05-olas
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2024-05-olas

### Keywords for Search

`vulnerability`

