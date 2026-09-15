---
# Core Classification
protocol: Blend
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62082
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2025-02-blend-v2-audit-certora-formal-verification
source_link: https://code4rena.com/reports/2025-02-blend-v2-audit-certora-formal-verification
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

[02] `get_market` may get dossed if there are too many reserves

### Overview

See description below for full details.

### Original Finding Content


<https://github.com/code-423n4/2025-02-blend/blob/f23b3260763488f365ef6a95bfb139c95b0ed0f9/blend-contracts-v2/pool/src/contract.rs# L412-L421>

### Finding description and impact

`get_market` loops through amount of reserves, of which there are no ways to remove them and no limit to how many that can be set/add.
```

    fn get_market(e: Env) -> (PoolConfig, Vec<Reserve>) {
        let pool_config = storage::get_pool_config(&e);
        let res_list = storage::get_res_list(&e);
        let mut reserves = Vec::<Reserve>::new(&e);
        for res_address in res_list.iter() {
            let res = Reserve::load(&e, &pool_config, &res_address);
            reserves.push_back(res);
        }
        (pool_config, reserves)
    }
```

### Recommended mitigation steps

Introduce a limit to how many reserves can be set. Also add a function to remove reserves.

---



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Blend |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2025-02-blend-v2-audit-certora-formal-verification
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2025-02-blend-v2-audit-certora-formal-verification

### Keywords for Search

`vulnerability`

