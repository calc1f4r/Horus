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
solodit_id: 45526
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/569
source_link: none
github_link: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/1007

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
  - valuevalk
  - Audinarey
  - John44
  - pashap9990
---

## Vulnerability Title

M-36: wrong amount of `sUSD` is used to open a short position in synthetix

### Overview


The bug report describes an issue with the synthetix platform, where the wrong amount of sUSD is used to open a short position. This was discovered by a group of users and the problem lies in the code that calculates the margin for the short position. The code is using the amount of ETH used in the transaction to mint sETH and then exchanged to sUSD, instead of the actual amount of sUSD received. This can lead to unpredictable results and even a denial of service attack. The report suggests considering using the correct amount of sUSD received after exchanging sETH to sUSD as a solution. 

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/1007 

## Found by 
Audinarey, John44, pashap9990, valuevalk

### Summary

per [OP `sUSD](https://optimistic.etherscan.io/token/0x8c6f28f2f1a3c87f0f938b96d27520d9751ec8d9#readContract) contract, the `sUSD` has 18 decimals

In the `liquidationType2()` the `amount` variable is the amount of ETH used in the transaction to mint sETH and then exchanged to `sUSD`


```solidity
File: borrowLiquidation.sol
349:         // Exchange sETH with sUSD
350:         synthetix.exchange( 
351:             0x7345544800000000000000000000000000000000000000000000000000000000,
352:             amount,
353:             0x7355534400000000000000000000000000000000000000000000000000000000
354:         );
355: 
356:         // Calculate the margin
357:         int256 margin = int256((amount * currentEthPrice) / 100);
358:         // Transfer the margin to synthetix
359:         synthetixPerpsV2.transferMargin(margin);
360: 
361:         // Submit an offchain delayed order in synthetix for short position with 1X leverage
362:         synthetixPerpsV2.submitOffchainDelayedOrder(
363:             -int((uint(margin * 1 ether * 1e16) / currentEthPrice)), 
364:             currentEthPrice * 1e16
365:         );

```
The problem is that, the [`margin`](https://github.com/sherlock-audit/2024-11-autonomint/blob/main/Blockchain/Blockchian/contracts/Core_logic/borrowLiquidation.sol#L357-L359) is suppose to be evaluated using the `sUSD` amount not the value of the amount of the original ETH asset.

### Root Cause

_No response_

### Internal pre-conditions

_No response_

### External pre-conditions

_No response_

### Attack Path

_No response_

### Impact

This can lead to unpredictable results during the liquidation including a DOS since the evaluated margin may be more that the actual amount od `sUSD` exchanged previously

### PoC

_No response_

### Mitigation

Consider using the amount of `sUSD` received after exchanging sETH to `sUSD`

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Autonomint Colored Dollar V1 |
| Report Date | N/A |
| Finders | valuevalk, Audinarey, John44, pashap9990 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/1007
- **Contest**: https://app.sherlock.xyz/audits/contests/569

### Keywords for Search

`vulnerability`

