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
solodit_id: 55061
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/InfiniFi-Spearbit-Security-Review-March-2025.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/InfiniFi-Spearbit-Security-Review-March-2025.pdf
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
finders_count: 4
finders:
  - R0bert
  - Slowfi
  - Jonatas Martins
  - Noah Marconi
---

## Vulnerability Title

UnwindingModule users can avoid slashes by withdrawing before the accrue call

### Overview


The report discusses a bug in the UnwindingModule of the infiniFi protocol. This bug allows users who have started the unwinding process to still receive any earned yield and losses from accrue calls. However, as accrue is not called upon withdrawals, users can exploit this by front-running the accrue call and avoiding any potential losses. The recommendation is to call `YieldSharing.accrue` before any `UnwindingModule.withdraw` call to prevent this exploit. The bug has been fixed in the latest update by reverting if there are any pending unaccrued losses during certain transactions. 

### Original Finding Content

## Severity: Medium Risk

## Context
UnwindingModule.sol#L103

## Description
In the UnwindingModule, users who have begun unwinding and are part of it, still are exposed to any earned yield and losses from accrue calls. However, as accrue is not called upon withdrawals, users could front-run any accrue call that will result in a slash by calling withdraw. The remaining users in the UnwindingModule would absorb the full impact of the negative yield. This could be easily abused by users within the infiniFi protocol to be exposed to yield gains without risking any losses/future slash.

## Recommendation
Consider calling `YieldSharing.accrue` before any `UnwindingModule.withdraw` call. This way, no one in the UnwindingModule can avoid their share of a slash simply by withdrawing preemptively.

## infiniFi
Fixed in 24513bd by reverting if there are pending unaccrued losses when a user does `siUSD ! iUSD`, `liUSD ! iUSD` or `iUSD ! USDC`.

## Spearbit
Fix verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
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

