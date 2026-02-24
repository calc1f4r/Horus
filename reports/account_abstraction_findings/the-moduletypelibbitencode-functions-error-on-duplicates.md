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
solodit_id: 43823
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

The ModuleTypeLib.bitEncode* functions error on duplicates

### Overview


This bug report discusses a problem with the bitEncode* functions in the ModuleTypeLib.sol file. When multiple ModuleTypes are encoded into a bitmask, the resulting bitmask is incorrect if the ModuleTypes are not all unique. This can lead to incorrect module types being returned in certain scenarios. The report includes a proof of concept and a recommendation to use bitwise OR instead of addition in the ModuleTypeLib functions. The bug has been fixed in PR 133 by Biconomy and Spearbit.

### Original Finding Content

## Severity: Medium Risk
## Context
ModuleTypeLib.sol#L28

## Description
When encoding several `ModuleType`s into a bitmask using the `bitEncode*` functions, the resulting bitmask will be incorrect when the module types are not all unique. For example, encoding the `MODULE_TYPE_VALIDATOR = 1` twice will result in an encoding of `MODULE_TYPE_EXECUTOR = 2`. This `EncodedModuleTypes` type can be used in modules, such as in the mock executor's `getModuleTypes()` which returns `(EncodedModuleTypes)`.

## Proof of Concept
```solidity
function test_bitEncode_error() public {
    ModuleType[] memory moduleTypes = new ModuleType[](2);
    moduleTypes[0] = ModuleType.wrap(MODULE_TYPE_VALIDATOR);
    moduleTypes[1] = ModuleType.wrap(MODULE_TYPE_VALIDATOR);
    EncodedModuleTypes enc = bitEncode(moduleTypes);
    // these assertions fail
    assertEq(isType(enc, ModuleType.wrap(MODULE_TYPE_VALIDATOR)), true, "should be a validator");
    assertEq(isType(enc, ModuleType.wrap(MODULE_TYPE_EXECUTOR)), false, "should not be an executor");
}
```

## Recommendation
Consider rewriting the `ModuleTypeLib` functions to use bitwise OR instead of addition. 
For example, for `bitEncode`, similar adjustments should be done for `isType` and `bitEncodeCalldata`.

```solidity
function bitEncode(ModuleType[] memory moduleTypes) internal pure returns (EncodedModuleTypes) {
    uint256 result;
    // Iterate through the moduleTypes array and set the corresponding bits in the result
    for (uint256 i; i < moduleTypes.length; i++) {
        result |= uint256(1) << ModuleType.unwrap(moduleTypes[i]);
    }
    return EncodedModuleTypes.wrap(result);
}
```

## Biconomy
Fixed in PR 133.

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

