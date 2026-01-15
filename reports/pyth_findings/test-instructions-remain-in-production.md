---
# Core Classification
protocol: Pyth Oracle
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48819
audit_firm: OtterSec
contest_link: https://pyth.network/
source_link: https://pyth.network/
github_link: https://github.com/pyth-network/pyth-client.

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
  - Robert Chen
  - OtterSec
  - William Wang
---

## Vulnerability Title

Test instructions remain in production

### Overview

See description below for full details.

### Original Finding Content

## Unit Test Instructions and Production Compilation

The `init_test` and `upd_test` instructions are intended to be used in unit tests. However, they are also compiled in production, which is unnecessary.

## Remediation

The `init_test` and `upd_test` functions, as well as their switch cases in the dispatch function, should be removed when compiling the on-chain program. This can be done with preprocessor directives.

## Patch

Pyth Data Association acknowledges the finding and developed a patch for this issue: **#182**.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Pyth Oracle |
| Report Date | N/A |
| Finders | Robert Chen, OtterSec, William Wang |

### Source Links

- **Source**: https://pyth.network/
- **GitHub**: https://github.com/pyth-network/pyth-client.
- **Contest**: https://pyth.network/

### Keywords for Search

`vulnerability`

