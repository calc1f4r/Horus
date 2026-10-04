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
solodit_id: 62982
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

Withdrawal queue `RequestPrice` can be front run in case of defaults

### Overview


The bug report explains that when the `processingMode` is set to `ProcessingMode.RequestPrice` in the `AccountableWithdrawalQueue`, there is an issue with the redeem request's value being fixed at the time of the request. This means that the request is processed at a potentially different price, which can disadvantage requesters. This can also lead to front-running defaults and causing losses for other users. To fix this, it is recommended to remove `processingMode` or implement a safeguard for large price movements. The bug has been fixed and verified by Cyfrin.

### Original Finding Content

**Description:** When `processingMode == ProcessingMode.RequestPrice` in `AccountableWithdrawalQueue`, a redeem request’s value is fixed at the request-time share price. The request is later processed potentially at a very different price.

**Impact:** * Normal operation: Requesters are typically disadvantaged because price usually rises as interest accrues. Locking at request time forfeits subsequent gains.
* Defaults: Requesters can front-run defaults by submitting withdrawals just before delinquency/default and keep the pre-default higher price, draining liquidity and pushing losses onto remaining LPs. This worsens loss socialization precisely when fairness matters most.

**Recommended Mitigation:** Consider removing `ProcessingMode.RequestPrice` (and `AccountableWithdrawalQueue .processingMode` all together) so redemption value is always determined at processing time. Alternatively implement a safeguard for large price movements that will invalidate the redeem request.

**Accontable:**
Fixed in commit [`4e5eef5`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/4e5eef57464d548ec09048eae27b6fcc1489a5c3)

**Cyfrin:** Verified. `processingMode` removed and current price used throughout.

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

