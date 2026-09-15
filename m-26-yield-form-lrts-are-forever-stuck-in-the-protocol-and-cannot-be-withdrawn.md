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
solodit_id: 45516
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/569
source_link: none
github_link: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/818

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
finders_count: 2
finders:
  - 0x73696d616f
  - Audinarey
---

## Vulnerability Title

M-26: Yield form LRTs are forever stuck in the protocol and cannot be withdrawn

### Overview


This bug report discusses an issue with the Yield form LRTs (Loan Repayment Tokens) in the Autonomint protocol. The yield from these tokens is supposed to be updated and stored in the treasury during borrower liquidation and withdrawal from the CDS (Credit Default Swap). However, the code for this process is flawed and the yield is stuck in the treasury with no way to retrieve it. This could potentially lead to a loss of funds for users. The report suggests implementing a mechanism to withdraw or distribute this yield to mitigate the issue.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/818 

## Found by 
0x73696d616f, Audinarey

### Summary

During borrower [liquidation](https://github.com/sherlock-audit/2024-11-autonomint/blob/main/Blockchain/Blockchian/contracts/Core_logic/borrowLiquidation.sol#L265-L273) (`liquidationType1()`) and [withdrawal from the CDS](https://github.com/sherlock-audit/2024-11-autonomint/blob/main/Blockchain/Blockchian/contracts/lib/CDSLib.sol#L667-L670), the yield from LRTs is updated and stored in the treasury.

### Root Cause



```solidity
File: CDSLib.sol
667:      @>         interfaces.treasury.updateYieldsFromLiquidatedLrts( // @audit SUBMITTED-HIGH: these funds are stuck forever in the treasury
668:                     weETHAmount - ((weETHAmountInETHValue * 1 ether) /  params.weETH_ExchangeRate) + 
669:                     rsETHAmount - ((rsETHAmountInETHValue * 1 ether) /  params.rsETH_ExchangeRate)
670:                 );


File: borrowLiquidation.sol
265:         uint256 yields = depositDetail.depositedAmount - ((depositDetail.depositedAmountInETH * 1 ether) / exchangeRate);
266: 
267:         // Update treasury data
268:         treasury.updateTotalVolumeOfBorrowersAmountinWei(depositDetail.depositedAmountInETH);
269:         treasury.updateTotalVolumeOfBorrowersAmountinUSD(depositDetail.depositedAmountUsdValue);
270:         treasury.updateDepositedCollateralAmountInWei(depositDetail.assetName, depositDetail.depositedAmountInETH);
271:         treasury.updateDepositedCollateralAmountInUsd(depositDetail.assetName, depositDetail.depositedAmountUsdValue);
272:         treasury.updateTotalInterestFromLiquidation(totalInterestFromLiquidation);
273:  @>     treasury.updateYieldsFromLiquidatedLrts(yields); // @audit ??? questionable

```

The problem is that there is no way to for the protocol to retrieve these funds neither is it distributed to users elsewhere

### Internal pre-conditions

_No response_

### External pre-conditions

_No response_

### Attack Path

_No response_

### Impact

Yield form LRTs is stuck in the treasury without a way to withdraw them

### PoC

_No response_

### Mitigation

Consider inplementing a mechanism to withdraw or distribute this yield

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Autonomint Colored Dollar V1 |
| Report Date | N/A |
| Finders | 0x73696d616f, Audinarey |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/818
- **Contest**: https://app.sherlock.xyz/audits/contests/569

### Keywords for Search

`vulnerability`

