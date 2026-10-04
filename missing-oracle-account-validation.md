---
# Core Classification
protocol: Adrena
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46808
audit_firm: OtterSec
contest_link: https://www.adrena.xyz/
source_link: https://www.adrena.xyz/
github_link: https://github.com/AdrenaDEX/adrena

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
finders_count: 2
finders:
  - Robert Chen
  - Tamta Topuria
---

## Vulnerability Title

Missing Oracle Account Validation

### Overview

See description below for full details.

### Original Finding Content

## Current Implementation of the `add_custody` Instruction

In the current implementation of the `add_custody` instruction, only the `oracle_type` is checked. This ensures the oracle type is Pyth and does not allow other oracle types outside the test environment. However, it does not validate if the provided oracle account is actually a valid Pyth oracle account.

> _instructions/admin/custody/add_custody.rsrust_

```rust
pub fn add_custody<'info>(
    ctx: Context<'_, '_, '_, 'info, AddCustody<'info>>,
    params: &AddCustodyParams,
) -> Result<u8> {
    // Preliminary checks
    {
        // Only Pyth oracle is supported outside of testnet
        if OracleType::try_from(params.oracle.oracle_type)? != OracleType::Pyth
            && !cfg!(feature = "test")
        {
            return err!(AdrenaError::InvalidEnvironment);
        }
    }
    [...]
}
```

## Remediation

Validate that the `oracle_account` corresponds to a valid Pyth oracle.

## Patch

Team accepted.

© 2024 Otter Audits LLC. All Rights Reserved. 43 / 59

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Adrena |
| Report Date | N/A |
| Finders | Robert Chen, Tamta Topuria |

### Source Links

- **Source**: https://www.adrena.xyz/
- **GitHub**: https://github.com/AdrenaDEX/adrena
- **Contest**: https://www.adrena.xyz/

### Keywords for Search

`vulnerability`

