---
# Core Classification
protocol: Sui Axelar (Gateway V2)
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47311
audit_firm: OtterSec
contest_link: https://www.axelar.network/
source_link: https://www.axelar.network/
github_link: https://github.com/axelarnetwork/axelar-cgp-sui

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
  - Tuyết Dương
  - Jessica Clendinen
---

## Vulnerability Title

Incorrect Function Call

### Overview


The report discusses a bug in a piece of code that is responsible for estimating the swap balance between two assets. Instead of using the correct function to retrieve the current balance of the asset being swapped, the code mistakenly calls a different function that only retrieves estimated amounts. This results in inaccurate estimates being made. The solution is to first store the balance of the asset being swapped before calling the function to retrieve estimated amounts. The bug has been fixed in a recent update.

### Original Finding Content

## Estimation Issue in Swap Functionality

The function `estimate` should estimate the swap balance of one asset (T2) from another asset (T1). However, instead of utilizing the correct function to retrieve the current balance of the asset being swapped (T2), it mistakenly calls `get_estimate`, which retrieves the estimated amounts instead of the actual balances.

> _sources/squid/deepbook_v2.moverust

```rust
public fun estimate<T1, T2>(self: &mut SwapInfo, pool: &Pool<T1, T2>, clock: &Clock) {
    [...]
    if(has_base) {
        let (amount_left, output) = predict_base_for_quote(
            pool,
            self.coin_bag().get_estimate<T1>(),
            lot_size,
            clock,
        );
        self.coin_bag().store_estimate<T1>(amount_left);
        self.coin_bag().store_estimate<T2>(output);
    }
    [...]
}
```

Since `get_estimate` returns zero (assuming no estimate has been stored), the estimation process will be based on an incorrect or missing balance amount, resulting in inaccurate estimates.

## Remediation

Ensure to store the balance of the asset being swapped to `estimate` before calling `get_estimate`.

## Patch

Fixed in PR #58.

© 2024 Otter Audits LLC. All Rights Reserved. 7/18

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Sui Axelar (Gateway V2) |
| Report Date | N/A |
| Finders | Robert Chen, Tuyết Dương, Jessica Clendinen |

### Source Links

- **Source**: https://www.axelar.network/
- **GitHub**: https://github.com/axelarnetwork/axelar-cgp-sui
- **Contest**: https://www.axelar.network/

### Keywords for Search

`vulnerability`

