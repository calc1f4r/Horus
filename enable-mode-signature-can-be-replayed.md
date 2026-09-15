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
solodit_id: 43810
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

Enable Mode Signature can be replayed

### Overview


This bug report discusses a high-risk issue in a specific section of code (ModuleManager.sol) related to enabling modules. The report explains that there are two validators used during enable mode, but they are independent and may have different trust assumptions and privileges. The problem is that there is no replay protection for the inner enableModeSignature, which means that the same module, moduleInitData, and enableModeSignature can be used in a different user operation to install the module a second time. This could also be replayed on another chain or smart account with the same owner. The recommendation is to implement replay protection for the enable mode signature, which can be done by signing over the userOpHash for the enable mode signature off-chain. This issue has been fixed by Biconomy and Spearbit.

### Original Finding Content

## High Risk Vulnerability Report

## Severity
**High Risk**

## Context
**ModuleManager.sol#L168-L171**

## Description
During enable mode, two validators are used:

1. **validator**: The module to be installed as any module type that can be defined. It must be a validator either already before the user operation or after enabling it as a validator in enable mode. This validator will be used to validate the final user operation.

2. **enableModeSigValidator**: This validator is used in `_checkEnableModeSignature` to check the `_getEnableModeDataHash(validator, initData)` for enabling the first validator.

Note that these two validators are independent of each other and might have different trust assumptions and privileges.

While a user operation has a nonce field (that is used in the userOpHash and its signature) and the entry point checks and increments this nonce to avoid replaying a user operation, the inner enableModeSignature does not have any such replay protection.

The same module, `moduleInitData`, and `enableModeSignature` can be used in a different user operation to install the module a second time, for example, after the user uninstalled the module already.

As the entire enable mode data is encoded in the `userOp.signature` that is not part of `userOpHash`, a bundler can replace the enable mode data with a different previously signed one without invalidating the user operation (as long as the enable mode bit and the validator encoded in the `userOp.nonce` match).

`op.signature = (moduleType, moduleInitData, enableModeValidator, enableModeSignature, userOpSignature)`

This signature can also be replayed across another chain, as well as on another smart account on the same chain with the same owner.

## Recommendation
The enable mode signature validator should implement its own replay protection. A gas-efficient way is to tie the enable mode signature to a specific user operation (as one enable mode should map to one user operation). This can be done by also signing over the `userOpHash` for the enable mode signature off-chain. 

On-chain, when `validateUserOp(op, userOpHash, missingAccountFunds)` is called, the passed `userOpHash` is used to reconstruct the message digest:

```solidity
function _getEnableModeDataHash(address module, uint256 moduleType, bytes32 userOpHash, bytes calldata initData) internal view returns (bytes32 digest) {
    // userOpHash is from validateUserOp
    digest = _hashTypedData(
        keccak256(
            abi.encode(
                // IMPORTANT! NEED TO CHANGE MODULE_ENABLE_MODE_TYPE_HASH TO INCLUDE THE NEW FIELDS
                MODULE_ENABLE_MODE_TYPE_HASH,
                module,
                moduleType,
                userOpHash,
                keccak256(initData)
            )
        )
    );
}
```

As there is replay protection for a `userOpHash` when coming from the entry point, there's also replay protection for the enable mode signature when verifying it in `validateUserOp` from the entry point.

## Fixes
- **Biconomy**: Fixed in PR 112 and documented in the wiki.
- **Spearbit**: Fixed.

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

