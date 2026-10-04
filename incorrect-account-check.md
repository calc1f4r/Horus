---
# Core Classification
protocol: Solayer Labs
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47341
audit_firm: OtterSec
contest_link: https://solayer.org/
source_link: https://solayer.org/
github_link: https://github.com/solayer-labs/restaking-program

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
finders_count: 2
finders:
  - Ajay Shankar Kunapareddy
  - Robert Chen
---

## Vulnerability Title

Incorrect Account Check

### Overview


The program is using the wrong account to check if the RST account is frozen, which can lead to incorrect behavior. The suggested solution is to refactor the code to check the correct account. The bug has been fixed in the latest updates.

### Original Finding Content

## Program Issue Overview

The program utilizes the condition `if self.lst_ata.is_frozen()` in `restaking::freeze_rst_account` to check if the RST account (`rst_ata`) is already frozen. However, this check is incorrect as the program performs it on the `lst_ata` account.

> _restaking-program/src/contexts/restaking.rs_

```rust
// Freeze RST token account if thawed
pub fn freeze_rst_account(&mut self) -> Result<()> {
    if self.lst_ata.is_frozen() {
        return Ok(())
    }
    let bump = [self.pool.bump];
    [...]
    freeze_account(ctx)
}
```

By checking the `is_frozen()` status of the incorrect account (`lst_ata` instead of `rst_ata`), the function may inaccurately determine that the RST account is already frozen when it is not. This may result in unintended behavior, such as skipping the freezing operation when freezing is necessary.

## Remediation

Refactor `freeze_rst_account` to check the status of the `rst_ata` account.

## Patch

Fixed in 9401126 and 4a25804.

© 2024 Otter Audits LLC. All Rights Reserved. 5/9

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Solayer Labs |
| Report Date | N/A |
| Finders | Ajay Shankar Kunapareddy, Robert Chen |

### Source Links

- **Source**: https://solayer.org/
- **GitHub**: https://github.com/solayer-labs/restaking-program
- **Contest**: https://solayer.org/

### Keywords for Search

`vulnerability`

