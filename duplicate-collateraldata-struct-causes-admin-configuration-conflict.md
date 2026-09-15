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
solodit_id: 49969
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
finders_count: 1
finders:
  - alexczm
---

## Vulnerability Title

Duplicate `Collateral.Data` struct causes admin configuration conflict

### Overview


The bug report is about a duplicate `Collateral.Data` struct causing a conflict in admin configurations. This results in a denial of service for admin rights. The issue is caused by the protocol accessing the same information from two different locations, but the admin is only able to update one of them. This means that important information cannot be updated, resulting in the need to relaunch the vault and causing inconvenience. The report suggests either removing the duplicate `Collateral.Data` or adding a new function for the admin to update the necessary parameters.

### Original Finding Content

## Summary

`Collateral.Data` information is saved in two locations. Protocol access this information from both places but admin can update only one of them resulting in a DoS for admin rights.

## Vulnerability Details

Collateral data is handled by [Collateral](https://github.com/Cyfrin/2025-01-zaros-part-2/blob/35deb3e92b2a32cd304bf61d27e6071ef36e446d/src/market-making/leaves/Collateral.sol#L14) library and saved at `COLLATERAL_LOCATION` storage location. It is configured by [MarketMakingEngineConfigurationBranch ::configureCollateral](https://github.com/Cyfrin/2025-01-zaros-part-2/blob/35deb3e92b2a32cd304bf61d27e6071ef36e446d/src/market-making/branches/MarketMakingEngineConfigurationBranch.sol#L505-L513) function and can be called multiple times by `admin`.

Same data structure is stored is [Vault](https://github.com/Cyfrin/2025-01-zaros-part-2/blob/35deb3e92b2a32cd304bf61d27e6071ef36e446d/src/market-making/leaves/Vault.sol#L107) leaf and is part of the bigger vault's data struct stored at `VAULT_LOCATION` storage location.
It is initialized when the vault is [created](https://github.com/Cyfrin/2025-01-zaros-part-2/blob/35deb3e92b2a32cd304bf61d27e6071ef36e446d/src/market-making/leaves/Vault.sol#L464-L480). If the vault exist this function [can't be called again](https://github.com/Cyfrin/2025-01-zaros-part-2/blob/35deb3e92b2a32cd304bf61d27e6071ef36e446d/src/market-making/leaves/Vault.sol#L467-L469). The vault's `self.collateral` data can't be updated.

```solidity
    function create(CreateParams memory params) internal {
        Data storage self = load(params.vaultId);


        if (self.id != 0) {
            revert Errors.VaultAlreadyExists(params.vaultId);
        }
        self.id = params.vaultId;
        self.depositCap = params.depositCap;
        self.withdrawalDelay = params.withdrawalDelay;
        self.indexToken = params.indexToken;
@>        self.collateral = params.collateral; // @audit set collateral data
        self.depositFee = params.depositFee;
        self.redeemFee = params.redeemFee;
        self.engine = params.engine;
        self.isLive = true;
    }
```

Two critical information are accessed from `colllateral.Data` stored in `vault`:

* `isEnable` status in [VaultRouterBranch::initiateWithdrawal](https://github.com/Cyfrin/2025-01-zaros-part-2/blob/35deb3e92b2a32cd304bf61d27e6071ef36e446d/src/market-making/branches/VaultRouterBranch.sol#L438-L440) and [deposit](https://github.com/Cyfrin/2025-01-zaros-part-2/blob/35deb3e92b2a32cd304bf61d27e6071ef36e446d/src/market-making/branches/VaultRouterBranch.sol#L290)
* `priceAdapter` in [VaultRouterBranch::getVaultCreditCapacity](https://github.com/Cyfrin/2025-01-zaros-part-2/blob/35deb3e92b2a32cd304bf61d27e6071ef36e446d/src/market-making/branches/VaultRouterBranch.sol#L81-L82) and [StabilityBranch::initiateSwap](https://github.com/Cyfrin/2025-01-zaros-part-2/blob/35deb3e92b2a32cd304bf61d27e6071ef36e446d/src/market-making/branches/StabilityBranch.sol#L233)

In case admin wants to update `priceAdapter` (eg. in case of a vulnerability in existing adaptor) or to disable the collateral, he can't.
The protocol can reach a situation where an asset is disabled in `market-making-engine` (via  `configureCollateral`) while is still active in a Vault.
Same for `priceAdapter`, it can have an adapter in a specific vault and a different adapter to be configured in engine for same asset.
In case of a vulnerable adaptor the vault must be shut down and re-created.

## Impact

Key vault parameters are inaccessible for admin to update, resulting the relaunch the vault and the associated  hassle.

## Tools Used

## Recommendations

There are two options. Either remove `Collateral.data` from Vault structure and update the code where required to interogate collateral data only from `COLLATERAL_LOCATION`.
Or, at least, add a new function (or update existing `Vault::update`) to allow admin to update these two parameters.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Part 2 |
| Report Date | N/A |
| Finders | alexczm |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2025-01-zaros-part-2
- **Contest**: https://codehawks.cyfrin.io/c/cm60h7a380000k66h6knt2vtl

### Keywords for Search

`vulnerability`

