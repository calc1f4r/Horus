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
solodit_id: 43813
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

Incorrect check in _enableMode prevents installing module types other than validator

### Overview


The report states that there is a bug in the code that prevents certain module types from being installed in Enable Mode. This check was not intended and needs to be removed. The bug has been fixed in PR 177 by Biconomy and Spearbit.

### Original Finding Content

## Severity: Medium Risk

## Context
(No context files were provided by the reviewer)

## Description
It was decided based on a previous review that the intention is to allow any module types to be installed in Enable Mode.

Current code has a check that prevents any module type other than a validator (or a multi type) from being installed on a nexus account via the enable mode.

```solidity
function _enableMode(bytes32 userOpHash, bytes calldata packedData) internal returns (bytes calldata userOpSignature) {
    address module;
    uint256 moduleType;
    bytes calldata moduleInitData;
    bytes calldata enableModeSignature;
    (module, moduleType, moduleInitData, enableModeSignature, userOpSignature) = packedData.parseEnableModeData();
    
    if (!_checkEnableModeSignature(_getEnableModeDataHash(module, moduleType, userOpHash, moduleInitData), enableModeSignature)) {
        revert EnableModeSigError();
    }

    // Ensure the module type is VALIDATOR or MULTI
    if (moduleType != MODULE_TYPE_VALIDATOR && moduleType != MODULE_TYPE_MULTI) revert InvalidModuleTypeId(moduleType); // <<<
    
    _installModule(moduleType, module, moduleInitData);
}
```

## Recommendation
Remove this check: 
```solidity
if (moduleType != MODULE_TYPE_VALIDATOR && moduleType != MODULE_TYPE_MULTI) revert InvalidModuleTypeId(moduleType);
```

## Biconomy
Fixed in PR 177.

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

