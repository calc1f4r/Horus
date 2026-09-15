---
# Core Classification
protocol: Cove_2025-04-16
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57978
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Cove-security-review_2025-04-16.md
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.20
financial_impact: low

# Scoring
quality_score: 1
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[L-03] Missing fee update in `completeRebalance()`

### Overview

See description below for full details.

### Original Finding Content

In Cove, we will rebalance the basket's asset weight periodically. In the rebalance process, we may trigger below 4 steps:

1. propose rebalance in timestamp X.
2. propose swap, and finish the internal trade in timestamp X + 1000.
3. execute the swap in timestamp X + 2000.
4. complete the rebalance in timestamp X + 3000. Notice: Anyone can trigger this function.

We can find out that in step1, we will trigger `_harvestManagementFee` to accrue the management fees before `timestamp X`. However, in the function `completeRebalance`, we don't accrue the management fee between timestamp X and timestamp X + 3000.

In function `completeRebalance`, we have one check `block.timestamp - self.rebalanceStatus.timestamp < self.stepDelay`. The default `stepDelay` is `15 minutes`. The maximum value is `1 hours`. It means that we may miss accruing around 15 minutes of management fees before we finish the rebalancing process.

Impact:

1. When we try to finish the rebalance, we will calculate the pending redeem share's assets amount according to the share's price. Because we don't acquire the last time slot's management fees, the `totalSupply` will be less than the expected value. (When we accrue management fees, we will mint some shares for the fee recipient). The redeemers can avoid paying the last time slot fees.
2. When we try to accrue the management fee next time, we will re-calculate the management fees between timestamp X and timestamp X + 3000. And we will use the latest `totalSupply`. If we have one large pending redeem in above stamp 4, the current `totalSupply` will be less than the actual total supply we should use to calculate the management fees between timestamp X and timestamp X + 3000. The protocol will miss one part of the expected management fees.

```solidity
    function proposeRebalance(BasketManagerStorage storage self, address[] calldata baskets) external {
        (uint256 pendingDeposits, uint256 pendingRedeems) =
            BasketToken(basket).prepareForRebalance(self.managementFees[basket], feeCollector);
    }
    function prepareForRebalance(
        uint16 feeBps,
        address feeCollector
    ) {
        _harvestManagementFee(feeBps, feeCollector);
    }
    function completeRebalance(
        BasketManagerStorage storage self,
        ExternalTrade[] calldata externalTrades,
        address[] calldata baskets,
        uint64[][] calldata basketTargetWeights,
        address[][] calldata basketAssets
    )
        if (block.timestamp - self.rebalanceStatus.timestamp < self.stepDelay) {
            revert TooEarlyToCompleteRebalance();
        }
    }
```

```solidity
    function _finalizeRebalance(
        BasketManagerStorage storage self,
        EulerRouter eulerRouter,
        address[] calldata baskets,
        address[][] calldata basketAssets
    ) {
        if (pendingRedeems > 0) {
            uint256 withdrawAmount = eulerRouter.getQuote(
                FixedPointMathLib.fullMulDiv(basketValue, pendingRedeems, BasketToken(basket).totalSupply()),
                // _USD_ISO_4217_CODE --> 840
                _USD_ISO_4217_CODE,
                baseAsset
            );
    }
    }
```

Accure the management fees in function `completeRebalance`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 1/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Cove_2025-04-16 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Cove-security-review_2025-04-16.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

