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
solodit_id: 45508
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/569
source_link: none
github_link: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/740

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
finders_count: 7
finders:
  - Audinarey
  - yoooo
  - 0xe4669da
  - santiellena
  - 0xNirix
---

## Vulnerability Title

M-18: Unbounded Liquidation Iterations Can Lead to Withdrawal DoS

### Overview


This bug report is about a problem in the Autonomint protocol that can cause users to be unable to withdraw their funds. The issue is caused by the protocol requiring users to go through all liquidation events since their initial deposit when they want to withdraw. This can lead to high gas costs and eventually exceed the block gas limit, preventing early depositors from withdrawing their funds. This bug was found by several people and can have a significant impact on users who opted for liquidation. Currently, there is no solution proposed to mitigate this issue.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/740 

## Found by 
0xNirix, 0xTamayo, 0xe4669da, Audinarey, santiellena, valuevalk, yoooo

### Summary

The protocol's requiring users to iterate through all liquidation events since their deposit during withdrawal will cause eventual transaction failure for early depositors as the number of liquidations grows over time, preventing them from withdrawing their funds.


### Root Cause

In `CDSLib.withdrawUser()` at https://github.com/sherlock-audit/2024-11-autonomint/blob/main/Blockchain/Blockchian/contracts/lib/CDSLib.sol#L640 the forced iteration through all historical liquidations between deposit and withdrawal time creates potential for unbounded gas costs:

```solidity
// In CDSLib.withdrawUser:
if (params.cdsDepositDetails.optedLiquidation) {
    for (uint128 i = (liquidationIndexAtDeposit + 1); i <= params.omniChainData.noOfLiquidations; i++) {
        uint128 liquidationAmount = params.cdsDepositDetails.liquidationAmount;
        if (liquidationAmount > 0) {
            CDSInterface.LiquidationInfo memory liquidationData = omniChainCDSLiqIndexToInfo[i];
            // Calculate share for each liquidation
            uint128 share = (liquidationAmount * 1e10) / uint128(liquidationData.availableLiquidationAmount);
            // Process liquidation share...
        }
    }
}
```

### Internal pre-conditions

_No response_

### External pre-conditions

_No response_

### Attack Path

1. Early user deposits with liquidation enabled (`liquidationIndexAtDeposit = currentLiquidations`)
2. Protocol operates normally over months/years
3. Many liquidations occur, incrementing `noOfLiquidations`
4. When early user attempts to withdraw:
   - Must process EVERY liquidation since their deposit
   - Gas costs grow linearly with number of liquidations
   - Eventually exceeds block gas limit

### Impact

Early CDS depositors who opted for liquidation will be unable to withdraw their funds once the number of liquidations grows too large, as their withdrawal transactions will exceed block gas limits

### PoC

_No response_

### Mitigation

_No response_

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Autonomint Colored Dollar V1 |
| Report Date | N/A |
| Finders | Audinarey, yoooo, 0xe4669da, santiellena, 0xNirix, valuevalk, 0xTamayo |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/740
- **Contest**: https://app.sherlock.xyz/audits/contests/569

### Keywords for Search

`vulnerability`

