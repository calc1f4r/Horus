---
# Core Classification
protocol: GTE
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64836
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2025-08-gte-perps-and-launchpad
source_link: https://code4rena.com/reports/2025-08-gte-perps-and-launchpad
github_link: https://code4rena.com/audits/2025-08-gte-perps-and-launchpad/submissions/F-21

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
finders_count: 4
finders:
  - lonelybones
  - Stormy
  - Mike\_Bello90
  - dhank
---

## Vulnerability Title

[M-01] Due to logical error when changing leverage the system also refunds the margin that should be backing the unrealized loss the account holds.

### Overview


The bug report discusses an issue with a function called `settleNewLeverage` in the `CollateralManager.sol` and `PerpManager.sol` files. This function is supposed to correctly adjust the margin balance of a user when they change the leverage of an already opened position. However, the function does not take into account the unrealized profit or loss (uPnL) of the position, resulting in the system refunding all excess margin to the user, including the margin that is used to cover ongoing losses. This can cause faulty bad debt and affect the insurance fund. The recommended solution is to refactor the function to consider the uPnL of the position and only take it into account if it is negative, indicating a loss for the user.

### Original Finding Content



* `perps/PerpManager.sol` [# L221](https://github.com/code-423n4/2025-08-gte-perps/blob/main/contracts/perps/PerpManager.sol# L221)
* `perps/types/CollateralManager.sol` [# L72](https://github.com/code-423n4/2025-08-gte-perps/blob/main/contracts/perps/types/CollateralManager.sol# L72)

On short explanation, when changing the leverage of already opened position, the system calculates the new intended margin based on the current position notional size and the changed leverage value. The intended margin is then checked against the position’s total equity (margin + upnl) to ensure that the position remains above the minimum open margin value.
```

        cache.fundingPayment = ClearingHouseLib.realizeFundingPayment(cache.assets, cache.positions);

        cache.newMargin = clearingHouse.getIntendedMargin(cache.assets, cache.positions);

        // assert open margin requirement met
        clearingHouse.assertOpenMarginRequired({
            assets: cache.assets,
            positions: cache.positions,
            margin: cache.newMargin.toInt256()
        });

        clearingHouse.setPositions({
            tradedAsset: "",
            account: account,
            subaccount: subaccount,
            assets: cache.assets,
            positions: cache.positions
        });

        // settle delta between new and prev margin & new and prev orderbook collateral
        collateralDelta = StorageLib.loadCollateralManager().settleNewLeverage({
            account: account,
            subaccount: subaccount,
            collateralDeltaFromBook: cache.collateralDeltaFromBook,
            newMargin: cache.newMargin.toInt256(),
            fundingPayment: cache.fundingPayment
        });
```

The function `settleNewLeverage` is supposed to correctly account the margin balance of the user when leverage is changed. However the function does not take into account the unrealized PnL when calculating the new margin balance. As a result, the system can refund all excess margin including the margin that is effectively used to cover ongoing unrealized losses the account holds.

Simple example with Bob:

* Bob has 20k long position at 1x leverage.
* The market moves against Bob and the position now has -10k uPnL.
* When changing leverage, the new intended margin for the position to be open is 5k.
* Under normal behaviour the system should refund (20k - 10k) - 5k = 5k refund.
* However when settling the new leverage, the system only keeps the new intended position margin.
* So the margin balance covering the loss of the -10k uPnL loss is also refunded to Bob.
* Due to this logical error faulty bad debt is inflicted to the system and covered by the insurance fund.
```

    function settleNewLeverage(
        CollateralManager storage self,
        address account,
        uint256 subaccount,
        int256 collateralDeltaFromBook,
        int256 newMargin,
        int256 fundingPayment
    ) internal returns (int256 collateralDelta) {
        int256 currentMargin = self.margin[account][subaccount] - fundingPayment;

        int256 collateralDeltaFromPosition = newMargin - currentMargin;

        collateralDelta = collateralDeltaFromPosition + collateralDeltaFromBook;

        self.handleCollateralDelta(account, collateralDelta);

        self.margin[account][subaccount] = newMargin;
    }
```

### Recommended mitigation steps

Refactor the function `settleNewLeverage` to consider the account’s uPnL as well. The uPnL should be taken into account only if its negative value indicates that there is unrealized loss owned by the account holder.
```

    function settleNewLeverage(
        CollateralManager storage self,
        address account,
        uint256 subaccount,
        int256 collateralDeltaFromBook,
        int256 newMargin,
        int256 fundingPayment,
        int256 upnl
    ) internal returns (int256 collateralDelta) {
        int256 effectiveUpnl = upnl < 0 ? upnl : int256(0);

        int256 currentMargin = self.margin[account][subaccount] + effectiveUpnl - fundingPayment;

        int256 collateralDeltaFromPosition = newMargin - currentMargin;

        collateralDelta = collateralDeltaFromPosition + collateralDeltaFromBook;

        self.handleCollateralDelta(account, collateralDelta);

        self.margin[account][subaccount] = newMargin;
```

---



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | GTE |
| Report Date | N/A |
| Finders | lonelybones, Stormy, Mike\_Bello90, dhank |

### Source Links

- **Source**: https://code4rena.com/reports/2025-08-gte-perps-and-launchpad
- **GitHub**: https://code4rena.com/audits/2025-08-gte-perps-and-launchpad/submissions/F-21
- **Contest**: https://code4rena.com/reports/2025-08-gte-perps-and-launchpad

### Keywords for Search

`vulnerability`

