---
# Core Classification
protocol: Vaultka
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37444
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-06-Vaultka.md
github_link: none

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
  - Zokyo
---

## Vulnerability Title

Method `requestWithdrawal` can fail if GMX reverts the txn

### Overview


This bug report is about a medium severity issue in the Contract GlmRouter.sol. The issue has been resolved, but it is important for beginners to understand what happened. 

The method `requestWithdrawal(...)` in the contract checks if the `glmAmount` being withdrawn is greater than `allPoolSplitingBps`. If it is, then tokens are withdrawn from all GM pools based on the current weight ratio. However, there is a scenario where all assets are in only one pool or one of the pools has a weight of 0, meaning no assets are deposited in that pool. In this case, the amount to withdraw from GMX for that pool will be 0, but the contract does not check for this. 

This can cause a problem when creating GMX transactions and sending them with fees, as the transaction will be reverted due to the amount being 0. This can result in the withdrawal transaction being reverted for users. 

To avoid this issue, it is recommended to add a check to ensure that the amount withdrawn from any pool is not 0. This will prevent the transaction from being reverted and ensure a smooth withdrawal process for users.

### Original Finding Content

**Severity**: Medium

**Status**: Resolved

**Description**

In Contract GlmRouter.sol, the method `requestWithdrawal(...)` checks if the `glmAmount` being withdrawn is > `allPoolSplitingBps`. If that is the case, then tokens are withdrawn from all GM pools based on the current weight ratio.

There could be a scenario where all of the assets are in only BTC/ETH pool or at least one of the market pools has a current weight of 0 i.e. no assets deposited for that GM pool.

In that case, the amount to withdraw from GMX for that GM pool will be 0 as well. But the contract doesn’t validate it.
```solidity
for (uint i = 0; i < poolLength; i++) {
               uint256 amount = ((manager.getCurrentWeight(i, totalAssets) * _glmAmount)) / DECIMAL_PRECISION; //if it is the last pool, withdraw the remaining glm amount
               if (i == poolLength - 1) {
                   keys[i] = _processWithdrawal(remainingGlmAmount, manager.getGmTokenAddress(i), glmPrice);                } else {
                   keys[i] = _processWithdrawal(amount, manager.getGmTokenAddress(i), glmPrice);
                   remainingGlmAmount -= amount;
               }
           }
```

It creates the GMX transactions and sends it along with the fee and this txn will be reverted as the amount is 0.

This will lead to the withdrawal txn being reverted for users.

**Recommendation**: 

Consider adding a check to ensure that the GLM amount withdrawn for any pool is not 0.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Vaultka |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-06-Vaultka.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

