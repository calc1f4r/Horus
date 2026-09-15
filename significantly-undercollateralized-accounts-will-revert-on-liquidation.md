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
solodit_id: 13251
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

Significantly undercollateralized accounts will revert on liquidation

### Overview

See description below for full details.

### Original Finding Content

#### Resolution



Remediated per Notional’s team notes in [commit](https://github.com/notional-finance/contracts-v2/pull/104/commits/2a749da0d2e4f3f6d9ea4c685dc264640729a792) by updating the calculations within `calculateDeleverageAmount`


#### Description


The Notional Strategy Vaults utilise collateral to allow leveraged borrowing as long as the account passes the `checkCollateralRatio` check that ensures the overall account value is at least `minCollateralRatio` greater than its debts.
If the account doesn’t have sufficient collateral, it goes through a liquidation process where some of the collateral is sold to liquidators for the account’s borrowed currency in attempt to improve the collateral ratio.
However, if the account is severely undercollateralised, the entire account position is liquidated and given over to the liquidator:


**contracts-v2/contracts/internal/vaults/VaultAccount.sol:L282-L289**



```
int256 depositRatio = maxLiquidatorDepositAssetCash.mul(vaultConfig.liquidationRate).div(vaultShareValue);

// Use equal to so we catch potential off by one issues, the deposit amount calculated inside the if statement
// below will round the maxLiquidatorDepositAssetCash down
if (depositRatio >= Constants.RATE\_PRECISION) {
    maxLiquidatorDepositAssetCash = vaultShareValue.divInRatePrecision(vaultConfig.liquidationRate);
    // Set this to true to ensure that the account gets fully liquidated
    mustLiquidateFullAmount = true;

```
Here, the liquidator will need to deposit exactly `maxLiquidatorDepositAssetCash=vaultShareValue/liquidationRate` in order to get all of account’s assets, i.e. all of `vaultShareValue` in the form of `vaultAccount.vaultShares`. In fact, later this deposit will be set in `vaultAccount.tempCashBalance`:


**contracts-v2/contracts/external/actions/VaultAccountAction.sol:L361-L380**



```
int256 maxLiquidatorDepositExternal = assetToken.convertToExternal(maxLiquidatorDepositAssetCash);

// NOTE: deposit amount external is always positive in this method
if (depositAmountExternal < maxLiquidatorDepositExternal) {
    // If this flag is set, the liquidator must deposit more cash in order to liquidate the account
    // down to a zero fCash balance because it will fall under the minimum borrowing limit.
    require(!mustLiquidateFull, "Must Liquidate All Debt");
} else {
    // In the other case, limit the deposited amount to the maximum
    depositAmountExternal = maxLiquidatorDepositExternal;
}

// Transfers the amount of asset tokens into Notional and credit it to the account's temp cash balance
int256 assetAmountExternalTransferred = assetToken.transfer(
    liquidator, vaultConfig.borrowCurrencyId, depositAmountExternal
);

vaultAccount.tempCashBalance = vaultAccount.tempCashBalance.add(
    assetToken.convertToInternal(assetAmountExternalTransferred)
);

```
Then the liquidator will get:


**contracts-v2/contracts/external/actions/VaultAccountAction.sol:L274-L281**



```
uint256 vaultSharesToLiquidator;
{
    vaultSharesToLiquidator = vaultAccount.tempCashBalance.toUint()
        .mul(vaultConfig.liquidationRate.toUint())
        .mul(vaultAccount.vaultShares)
        .div(vaultShareValue.toUint())
        .div(uint256(Constants.RATE\_PRECISION));
}

```
And if (except for precision and conversions) `vaultAccount.tempCashBalance=maxLiquidatorDepositAssetCash=vaultShareValue/liquidationRate`, then `vaultSharesToLiquidator = (vaultAccount.tempCashBalance * liquidationRate * vaultAccount.vaultShares) / (vaultShareValue)`
becomes
`vaultSharesToLiquidator = ((vaultShareValue/liquidationRate)* liquidationRate * vaultAccount.vaultShares) / (vaultShareValue) = vaultAccount.vaultShares`


In other words, the liquidator needed to deposit exactly `vaultShareValue/liquidationRate` to get all `vaultAccount.vaultShares`. However, the liquidator deposit (what would be in `vaultAccount.tempCashBalance`) needs to cover all of that account’s debt, i.e. `vaultAccount.fCash`. At the end of the liquidation process, the vault account has its fCash and tempCash balances updated:


**contracts-v2/contracts/external/actions/VaultAccountAction.sol:L289-L290**



```
int256 fCashToReduce = vaultConfig.assetRate.convertToUnderlying(vaultAccount.tempCashBalance);
vaultAccount.updateAccountfCash(vaultConfig, vaultState, fCashToReduce, vaultAccount.tempCashBalance.neg());

```
**contracts-v2/contracts/internal/vaults/VaultAccount.sol:L77-L88**



```
function updateAccountfCash(
    VaultAccount memory vaultAccount,
    VaultConfig memory vaultConfig,
    VaultState memory vaultState,
    int256 netfCash,
    int256 netAssetCash
) internal {
    vaultAccount.tempCashBalance = vaultAccount.tempCashBalance.add(netAssetCash);

    // Update fCash state on the account and the vault
    vaultAccount.fCash = vaultAccount.fCash.add(netfCash);
    require(vaultAccount.fCash <= 0);

```
While the `vaultAccount.tempCashBalance` gets cleared to 0, the `vaultAccount.fCash` amount only gets to `vaultAccount.fCash = vaultAccount.fCash.add(netfCash)`, and `netfCash=fCashToReduce = vaultConfig.assetRate.convertToUnderlying(vaultAccount.tempCashBalance)`, which, based on the constraints above essentially becomes:


`vaultAccount.fCash=vaultAccount.fCash+vaultConfig.assetRate.convertToUnderlying(assetToken.convertToExternal(vaultShareValue/vaultConfig.liquidationRate))`


However, later this account is set on storage, and, considering it is going through 100% liquidation, the account will necessarily be below minimum borrow size and will need to be at `vaultAccount.fCash==0`.


**contracts-v2/contracts/internal/vaults/VaultAccount.sol:L52-L62**



```
function setVaultAccount(VaultAccount memory vaultAccount, VaultConfig memory vaultConfig) internal {
    mapping(address => mapping(address => VaultAccountStorage)) storage store = LibStorage
        .getVaultAccount();
    VaultAccountStorage storage s = store[vaultAccount.account][vaultConfig.vault];

    // The temporary cash balance must be cleared to zero by the end of the transaction
    require(vaultAccount.tempCashBalance == 0); // dev: cash balance not cleared
    // An account must maintain a minimum borrow size in order to enter the vault. If the account
    // wants to exit under the minimum borrow size it must fully exit so that we do not have dust
    // accounts that become insolvent.
    require(vaultAccount.fCash == 0 || vaultConfig.minAccountBorrowSize <= vaultAccount.fCash.neg(), "Min Borrow");

```
The case where vaultAccount.fCash>0 is taken care of by taking any extra repaid value and assigning it to the protocol, zeroing out the account’s balances:


**contracts-v2/contracts/external/actions/VaultAccountAction.sol:L293**



```
if (vaultAccount.fCash > 0) vaultAccount.fCash = 0;

```
The case where `vaultAccount.fCash < 0` is however not addressed, and instead the process will revert. This will occur whenever the vaultShareValue discounted with the liquidation rate is less than the fCash debt after all the conversions between external and underlying accounting. So, whenever the below is true, the account will not be liquidate-able.
`fCash>vaultShareValue/liquidationRate`


This is an issue because the account is still technically solvent even though it is undercollateralized, but the current implementation would simply revert until the account is entirely insolvent (still without liquidation options) or its balances are restored enough to be liquidated fully.


Consider implementing a dynamic liquidation rate that becomes smaller the closer the account is to insolvency, thereby encouraging liquidators to promptly liquidate the accounts.

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

