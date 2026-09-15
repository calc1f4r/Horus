---
# Core Classification
protocol: Fastlane Atlas
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36794
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Fastlane-Spearbit-Security-Review-April-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Fastlane-Spearbit-Security-Review-April-2024.pdf
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
finders_count: 3
finders:
  - Riley Holterhus
  - Blockdev
  - Gerard Persoon
---

## Vulnerability Title

Borrow() s after validateBalances()

### Overview


This bug report discusses a high-risk issue in the GasAccounting.sol code. The function borrow() can still be called in certain phases, even though it should not be accessible at that point. This could lead to the solver being griefed and also poses a risk of circumventing the unbonding period. The recommended solution is to restrict access to borrow() in these phases, but the current logic does not work in Atlas. The bug has been fixed in PR 227 by only allowing borrow() to be called in the SolverOperation phase or before. This fix has been verified by Spearbit.

### Original Finding Content

## Security Assessment Report

## Severity
**High Risk**

## Context
- GasAccounting.sol#L29-L55
- GasAccounting.sol#L254-L298

## Description
The function `borrow()` can still be called in the `AllocateValue` and `PostOps` phases. As this occurs after `validateBalances()`, the solver must account for this in `_settle()`. However, the solver is no longer in control and could be adversely affected by this design choice. 

Another risk is highlighted in the issue titled "Circumvent AtlETH unbonding period".

## Recommendation
The most logical approach would be to restrict access to `borrow()` during these phases. However, the logic from `SafetyBits` does not apply in Atlas / `borrow()` due to the variable key not being accessible. To address this issue, the `ExecutionPhase` should be retained at the Atlas level.

Refer to the issue "Locking mechanism is complicated" for more context.

## Fastlane
Fixed in PR 227 by only allowing `borrow()` to be called in the `SolverOperation` phase or earlier.

## Spearbit
Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Fastlane Atlas |
| Report Date | N/A |
| Finders | Riley Holterhus, Blockdev, Gerard Persoon |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Fastlane-Spearbit-Security-Review-April-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Fastlane-Spearbit-Security-Review-April-2024.pdf

### Keywords for Search

`vulnerability`

