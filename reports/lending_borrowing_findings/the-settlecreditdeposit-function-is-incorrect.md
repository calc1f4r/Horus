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
solodit_id: 49984
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
  - kupiasec
---

## Vulnerability Title

The `settleCreditDeposit` function is incorrect.

### Overview

The `settleCreditDeposit` function in the `Market.sol` file is incorrect. This is a high-risk issue as it affects the calculation of the vault's debt. The issue occurs because the `CreditDeposit` (providers' profit) is counted twice in the vault debt calculation. This can result in losses for users. To fix this issue, the `CreditDeposit` should only be counted in either `usdcCreditPerVaultShare` or `realizedDebtUsdPerVaultShare` and not both.

### Original Finding Content

## Summary
The `CreditDeposit` (providers' profit) was counted twice in the vault debt.

## Vulnerability Details

https://github.com/Cyfrin/2025-01-zaros-part-2/blob/main/src/market-making/leaves/Market.sol#L443
```solidity
443:function settleCreditDeposit(Data storage self, address settledAsset, UD60x18 netUsdcReceivedX18) internal {
        // removes the credit deposit asset that has just been settled for usdc
        self.creditDeposits.remove(settledAsset);

        // calculate the usdc that has been accumulated per usd of credit delegated to the market
        UD60x18 addedUsdcPerCreditShareX18 = netUsdcReceivedX18.div(ud60x18(self.totalDelegatedCreditUsd));

        // add the usdc acquired to the accumulated usdc credit variable
        self.usdcCreditPerVaultShare =
            ud60x18(self.usdcCreditPerVaultShare).add(addedUsdcPerCreditShareX18).intoUint128();

        // deduct the amount of usdc credit from the realized debt per vault share, so we don't double count it
        self.realizedDebtUsdPerVaultShare = sd59x18(self.realizedDebtUsdPerVaultShare).sub(
            addedUsdcPerCreditShareX18.intoSD59x18()
        ).intoInt256().toInt128();
    }
278:function getVaultAccumulatedValues(
        ...
    )
        internal
        view
        returns (
            SD59x18 realizedDebtChangeUsdX18,
            SD59x18 unrealizedDebtChangeUsdX18,
            UD60x18 usdcCreditChangeX18,
            UD60x18 wethRewardChangeX18
        )
    {
        ...
        realizedDebtChangeUsdX18 = !lastVaultDistributedRealizedDebtUsdPerShareX18.isZero()
            ? sd59x18(self.realizedDebtUsdPerVaultShare).sub(lastVaultDistributedRealizedDebtUsdPerShareX18).mul(
                vaultCreditShareX18.intoSD59x18()
            )
            : SD59x18_ZERO;
        ...
        usdcCreditChangeX18 = !lastVaultDistributedUsdcCreditPerShareX18.isZero()
            ? ud60x18(self.usdcCreditPerVaultShare).sub(lastVaultDistributedUsdcCreditPerShareX18).mul(
                vaultCreditShareX18
            )
            : UD60x18_ZERO;
        ...
    }
```
The `CreditDeposit` was counted in both of `realizedDebtChangeUsdX18` and `usdcCreditChangeX18`.
```solidity
Vault.sol
268:function _recalculateConnectedMarketsState(
        Data storage self,
        uint128[] memory connectedMarketsIdsCache,
        bool shouldRehydrateCache
    )
        private
        returns (
            uint128[] memory rehydratedConnectedMarketsIdsCache,
            SD59x18 vaultTotalRealizedDebtChangeUsdX18,
            SD59x18 vaultTotalUnrealizedDebtChangeUsdX18,
            UD60x18 vaultTotalUsdcCreditChangeX18,
            UD60x18 vaultTotalWethRewardChangeX18
        )
    {
        ...
        for (uint256 i; i < connectedMarketsIdsCache.length; i++) {
            ...
            if (!ctx.marketUnrealizedDebtUsdX18.isZero() || !ctx.marketRealizedDebtUsdX18.isZero()) {
                // distribute the market's debt to its connected vaults
                market.distributeDebtToVaults(ctx.marketUnrealizedDebtUsdX18, ctx.marketRealizedDebtUsdX18);
            }
            ...
            if (!market.getTotalDelegatedCreditUsd().isZero()) {
                ...
                (
                    ctx.realizedDebtChangeUsdX18,
                    ctx.unrealizedDebtChangeUsdX18,
                    ctx.usdcCreditChangeX18,
                    ctx.wethRewardChangeX18
                ) = market.getVaultAccumulatedValues(
                    ud60x18(creditDelegation.valueUsd),
                    sd59x18(creditDelegation.lastVaultDistributedRealizedDebtUsdPerShare),
                    sd59x18(creditDelegation.lastVaultDistributedUnrealizedDebtUsdPerShare),
                    ud60x18(creditDelegation.lastVaultDistributedUsdcCreditPerShare),
                    ud60x18(creditDelegation.lastVaultDistributedWethRewardPerShare)
                );
            }
            ...
        }
    }
369:function recalculateVaultsCreditCapacity(uint256[] memory vaultsIds) internal {
        for (uint256 i; i < vaultsIds.length; i++) {
            ...
            (
                uint128[] memory updatedConnectedMarketsIdsCache,
                SD59x18 vaultTotalRealizedDebtChangeUsdX18,
                SD59x18 vaultTotalUnrealizedDebtChangeUsdX18,
                UD60x18 vaultTotalUsdcCreditChangeX18,
                UD60x18 vaultTotalWethRewardChangeX18
            ) = _recalculateConnectedMarketsState(self, connectedMarketsIdsCache, true);
            ...
            if (!vaultTotalRealizedDebtChangeUsdX18.isZero()) {
                self.marketsRealizedDebtUsd = sd59x18(self.marketsRealizedDebtUsd).add(
                    vaultTotalRealizedDebtChangeUsdX18
                ).intoInt256().toInt128();
            }
            ...
            if (!vaultTotalUsdcCreditChangeX18.isZero()) {
                self.depositedUsdc = ud60x18(self.depositedUsdc).add(vaultTotalUsdcCreditChangeX18).intoUint128();
            }
            ...
        }
    }
```
The `CreditDeposit` was counted in both of `vaultTotalRealizedDebtChangeUsdX18` and `vaultTotalUsdcCreditChangeX18`.
```solidity
239:function getUnsettledRealizedDebt(Data storage self)
        internal
        view
        returns (SD59x18 unsettledRealizedDebtUsdX18)
    {
        unsettledRealizedDebtUsdX18 =
            sd59x18(self.marketsRealizedDebtUsd).add(unary(ud60x18(self.depositedUsdc).intoSD59x18()));
    }
```
The `CreditDeposit` was counted twice in the `getUnsettledRealizedDebt`.

## Impact
The vault's debt calculation was incorrect.
Incorrect accounting results in losses for users.

## Recommendations
Consider counting the `CreditDeposit` in either `usdcCreditPerVaultShare` or `realizedDebtUsdPerVaultShare`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Part 2 |
| Report Date | N/A |
| Finders | kupiasec |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2025-01-zaros-part-2
- **Contest**: https://codehawks.cyfrin.io/c/cm60h7a380000k66h6knt2vtl

### Keywords for Search

`vulnerability`

