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
solodit_id: 48820
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

Test instructions do not check exponent

### Overview

See description below for full details.

### Original Finding Content

## Overview of init_price and upd_test Instructions

The `init_price` instruction performs bounds checks on the exponent `cptr->expo_`.

## Code Snippet - init_price
```c
oracle.c:L270-L275
cmd_init_price_t *cptr = (cmd_init_price_t*)prm->data;
if ( prm->data_len != sizeof( cmd_init_price_t ) ||
    cptr->expo_ > PC_MAX_NUM_DECIMALS ||
    cptr->expo_ < -PC_MAX_NUM_DECIMALS ) {
    return ERROR_INVALID_ARGUMENT;
}
```

However, there is no such check for the exponent `cmd->expo_` in the `upd_test` instruction.

## Code Snippet - upd_test
```c
oracle.c:L478-L486
cmd_upd_test_t *cmd = (cmd_upd_test_t*)prm->data;
pc_price_t *px = (pc_price_t*)ka[1].data;
if ( prm->data_len != sizeof( cmd_upd_test_t ) ||
    px->magic_ != PC_MAGIC ||
    px->ver_ != cmd->ver_ ||
    px->type_ != PC_ACCTYPE_TEST ||
    cmd->num_ > PC_COMP_SIZE ) {
    return ERROR_INVALID_ARGUMENT;
}
```

## Remediation
The `upd_test` instruction should perform bounds checks on the provided exponent.

## Patch
Pyth Data Association acknowledges the finding and developed a patch for this issue: `#182`.

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

