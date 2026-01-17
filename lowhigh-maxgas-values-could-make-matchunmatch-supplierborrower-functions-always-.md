---
# Core Classification
protocol: Morpho
chain: everychain
category: logic
vulnerability_type: validation

# Attack Vector Details
attack_type: validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6935
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - validation
  - gas_limit

protocol_categories:
  - cdp
  - derivatives
  - dexes
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - hack3r-0m
  - Jay Jonah
  - Christoph Michel
  - Emanuele Ricci
---

## Vulnerability Title

Low/high MaxGas values could make match/unmatch supplier/borrower functions always “fail” or revert

### Overview


This bug report is about the variable maxGas used in the contracts PositionsManagerForAaveGettersSetters.sol and PositionsManagerForAaveLogic.sol. The variable maxGas is used to determine how much gas the matchSuppliers, unmatchSuppliers, matchBorrowers, and unmatchBorrowers functions can consume while trying to match/unmatch supplier/borrower and also updating their position if matched. If maxGas is set to 0, the loop will be skipped entirely, and if maxGas is set too low, the loop may not be able to match/unmatch all available suppliers/borrowers and may consume all the block gas, causing the transaction to revert. It is recommended that enough tests be done to determine a safe minimum/maximum value for maxGas. Morpho has suggested that the parameters will be decided by governance in the future, with a time-lock of seven days to ensure everyone can check the relevance of these parameters, and that the governance has no incentives to implement wrong parameters that could harm Morpho and its users. Spearbit has acknowledged this.

### Original Finding Content

## Vulnerability Report

## Severity
**Medium Risk**

## Context
- PositionsManagerForAaveGettersSetters.sol#L47-L50
- PositionsManagerForAaveLogic.sol#L34

## Description
The `maxGas` variable is used to determine how much gas the `matchSuppliers`, `unmatchSuppliers`, `matchBorrowers`, and `unmatchBorrowers` functions can consume while trying to match/unmatch suppliers/borrowers and also updating their position if matched.

- `maxGas = 0` will make the process skip the loop entirely.
- A low `maxGas` will make the loop run at least one time, but the smaller the `maxGas`, the higher the possibility that not all available suppliers/borrowers are matched/unmatched.
- A very high `maxGas` could cause the loop to consume all the block gas, leading to a transaction revert.

*Note:* `maxGas` can be overridden by the user when calling the `supply` or `borrow` functions.

## Recommendation
Conduct thorough testing to determine a safe minimum and maximum value for `maxGas`.

## Morpho
These parameters will be decided by governance in the future. We will implement a time-lock of seven days to ensure everyone can review the relevance of these parameters. Additionally, the governance has no incentives to implement incorrect parameters that could harm Morpho and its users.

## Spearbit
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Morpho |
| Report Date | N/A |
| Finders | hack3r-0m, Jay Jonah, Christoph Michel, Emanuele Ricci |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Spearbit-Security-Review.pdf

### Keywords for Search

`Validation, Gas Limit`

