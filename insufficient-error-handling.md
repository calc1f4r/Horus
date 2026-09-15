---
# Core Classification
protocol: Cosmos LSM
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46746
audit_firm: OtterSec
contest_link: https://cosmos.network/
source_link: https://cosmos.network/
github_link: https://github.com/cosmos/cosmos-sdk

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
finders_count: 3
finders:
  - James Wang
  - Robert Chen
  - Tuyết Dương
---

## Vulnerability Title

Insufficient Error Handling

### Overview

See description below for full details.

### Original Finding Content

## Error Handling Issues in msg_server

`ValidatorBond`, `RedeemTokensForShares`, and `UnbondValidator` in `msg_server` lack sufficient error handling for certain function calls (`SetDelegation`, `bondedTokensToNotBonded`, and `jailValidator`, respectively). Missing error checks may affect delegation states in the staking module, leading to inconsistencies in the bonded and not-bonded pools and impacting validator management.

## Remediation

Utilize a linter, such as `errcheck`, which checks for unchecked errors in Go code. `errcheck` helps detect cases where error handling is missing.

## Patch

Fixed in PR#22519.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Cosmos LSM |
| Report Date | N/A |
| Finders | James Wang, Robert Chen, Tuyết Dương |

### Source Links

- **Source**: https://cosmos.network/
- **GitHub**: https://github.com/cosmos/cosmos-sdk
- **Contest**: https://cosmos.network/

### Keywords for Search

`vulnerability`

