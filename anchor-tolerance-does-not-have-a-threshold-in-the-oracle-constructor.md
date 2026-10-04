---
# Core Classification
protocol: Protocol MultiversX
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51028
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/hatom/hatom-protocol-multiversx
source_link: https://www.halborn.com/audits/hatom/hatom-protocol-multiversx
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
  - Halborn
---

## Vulnerability Title

ANCHOR TOLERANCE DOES NOT HAVE A THRESHOLD IN THE ORACLE CONSTRUCTOR

### Overview

See description below for full details.

### Original Finding Content

##### Description

The anchor tolerance is set to ensure the acceptable deviation between the oracle's reported price and the actual market price of the asset. In the oracle's `init` function, this deviation is set using the parameter `anchor_tolerance`. The function `set_anchor_tolerance_internal` checks that the lower\_bound is at least 1, but the upper bound is 1 + the submitted anchor tolerance, so the upper bound can have any value.

Big upper bounds could make the oracle vulnerable to price manipulations and/or high volatility.

  

### Code Location

Down below is the code snippet from the `set_anchor_tolerance_internal` function:

The upper bound is calculated here:

  

* oracle/src/[common.rs](http://common.rs)

```
fn set_anchor_tolerance_internal(&self, anchor_tolerance: &BigUint) {
        let wad = BigUint::from(WAD);
        let upper_bound = &wad + anchor_tolerance;
        let lower_bound = if anchor_tolerance < &wad {
            &wad - anchor_tolerance
        } else {
            // avoid prices being zero
            BigUint::from(1u32)
        };
        self.upper_bound_ratio().set(upper_bound);
        self.lower_bound_ratio().set(lower_bound);
    }
```

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:N/R:N/S:U (0.0)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:N/R:N/S:U)

##### Recommendation

It is recommended to set a max value for the upper bound, so the anchor tolerance is always between a reasonable value.

  
  

### Remediation Plan

**SOLVED:** The issue was solved in commit `035ec` by setting a `max_anchor_tolerance` value as threshold.

##### Remediation Hash

<https://github.com/HatomProtocol/hatom-protocol/commit/035ec0aa60acbaeeb27fb02db818854c0ed19403>

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Protocol MultiversX |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/hatom/hatom-protocol-multiversx
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/hatom/hatom-protocol-multiversx

### Keywords for Search

`vulnerability`

