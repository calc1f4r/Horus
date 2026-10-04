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
solodit_id: 45473
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/569
source_link: none
github_link: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/775

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
finders_count: 3
finders:
  - 0x73696d616f
  - santiellena
  - 0x37
---

## Vulnerability Title

H-20: `borrowing::liquidate()` sends the wrong liquidation index to the destination chain, overwritting liquidation information and getting collateral stuck

### Overview


Issue H-20: `borrowing::liquidate()` sends the wrong liquidation index when sending information to another chain. This causes liquidation information to be overwritten and can lead to collaterals being stuck. The wrong variable is being used in the code, which results in the incorrect index being sent. This can happen when multiple liquidations occur on different chains. The impact of this bug is that collaterals can become stuck and cannot be withdrawn. To fix this, the correct index should be passed when sending information to another chain.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/775 

## Found by 
0x37, 0x73696d616f, santiellena

### Summary

`borrowing::liquidate()` sends the `noOfLiquidations` variable as liquidation index to the other chain. However, liquidations are tracked in `omniChainData.noOfLiquidations`, on both chains. For example, if a liquidation happens on chain A, it increases to 1 and sends this information to chain B. If a liquidation happens on chain B, it will have index 2, not 1. 

### Root Cause

In `borrowing:402`, the wrong variable is sent as liquidation index to the other chain.

### Internal pre-conditions

None.

### External pre-conditions

None.

### Attack Path

1. Liquidation happens on chain A, incrementing `omniChainData.noOfLiquidations` to 1 and `noOfLiquidations` to 1 also.
2. Liquidation happens on chain B, [with index 2](https://github.com/sherlock-audit/2024-11-autonomint/blob/main/Blockchain/Blockchian/contracts/Core_logic/borrowLiquidation.sol#L199) (it received the omnichain data from chain A and then incremented it). In chain B, it sends the liquidation info to chain A, but sends with index 1, not 2, as it uses the local  `noOfLiquidations` to send the index.
3. Chain A will have liquidation info with index 1 overiwritten by the liquidation of chain B, leading to stuck collateral of the first liquidation in chain A (as long as depositors have not withdraw, but if they have, they can't withdraw the second liquidation anyway).

### Impact

Stuck collateral.

### PoC

See above.

### Mitigation

Pass in the correct index, given by `omnichainData.noOfLiquidations`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Autonomint Colored Dollar V1 |
| Report Date | N/A |
| Finders | 0x73696d616f, santiellena, 0x37 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/775
- **Contest**: https://app.sherlock.xyz/audits/contests/569

### Keywords for Search

`vulnerability`

