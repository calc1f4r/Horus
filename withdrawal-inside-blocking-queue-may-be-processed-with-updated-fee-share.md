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
solodit_id: 63994
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

Withdrawal inside blocking queue may be processed with updated fee share

### Overview

See description below for full details.

### Original Finding Content

## Severity: Low Risk

## Context
BlockedWithdrawalQueue.sol#L186

## Description
BlockedWithdrawalQueue calculates unstaking fees at withdrawal processing time rather than when the withdrawal is queued. If the fee rate changes while the withdrawal is pending, the user will be charged using the updated unstaking fee rate. This may result in the user paying a different fee than expected at the time they initiated the withdrawal.

## Recommendation
Store the unstaking fee rate in the BlockedWithdrawal struct at the moment the withdrawal is queued, and use that stored value when calculating fees during withdrawal processing.

## Kinetiq
Acknowledged. Will address in full permissionless roll out given don't expect significant changes to unstake fee rate for our markets version.

## Spearbit
Acknowledged.

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

