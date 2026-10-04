---
# Core Classification
protocol: Notional Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13247
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2022/07/notional-finance/
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

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - insurance

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - George Kobakhidze
  -  Chingiz Mardanov
  -  Sergii Kravchenko

---

## Vulnerability Title

Secondary Currency debt is not managed by the Notional Controller

### Overview

See description below for full details.

### Original Finding Content

#### Resolution



Remediated per Notional’s team notes in [commit](https://github.com/notional-finance/contracts-v2/pull/104/commits/6a7b3af67918596dbbeb6bf66c0d228a350baf3d) by adding valuation for secondary borrow within the vault.


#### Description


Some of the Notional Strategy Vaults may allow for secondary currencies to be borrowed as part of the same strategy. For example, a strategy may allow for USDC to be its primary borrow currency as well as have ETH as its secondary borrow currency.


In order to enter the vault, a user would have to deposit `depositAmountExternal` of the primary borrow currency when calling `VaultAccountAction.enterVault()`. This would allow the user to borrow with leverage, as long as the `vaultConfig.checkCollateralRatio()` check on that account succeeds, which is based on the initial deposit and borrow currency amounts. This collateral ratio check is then performed throughout that user account’s lifecycle in that vault, such as when they try to roll their maturity, or when liquidators try to perform collateral checks to ensure there is no bad debt.


However, in the event that the vault has a secondary borrow currency as well, that additional secondary debt is not calculated as part of the `checkCollateralRatio()` check. The only debt that is being considered is the `vaultAccount.fCash` that corresponds to the primary borrow currency debt:


**contracts-v2/contracts/internal/vaults/VaultConfiguration.sol:L313-L319**



```
function checkCollateralRatio(
    VaultConfig memory vaultConfig,
    VaultState memory vaultState,
    VaultAccount memory vaultAccount
) internal view {
    (int256 collateralRatio, /\* \*/) = calculateCollateralRatio(
        vaultConfig, vaultState, vaultAccount.account, vaultAccount.vaultShares, vaultAccount.fCash

```
**contracts-v2/contracts/internal/vaults/VaultConfiguration.sol:L278-L292**



```
function calculateCollateralRatio(
    VaultConfig memory vaultConfig,
    VaultState memory vaultState,
    address account,
    uint256 vaultShares,
    int256 fCash
) internal view returns (int256 collateralRatio, int256 vaultShareValue) {
    vaultShareValue = vaultState.getCashValueOfShare(vaultConfig, account, vaultShares);

    // We do not discount fCash to present value so that we do not introduce interest
    // rate risk in this calculation. The economic benefit of discounting will be very
    // minor relative to the added complexity of accounting for interest rate risk.

    // Convert fCash to a positive amount of asset cash
    int256 debtOutstanding = vaultConfig.assetRate.convertFromUnderlying(fCash.neg());

```
Whereas the value of strategy tokens that belong to that user account are being calculated by calling `IStrategyVault(vault).convertStrategyToUnderlying()` on the associated strategy vault:


**contracts-v2/contracts/internal/vaults/VaultState.sol:L314-L324**



```
function getCashValueOfShare(
    VaultState memory vaultState,
    VaultConfig memory vaultConfig,
    address account,
    uint256 vaultShares
) internal view returns (int256 assetCashValue) {
    if (vaultShares == 0) return 0;
    (uint256 assetCash, uint256 strategyTokens) = getPoolShare(vaultState, vaultShares);
    int256 underlyingInternalStrategyTokenValue = \_getStrategyTokenValueUnderlyingInternal(
        vaultConfig.borrowCurrencyId, vaultConfig.vault, account, strategyTokens, vaultState.maturity
    );

```
**contracts-v2/contracts/internal/vaults/VaultState.sol:L296-L311**



```
function \_getStrategyTokenValueUnderlyingInternal(
    uint16 currencyId,
    address vault,
    address account,
    uint256 strategyTokens,
    uint256 maturity
) private view returns (int256) {
    Token memory token = TokenHandler.getUnderlyingToken(currencyId);
    // This will be true if the the token is "NonMintable" meaning that it does not have
    // an underlying token, only an asset token
    if (token.decimals == 0) token = TokenHandler.getAssetToken(currencyId);

    return token.convertToInternal(
        IStrategyVault(vault).convertStrategyToUnderlying(account, strategyTokens, maturity)
    );
}

```
From conversations with the Notional team, it is assumed that this call returns the strategy token value subtracted against the secondary currencies debt, as is the case in the `Balancer2TokenVault` for example. In other words, when collateral ratio checks are performed, those strategy vaults that utilize secondary currency borrows would need to calculate the value of strategy tokens already accounting for any secondary debt. However, this is a dependency for a critical piece of the Notional controller’s strategy vaults collateral checks.


Therefore, even though the strategy vaults' code and logic would be vetted before their whitelisting into the Notional system, they would still remain an external dependency with relatively arbitrary code responsible for the liquidation infrastructure that could lead to bad debt or incorrect liquidations if the vaults give inaccurate information, and thus potential loss of funds.


#### Recommendation


Specific strategy vault implementations using secondary borrows were not in scope of this audit. However, since the core Notional Vault system was, and it includes secondary borrow currency functionality, from the point of view of the larger Notional system it is recommended to include secondary debt checks within the Notional controller contract to reduce external dependency on the strategy vaults' logic.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Notional Finance |
| Report Date | N/A |
| Finders | George Kobakhidze,  Chingiz Mardanov,  Sergii Kravchenko
 |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2022/07/notional-finance/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

