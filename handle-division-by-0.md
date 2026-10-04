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
solodit_id: 13245
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2022/07/notional-finance/
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

Handle division by 0

### Overview


The Notional team identified three places in their contract code where division by zero could occur, potentially leading to reverts and disrupting operations. The team remediated the issue by adding checks to account for division by zero in the settle vault account, as well as a short circuit to ensure debtSharesToRepay is never zero. The team also acknowledged that the contract will revert when vaultShareValue is zero, but decided to not make any changes related to that.

It is important to handle cases where the denominator could be zero appropriately, as this code could be reutilized in other circumstances later that could cause reverts and even disrupt operations more frequently.

### Original Finding Content

#### Resolution



Remediated per Notional’s team notes in [commit](https://github.com/notional-finance/contracts-v2/pull/104/commits/1681e16cd798fb60e756051d051de075ab641d21) by adding the following checks:


* Check to account for div by zero in settle vault account
* Short circuit to ensure debtSharesToRepay is never zero. Divide by zero may still occur but this would signal a critical accounting issue


The Notional team also acknowledged that the contract will revert when `vaultShareValue = 0`. The team decided to not make any changes related to that since liquidation will not accomplish anything for an account with no vault share value.




#### Description


There are a few places in the code where division by zero may occur but isn’t handled.


#### Examples


If the vault settles at exactly 0 value with 0 remaining strategy token value, there may be an unhandled division by zero trying to divide claims on the settled assets:


**contracts-v2/contracts/internal/vaults/VaultAccount.sol:L424-L436**



```
int256 settledVaultValue = settlementRate.convertToUnderlying(residualAssetCashBalance)
    .add(totalStrategyTokenValueAtSettlement);

// If the vault is insolvent (meaning residualAssetCashBalance < 0), it is necessarily
// true that totalStrategyTokens == 0 (meaning all tokens were sold in an attempt to
// repay the debt). That means settledVaultValue == residualAssetCashBalance, strategyTokenClaim == 0
// and assetCashClaim == totalAccountValue. Accounts that are still solvent will be paid from the
// reserve, accounts that are insolvent will have a totalAccountValue == 0.
strategyTokenClaim = totalAccountValue.mul(vaultState.totalStrategyTokens.toInt())
    .div(settledVaultValue).toUint();

assetCashClaim = totalAccountValue.mul(residualAssetCashBalance)
    .div(settledVaultValue);

```
If a vault account is entirely insolvent and its `vaultShareValue` is zero, there will be an unhandled division by zero during liquidation:


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
If a vault account’s secondary debt is being repaid when there is none, there will be an unhandled division by zero:


**contracts-v2/contracts/internal/vaults/VaultConfiguration.sol:L661-L666**



```
VaultSecondaryBorrowStorage storage balance =
    LibStorage.getVaultSecondaryBorrow()[vaultConfig.vault][maturity][currencyId];
uint256 totalfCashBorrowed = balance.totalfCashBorrowed;
uint256 totalAccountDebtShares = balance.totalAccountDebtShares;

fCashToLend = debtSharesToRepay.mul(totalfCashBorrowed).div(totalAccountDebtShares).toInt();

```
While these cases may be unlikely today, this code could be reutilized in other circumstances later that could cause reverts and even disrupt operations more frequently.


#### Recommendation


Handle the cases where the denominator could be zero appropriately.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

