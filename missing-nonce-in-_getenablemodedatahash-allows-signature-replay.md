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
solodit_id: 36589
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
finders_count: 1
finders:
  - MiloTruck
---

## Vulnerability Title

Missing nonce in `_getEnableModeDataHash()` allows signature replay

### Overview


This bug report discusses an issue in the `_getEnableModeDataHash()` function of the Nexus smart contract. The function does not include a nonce, which allows for enable mode signatures to be replayed. This means that a malicious user can use a previously used signature to reinstall a validator without the owner's permission. This could potentially give the attacker access to execute transactions on behalf of the Nexus account. To fix this issue, it is recommended to include a nonce in the `_getEnableModeDataHash()` function.

### Original Finding Content

## Summary

`_getEnableModeDataHash()` doesn't include a nonce, thereby allowing enable mode signatures to be replayed.

## Vulnerability Details

When Nexus account owners send a transaction with enable mode in `PackedUserOperation.nonce`, [`validateUserOp()`](https://github.com/Cyfrin/2024-07-biconomy/blob/main/contracts/Nexus.sol#L97-L112) calls `_enableMode()` to install the validator as a new module.

[Nexus.sol#L108-L109](https://github.com/Cyfrin/2024-07-biconomy/blob/main/contracts/Nexus.sol#L108-L109)

```solidity
PackedUserOperation memory userOp = op;
userOp.signature = _enableMode(validator, op.signature);
```

To ensure that the account owner has allowed the validator to be installed, the validator (ie. `module` shown below) is hashed alongside its data (ie. `moduleInitData`) in `_getEnableModeDataHash()`, and subsequently checked to be signed by the owner in `enableModeSignature` in `_checkEnableModeSignature()`:

[ModuleManager.sol#L166-L171](https://github.com/Cyfrin/2024-07-biconomy/blob/main/contracts/base/ModuleManager.sol#L166-L171)

```solidity
(moduleType, moduleInitData, enableModeSignature, userOpSignature) = packedData.parseEnableModeData();  

_checkEnableModeSignature(
    _getEnableModeDataHash(module, moduleInitData),
    enableModeSignature
);
_installModule(moduleType, module, moduleInitData);
```

However, the hash returned by `_getEnableModeDataHash()` does not include a nonce:

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

This allows the owner's signature to be used repeatedly.

As a result, if a validator that was previously installed through `_enableMode()` is uninstalled by the owner, a malicious relayer/bundler can re-use the previous signature to re-install it through `validatorUserOp()` again, despite not having the owner's permission.

## Impact

Due to signature replay, validators that have been uninstalled by Nexus account owners can be re-installed without their permission. 

This is especially problematic as validators are used by Nexus accounts for access control - being able to re-install a validator without the owner's permission might affect the Nexus account's permissions and allow attackers to execute transactions on behalf of the account.

## Recommendations

Include a nonce in `_getEnableModeDataHash()` to ensure that enable mode signatures cannot be replayed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Biconomy: Nexus |
| Report Date | N/A |
| Finders | MiloTruck |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2024-07-biconomy
- **Contest**: https://codehawks.cyfrin.io/c/cly8oizwp00014brg47oo8pt1

### Keywords for Search

`vulnerability`

