---
# Core Classification
protocol: Securitize Vaultv2 Rwasegwrap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64294
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md
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
finders_count: 2
finders:
  - Hans
  - Rodion
---

## Vulnerability Title

Shared configuration parameters across different asset types in vault deployers leads to incorrect pricing and fee calculations

### Overview


This bug report discusses an issue with the `VaultDeployer` and `SecuritizeVaultDeployer` contracts. These contracts have shared configuration parameters that are used for all deployed vaults, regardless of the type of asset. This means that different assets, such as real estate tokens and commodity tokens, share the same parameters, leading to incorrect pricing calculations and potential economic losses for users. The report recommends two solutions to fix this issue, either by modifying the vault deployer architecture to support asset-specific configurations or by storing the asset and liquid token addresses in the deployer and removing them from the deploy function. The bug has been fixed by the Securitize team and verified by Cyfrin.

### Original Finding Content

**Description:** The `VaultDeployer` and `SecuritizeVaultDeployer` contracts maintain shared configuration parameters (`navProvider`, `feeManager`, `redemptionAddress`) that are applied to all deployed vaults regardless of their underlying asset type. When `SegregatedVaultDeployer::deploy()` or `SecuritizeVaultDeployer::deploy()` is called with different `assetToken` and `liquidationToken` parameters to support various vault types, the same `navProvider` is used across all deployments. This creates a critical architectural flaw because different RWA assets require asset-specific NAV providers for accurate valuation.

In `SecuritizeVaultV2`, the `navProvider.rate()` is extensively used in critical functions like `_convertToShares()`, `_convertToAssets()`, and `getShareValue()` to determine share-to-asset conversion ratios. When vaults for different assets (e.g., real estate tokens vs commodity tokens) share the same NAV provider, the pricing calculations become incorrect for at least one of the asset types.

Similar issues exist with:
- `SecuritizeVaultDeployer.feeManager` - applies the same fee logic to all asset types
- `SecuritizeVaultDeployer.redemptionAddress` - uses the same redemption contract for different assets that may require different redemption mechanisms

Note that `SegregatedVault` does not use `navProvider` in its calculations, so it is not directly affected by this issue, but the architecture problem persists in the deployment pattern.

**Impact:** Users depositing assets into vaults with incorrect NAV providers will receive wrong share amounts, leading to economic losses and potential exploitation opportunities where attackers can deposit low-value assets but receive shares calculated using high-value asset NAV rates.

```solidity
// In SecuritizeVaultDeployer::deploy()
BeaconProxy proxy = new BeaconProxy(
    upgradeableBeacon,
    abi.encodeWithSelector(
        SecuritizeVaultV2(payable(address(0))).initializeV2.selector,
        name,
        symbol,
        assetToken,      // Different per deployment
        redemptionAddress, // Same for all deployments - ISSUE
        liquidationToken,
        navProvider,     // Same for all deployments - ISSUE
        feeManager       // Same for all deployments - ISSUE
    )
);
```

**Recommended Mitigation:** We understand that these parameters are meant to be managed by only the admin, and that is why it's managed by the contract instead of allowing users to specify in the deploy function. We recommend the team consider either of below two solutions.

1. Modify the vault deployer architecture to support asset-specific configurations. Below is an example implementation.

```diff
+ mapping(address => address) public assetNavProviders;
+ mapping(address => address) public assetFeeManagers;
+ mapping(address => address) public assetRedemptionAddresses;

+ function setAssetConfiguration(
+     address assetToken,
+     address navProvider,
+     address feeManager,
+     address redemptionAddress
+ ) external onlyRole(DEFAULT_ADMIN_ROLE) {
+     assetNavProviders[assetToken] = navProvider;
+     assetFeeManagers[assetToken] = feeManager;
+     assetRedemptionAddresses[assetToken] = redemptionAddress;
+ }
```
2. If the intention is to have one deployer for every pair of asset token ad liquid token, store the asset token address and liquid token address in the deployer with the nav provider together and remove the `assetToken` adn `liquidToken` parameters from the deploy function.

**Securitize:** Fixed in commit [05044b](https://github.com/securitize-io/bc-rwa-seg-wrap-sc/commit/05044b3f10d66d82ad134fc73f712c62ba5796e2).

**Cyfrin:** Verified.

\clearpage

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Securitize Vaultv2 Rwasegwrap |
| Report Date | N/A |
| Finders | Hans, Rodion |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

