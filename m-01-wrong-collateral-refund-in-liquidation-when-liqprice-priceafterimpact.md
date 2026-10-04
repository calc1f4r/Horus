---
# Core Classification
protocol: Ostium_2025-04-06
chain: everychain
category: uncategorized
vulnerability_type: abi_encoding

# Attack Vector Details
attack_type: abi_encoding
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61521
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Ostium-security-review_2025-04-06.md
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 3.6

# Context Tags
tags:
  - abi_encoding

protocol_categories:
  - gaming

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-01] Wrong collateral refund in liquidation when `liqPrice == priceAfterImpact`

### Overview


The report describes a bug in the system where during a liquidation process, the system may incorrectly refund a portion of the user's collateral. This happens because of a discrepancy in how certain values are calculated. The recommendation is to explicitly set a value to 0 during liquidation to prevent any unintended refunds. 

### Original Finding Content


## Severity

**Impact:** High

**Likelihood:** Low

## Description

When a liquidation is triggered and the Oracle price used results in `liqPrice == priceAfterImpact` during the execution of `executeAutomationCloseOrderCallback()`, the system may incorrectly refund a portion of the user collateral - approximately equal to the `liquidationFee`.

This occurs due to a discrepancy in how `value` and `liqMarginValue` are calculated within the `getTradeValuePure()` function. Under specific conditions (`liqPrice == priceAfterImpact`), `value` can become greater than `liqMarginValue`, even though the position should be fully liquidated.

Within the new `Margin-Based Liquidations` logic, users should not receive any collateral back during liquidation. The entire collateral should be distributed between the `liquidationFee` and the `Vault` to cover losing trade.

However, do to the legacy refund logic that remains in the code:

```solidity
@>      uint256 usdcSentToVault = usdcLeftInStorage - usdcSentToTrader;
        storageT.transferUsdc(address(storageT), address(this), usdcSentToVault);
        vault.receiveAssets(usdcSentToVault, trade.trader);
@>      if (usdcSentToTrader > 0) storageT.transferUsdc(address(storageT), trade.trader, usdcSentToTrader);
```

With combination to the incorrect calculation of `value` and `liqMarginValue`, the `usdcSentToTrader` returned from the `getTradeValue()` function may end up being roughly equal to the `liquidationFee`, resulting in an unintended refund to the liquidated trader.

## Recommendation

Ensure that `usdcSentToTrader` is explicitly set to `0` during liquidation, preventing any collateral refund:

```diff
    if (liquidationFee > 0) {
        storageT.transferUsdc(address(storageT), address(this), liquidationFee);
        vault.distributeReward(liquidationFee);
        emit VaultLiqFeeCharged(orderId, tradeId, trade.trader, liquidationFee);
+
+       usdcSentToTrader = 0;
    }
```





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 3.6/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Ostium_2025-04-06 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Ostium-security-review_2025-04-06.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`ABI Encoding`

