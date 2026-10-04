---
# Core Classification
protocol: Wallek
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35382
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-04-04-Wallek.md
github_link: none

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
finders_count: 1
finders:
  - Zokyo
---

## Vulnerability Title

Unused 'public' visibility.

### Overview

See description below for full details.

### Original Finding Content

**Severity**: Informational

**Status**: Resolved

**Description**

TestStake: emergency WithdrawMatic(), feeWithdraw(), addFreezeWallet(), setOwnersAndMinimum Signatures(), revokeVote(), proposeAndVote Upgrade(), totalAmount(), updateStakeWallet(), unStakeAll(), reStake(), stake(), addNRemoveAdmin(), setStakeFee(), initialize().
The functions have 'public' visibility, yet they are not used anywhere inside the contract, inherited contracts, or derived contracts. Therefore, it is recommended that they be given 'external visibility to reduce gas consumption and improve code consistency and readability.

**Recommendation:**

Transfer the accumulated amount instead of multiple external calls.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Wallek |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-04-04-Wallek.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

