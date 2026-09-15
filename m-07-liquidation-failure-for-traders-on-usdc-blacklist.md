---
# Core Classification
protocol: GainsNetwork-February
chain: everychain
category: uncategorized
vulnerability_type: liquidation

# Attack Vector Details
attack_type: liquidation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37804
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/GainsNetwork-security-review-February.md
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
  - liquidation
  - blacklisted
  - weird_erc20

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-07] Liquidation failure for traders on USDC blacklist

### Overview


The bug report describes an issue where a trade is not properly unregistered and collateral is not returned to the trader during the process of liquidating an account. This can lead to financial losses for the vault and the issue is considered high severity with a low likelihood of occurring. The report recommends changing the process to allow traders to claim their collateral instead of having it pushed to them.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Low

## Description

During the process of liquidating an account, the associated trade is unregistered, and any remaining collateral is returned to the trader. In case liquidation happens, the `tradeValueCollateral` is 0.

        function _unregisterTrade(
            ITradingStorage.Trade memory _trade,
            bool _marketOrder,
            int256 _percentProfit,
            uint256 _closingFeeCollateral,
            uint256 _triggerFeeCollateral
        ) internal returns (uint256 tradeValueCollateral) {
            ...
                if (tradeValueCollateral > collateralLeftInStorage) {
                    vault.sendAssets(tradeValueCollateral - collateralLeftInStorage, _trade.user);
                    _transferCollateralToAddress(_trade.collateralIndex, _trade.user, collateralLeftInStorage);
                } else {
                    _sendToVault(_trade.collateralIndex, collateralLeftInStorage - tradeValueCollateral, _trade.user);
                    _transferCollateralToAddress(_trade.collateralIndex, _trade.user, tradeValueCollateral);
                }

                // 4.2 If collateral in vault, just send collateral to trader from vault
            } else {
                vault.sendAssets(tradeValueCollateral, _trade.user);
            }
        }

However, this process is failed if the trader has been blacklisted by the USDC contract. Specifically, the liquidation attempt fails when trying to transfer a `tradeValueCollateral` of 0, due to a revert in the `_transferCollateralToAddress` function. This can lead to financial losses for the vault, as positions may continue to depreciate without the possibility of liquidation.

## Recommendations

Instead of pushing the collateral amount to traders, let them claim it (Pull over push pattern).

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | GainsNetwork-February |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/GainsNetwork-security-review-February.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`Liquidation, Blacklisted, Weird ERC20`

