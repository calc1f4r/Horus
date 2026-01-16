---
# Core Classification
protocol: Liquid Collective
chain: everychain
category: logic
vulnerability_type: validation

# Attack Vector Details
attack_type: validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7025
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/LiquidCollective-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/LiquidCollective-Spearbit-Security-Review.pdf
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
  - admin

protocol_categories:
  - staking_pool
  - liquid_staking
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - Optimum
  - Matt Eccentricexit
  - Danyal Ellahi
  - Saw-mon and Natalie
  - Emanuele Ricci
---

## Vulnerability Title

LibOwnable._setAdmin allows setting address(0) as the admin of the contract

### Overview


This bug report details an issue with the LibOwnable library, where contracts that call LibOwnable._setAdmin with address(0) will not revert and functions that should be callable by an admin cannot be called anymore. This affects four contracts that import and use the LibOwnable library: AllowlistV1, OperatorsRegistryV1, OracleV1, and RiverV1. The recommendation is to add a check inside LibOwnable._setAdmin to prevent setting address(0) as the admin, or move that specific check in each contract that import and use LibOwnable. The recommendation has been implemented in SPEARBIT/11, but there are still some issues that need to be addressed, such as missing natspec comments and events for _setAdmin. These issues have been addressed in SPEARBIT/33.

### Original Finding Content

## Severity: Medium Risk

## Context
LibOwnable.sol#L8-L10

## Description
While other contracts like RiverAddress (for example) do not allow `address(0)` to be used as a set input parameter, there is no similar check inside `LibOwnable._setAdmin`. Because of this, contracts that call `LibOwnable._setAdmin` with `address(0)` will not revert, and functions that should be callable by an admin cannot be called anymore.

### This is the list of contracts that import and use the LibOwnable library:
- AllowlistV1
- OperatorsRegistryV1
- OracleV1
- RiverV1

## Recommendation
Consider adding a check inside `LibOwnable._setAdmin` to prevent setting `address(0)` as the admin, or move that specific check into each contract that imports and uses `LibOwnable`.

### Alluvial
Recommendation implemented in SPEARBIT/11.

### Spearbit
**Note 1:** Still missing (client said it will be implemented in other PRs)
- Administrable misses all Natspec comments
- Event for `_setAdmin` is still missing but will be added to Initializable event in another PR

**Note 2:** Client has acknowledged that all the contracts that inherit from Administrable have the ability to transfer ownership, even contracts like AllowlistV1 that didn't have the ability before this PR.

### Alluvial 
Issues in Note 1 addressed in SPEARBIT/33.

### Spearbit 
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Liquid Collective |
| Report Date | N/A |
| Finders | Optimum, Matt Eccentricexit, Danyal Ellahi, Saw-mon and Natalie, Emanuele Ricci |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/LiquidCollective-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/LiquidCollective-Spearbit-Security-Review.pdf

### Keywords for Search

`Validation, Admin`

