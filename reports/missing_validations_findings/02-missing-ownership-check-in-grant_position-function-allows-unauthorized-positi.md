---
# Core Classification
protocol: Superposition
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45242
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-10-superposition
source_link: https://code4rena.com/reports/2024-10-superposition
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

[02] Missing ownership check in `grant_position` function allows unauthorized position transfers

### Overview

See description below for full details.

### Original Finding Content


The `grant_position` function is to require that a position must not have an owner before granting ownership as hinted [here](https://github.com/code-423n4/2024-10-superposition/blob/7ad51104a8514d46e5c3d756264564426f2927fe/pkg/seawater/src/lib.rs#L452). Albeit, the function does not enforce this requirement. The function directly sets the new owner without verifying if the position is already owned, which could allow unauthorized overwriting of position ownership.

https://github.com/code-423n4/2024-10-superposition/blob/7ad51104a8514d46e5c3d756264564426f2927fe/pkg/seawater/src/lib.rs#L453-L462

```rust
/// Makes the user the owner of a position. The position must not have an owner.
fn grant_position(&mut self, owner: Address, id: U256) {
    // set owner
    self.position_owners.setter(id).set(owner);
    
    // increment count
    let owned_positions_count = self.owned_positions.get(owner) + U256::one();
    self.owned_positions
        .setter(owner)
        .set(owned_positions_count);
}
```

This could allow unauthorized transfers of position ownership, going against the intention.

### Recommendation

Consider adding a check at the beginning of the `grant_position` function to verify that the position's current owner is `Address::ZERO` before proceeding with the ownership transfer. Also add a new error msg to handle cases where a position is already owned.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Superposition |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2024-10-superposition
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2024-10-superposition

### Keywords for Search

`vulnerability`

