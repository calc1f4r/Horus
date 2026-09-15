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
solodit_id: 43824
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Biconomy-Spearbit-Security-Review-October-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Biconomy-Spearbit-Security-Review-October-2024.pdf
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
finders_count: 7
finders:
  - Blockdev
  - Devtooligan
  - Chinmay Farkya
  - Christoph Michel
  - Víctor Martínez
---

## Vulnerability Title

RegistryFactory.addAttester allows duplicate and unsorted attesters breaking ERC-7484 compli-

### Overview


The report discusses a bug in the RegistryFactory smart contract, specifically in the addAttester function. This bug allows for duplicate attesters to be added to the internal list, causing issues such as duplicates not being removed and smart account deployments failing. The recommendation is to check for unique and sorted attesters, potentially by replacing the addAttesters and removeAttesters functions with a setAttesters function. The bug has been fixed in PR 134 for Biconomy and Spearbit has also fixed it by adding a sort to the updated array.

### Original Finding Content

## Audit Report

## Severity: Medium Risk

### Context
`RegistryFactory.sol#L58`

### Description
The `RegistryFactory.addAttester` function allows adding duplicates, and the new attester is pushed as the last element to the internal list. This leads to several issues:

1. Duplicate attesters are not removed by a single `removeAttester` call.
2. Upon deployment of a smart account, when `REGISTRY.check(module, moduleType, attesters, threshold)` is called, duplicates or unsorted elements in attesters will revert according to EIP-7484 registry. The attesters provided MUST be unique and sorted, and the Registry MUST revert if they are not. Factory deployments can fail if the attesters are misconfigured. This misconfiguration will only be found out later when an actual deployment is performed.

### Recommendation
Consider checking that the attesters array is unique and sorted. For example, replace `addAttesters` and `removeAttesters` with a `setAttesters(address[] calldata attesters)` function that iterates over the new attesters to ensure these properties.

### Biconomy
Fixed in PR 134.

### Spearbit
Fixed. The `addAttesters` and `removeAttesters` functions were kept and now perform a sort on the updated array.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

