---
# Core Classification
protocol: Biconomy Nexus
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43811
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Biconomy-Spearbit-Security-Review-October-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Biconomy-Spearbit-Security-Review-October-2024.pdf
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
finders_count: 7
finders:
  - Blockdev
  - Devtooligan
  - Chinmay Farkya
  - Christoph Michel
  - Víctor Martínez
---

## Vulnerability Title

Enable Mode Signature ignores module type

### Overview


This bug report discusses an issue in the ModuleManager.sol code where two validators are used during enable mode. The first validator is used to validate the final userOp, while the second validator is used to check the enable mode signature. However, these two validators are independent and may have different trust assumptions and privileges. This means that the owner of the enableModeSigValidator may only want to produce a signature for a specific module type, but the signature only covers the module and initData fields, not the module type. This allows the user op submitter to forge the module type without invalidating the enable mode signature, and install the module as any type they want. The report recommends signing the module type as part of the enable mode data hash to prevent this issue. The bug has been fixed by Biconomy and Spearbit.

### Original Finding Content

## High Risk Advisory

## Severity
**High Risk**

## Context
`ModuleManager.sol#L168-L171`

## Description
During enable mode, two validators are used:

1. **validator**: This is the module to be installed as any module type that can be defined. It must be a validator either already before the user operation or after enabling it as a validator in enable mode. This validator will be used to validate the final user operation.

2. **enableModeSigValidator**: This validator is used in `_checkEnableModeSignature` to check the `_getEnableModeDataHash(validator, initData)` for enabling the first validator.

Note that these two validators are independent of each other and may have different trust assumptions and privileges. The `enableModeSigValidator` owner might only want to produce a signature for a specific module type. However, the signature is only over the module (`validator`) and `initData` fields, not over the `moduleType` that the module will be installed as. The user operation submitter can forge the module type without invalidating the enable mode signature, as the entire enable mode data is encoded in the `userOp.signature`, which is not part of `userOpHash`.

They can then create a user operation with the forged enable mode module type to install the module as any type they want. A multi-type validator can be installed as all of its types.

## Recommendation
Consider signing the module type as part of the `_getEnableModeDataHash`.

## Biconomy
- Fixed PR 112.

## Spearbit
- Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Biconomy Nexus |
| Report Date | N/A |
| Finders | Blockdev, Devtooligan, Chinmay Farkya, Christoph Michel, Víctor Martínez, Noah Marconi |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Biconomy-Spearbit-Security-Review-October-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Biconomy-Spearbit-Security-Review-October-2024.pdf

### Keywords for Search

`vulnerability`

