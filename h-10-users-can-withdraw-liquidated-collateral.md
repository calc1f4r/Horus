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
solodit_id: 45463
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/569
source_link: none
github_link: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/696

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
finders_count: 7
finders:
  - volodya
  - wellbyt3
  - santiellena
  - 0x37
  - t.aksoy
---

## Vulnerability Title

H-10: Users can withdraw liquidated collateral

### Overview


This bug report discusses an issue with the Autonomint protocol that allows users who have been liquidated to still withdraw their collateral and repay their debt. This is problematic because the collateral has already been sent to Synthetix, and the withdrawn collateral may be taken from the deposits of other borrowers. The root cause of this issue is that the necessary state changes are not performed in a specific type of liquidation. This can have a negative impact on the protocol and its users. To mitigate this issue, the appropriate state changes should be made when this type of liquidation is called.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/696 

## Found by 
0x37, John44, santiellena, t.aksoy, valuevalk, volodya, wellbyt3

### Summary

If a user gets liquidated through `liquidationType2` they will still be able to withdraw their collateral and repay their debt as `depositDetail.liquidated` is not set to true. This is problematic as the collateral will have already been sent to Synthethix, and the collateral that the liquidated user withdraws will most likely be taken from the collateral of other users.

Furthermore, the necessary liquidation state changes performed in `liquidationType1` are omitted in the second type:
https://github.com/sherlock-audit/2024-11-autonomint/blob/0d324e04d4c0ca306e1ae4d4c65f0cb9d681751b/Blockchain/Blockchian/contracts/Core_logic/borrowLiquidation.sol#L241-L277

This is problematic as numerous parts of the protocol are reliant on this values, for example the CDS cumulative value which determines the profits/losses of CDS depositors.

### Root Cause

In borrowLiquidation.liquidationType2 `depositDetail.liquidated` is not set to true.
https://github.com/sherlock-audit/2024-11-autonomint/blob/0d324e04d4c0ca306e1ae4d4c65f0cb9d681751b/Blockchain/Blockchian/contracts/Core_logic/borrowLiquidation.sol#L324-L366

### Internal pre-conditions

_No response_

### External pre-conditions

_No response_

### Attack Path

1. A user gets liquidated through `liquidationType2` and their collateral gets transferred to Synthetix.
2. Even though they have been liquidated they can still withdraw their collateral as no state changes have been made to their deposit.

### Impact

Liquidated users can withdraw their collateral. If that occurs the withdrawn collateral will be taken from the deposits of other borrowers.

### PoC

_No response_

### Mitigation

Perform the appropriate state changes when `liquidationType2` gets called.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Autonomint Colored Dollar V1 |
| Report Date | N/A |
| Finders | volodya, wellbyt3, santiellena, 0x37, t.aksoy, valuevalk, John44 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/696
- **Contest**: https://app.sherlock.xyz/audits/contests/569

### Keywords for Search

`vulnerability`

