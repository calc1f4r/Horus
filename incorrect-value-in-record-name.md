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
solodit_id: 48093
audit_firm: OtterSec
contest_link: https://mystenlabs.com/
source_link: https://mystenlabs.com/
github_link: https://github.com/MystenLabs/sui

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
finders_count: 5
finders:
  - Cauê Obici
  - Michal Bochnak
  - James Wang
  - Robert Chen
  - OtterSec
---

## Vulnerability Title

Incorrect Value In Record Name

### Overview


The function "registry::get_name_record_all_fields" is supposed to retrieve certain information from a given domain name. However, there are two situations where it returns incorrect values. Firstly, when the domain is a normal one, the function returns an empty string for the default domain name. Secondly, when the domain is a subdomain of "addr.reverse", the function returns the default domain name without checking for validity. To fix this, the code needs to be adjusted to handle these scenarios properly. Currently, this part of the code has been removed and will be rewritten in the future.

### Original Finding Content

## Documentation for `get_name_record_all_fields`

`registry::get_name_record_all_fields` retrieves owner, linked address, TTL, and default domain name from a domain name.

## Source
```
source/tmp/registry.move RUST
```

## Function Signature
```rust
public fun get_name_record_all_fields(suins: &SuiNS, domain_name: vector<u8>)
    -> (address, address, u64, String) {
    let name_record = get_name_record(suins, utf8(domain_name));
    (
        name_record_owner(name_record),
        name_record_linked_addr(name_record),
        name_record_ttl(name_record),
        name_record_default_domain_name(name_record)
    )
}
```

## Description
This function returns erroneous values under two circumstances:
1. When the domain is a normal domain, the function returns an empty string for `default_domain_name`.
2. When the domain is a subdomain of `addr.reverse`, the function returns the default domain name without validation.

## Remediation
Handle the previous scenarios and return the correct value.

## Patch
This portion of the code has been temporarily removed and will be rewritten in the future.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

