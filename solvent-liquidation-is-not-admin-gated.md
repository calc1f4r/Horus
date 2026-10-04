---
# Core Classification
protocol: Honey
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48578
audit_firm: OtterSec
contest_link: https://honey.finance/
source_link: https://honey.finance/
github_link: github.com/honey-labs/nftLendBorrow.

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
finders_count: 3
finders:
  - Shiva Genji
  - OtterSec
  - William Wang
---

## Vulnerability Title

Solvent Liquidation Is Not Admin-Gated

### Overview


The report states that there is a bug in the fourth step of a process called OS-HNY-ADV-00. The bug is related to the "LiquidateSolvent" instruction and the fact that the instruction does not verify if the signer is an admin-controlled address. This means that an attacker could use their own executor account to burn loan notes without transferring tokens. The suggested solution is to use Anchor's address constraint to match the executor account against a hard-coded public key that is admin-controlled. This issue has been fixed in version 53b1491.

### Original Finding Content

## OS-HNY-ADV-00 Process Step 4

The fourth step of the process described in OS-HNY-ADV-00 is performed via the `LiquidateSolvent` instruction. Similarly, notice that the instruction’s signer is not verified to be an admin-controlled address. By specifying their own executor account, an attacker can burn loan notes without transferring tokens.

## Code Snippet

```rust
src/instructions/liquidate_solvent.rs
64 /// The admin/authority that has permission to execute solvent liquidation
65 #[account(mut)]
66 pub executor: Signer<'info>,
```

## Remediation

Use Anchor’s address constraint to match the executor account against a hard-coded public key, which should be admin-controlled.

## Patch

Fixed in commit `53b1491`.

© 2022 OtterSec LLC. All Rights Reserved. 7 / 25

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Honey |
| Report Date | N/A |
| Finders | Shiva Genji, OtterSec, William Wang |

### Source Links

- **Source**: https://honey.finance/
- **GitHub**: github.com/honey-labs/nftLendBorrow.
- **Contest**: https://honey.finance/

### Keywords for Search

`vulnerability`

