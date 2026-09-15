---
# Core Classification
protocol: Mysten Labs Sui
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48097
audit_firm: OtterSec
contest_link: https://mystenlabs.com/
source_link: https://mystenlabs.com/
github_link: https://github.com/MystenLabs/sui

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
finders_count: 5
finders:
  - Cauê Obici
  - Michal Bochnak
  - James Wang
  - Robert Chen
  - OtterSec
---

## Vulnerability Title

Absence Of Checks For Max TTL

### Overview


This bug report discusses a problem with the MAX_TTL constant in registry.move. The issue is that this constant is not being checked when new domains are registered or when a new TTL (Time to Live) value is assigned. This means that users can assign invalid TTL values to their domain names. The code responsible for this check has been temporarily removed and will be rewritten in the future. To fix this issue, proper validation checks need to be implemented to enforce the maximum TTL size during domain registration and when setting the TTL value.

### Original Finding Content

## TTL Validation Issue in `registry.move`

The `MAX_TTL` constant is present in `registry.move`. However, it is not verified when new domains are registered or a new TTL is assigned. In the absence of this check, users may assign invalid TTL values to their domain names.

## Code Snippet

```rust
public entry fun set_ttl(suins: &mut SuiNS, domain_name: vector<u8>, ttl: u64, ctx: &mut TxContext) {
    authorised(suins, domain_name, ctx);
    let domain_name = string::utf8(domain_name);
    let record = get_name_record_mut(suins, domain_name);
    *entity::name_record_ttl_mut(record) = ttl;
    event::emit(TTLChangedEvent { domain_name, new_ttl: ttl });
}
```

```rust
public(friend) fun set_record_internal(
    suins: &mut SuiNS,
    domain_name: String,
    owner: address,
    ttl: u64,
    ctx: &mut TxContext,
) {
    let registry = entity::registry_mut(suins);
    if (table::contains(registry, domain_name)) {
        let record = table::borrow_mut(registry, domain_name);
        *name_record_owner_mut(record) = owner;
        *name_record_ttl_mut(record) = ttl;
        *name_record_linked_addr_mut(record) = owner;
    } else new_record(suins, domain_name, owner, ttl, ctx);
}
```

## Remediation

Implement proper validation checks to enforce the maximum TTL size during domain registration and when setting the TTL value.

## Patch

This portion of the code has been temporarily removed and will be rewritten in the future.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Mysten Labs Sui |
| Report Date | N/A |
| Finders | Cauê Obici, Michal Bochnak, James Wang, Robert Chen, OtterSec |

### Source Links

- **Source**: https://mystenlabs.com/
- **GitHub**: https://github.com/MystenLabs/sui
- **Contest**: https://mystenlabs.com/

### Keywords for Search

`vulnerability`

