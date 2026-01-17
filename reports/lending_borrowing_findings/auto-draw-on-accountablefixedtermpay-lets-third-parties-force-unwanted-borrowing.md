---
# Core Classification
protocol: Accountable
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62983
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md
github_link: none

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

protocol_categories:
  - options_vault
  - liquidity_manager
  - insurance
  - uncollateralized_lending

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Immeas
  - Chinmay
  - Alexzoid
---

## Vulnerability Title

Auto-draw on `AccountableFixedTerm::pay` lets third parties force unwanted borrowing

### Overview


The bug report discusses an issue with the `AccountableFixedTerm` contract's `pay` function. This function automatically draws any positive drawable funds before transferring due interest or fees. However, this can lead to unexpected increases in debt for the borrower if a third party deposits funds into the vault right before the borrower calls `pay`. This can be exploited to cause griefing or economic denial of service attacks. The recommended solution is to remove the auto-draw feature from the `pay` function and only allow loan increases through explicit borrower actions. This bug has been fixed in the `03f871b` commit of the `credit-vaults-internal` repository.

### Original Finding Content

In [`AccountableFixedTerm::pay`](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/strategies/AccountableFixedTerm.sol#L354-L357), any positive `_loan.drawableFunds` are automatically drawn via `_updateAndRelease(drawableFunds)` before transferring the due interest/fees:
```solidity
uint256 drawableFunds = _loan.drawableFunds;
if (drawableFunds > 0) {
    _updateAndRelease(drawableFunds);
}
```

Since `_loan.drawableFunds` increases when users deposit/mint into the vault, a third party can deposit immediately before the borrower calls `pay`. This causes `pay` to both increase `_loan.outstandingPrincipal` by the new liquidity and also add remaining-term interest on that added principal, while releasing the assets to the borrower, without borrower consent.

**Impact:** Borrower loses discretion over principal size. Calling `pay` can increase debt (principal + future interest) unexpectedly. This enables griefing/economic DoS as attackers can “stuff” the vault before each payment window, repeatedly forcing draws and increasing interest payments in the future.

**Recommended Mitigation:** Consider removing auto-draw from `AccountableFixedTerm::pay`. Loan increases should occur only via an explicit borrower action (e.g., `draw(uint256)`), not implicitly during interest payment.

**Accountable:** Fixed in commit [`03f871b`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/03f871bfc7baff5fe5f9dfbd8a0ef74e99619e78)

**Cyfrin:** Verified. "auto-draw" is removed from `pay`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Accountable |
| Report Date | N/A |
| Finders | Immeas, Chinmay, Alexzoid |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

