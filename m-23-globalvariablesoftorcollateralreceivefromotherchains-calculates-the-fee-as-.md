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
solodit_id: 45513
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/569
source_link: none
github_link: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/795

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

M-23: `GlobalVariables::oftOrCollateralReceiveFromOtherChains()` calculates the fee as if it was the same in both chains, which is false

### Overview


The bug report is about an issue with a function called `GlobalVariables::oftOrCollateralReceiveFromOtherChains()`. This function is used to transfer tokens or Ethereum from one blockchain to another. However, there is a problem with how the fee for this transfer is calculated. The function calculates the fee as if the transfer is going from the current blockchain to the destination blockchain, when in reality it is the opposite. This can result in either overcharging or reverts when the transfer is made. The root cause of this issue is that the fee is calculated based on the wrong direction. This bug can cause problems with transferring tokens or Ethereum between blockchains. There is no known way to prevent this issue, but the report suggests adding a variable to track the costs as a possible solution.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/795 

## Found by 
0x73696d616f

### Summary

`GlobalVariables::oftOrCollateralReceiveFromOtherChains()` send a message to the other chain requesting token/eth transfers to the current chain. In the process, it forwards ETH to pay for the cross chain transfer from the destination to the current chain. However, it calculates the fee as if the direction was current to destination, when in reality it is the opposite and the fee will be different. Thus, it will either overchage or revert in the destination chain.

### Root Cause

In `GlobalVariables::oftOrCollateralReceiveFromOtherChains()` fee is calculated as if the [direction](https://github.com/sherlock-audit/2024-11-autonomint/blob/main/Blockchain/Blockchian/contracts/Core_logic/GlobalVariables.sol#L250) is current to destination, when it is the opposite.

### Internal pre-conditions

None.

### External pre-conditions

None.

### Attack Path

1. `GlobalVariables::oftOrCollateralReceiveFromOtherChains()` is called, but the fee is incorrectly calculated.

### Impact

Overcharging of the fee or charging too little, which will lead to reverts on the destination chain.

### PoC

See links.

### Mitigation

Add a variable admin set to track the costs.

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
- **GitHub**: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/795
- **Contest**: https://app.sherlock.xyz/audits/contests/569

### Keywords for Search

`vulnerability`

