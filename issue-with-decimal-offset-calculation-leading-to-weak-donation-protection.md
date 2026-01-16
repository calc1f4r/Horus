---
# Core Classification
protocol: Part 2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49968
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/cm60h7a380000k66h6knt2vtl
source_link: none
github_link: https://github.com/Cyfrin/2025-01-zaros-part-2

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
finders_count: 2
finders:
  - alexczm
  - oxelmiguel
---

## Vulnerability Title

Issue with Decimal Offset Calculation Leading to Weak Donation Protection

### Overview


This bug report discusses an issue with the calculation of a variable called `decimalOffset` which is used in a formula to protect against donation attacks on a protocol. The report identifies three main problems with the current implementation: unpredictability, dependency on another variable, and weak protection in some cases. These issues can potentially allow attackers to exploit the protocol and create a denial-of-service scenario for users with small balances. To fix this, the report suggests implementing a fixed value for `decimalOffset` instead of calculating it dynamically. This will provide consistent and effective protection against donation attacks. 

### Original Finding Content

## Summary

In the current implementation, the calculation of `decimalOffset` is dynamic and based on the difference between `SYSTEM_DECIMALS` (18) and the decimals of the `indexToken`:

[Source Code Reference](https://github.com/Cyfrin/2025-01-zaros-part-2/blob/35deb3e92b2a32cd304bf61d27e6071ef36e446d/src/market-making/branches/VaultRouterBranch.sol#L173)

```solidity
uint8 decimalOffset = Constants.SYSTEM_DECIMALS - IERC20Metadata(vault.indexToken).decimals();
```

This offset is used in the formula:

```solidity
IERC4626(vault.indexToken).totalSupply() + 10 ** decimalOffset
```

The purpose of adding `10 ** decimalOffset` is to introduce a **virtual share adjustment** to mitigate donation attacks.

[OpenZeppelin ERC-4626 Documentation](https://docs.openzeppelin.com/contracts/4.x/erc4626)

## Issues with Dynamic Decimal Offset

## 1. **Unpredictability**
   - The value of `decimalOffset` depends on `indexToken.decimals()`, leading to inconsistent behavior across different tokens.
   - If `indexToken.decimals()` is 18, `decimalOffset` is `0`, effectively bypassing the intended protection.
   - If `indexToken.decimals()` is 6, `decimalOffset` is `12`, which may be overly restrictive.

### 2. **Dependency on `IERC20Metadata(vault.indexToken).decimals()`**
   - The `decimals()` function returns the sum of the asset token’s decimals and `decimalsOffset`:



   ```solidity
   function decimals() public view virtual override(IERC20Metadata, ERC20Upgradeable) returns (uint8) {
       ERC4626Storage storage $ = _getERC4626Storage();
       return $._underlyingDecimals + _decimalsOffset();
   }
   ```
 - `decimalsOffset` is set by the deployer of the ZLP vault.

   https://github.com/Cyfrin/2025-01-zaros-part-2/blob/35deb3e92b2a32cd304bf61d27e6071ef36e446d/src/zlp/ZlpVault.sol#L74

   ```solidity
   zlpVaultStorage.decimalsOffset = decimalsOffset;
   ```

  
   - If an 18-decimal asset is used, `decimalsOffset` must be set to zero to ensure that `indexToken.decimals()` remains 18.

   - This means that the offset used to mitigate donation attacks will also be zero, nullifying its intended protection.

### 3. **Weak Protection in Some Cases**
   - A `decimalOffset` of `0` results in an added value of `1`, offering no real defense.
   - A `decimalOffset` of `1` or `2` introduces a minor buffer but still allows donation attacks.
   - The inconsistency makes the protocol vulnerable in some cases and overly strict in others.


## Impact

The protocol includes a check that reverts deposits if they result in zero shares, preventing donation attacks. However, this allows attackers to create a denial-of-service (DoS) scenario for users with small balances by increasing the minimum asset deposit required to receive at least one share. This issue arises because, for tokens with 18 decimals, no effective offset is applied, making donations inexpensive.

## Proof of concept


In the `createZlpVaults` function used for testing, the `decimalsOffset` is determined by `Constants.SYSTEM_DECIMALS - vaultsConfig[i].decimals`:  


https://github.com/Cyfrin/2025-01-zaros-part-2/blob/35deb3e92b2a32cd304bf61d27e6071ef36e446d/script/vaults/Vaults.sol#L109

```solidity
function createZlpVaults(address marketMakingEngine, address owner, uint256[2] memory vaultsIdsRange) public {
        // ****
        
            // deploy zlp vault as an upgradeable proxy
            address zlpVaultImpl = address(new ZlpVault());
            bytes memory zlpVaultInitData = abi.encodeWithSelector(
                ZlpVault.initialize.selector,
                marketMakingEngine,
                Constants.SYSTEM_DECIMALS - vaultsConfig[i].decimals,
                owner,
                IERC20(vaultAsset),
                vaultsConfig[i].vaultId
            );
        // ****
    }
```

For an asset with 18 decimals:  

- The `decimalsOffset` in the vault is calculated as `Constants.SYSTEM_DECIMALS - 18 = 0`.  
- The `indexToken` decimals become `18 + 0 = 18`.  
- The `decimalOffset` used for donation protection is `18 - 18 = 0`.  

This means that for assets with 18 decimals, no effective offset is applied, making donation attacks inexpensive and reducing the protocol’s protection against such exploits.


## Proposed Solution: Fixed Decimal Offset

To ensure **consistent** and **effective** mitigation of donation attacks, we propose replacing the dynamic `decimalOffset` with a fixed value.

### Implementation of Fixed Offset
Instead of computing `decimalOffset` dynamically, define it as a constant:

```solidity
uint8 constant FIXED_DECIMAL_OFFSET = 6; // Chosen based on attack resistance and usability trade-offs
```

**Note:** An offset of `3` forces an attacker to make a donation 1,000 times as large.

Then modify the calculation as follows:

```solidity
uint256 previewAssetsOut = sharesIn.mulDiv(
    totalAssetsMinusVaultDebt,
    IERC4626(vault.indexToken).totalSupply() + 10 ** FIXED_DECIMAL_OFFSET,
    MathOpenZeppelin.Rounding.Floor
);
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Part 2 |
| Report Date | N/A |
| Finders | alexczm, oxelmiguel |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2025-01-zaros-part-2
- **Contest**: https://codehawks.cyfrin.io/c/cm60h7a380000k66h6knt2vtl

### Keywords for Search

`vulnerability`

