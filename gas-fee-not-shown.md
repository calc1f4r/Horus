---
# Core Classification
protocol: Mystic Snap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47929
audit_firm: OtterSec
contest_link: https://github.com/cosmos/snap
source_link: https://github.com/cosmos/snap
github_link: https://github.com/cosmos/snap

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
  - Caue Obici
  - Robert Chen
  - OtterSec
---

## Vulnerability Title

Gas Fee Not Shown

### Overview


This bug report discusses an issue where the confirmation dialog for a transaction does not display the necessary fees, potentially allowing for malicious transactions to drain the user's assets. The suggested solution is to show the fees in the confirmation dialog before the user approves the transaction. The bug has been fixed in a recent commit by adding a fees field in the approval dialog and calculating the fees for the transaction.

### Original Finding Content

## Transaction Confirmation Vulnerability

When requesting a transaction using `transact` in the remote procedure call, the confirmation dialog does not show the fees necessary to complete the transaction. In particular, a malicious transaction may set a high gas fee to drain the user’s assets.

## Code Example

```typescript
// Ensure user confirms transaction
confirmation = await snap.request({
  method: "snap_dialog",
  params: {
    type: "confirmation",
    content: panel([
      heading("Confirm Transaction"),
      divider(),
      heading("Chain"),
      text(`${request.params.chain_id}`),
      divider(),
      heading("Chain"),
      text(`${request.params.msgs}`),
    ]),
  },
});
```

## Remediation

Show the transaction fees in the confirmation dialog, so the user may see it before approving the transaction.

## Patch

Fixed in commit `9da9a9a` by adding the fees field in the approval dialog:

```typescript
// Calculate fees for transaction
let fees: Fees = {
  amount: [],
  gas: "200000",
};

if (request.params.fees) {
  if (typeof request.params.fees == "string") {
    fees = JSON.parse(request.params.fees);
  }
}
```

---

Cosmos Snap Audit 04 | Vulnerabilities

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Mystic Snap |
| Report Date | N/A |
| Finders | Caue Obici, Robert Chen, OtterSec |

### Source Links

- **Source**: https://github.com/cosmos/snap
- **GitHub**: https://github.com/cosmos/snap
- **Contest**: https://github.com/cosmos/snap

### Keywords for Search

`vulnerability`

