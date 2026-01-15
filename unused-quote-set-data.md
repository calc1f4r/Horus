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
solodit_id: 48818
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

Unused quote-set data

### Overview

See description below for full details.

### Original Finding Content

## Quote-set Data’s `decay_` Lookup Table

The `decay_` lookup table is unused in the codebase, besides being initialized in the `qset_new` function.

## File Reference
`upd_aggregate.h:L14-L23`

```c
typedef struct pc_qset
{
    pd_t iprice_[PC_COMP_SIZE];
    pd_t uprice_[PC_COMP_SIZE];
    pd_t lprice_[PC_COMP_SIZE];
    pd_t weight_[PC_COMP_SIZE];
    int64_t decay_[1 + PC_MAX_SEND_LATENCY];
    int64_t fact_[PC_FACTOR_SIZE];
    int32_t expo_;
} pc_qset_t;
```

## Remediation
The `decay_` field should be removed entirely.

## Patch
Pyth Data Association acknowledges the finding, but doesn't believe it has security implications. However, they may deploy a fix to address it.

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

