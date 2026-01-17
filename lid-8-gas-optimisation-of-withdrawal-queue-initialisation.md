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
solodit_id: 53476
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-04-14-Lido.md
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
  - Hexens
---

## Vulnerability Title

[LID-8] Gas optimisation of withdrawal queue initialisation

### Overview

See description below for full details.

### Original Finding Content

**Severity:** Low

**Path:** WithdrawalQueueBase.sol:_initializeQueue#L470-L476

**Description:** 

The function `_initializeQueue` is called upon initialisation of the Withdrawal Queue contract. We found that it could be further gas optimised.

1. A zero struct `WithdrawalRequest` is created and written to the 0th key in the queue, however the first 2 elements that occupy the first storage slot are default values (`0`). Only the timestamp and claim marker are set, which occupy the second storage slot. It is therefore cheaper to directly write to these values:
```
_getQueue()[0].timestamp = uint64(block.timestamp);
_getQueue()[0].claimed = true;
```
2. A zero struct `DiscountCheckpoint` with default values (`0`) for all elements is written to the 0th key in the checkpoints. Because it is a mapping, the 0th index would already return a `DiscountCheckpoint` with default values upon reading. Therefore, the assignment can be completely removed.

```
function _initializeQueue() internal {
    // setting dummy zero structs in checkpoints and queue beginning
    // to avoid uint underflows and related if-branches
    // 0-index is reserved as 'not_found' response in the interface everywhere
    _getQueue()[0] = WithdrawalRequest(0, 0, payable(0), uint64(block.number), true);
    _getCheckpoints()[getLastCheckpointIndex()] = DiscountCheckpoint(0, 0);
}
```

**Remediation:**  See description.

**Status:**  Acknowledged

- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Hexens |
| Protocol | Lido |
| Report Date | N/A |
| Finders | Hexens |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-04-14-Lido.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

