---
# Core Classification
protocol: Kinetiq LST Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63995
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Kinetiq-Spearbit-Security-Review-November-2025.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Kinetiq-Spearbit-Security-Review-November-2025.pdf
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
finders_count: 4
finders:
  - 0xRajeev
  - Kamensec
  - Optimum
  - Rvierdiiev
---

## Vulnerability Title

Slippage protection is missing for the withdrawOnceLive

### Overview

See description below for full details.

### Original Finding Content

## Severity: Low Risk

## Context
EXManager.sol#L550-L555

## Description
When a user withdraws with `withdrawOnceLive()`, they intend to redeem a specific shares amount of exLST. However, depending on `availableWithdrawals()` amount, part—or even all—of the withdrawal may become blocked and placed into the `BlockedWithdrawalQueue` for an unknown period of time. Currently, there is no slippage protection mechanism. In the worst-case scenario, the entire withdrawal request can be forced into the blocked queue, which may be highly unexpected and undesirable for the user.

## Recommendation
Introduce an additional parameter (e.g., `maxBlockedShares`) to define the maximum amount of shares the user is willing to have queued. If more would be blocked, revert the transaction to protect the user from unintended outcomes.

## Kinetiq
Fixed in PR 59.

## Spearbit
Fix verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Kinetiq LST Protocol |
| Report Date | N/A |
| Finders | 0xRajeev, Kamensec, Optimum, Rvierdiiev |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Kinetiq-Spearbit-Security-Review-November-2025.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Kinetiq-Spearbit-Security-Review-November-2025.pdf

### Keywords for Search

`vulnerability`

