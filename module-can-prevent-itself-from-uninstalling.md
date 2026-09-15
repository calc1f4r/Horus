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
solodit_id: 43816
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

Module can prevent itself from uninstalling

### Overview


A bug has been reported in the Nexus smart contract, which is a program that manages other programs called modules. The bug is in the code that handles uninstalling modules. When a module is being uninstalled, the code calls a function in the module called "onUninstall". If this function fails, the code also fails and the module cannot be uninstalled. This could be a problem if a malicious module is discovered, as it would prevent it from being removed and could potentially cause harm to users. The recommendation is to ignore any errors in the "onUninstall" function and continue with the uninstallation process. This bug has been fixed in the code by two companies named Biconomy and Spearbit.

### Original Finding Content

## Security Analysis Report

## Severity
**Medium Risk**

## Context
- `ModuleManager.sol#L226`
- `ModuleManager.sol#L244`
- `ModuleManager.sol#L263`
- `ModuleManager.sol#L312`
- `Nexus.sol#L208-L214`

## Description
When `Nexus.uninstallModule(..., module, ...)` is called to uninstall a module, `module.unUninstall(...)` is called eventually. Nexus can be stopped from uninstalling if `module.onUninstall()` reverts, as it also reverts the call to Nexus. This poses a risk if a module is malicious (or later discovered to be malicious), since they have the privilege of validating or executing a User Operation.

## Recommendation
Ignore reverts when `.onUninstall()` is called on a module, and continue the execution of code in the Nexus contract.

## Biconomy
Fixed in PR 117 and PR 143.

## Spearbit
Fixed.

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

