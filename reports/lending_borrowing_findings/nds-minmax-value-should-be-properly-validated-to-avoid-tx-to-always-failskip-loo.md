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
solodit_id: 6936
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

NDS min/max value should be properly validated to avoid tx to always fail/skip loop

### Overview


This bug report concerns the PositionsManagerForAaveGettersSetters.sol#L40-L43, which is currently initialized with a default value of NDS = 20. This value is used by the MatchingEngineForAave when it needs to call DoubleLinkedList.insertSorted in both updateBorrowers and updateSuppliers. 

The problems with this default value are two-fold: a low NDS value would make the loop inside insertSorted exit early, increasing the probability of a supplier/borrower to be added to the tail of the list, and a very high value would make the transaction revert each time one of the functions directly or indirectly call insertSorted. 

The recommendation is to make enough tests to determine a safe min/max value for NDS that protect from DOS but still make the protocol perform as expected. Morpho has implemented the fix, and Spearbit has acknowledged it.

### Original Finding Content

## Security Report

## Severity
**Medium Risk**

## Context
`PositionsManagerForAaveGettersSetters.sol#L40-L43`

## Description
`PositionsManagerForAaveLogic` is currently initialized with a default value of `NDS = 20`. The `NDS` value is used by `MatchingEngineForAave` when it needs to call `DoubleLinkedList.insertSorted` in both `updateBorrowers` and `updateSuppliers`. 

`updateBorrowers` and `updateSuppliers` are called by:
- `MatchingEngineForAave.matchBorrowers`
- `MatchingEngineForAave.unmatchBorrowers`
- `MatchingEngineForAave.matchSuppliers`
- `MatchingEngineForAave.unmatchSuppliers`

These functions, along with the directly invoked `updateBorrowers` and `updateSuppliers`, are also called by `PositionsManagerForAaveLogic`.

## Problems
- A low `NDS` value would make the loop inside `insertSorted` exit early, increasing the probability of a supplier/borrower being added to the tail of the list. This is something that Morpho aims to avoid as it would decrease protocol performance during supplier/borrower match/unmatch operations.
- In cases where a list is long enough, a very high value could cause the transaction to revert every time one of those functions directly or indirectly calls `insertSorted`. The gas "rail guard" present in the match/unmatch supplier/borrower processes becomes ineffective because the loop would be executed at least once.

## Recommendation
Conduct sufficient tests to determine a safe minimum and maximum value for `NDS` that protects against denial-of-service (DOS) while still ensuring the protocol performs as expected.

## Morpho
Fix has been implemented.

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

`Validation`

