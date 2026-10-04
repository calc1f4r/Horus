---
# Core Classification
protocol: Pyth
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48550
audit_firm: OtterSec
contest_link: https://pyth.network/
source_link: https://pyth.network/
github_link: https://github.com/pyth-network/pyth-crosschain/tree/main/aptos

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
  - Harrison Green
  - Robert Chen
  - OtterSec
---

## Vulnerability Title

Assert Length Equality in pyth::parse_data_sources

### Overview

See description below for full details.

### Original Finding Content

## The `pyth::parse_data_sources` Function

The `pyth::parse_data_sources` function takes a list of `emitter_chain_ids` and `emitter_addresses`.  
The function iterates through `emitter_chain_ids` and expects to find a matching address for each entry:

```rust
pyth.move MOVE
fun parse_data_sources(
    emitter_chain_ids: vector<u64>,
    emitter_addresses: vector<vector<u8>>
): vector<DataSource> {
    let sources = vector::empty();
    let i = 0;
    while (i < vector::length(&emitter_chain_ids)) {
        vector::push_back(&mut sources, data_source::new(
            *vector::borrow(&emitter_chain_ids, i),
            external_address::from_bytes(*vector::borrow(&emitter_addresses, i))
        ));
        i = i + 1;
    };
    sources
}
```

In the case where `emitter_addresses` is larger than `emitter_chain_ids`, the function will effectively ignore the extra addresses.

## Remediation

Add a length equality check to ensure the two arguments have the same length.

## Patch

Fixed in #337.

© 2022 OtterSec LLC. All Rights Reserved. 9 / 16

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Pyth |
| Report Date | N/A |
| Finders | Harrison Green, Robert Chen, OtterSec |

### Source Links

- **Source**: https://pyth.network/
- **GitHub**: https://github.com/pyth-network/pyth-crosschain/tree/main/aptos
- **Contest**: https://pyth.network/

### Keywords for Search

`vulnerability`

