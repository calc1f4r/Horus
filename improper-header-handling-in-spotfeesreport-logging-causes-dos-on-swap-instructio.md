---
# Core Classification
protocol: Deriverse Dex
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64514
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
github_link: none

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
finders_count: 4
finders:
  - RajKumar
  - Ctrus
  - Alexzoid
  - JesJupyter
---

## Vulnerability Title

Improper header handling in `SpotFeesReport` logging causes DoS on swap instruction

### Overview


This bug report is about a function called `match_orders` which has an issue with handling a variable called `client.header`. The function works fine when the variable is empty, but it fails when the value of `total_fees` is greater than 0. This bug can cause a permanent denial of service (DOS) when the user is trying to use the swap instruction. The recommended solution is to handle this issue gracefully instead of causing the function to fail. The bug has been fixed in a recent update and has been verified by the team.

### Original Finding Content

**Description:** In `match_orders`, `ref_payment` handles `client.header` being None by defaulting to 0, but `ref_client_id` uses `ok_or` and returns an error if `header` is None. This causes the function to fail when `total_fees` > 0 and `header` is None.

```rust
            solana_program::log::sol_log_data(&[bytemuck::bytes_of::<SpotFeesReport>(
                &SpotFeesReport {
                    tag: log_type::SPOT_FEES,
                    fees: total_fees,
                    ref_payment,
                    ref_client_id: client
                        .header
                        .as_ref()
                        .ok_or(drv_err!(DeriverseErrorKind::ClientPrimaryAccountMustBeSome))?
                        .ref_client_id,
                    ..SpotFeesReport::zeroed()
                },
            )]);
```

This will always happen when the user is using the swap instruction.

**Impact:** The impact is high, as this issue results in a permanent DOS whenever the swap instruction is executed and `total_fees > 0` is true.

**Recommended Mitigation:** Consider handling this gracefully instead of reverting when the header is None.

**Deriverse:** Fixed in commit [4f7bc8](https://github.com/deriverse/protocol-v1/commit/4f7bc8ac68325aa93b339ff91c0ac794ea17ffd9).

**Cyfrin:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Deriverse Dex |
| Report Date | N/A |
| Finders | RajKumar, Ctrus, Alexzoid, JesJupyter |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

