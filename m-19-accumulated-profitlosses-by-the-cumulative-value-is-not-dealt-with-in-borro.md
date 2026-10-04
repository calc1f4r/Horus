---
# Core Classification
protocol: Autonomint Colored Dollar V1
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45509
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/569
source_link: none
github_link: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/755

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
  - 0x73696d616f
---

## Vulnerability Title

M-19: Accumulated profit/losses by the cumulative value is not dealt with in `borrowingLiquidation::liquidationType1()`, leading to losses

### Overview


The report discusses a bug in the `borrowingLiquidation::liquidationType1()` function of the `borrowLiquidation.sol` file that leads to losses. The bug was found by user 0x73696d616f and is caused by the function not considering the cumulative values when reducing the `totalVolumeOfBorrowersAmountinWei` and `totalCdsDepositedAmount` variables. This can result in issues when the price drops and a borrower deposits a small amount to trigger a cumulative value update, leading to a loss. The impact of this bug is that a CDS depositor cannot withdraw their deposit until the cumulative value recovers. The report suggests handling the cumulative values when liquidating as a mitigation strategy.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/755 

## Found by 
0x73696d616f

### Summary

`borrowingLiquidation::liquidationType1()` [reduces](https://github.com/sherlock-audit/2024-11-autonomint/blob/main/Blockchain/Blockchian/contracts/Core_logic/borrowLiquidation.sol#L248-L252) `omniChainData.totalVolumeOfBorrowersAmountinWei` and `omniChainData.totalCdsDepositedAmount` without any consideration for the cumulative values so far, leading to losses. The cumulative value at each price is calculated essentially by `priceDiff *  omniChainData.totalVolumeOfBorrowersAmountinWei / omniChainData.totalCdsDepositedAmount`, so changing these 2 variables without tracking correctly the cumulative value leads to issues, as shown below.

### Root Cause

In `borrowLiquidation.sol:248/252`, `totalCdsDepositedAmount` and `totalVolumeOfBorrowersAmountinWei` are modified without considering the cumulative values.

### Internal pre-conditions

None.

### External pre-conditions

None.

### Attack Path

1. Consider a starting price of 1000 USD / ETH.
1. Cds deposit of 1000 USDa.
2. Borrow deposit of 1 ETH, borrowing 800 USDa.
3. Price drops to 800 USD / ETH.
4. Borrower deposits 1 wei to trigger cumulative value update, which registers a loss of roughly `1 * (1000 - 800) / 1000 = 0.2`.
5. Liquidation of the first borrower happens, which will reduce `omnichainData.totalCdsDepositAmount` to `360` (800 to treasury + 20 to abond calculated from 10% of 1000 - 800, cds profit of 1000 - 800 - 20 = 180, which yields a final cds deposited amount of 1000 - (800 + 20 - 180) = 360).
6. Cds depositor withdraws the 1000 USDa (disregarding the 1 wei borrower which doesnt really matter but technically would revert due to the 20% ratio), calculating a return amount of `1000 - 1000*0.2 = 800`. [Then](https://github.com/sherlock-audit/2024-11-autonomint/blob/main/Blockchain/Blockchian/contracts/lib/CDSLib.sol#L664-L665), `uint256 returnAmountWithGains = params.returnAmount + params.cdsDepositDetails.liquidationAmount - params.cdsDepositDetails.initialLiquidationAmount = 800 + 180 - 1000`, which underflows. 180 comes from doing 1000 - 820, where 820 is the liquidation amounted needed (debt + return to abond).

### Impact

Cds depositor can never withdraw until the cumulative value recovers. Alternatively, consider that calculating the cumulative value before liquidation yields -0.2, but after liquidating yields -0 (totalVolumeOfBorrowersAmountinWei becomes 0, so the cumulative value loss is 0), which goes to show that effectively it is incorrectly handled. Any user can trigger cumulative value updates before liquidations to force this bug, if needed.

### PoC

See the calculations above.

### Mitigation

Handle the cumulative values when liquidating.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Autonomint Colored Dollar V1 |
| Report Date | N/A |
| Finders | 0x73696d616f |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/755
- **Contest**: https://app.sherlock.xyz/audits/contests/569

### Keywords for Search

`vulnerability`

