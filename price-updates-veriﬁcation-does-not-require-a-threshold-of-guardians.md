---
# Core Classification
protocol: Layer N
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54000
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/6e130af9-2dbf-41f3-8cd7-df28be1006f2
source_link: https://cdn.cantina.xyz/reports/cantina_layern_august2024.pdf
github_link: none

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
  - zigtur
  - Rikard Hjort
  - defsec
---

## Vulnerability Title

Price updates veriﬁcation does not require a threshold of guardians 

### Overview


The `PriceUpdates::verify` function is used to make sure that the Pyth price feed update is valid. However, it does not check if a minimum number of guardians have approved the update. This means that even if only one guardian approves the update, it will still be considered valid. To fix this, the function should be updated to include additional checks such as ensuring that each guardian is unique and that a certain number of guardians have approved the update. This issue has been fixed in PR 1060 and a threshold of 2/3 of the configured guardians must now be met for the update to be considered valid.

### Original Finding Content

## PriceUpdates::verify Function

## Context 
`pyth.rs#L213-L231`

## Description 
The `PriceUpdates::verify` function is used during the Pyth price feed update action to ensure that:

1. The update guardian set index corresponds to the admin configured index.
2. The update guardian set is not empty.
3. Each update guardian is known in the guardian set configured by the admin.

```rust
pub fn verify(&self, guardian_set: &GuardianSet) -> bool {
    if guardian_set.index != self.guardian_set_index { // @audit: Check 1
        return false;
    }
    if self.guardians.is_empty() { // @audit: Check 2
        return false;
    }
    for (index, guardian) in self.guardians.iter() { // @audit: Check 3
        let address = guardian_set.addresses.get(*index);
        match address {
            Some(x) if x == guardian => continue,
            _ => return false,
        }
    }
    true
}
```

However, `verify` does not ensure that a minimum threshold of guardians approved the price update (Wormhole VAAs). In the current state, a single valid guardian in the update will make the verification succeed. According to the Wormhole documentation about security, a message is considered valid if 2/3 of the guardians signed it:

> If a super majority (e.g. 13 out of 19) Guardians sign the same message, it can be considered valid.

## Recommendation 
The `PriceUpdates::verify` function should implement additional checks:

- Ensure that each guardian in the update guardian set is unique.
- Ensure that the length of the update guardian set is greater than or equal to a threshold (e.g. 2/3 of the configured guardians). It is 13 when 19 guardians are configured according to Wormhole documentation.

## LayerN 
Fixed in PR 1060.

## Cantina Managed 
Fixed. During a price feed processing, a threshold of 2/3 of the configured guardians setup must be met. This is achieved in `Users::check_pyth_update`. Moreover, the threshold is designed to avoid loss of precision due to division.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Layer N |
| Report Date | N/A |
| Finders | zigtur, Rikard Hjort, defsec |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_layern_august2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/6e130af9-2dbf-41f3-8cd7-df28be1006f2

### Keywords for Search

`vulnerability`

