---
# Core Classification
protocol: Karak
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41077
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-07-karak
source_link: https://code4rena.com/reports/2024-07-karak
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[04] `maxDeposit`, `maxMint`, `maxRedeem`, and `maxWithdraw` functions do not return 0 when they should

### Overview

See description below for full details.

### Original Finding Content


### Description
The following `pauseVault` function of the `Core` contract can be called to pause the `Vault` contract's `deposit`, `mint`, `startRedeem`, and `finishRedeem` functions. Also, the `Vault` contract's `withdraw` and `redeem` functions below always revert. Since the `Vault` contract inherits `solady`'s `ERC4626` contract, calling the `Vault` contract's `maxDeposit`, `maxMint`, `maxRedeem`, and `maxWithdraw` functions would not return 0 even when the respective `deposit`, `mint`, `startRedeem`, and `finishRedeem` functions are paused and `withdraw` and `redeem` functions always revert.

As specified in https://eips.ethereum.org/EIPS/eip-4626:
- `maxDeposit` `MUST factor in both global and user-specific limits, like if deposits are entirely disabled (even temporarily) it MUST return 0`;
- `maxMint` `MUST factor in both global and user-specific limits, like if mints are entirely disabled (even temporarily) it MUST return 0`;
- `maxRedeem` `MUST factor in both global and user-specific limits, like if redemption is entirely disabled (even temporarily) it MUST return 0`;
- `maxWithdraw` `MUST factor in both global and user-specific limits, like if withdrawals are entirely disabled (even temporarily) it MUST return 0`.

Hence, these `maxDeposit`, `maxMint`, `maxRedeem`, and `maxWithdraw` functions should return 0 when the respective `deposit`, `mint`, `startRedeem`, and `finishRedeem` functions are paused and `withdraw` and `redeem` functions always revert but that is not the case currently. As a result, these `maxDeposit`, `maxMint`, `maxRedeem`, and `maxWithdraw` functions are not compliant with the EIP-4626 standard.

https://github.com/code-423n4/2024-07-karak/blob/53eb78ebda718d752023db4faff4ab1567327db4/src/Core.sol#L197-L199
```solidity
    function pauseVault(IKarakBaseVault vault, uint256 map) external onlyRolesOrOwner(Constants.MANAGER_ROLE) {
        vault.pause(map);
    }
```

https://github.com/code-423n4/2024-07-karak/blob/53eb78ebda718d752023db4faff4ab1567327db4/src/Vault.sol#L331-L362
```solidity
    function withdraw(uint256 assets, address to, address owner)
        public
        override
        whenFunctionNotPaused(Constants.PAUSE_VAULT_WITHDRAW)
        nonReentrant
        returns (uint256 shares)
    {
        // To suppress warnings
        owner = owner;
        assets = assets;
        to = to;
        shares = shares;

        revert NotImplemented();
    }
    ...
    function redeem(uint256 shares, address to, address owner)
        public
        override
        whenFunctionNotPaused(Constants.PAUSE_VAULT_REDEEM)
        nonReentrant
        returns (uint256 assets)
    {
        // To suppress warnings
        owner = owner;
        to = to;
        shares = shares;
        assets = assets;

        revert NotImplemented();
    }
```

https://github.com/code-423n4/2024-07-karak/blob/53eb78ebda718d752023db4faff4ab1567327db4/src/Vault.sol#L5-L29
```solidity
import {ERC4626, ERC20} from "solady/src/tokens/ERC4626.sol";
...
contract Vault is ERC4626, Initializable, Ownable, Pauser, ReentrancyGuard, ExtSloads, IVault {
```

https://github.com/vectorized/solady/blob/main/src/tokens/ERC4626.sol#L326-L359
```solidity
    function maxDeposit(address to) public view virtual returns (uint256 maxAssets) {
        to = to; // Silence unused variable warning.
        maxAssets = type(uint256).max;
    }

    ...
    function maxMint(address to) public view virtual returns (uint256 maxShares) {
        to = to; // Silence unused variable warning.
        maxShares = type(uint256).max;
    }

    ...
    function maxWithdraw(address owner) public view virtual returns (uint256 maxAssets) {
        maxAssets = convertToAssets(balanceOf(owner));
    }

    ...
    function maxRedeem(address owner) public view virtual returns (uint256 maxShares) {
        maxShares = balanceOf(owner);
    }
```

### Recommended Mitigation
The `Vault` contract can be updated to add the `maxDeposit`, `maxMint`, `maxRedeem`, and `maxWithdraw` functions to override the corresponding functions in `solady`'s `ERC4626` contract in which these `maxDeposit`, `maxMint`, `maxRedeem`, and `maxWithdraw` functions would return 0 when the respective `deposit`, `mint`, `startRedeem`, and `finishRedeem` functions are paused and `withdraw` and `redeem` functions always revert.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Karak |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2024-07-karak
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2024-07-karak

### Keywords for Search

`vulnerability`

