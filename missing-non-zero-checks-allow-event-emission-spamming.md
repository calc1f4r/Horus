---
# Core Classification
protocol: Axiom Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41048
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Axiom-contracts-Spearbit-Security-Review-October-2023.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Axiom-contracts-Spearbit-Security-Review-October-2023.pdf
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
finders_count: 5
finders:
  - Blockdev
  - Riley Holterhus
  - Desmond Ho
  - Lucas Goiriz
  - David Chaparro
---

## Vulnerability Title

Missing non-zero checks allow event emission spamming

### Overview

See description below for full details.

### Original Finding Content

## Security Issue Report

## Severity
**Low Risk**

## Context
- AxiomV2Query.sol#L387  
- AxiomV2Query.sol#L421  

## Description
Functions `withdraw()` and `deposit()` are meant to facilitate deposits and withdrawals. However, they do not check if non-zero ether is deposited or withdrawn. Given their permissionless nature, this allows anyone to grief the system with zero ether deposits, causing the emission of events which may hinder indexing/monitoring systems.

## Recommendation
Add non-zero checks for `deposit` and `withdraw` before event emission.

## Axiom
This issue has been addressed in PR 93.

## Spearbit
**Fixed.**

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Axiom Contracts |
| Report Date | N/A |
| Finders | Blockdev, Riley Holterhus, Desmond Ho, Lucas Goiriz, David Chaparro |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Axiom-contracts-Spearbit-Security-Review-October-2023.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Axiom-contracts-Spearbit-Security-Review-October-2023.pdf

### Keywords for Search

`vulnerability`

