---
# Core Classification
protocol: infiniFi contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55050
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/InfiniFi-Spearbit-Security-Review-March-2025.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/InfiniFi-Spearbit-Security-Review-March-2025.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 3

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - R0bert
  - Slowfi
  - Jonatas Martins
  - Noah Marconi
---

## Vulnerability Title

Double-claiming of accrued rewards via unwinding after accrue call

### Overview


This bug report is about a high-risk vulnerability found in a code called UnwindingModule. The issue occurs when a user receives their share of newly deposited rewards during an accrue event, and then immediately moves into the UnwindingModule. This allows them to receive a second portion of the same rewards, which is unfair to other users. The problem is caused by the `balanceOf` calculation starting from a previous epoch, which counts the user as if they were always present on the unwinding side. The recommendation is to adjust the reward distribution logic to prevent users from receiving double rewards for the same epoch. The bug has been fixed in a recent update and verified by a third party.

### Original Finding Content

## High Risk Vulnerability Report

## Severity
**High Risk**

## Context
`UnwindingModule.sol#L103`

## Description
When a user is in the LockingController during an accrue event, they receive their share of newly deposited rewards for that epoch. By immediately calling `startUnwinding` in the same epoch, they move into the UnwindingModule just in time for the UnwindingModule's reward distribution logic to count them as though they were always present on the unwinding side. This effectively grants them a second portion of the same rewards. In practice, the user gains extra shares at the expense of other unwinding users, whose balances are unfairly diluted.

This exploit occurs because the UnwindingModule's `balanceOf` calculation begins iterating from `position.fromEpoch - 1`, meaning that if a user arrives right after an accrue call, they are treated as if they had been in the unwinding side throughout that epoch.

## Recommendation
Adjust the reward distribution logic so that a user cannot receive two sets of rewards for the same epoch. One option is to remove or revise the `position.fromEpoch - 1` iteration start in the `balanceOf` function and ensure that newly arrived users in the UnwindingModule are ineligible for the current epoch's distribution if they were counted on the LockingController side.

## Additional Information
- **infiniFi:** Fixed in `d683c30`.
- **Spearbit:** Fix verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 3/5 |
| Audit Firm | Spearbit |
| Protocol | infiniFi contracts |
| Report Date | N/A |
| Finders | R0bert, Slowfi, Jonatas Martins, Noah Marconi |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/InfiniFi-Spearbit-Security-Review-March-2025.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/InfiniFi-Spearbit-Security-Review-March-2025.pdf

### Keywords for Search

`vulnerability`

