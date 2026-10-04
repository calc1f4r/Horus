---
# Core Classification
protocol: Sanctum
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47588
audit_firm: OtterSec
contest_link: https://www.sanctum.so/
source_link: https://www.sanctum.so/
github_link: https://github.com/igneous-labs/S/tree/ottersec-231220

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
finders_count: 4
finders:
  - OtterSec
  - Robert Chen
  - Tamta Topuria
  - Thibault Marboud
---

## Vulnerability Title

Missing Rebalance Checks

### Overview


Summary:
The start_rebalance function is not properly verifying the destination mint account in the end_rebalance function, which could result in fund loss if the address is incorrect. A fix has been implemented in version 2dec5bb.

### Original Finding Content

## Rebalance Operation Overview

`start_rebalance` initiates a re-balance operation between two liquidity pools. `end_rebalance` is expected to conclude the re-balance operation. However, `start_rebalance` fails to perform a thorough check on the destination liquidity pool’s mint account within `process_start_rebalance`, specifically the `dst_lst_mint` account of `end_rebalance`. The absence of this verification of the destination mint account renders the system susceptible to fund loss if the address in `dst_lst_mint` is inadvertently set to an incorrect value.

## Code Snippet

```rust
pub fn process_start_rebalance(
    accounts: &[AccountInfo],
    args: StartRebalanceIxArgs,
) -> ProgramResult {
    let (
        accounts,
        SrcDstLstSolValueCalculatorCpis {
            src_lst: src_lst_cpi,
            dst_lst: dst_lst_cpi,
        },
        SrcDstLstIndexes {
            src_lst_index,
            dst_lst_index,
        },
    ) = verify_start_rebalance(accounts, &args)?;
    [...]
}
```

## Remediation

Implement checks in `process_start_rebalance` to ensure the destination mint account aligns with the expected properties.

## Patch

Fixed in commit `2dec5bb`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Sanctum |
| Report Date | N/A |
| Finders | OtterSec, Robert Chen, Tamta Topuria, Thibault Marboud |

### Source Links

- **Source**: https://www.sanctum.so/
- **GitHub**: https://github.com/igneous-labs/S/tree/ottersec-231220
- **Contest**: https://www.sanctum.so/

### Keywords for Search

`vulnerability`

