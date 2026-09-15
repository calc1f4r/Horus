---
# Core Classification
protocol: LEND
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58377
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/908
source_link: none
github_link: https://github.com/sherlock-audit/2025-05-lend-audit-contest-judging/issues/578

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 6
finders:
  - future
  - coin2own
  - 0xc0ffEE
  - jokr
  - h2134
---

## Vulnerability Title

H-8: Cross-chain liquidations will be blocked due to incorrect maxLiquidatable amount calculation.

### Overview


The report discusses a bug found in a cross-chain liquidation function in a lending platform. The function incorrectly calculates the maximum amount that can be repaid during a liquidation, resulting in valid cross-chain liquidations being rejected. This is due to the function not including borrow amounts where the current chain is the destination chain. The bug can be exploited by a user who has a cross-chain borrow originating from another chain. The impact of this bug is that valid cross-chain liquidations will be blocked. To mitigate this issue, a new function should be introduced to accurately calculate the maximum amount that can be repaid during a cross-chain liquidation.

### Original Finding Content

Source: https://github.com/sherlock-audit/2025-05-lend-audit-contest-judging/issues/578 

## Found by 
0xc0ffEE, coin2own, future, h2134, jokr, wickie

### Summary

During cross-chain liquidations, the `_validateAndPrepareLiquidation` function verifies that `repayAmount <= maxLiquidationAmount`. However, the computed `maxLiquidationAmount` from the `getMaxLiquidationRepayAmount()` function is incorrect if we want to calculate cross-chain collaterals.

```solidity
function getMaxLiquidationRepayAmount(address borrower, address lToken, bool isSameChain)
    external
    view
    returns (uint256)
{
    uint256 currentBorrow = 0;

    currentBorrow += isSameChain
        ? borrowWithInterestSame(borrower, lToken)
        : borrowWithInterest(borrower, lToken);

    uint256 closeFactorMantissa = LendtrollerInterfaceV2(lendtroller).closeFactorMantissa();
    uint256 maxRepay = (currentBorrow * closeFactorMantissa) / 1e18;

    return maxRepay;
}
```

https://github.com/sherlock-audit/2025-05-lend-audit-contest/blob/main/Lend-V2/src/LayerZero/LendStorage.sol#L573-L591

https://github.com/sherlock-audit/2025-05-lend-audit-contest/blob/main/Lend-V2/src/LayerZero/LendStorage.sol#L478-L504



The issue lies in the use of `borrowWithInterest()`, which returns the sum of cross-chain borrows *originating from* the current chain. It **does not** include borrow amounts where the current chain is the **destination chain**.

As a result, if a user has a cross-chain borrow ( originated from another chain), it will not be considered in the liquidation cap calculation. Consequently, valid cross-chain liquidations can be incorrectly rejected.

### Root Cause

The `borrowWithInterest()` function only returns borrows initiated from the current chain, not borrows whose destination chain is current chain (cross-chain collaterals)

Using it to calculate liquidation cap of cross-chain borrows on destination chain leads wrong `maxLiquidationAmount` reverting valid liquidations.

### Internal Pre-conditions


1. User has cross-chain collateral on this chain.
2. No (or less)  cross-chain borrows of that token initiated from this chain.

### External Pre-conditions


### Attack Path

1. Alice has a $1,000 borrow position on Chain B (destination chain), which originated from Chain A.
2. The borrow is undercollateralized and should be liquidated.
3. A liquidator tries to initiate cross-chain liquidation for $500 of Alice’s borrow on Chain B.
4. Since Alice has no borrows of that token initiated from Chain B, both `borrowWithInterest()` returns 0.
5. As a result, `maxLiquidationAmount` is calculated as 0.
6. The liquidation fails due to this incorrect cap check:

```solidity
require(params.repayAmount <= maxLiquidationAmount, "Exceeds max liquidation");
```

### Impact

Valid cross-chain liquidations will be blocked 

### PoC

_No response_

### Mitigation

Introduce a new function that accurately aggregates all cross-chain collaterals of a given token for a user whose destination chain is current chain. Use this function instead of `borrowWithInterest()` when calculating `maxLiquidationAmount` during cross-chain liquidations.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | LEND |
| Report Date | N/A |
| Finders | future, coin2own, 0xc0ffEE, jokr, h2134, wickie |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-05-lend-audit-contest-judging/issues/578
- **Contest**: https://app.sherlock.xyz/audits/contests/908

### Keywords for Search

`vulnerability`

