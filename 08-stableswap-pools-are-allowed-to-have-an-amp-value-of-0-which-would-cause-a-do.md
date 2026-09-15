---
# Core Classification
protocol: MANTRA
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55015
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-11-mantra-dex
source_link: https://code4rena.com/reports/2024-11-mantra-dex
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

[08] Stableswap pools are allowed to have an amp value of 0 which would cause a DOS to swaps on pools

### Overview

See description below for full details.

### Original Finding Content


[/contracts/pool-manager/schema/pool-manager.json# L588-L612](https://github.com/code-423n4/2024-11-mantra-dex/blob/26714ea59dab7ecfafca9db1138d60adcf513588/contracts/pool-manager/schema/pool-manager.json# L588-L612)
```

      "PoolType": {
        "description": "Possible pool types, it can be either a constant product (xyk) pool or a stable swap pool.",
        "oneOf": [
          {
            "description": "A stable swap pool.",
            "type": "object",
            "required": [
              "stable_swap"
            ],
            "properties": {
              "stable_swap": {
                "type": "object",
                "required": [
                  "amp"
                ],
                "properties": {
                  "amp": {
                    "description": "The amount of amplification to perform on the constant product part of the swap formula.",
                    "type": "integer",
                    "format": "uint64",
                    "minimum": 0.0
                  }
                },
                "additionalProperties": false
              }
```

We can see that during creation of a stable swap pool the amp value is allowed to be 0, which is not a valid value.

This has been flagged in the forked WhiteWhale audit report previously, see [report here](https://github.com/SCV-Security/PublicReports/blob/main/WhiteWhale/White%20Whale%20-%20Core%20Pool%20Contracts%20-%20Audit%20Report%20v1.0.pdf). However, the issue is that when we have an amp value of 0, all swaps would fail.

### Impact

Borderline here, considering with an amp value of 0, all swaps would fail causing a DOS in using the pool.

> *After a further review, this case completely bricks the pool instance and as such a more detailed report has been submitted.*

### Recommended Mitigation Steps

Change the min amp value to 1, as done in the [test module](https://github.com/code-423n4/2024-11-mantra-dex/blob/26714ea59dab7ecfafca9db1138d60adcf513588/contracts/pool-manager/src/helpers.rs# L957-L958):
```

    /// Minimum amplification coefficient.
    pub const MIN_AMP: u64 = 1;
```



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | MANTRA |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2024-11-mantra-dex
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2024-11-mantra-dex

### Keywords for Search

`vulnerability`

