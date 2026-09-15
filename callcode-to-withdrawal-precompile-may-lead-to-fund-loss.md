---
# Core Classification
protocol: Tezos Kernel Scope 1, 2 and 3
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43585
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Tezos-Spearbit-Security-Review-June-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Tezos-Spearbit-Security-Review-June-2024.pdf
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
  - Lukasz Glen
  - Wei Tang
  - Defsec
---

## Vulnerability Title

CALLCODE to withdrawal precompile may lead to fund loss

### Overview


Summary:

The withdrawal function in the code is not properly checking the source and target of a transfer, which could lead to a loss of funds. This is a critical issue and needs to be fixed. The recommended solutions are to either properly check the transfer object or disable certain call options. The issue has been fixed by MR 13997 and verified by Spearbit.

### Original Finding Content

## Critical Risk Report

## Severity
**Critical Risk**

## Context
`withdrawal.rs#L23`

## Description
The current withdrawal precompile implementation blindly accepts a Transfer without checking its source and target. When a `CALLCODE` instruction executes, it creates a Transfer object with the following values:

- **source**: the context address.
- **target**: same as source.

The transfer would then be compiled by sputnikvm. It may sound like a no-op, but it's an important implementation detail due to EVM's special account existence rules. 

The fund will not be transferred to the precompile, but the precompile routine is invoked, passed with the above Transfer object. The precompile then blindly creates a Withdrawal message, but the source money is not deducted at all. This is a critical severity issue due to its attack simplicity and the impact of fund loss on L2.

## Recommendation
To be discussed. Two options are available:

1. Properly check the Transfer object.
2. Disable all call variants except CALL.

Option (2) is preferred by the auditor.

## Etherlink
Fixed by MR 13997.

## Spearbit
Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Tezos Kernel Scope 1, 2 and 3 |
| Report Date | N/A |
| Finders | Lukasz Glen, Wei Tang, Defsec |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Tezos-Spearbit-Security-Review-June-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Tezos-Spearbit-Security-Review-June-2024.pdf

### Keywords for Search

`vulnerability`

