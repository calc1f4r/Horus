---
# Core Classification
protocol: Liquid Collective PRD
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26506
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/LiquidCollectivePR-Spearbit-Security-Review-Sept.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/LiquidCollectivePR-Spearbit-Security-Review-Sept.pdf
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
  - Xiaoming90 
  - Saw-mon and Natalie 
  - Optimum 
  - Ellahi 
---

## Vulnerability Title

TlcMigration.migrate : Missing input validation

### Overview

See description below for full details.

### Original Finding Content

## Vulnerability Report

## Severity
Low Risk

## Context
`TLC_globalUnlockScheduleMigration.sol#L365-L386`

## Description
The upcoming change in some of the vesting schedules is going to be executed via the `migrate` function, which at the current version of the code is missing necessary validation checks to make sure no erroneous values are inserted.

## Recommendation
Consider adding the following post-effects validation checks:
1. Ensure that `VestingSchedule.cliffDuration` cannot be longer than the total duration (`VestingSchedule.duration`).
2. `VestingSchedule.end` should not be less than `VestingSchedule.start + VestingSchedule.cliffDuration + delta` (for partial release) or `VestingSchedule.start + VestingSchedule.duration` (for full release).
3. Ensure that all vesting schedules have the unlock date `VestingSchedule.start + VestingSchedule.lockDuration` set to **16/10/2024 0:00 GMT+0**.

## Liquid Collective
Fixed in commit `340d9f` and commit `4f63c4`.

## Spearbit
Fixed in commit `340d9f` and commit `4f63c4` by implementing the auditor's recommendations.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Liquid Collective PRD |
| Report Date | N/A |
| Finders | Xiaoming90 , Saw-mon and Natalie , Optimum , Ellahi  |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/LiquidCollectivePR-Spearbit-Security-Review-Sept.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/LiquidCollectivePR-Spearbit-Security-Review-Sept.pdf

### Keywords for Search

`vulnerability`

