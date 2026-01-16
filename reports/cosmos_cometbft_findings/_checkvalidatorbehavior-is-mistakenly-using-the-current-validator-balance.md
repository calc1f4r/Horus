---
# Core Classification
protocol: Kinetiq LST
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58599
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Kinetiq-Spearbit-Security-Review-March-2025.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Kinetiq-Spearbit-Security-Review-March-2025.pdf
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
  - Rvierdiiev
  - Slowfi
  - Hyh
  - Optimum
---

## Vulnerability Title

_checkValidatorBehavior() is mistakenly using the current validator balance

### Overview


The bug report discusses an issue with the `_checkValidatorBehavior()` function in the OracleManager.sol file. This function is responsible for checking the reasonableness of changes in the slashed amount and rewards amount. The problem arises when tolerance levels, represented as percentages of the current balance of the validator, are used to make these checks. In a specific scenario, the function returns a false result instead of the expected true result. The recommendation is to fetch the balance before the change and use it for the checks instead. The bug has been acknowledged by Kinetiq and Cantina Managed.

### Original Finding Content

## Medium Risk Report

## Severity
Medium Risk

## Context
OracleManager.sol#L165

## Description
The `_checkValidatorBehavior()` function implements checks to ensure that the changes in the slashed amount and rewards amount are reasonable. To achieve this, tolerance levels are defined for both variables. 

In practice, these tolerance levels are represented as percentages of the `avgBalance` parameter, which is the current balance of the validator (after the change). 

To better understand the issue, let's consider a simple example:

- **SlashingTolerance** = 10%.
- Current balance of validator A is 100 (already stored inside the ValidatorManager contract).
- At this point, there is a slashing of 10.
- For simplicity, assuming all oracles submit the same values, in the call to `generatePerformance()`, we will have:
  - `avgBalance` = 90.
  - `avgSlashAmount` = 10.

The issue here is that the call to `_checkValidatorBehavior()` will return false (instead of true) since the computation will be:

```
slashingBps = (10 / 90) % > SlashingTolerance (10%).
```

## Recommendation
Consider fetching the balance before the change by calling `ValidatorManager.validatorPerformance()` and using it for `_checkValidatorBehavior()` instead.

## Acknowledgements
- Kinetiq: Acknowledged.
- Cantina Managed: Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Kinetiq LST |
| Report Date | N/A |
| Finders | Rvierdiiev, Slowfi, Hyh, Optimum |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Kinetiq-Spearbit-Security-Review-March-2025.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Kinetiq-Spearbit-Security-Review-March-2025.pdf

### Keywords for Search

`vulnerability`

