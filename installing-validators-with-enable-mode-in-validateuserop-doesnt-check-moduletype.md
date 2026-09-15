---
# Core Classification
protocol: Biconomy: Nexus
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36587
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/cly8oizwp00014brg47oo8pt1
source_link: none
github_link: https://github.com/Cyfrin/2024-07-biconomy

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
finders_count: 2
finders:
  - adriro
  - MiloTruck
---

## Vulnerability Title

Installing validators with enable mode in `validateUserOp()` doesn't check `moduleType`

### Overview


This bug report discusses an issue with the `_checkEnableModeSignature()` function in the Nexus contract. The function does not check whether the `moduleType` is allowed by the owner's signature when installing validators using the `validateUserOp()` function. This means that a malicious user can install a validator with any module type, even if the owner did not give permission. This can have serious consequences, especially if the validator is a multi-type module or an executor module. The report recommends either calling `_installModule()` with `MODULE_TYPE_VALIDATOR` instead of having it as a parameter, or including `moduleType` in the hash returned by `_getEnableModeDataHash()` to ensure that the owner's signature permits the module type. 

### Original Finding Content

## Summary

`_checkEnableModeSignature()` doesn't check that `moduleType` is permitted by the owner's signature.

## Vulnerability Details

When Nexus account owners send a transaction with enable mode in `PackedUserOperation.nonce`, [`validateUserOp()`](https://github.com/Cyfrin/2024-07-biconomy/blob/main/contracts/Nexus.sol#L97-L112) calls `_enableMode()` to install the validator as a new module.

[Nexus.sol#L108-L109](https://github.com/Cyfrin/2024-07-biconomy/blob/main/contracts/Nexus.sol#L108-L109)

```solidity
PackedUserOperation memory userOp = op;
userOp.signature = _enableMode(validator, op.signature);
```

The `moduleType` and `moduleInitData` of the validator to be installed is decoded from `PackedUserOperation.signature`:

[ModuleManager.sol#L166-L171](https://github.com/Cyfrin/2024-07-biconomy/blob/main/contracts/base/ModuleManager.sol#L166-L171)

```solidity
(moduleType, moduleInitData, enableModeSignature, userOpSignature) = packedData.parseEnableModeData();  

_checkEnableModeSignature(
    _getEnableModeDataHash(module, moduleInitData),
    enableModeSignature
);
_installModule(moduleType, module, moduleInitData);
```

As seen from above, to ensure that the account owner has allowed the validator to be installed with `moduleInitData`,  `module` and `moduleInitData` are hashed, and the hash is checked to be signed by the owner with `enableModeSignature`.

However, `moduleType` is not included in the hash, as seen in `_getEnableModeDataHash()`:

[ModuleManager.sol#L388-L398](https://github.com/Cyfrin/2024-07-biconomy/blob/main/contracts/base/ModuleManager.sol#L388-L398)

```solidity
function _getEnableModeDataHash(address module, bytes calldata initData) internal view returns (bytes32 digest) {
    digest = _hashTypedData(
        keccak256(
            abi.encode(
                MODULE_ENABLE_MODE_TYPE_HASH,
                module,
                keccak256(initData)
            )
        )
    );
}
```

This allows a malicious relayer/bundler to call `validateUserOp()` and specify `moduleType` as any module type. For example, instead of `MODULE_TYPE_VALIDATOR`, the attacker can specify it as `MODULE_TYPE_EXECUTOR`.

If the validator happens to be a multi-type module, this is problematic an attacker can install the validator with any module type, without the owner's permission.

## Impact

An attacker can install validators through enable mode and `validateUserOp()` with any module type, without permission from the owner.

Depending on the module being installed, this can have drastic consequences on the account, with the highest impact being executor modules as they can `delegatecall`.

## Recommendations

If `_enableMode()` is only meant to install validators, consider calling `_installModule()` with `MODULE_TYPE_VALIDATOR` instead of having it as a parameter.

Otherwise, include `moduleType` in the hash returned by `_getEnableModeDataHash()`. This ensures that the module type is permitted by the account owner's signature.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Biconomy: Nexus |
| Report Date | N/A |
| Finders | adriro, MiloTruck |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2024-07-biconomy
- **Contest**: https://codehawks.cyfrin.io/c/cly8oizwp00014brg47oo8pt1

### Keywords for Search

`vulnerability`

