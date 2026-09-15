---
# Core Classification
protocol: Ethos Reserve
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43381
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-02-ethos
source_link: https://code4rena.com/reports/2023-02-ethos
github_link: https://github.com/code-423n4/2023-02-ethos-findings/issues/481

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

protocol_categories:
  - liquid_staking
  - cdp
  - yield
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - 0xBeirao
  - bin2chen
---

## Vulnerability Title

[H-01] Re-balancing the vault allocation may always revert when distributing profits: resulting of a massive system DOS

### Overview


There is a bug in the code that calculates rewards for staked units in the Ethos-Core contract. This can lead to a negative value being assigned to an unsigned integer, causing the program to crash. This bug can also cause a denial-of-service attack if the profit is greater than a certain threshold. The bug can be fixed by skipping the calculation if the value to be assigned is 0. The bug has been confirmed by the Ethos Reserve.

### Original Finding Content


**[updateRewardSum](https://github.com/code-423n4/2023-02-ethos/blob/73687f32b934c9d697b97745356cdf8a1f264955/Ethos-Core/contracts/StabilityPool.sol#L486-L500)** function call **[\_computeRewardsPerUnitStaked](https://github.com/code-423n4/2023-02-ethos/blob/73687f32b934c9d697b97745356cdf8a1f264955/Ethos-Core/contracts/StabilityPool.sol#L493)** with **\_debtToOffset** set to 0. Meaning that the assignment [L531](https://github.com/code-423n4/2023-02-ethos/blob/73687f32b934c9d697b97745356cdf8a1f264955/Ethos-Core/contracts/StabilityPool.sol#L531) will revert if `lastLUSDLossError_Offset != 0` (which is likely the case) because we try to assign a negative value to an **uint**.

### Impact

**[\_rebalance()](https://github.com/code-423n4/2023-02-ethos/blob/73687f32b934c9d697b97745356cdf8a1f264955/Ethos-Core/contracts/ActivePool.sol#L239)** will be definitely DOS if the profit is greater than the **[yieldClainThreshold](https://github.com/code-423n4/2023-02-ethos/blob/73687f32b934c9d697b97745356cdf8a1f264955/Ethos-Core/contracts/ActivePool.sol#L252)** ⇒ **[vars.profit != 0](https://github.com/code-423n4/2023-02-ethos/blob/73687f32b934c9d697b97745356cdf8a1f264955/Ethos-Core/contracts/ActivePool.sol#L286)**.

Because they call **\_rebalance()** all these functions will be DOS :

In `BorrowerOperations` 100% DOS
- openTrove
- closeTrove
- \_adjustTrove
- addColl, withdrawColl
- withdrawLUSD, repayLUSD

In `TroveManager` 80% DOS
- liquidateTroves
- batchLiquidateTroves
- redeemCloseTrove

### Proof of Concept

Context : the vault has compound enough profit to withdraw. ([here](https://github.com/code-423n4/2023-02-ethos/blob/73687f32b934c9d697b97745356cdf8a1f264955/Ethos-Core/contracts/ActivePool.sol#L252))

Alice initiates a trove liquidation. **[offset()](https://github.com/code-423n4/2023-02-ethos/blob/73687f32b934c9d697b97745356cdf8a1f264955/Ethos-Core/contracts/StabilityPool.sol#L466)** in `StabilityPool` is called to cancels out the trove debt against the LUSD contained in the Stability Pool.

A floor division errors occur so now **[lastLUSDLossError_Offset](https://github.com/code-423n4/2023-02-ethos/blob/73687f32b934c9d697b97745356cdf8a1f264955/Ethos-Core/contracts/StabilityPool.sol#L537)** is not null.

Now, every time **[\_rebalance()](https://github.com/code-423n4/2023-02-ethos/blob/73687f32b934c9d697b97745356cdf8a1f264955/Ethos-Core/contracts/ActivePool.sol#L305)** is called the transaction will revert.

### Recommended Mitigation

In [StabilityPool.sol#L504-L544](https://github.com/code-423n4/2023-02-ethos/blob/73687f32b934c9d697b97745356cdf8a1f264955/Ethos-Core/contracts/StabilityPool.sol#L504-L544), just skip the floor division errors calculation if `_debtToOffset == 0`

```solidity
if(_debtToOffset != 0){
	[StabilityPool.sol#L526-L538](https://github.com/code-423n4/2023-02-ethos/blob/73687f32b934c9d697b97745356cdf8a1f264955/Ethos-Core/contracts/StabilityPool.sol#L526-L538)
}
```

**[tess3rac7 (Ethos Reserve) confirmed](https://github.com/code-423n4/2023-02-ethos-findings/issues/481#issuecomment-1516723296)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Ethos Reserve |
| Report Date | N/A |
| Finders | 0xBeirao, bin2chen |

### Source Links

- **Source**: https://code4rena.com/reports/2023-02-ethos
- **GitHub**: https://github.com/code-423n4/2023-02-ethos-findings/issues/481
- **Contest**: https://code4rena.com/reports/2023-02-ethos

### Keywords for Search

`vulnerability`

