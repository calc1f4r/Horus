---
# Core Classification
protocol: Brava Labs
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53565
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/brava/report.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/brava/report.pdf
github_link: none

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
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

Protocol Fees Can Be Bypassed By Users

### Overview


The bug report discusses an issue where users can manipulate fee timestamps, potentially avoiding fee payments when interacting with Brava. This can be done by sending a transaction to the `setFeeTimestamp()` function without any restrictions. This could lead to users evading fee payments by updating the timestamp before withdrawing funds. To fix this, Brava Labs have added a guard to restrict calls from Safe wallets to only approved actions. This may require significant changes to the fee protocol's design.

### Original Finding Content

## Description

Fee timestamps are crucial for calculating the payments users owe to Brava during interactions; however, users can directly manipulate these timestamps, potentially avoiding any fee payments.

A user can interact directly with the AdminVault contract through their Safe wallet by sending a transaction to the `setFeeTimestamp()` function, specifying the pool addresses where they hold active deposits. 

There are no access restrictions on this function, allowing the user to update the `lastFeeTimestamp` for both their Safe wallet and the specified pool to the current timestamp. Because `lastFeeTimestamp` plays a critical role in the `_calculateFee()` function, which assesses fees for nearly all user actions, this could enable a user to maliciously update the timestamp before withdrawing funds, thereby evading fee payments.

## Recommendations

- Users should not have unrestricted access to alter their fee timestamp.
- Addressing this vulnerability would likely require significant modifications to the fee protocol’s design.

## Resolution

Brava Labs have added a guard to the Safe wallets that end users deploy. This restricts calls made from the Safe wallet to only be sent to the `SequenceExecutor` contract which, in turn, checks that only approved actions are performed from the Safe wallet.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Brava Labs |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/brava/report.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/brava/report.pdf

### Keywords for Search

`vulnerability`

