---
# Core Classification
protocol: Laminar Markets
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48513
audit_firm: OtterSec
contest_link: https://laminar.markets/
source_link: https://laminar.markets/
github_link: http://github.com/laminar-markets/markets

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Robert Chen
  - Naveen Kumar J
  - OtterSec
  - Ajay Shankar K
---

## Vulnerability Title

Tail Not Updating on Node Removal

### Overview

The bug report discusses an issue with the queue::remove function in the RUST programming language. The problem is that the tail node is not being updated when a lone root node or tail node is removed. This can lead to incorrect procedures and cause transaction failures when using the tail node for operations such as iteration. The report includes a proof of concept and a suggested patch to fix the issue.

### Original Finding Content

## Issue with Queue Remove Function

In the `queue::remove` function, the tail node is never updated. This means that whenever a lone root node or a tail node is removed, any subsequent procedures involving the tail node will be incorrect because the tail is not getting updated by this function.

## Code Snippet

```rust
public fun remove<V: store + drop>(queue: &mut Queue<V>, index_to_remove: u64, prev_index: Option<u64>) {
    vector::push_back(&mut queue.free_indices, index_to_remove);
    if (option::is_none(&prev_index)) {
        let node = vector::borrow(&mut queue.nodes, index_to_remove);
        queue.head = node.next;
    } else {
        let next = {
            let node = vector::borrow(&mut queue.nodes, index_to_remove);
            node.next
        };
        let prev_node = vector::borrow_mut(&mut queue.nodes, *option::borrow(&prev_index));
        prev_node.next = next;
    };
    let node = vector::borrow_mut(&mut queue.nodes, index_to_remove);
    node.next = guarded_idx::sentinel();
}
```

The iterator or any other operation that makes use of the tail node will not perform correctly (i.e., cause a transaction failure) as the tail is erroneously pointing to a different node. This would make the tail pointing to a deleted order, thus causing the order book to malfunction.

## Proof of Concept

See **Queue Remove POC**.

## Remediation

To remediate this issue, update the tail when removing the head or tail nodes in a queue.

## Patch

Patch added in commit `0cebfa36`.

© 2022 OtterSec LLC. All Rights Reserved. 7 / 22

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Laminar Markets |
| Report Date | N/A |
| Finders | Robert Chen, Naveen Kumar J, OtterSec, Ajay Shankar K |

### Source Links

- **Source**: https://laminar.markets/
- **GitHub**: http://github.com/laminar-markets/markets
- **Contest**: https://laminar.markets/

### Keywords for Search

`vulnerability`

