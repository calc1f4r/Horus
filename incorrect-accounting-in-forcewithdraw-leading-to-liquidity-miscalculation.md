---
# Core Classification
protocol: Ludex Labs
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52929
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/82ea7f9c-0383-45e9-9630-5863839fa2c5
source_link: https://cdn.cantina.xyz/reports/cantina_riskiit_february2025.pdf
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

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Cryptara
  - r0bert
---

## Vulnerability Title

Incorrect Accounting in forceWithdraw Leading to Liquidity Miscalculation 

### Overview


The forceWithdraw function in the contract is not updating the total amount of available funds correctly after a forced withdrawal, leading to inaccurate tracking of funds. This can result in the contract running out of funds and causing failed transactions. To fix this issue, the function should be updated to accurately decrease the total amount of available funds. This issue has been fixed in PR 51 by Ludex Labs and has been confirmed as fixed by Cantina Managed.

### Original Finding Content

## Review of `forceWithdraw` Function

## Context
(No context files were provided by the reviewer)

## Description
The `forceWithdraw` function does not correctly update `tokenTotalOnLine` or `totalOnLine` after executing a forced withdrawal. This leads to inaccurate tracking of funds, as the withdrawn amount remains counted as part of the available liquidity even though it has already been transferred out of the contract.

By failing to decrement `tokenTotalOnLine` and `totalOnLine`, the protocol incorrectly assumes that more funds are available than actually exist. This can lead to protocol insolvency, where winnings or withdrawals that should be covered by on-chain liquidity may be approved when the contract does not actually hold sufficient funds. Since the system still considers withdrawn amounts as “active” liquidity, future payout calculations will rely on incorrect values, potentially resulting in failed transactions or unintended insolvency.

## Recommendation
The `forceWithdraw` function should explicitly decrease `tokenTotalOnLine` and `totalOnLine` by the withdrawn amount to maintain accurate liquidity tracking. Ensuring these values are correctly updated prevents the contract from overestimating its available funds, safeguarding against insolvency risks and maintaining the integrity of liquidity management.

## Action Items
- **Ludex Labs**: Fixed in PR 51.
- **Cantina Managed**: Fix ok.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Ludex Labs |
| Report Date | N/A |
| Finders | Cryptara, r0bert |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_riskiit_february2025.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/82ea7f9c-0383-45e9-9630-5863839fa2c5

### Keywords for Search

`vulnerability`

