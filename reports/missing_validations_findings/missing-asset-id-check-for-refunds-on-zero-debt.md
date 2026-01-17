---
# Core Classification
protocol: Fluid Protocol (Hydrogen Labs)
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46897
audit_firm: OtterSec
contest_link: https://fluidprotocol.xyz/
source_link: https://fluidprotocol.xyz/
github_link: https://github.com/Hydrogen-Labs/fluid-protocol

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
finders_count: 3
finders:
  - James Wang
  - Alpha Toure
  - Renato Eugenio Maria Marziano
---

## Vulnerability Title

Missing Asset ID Check for Refunds on Zero Debt

### Overview

See description below for full details.

### Original Finding Content

## Vulnerability Overview

The vulnerability concerns the refund logic for excess USDF in `close_trove` when the debt is zero. If the amount of USDF sent (`msg_amount`) is greater than the debt, the difference is treated as "excess" and is refunded to the borrower. However, the issue arises from the fact that there is no asset type check when the debt is zero. The `msg_asset_id` check is only done when the debt is greater than zero.

## Code Snippet

```sway
// borrow-operations-contract/src/main.sw
// Close an existing trove
#[storage(read, write), payable]
fn close_trove(asset_contract: AssetId) {
    [...]
    active_pool.send_asset(borrower, coll, asset_contract);
    if (debt < msg_amount()) {
        let excess_usdf_returned = msg_amount() - debt;
        transfer(borrower, usdf_asset_id, excess_usdf_returned);
    }
    storage.lock_close_trove.write(false);
}
```

This implies that if the debt happens to be zero and the borrower sends any asset type (not necessarily USDF), the excess refund logic may execute. This would allow a malicious borrower to manipulate the system by sending non-USDF tokens or even tokens of no value and receiving USDF in return. While the current system does not seem to have any identified methods to get a debt of exactly zero without closing the trove automatically, it’s always safer to proactively address this, as if this vulnerability were to somehow occur, it could have severe financial consequences.

## Remediation

Add a check for `msg_asset_id` even if the debt is zero. This ensures that only valid USDF tokens are involved in the transaction.

## Patch

Resolved in `ffc5193`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Fluid Protocol (Hydrogen Labs) |
| Report Date | N/A |
| Finders | James Wang, Alpha Toure, Renato Eugenio Maria Marziano |

### Source Links

- **Source**: https://fluidprotocol.xyz/
- **GitHub**: https://github.com/Hydrogen-Labs/fluid-protocol
- **Contest**: https://fluidprotocol.xyz/

### Keywords for Search

`vulnerability`

