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
solodit_id: 45498
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/569
source_link: none
github_link: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/375

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
finders_count: 5
finders:
  - 0xAadi
  - Cybrid
  - CL001
  - John44
  - 0x37
---

## Vulnerability Title

M-8: Incorrect totalVolumeOfBorrowersAmountinWei update in withdraw()

### Overview

The report describes an issue with the `totalVolumeOfBorrowersAmountinWei` variable in the `withdraw()` function of the Autonomint contract. The problem is that the variable is not being updated correctly, as it deducts the wrong amount from the total collateral amount when borrowers withdraw their collateral. This is because the code uses the `depositDetail.depositedAmount` variable, which may not always be in Ether. As a result, all calculations related to `totalVolumeOfBorrowersAmountinWei` will be incorrect, potentially causing CDS owners to receive more or less than expected. The report recommends deducting `depositedAmountInETH` instead when users withdraw their collateral to fix the issue.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/375 

## Found by 
0x37, 0xAadi, CL001, Cybrid, John44

### Summary

In withdraw, we should deduct `depositedAmountInETH` not `depositedAmount` from the `totalVolumeOfBorrowersAmountinWei`.

### Root Cause

When borrowers withdraw collateral, we will [update `totalVolumeOfBorrowersAmountinWei`](https://github.com/sherlock-audit/2024-11-autonomint/blob/main/Blockchain/Blockchian/contracts/lib/BorrowLib.sol#L920).
The `totalVolumeOfBorrowersAmountinWei` is the total collateral amount in term of Ether. When borrowers withdraw collateral, we should deduct the related amount in Ether from the `totalVolumeOfBorrowersAmountinWei`.

The problem is that we use `depositDetail.depositedAmount`. The `depositDetail.depositedAmount` means this deposit's collateral amount, maybe Ether's amount, or WrsETH amount. This will cause that if this borrower's deposit asset is not Ether, e.g. WrsETH, we will deduct less amount from `totalVolumeOfBorrowersAmountinWei` than expected.

This will cause all calculations related with `totalVolumeOfBorrowersAmountinWei` will be incorrect.
 
```solidity
omniChainData.totalVolumeOfBorrowersAmountinWei -= depositDetail.depositedAmount;
``` 
```solidity
    function deposit(
        IBorrowing.BorrowLibDeposit_Params memory libParams,
        IBorrowing.BorrowDepositParams memory params,
        IBorrowing.Interfaces memory interfaces,
        mapping(IBorrowing.AssetName => address assetAddress) storage assetAddress
    ) public returns (uint256) {
        uint256 depositingAmount = params.depositingAmount;
        ...
        depositDetail.depositedAmount = uint128(depositingAmount);
}
```

### Internal pre-conditions

N/A

### External pre-conditions

N/A

### Attack Path

N/A

### Impact

After borrowers withdraw non-Ether collateral(weETH, wrsETH), the `totalVolumeOfBorrowersAmountinWei` will be incorrect. This will cause all calculations related with `totalVolumeOfBorrowersAmountinWei` will be incorrect.
For example:
cds's cumulativeValue will be calculated incorrectly.
```solidity
        CalculateValueResult memory result = _calculateCumulativeValue(
            omniChainData.totalVolumeOfBorrowersAmountinWei,
            omniChainData.totalCdsDepositedAmount,
            ethPrice // current ether price.
        );
```
CDS owners can get more or less than expected.

### PoC

N/A

### Mitigation

Deduct `depositedAmountInETH` from `totalVolumeOfBorrowersAmountinWei` when users withdraw collateral.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Autonomint Colored Dollar V1 |
| Report Date | N/A |
| Finders | 0xAadi, Cybrid, CL001, John44, 0x37 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/375
- **Contest**: https://app.sherlock.xyz/audits/contests/569

### Keywords for Search

`vulnerability`

