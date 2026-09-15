---
# Core Classification
protocol: Mysten Deepbook
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47057
audit_firm: OtterSec
contest_link: https://mystenlabs.com/
source_link: https://mystenlabs.com/
github_link: https://github.com/MystenLabs/deepbookv3

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

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
  - Sangsoo Kang
  - MichałBochnak
---

## Vulnerability Title

Denial Of Service Due To Excessive Gas Consumption

### Overview


The vulnerability in this report is caused by an attacker flooding the order book with a large number of small orders, which can cause a high number of remove operations and exceed the max_computation_budget limit. This can block legitimate traders from executing their orders. To fix this issue, the number of orders per account and per transaction should be limited. The vulnerability has been resolved in two pull requests.

### Original Finding Content

## Vulnerability Overview

The vulnerability lies in the potential for a malicious actor to exploit the `max_computation_budget` limit by flooding the order book with a large number of small orders. Each time an order is fully filled, the `process_maker_fill` removes an `order_id` from the open order list of the maker. A malicious actor may create a large number of small orders at a specific price level. When a large market order is placed against this price level, a cascade of order matches occurs, resulting in a high number of `vec_set::remove` operations.

> _account.moverust_

```rust
public(package) fun process_maker_fill(self: &mut Account, fill: &Fill) {
    [...]
    if (fill.expired() || fill.completed()) {
        self.open_orders.remove(&fill.maker_order_id());
    }
}
```

If the gas consumption exceeds the `max_computation_budget` limit, the transaction will fail, effectively blocking legitimate orders. Thus, the attacker prevents legitimate traders from executing their orders by exploiting the fact that the time complexity of `vec_set::remove` is O(n).

## Remediation

Limit the number of orders that a single account can have and the number of orders that can be executed per transaction.

## Patch

Resolved in PR #204 and PR #220.

© 2024 Otter Audits LLC. All Rights Reserved. 11/27

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Mysten Deepbook |
| Report Date | N/A |
| Finders | Robert Chen, Sangsoo Kang, MichałBochnak |

### Source Links

- **Source**: https://mystenlabs.com/
- **GitHub**: https://github.com/MystenLabs/deepbookv3
- **Contest**: https://mystenlabs.com/

### Keywords for Search

`vulnerability`

