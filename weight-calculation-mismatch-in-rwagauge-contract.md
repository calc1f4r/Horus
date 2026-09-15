---
# Core Classification
protocol: Core Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57257
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj
source_link: none
github_link: https://github.com/Cyfrin/2025-02-raac

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - drlaravel
---

## Vulnerability Title

Weight Calculation Mismatch in RWAGauge Contract

### Overview

See description below for full details.

### Original Finding Content

## &#x20;

&#x20;

## Summary

The `RWAGauge` contract's `getTotalWeight()` function incorrectly returns the total staked token supply instead of the time-weighted boosted weight of the staked tokens. This leads to inaccurate reward distribution, as users with higher boosts are under-rewarded while those with lower boosts are over-rewarded. A proposed fix involves implementing a new function, `calculateTotalBoostedWeight()`, to accurately calculate the total weight based on individual user balances and their respective boost factors.

## Vulnerability Details

The `getTotalWeight()` function, as currently implemented, simply returns `totalSupply()`. This value represents the total number of staked tokens, but doesn't account for any boosting mechanisms applied to individual user's balances. In a gauge where boosting (e.g., based on staking duration or some other metric) is present, this directly translates to a misrepresentation of users' actual voting power and reward entitlement.

Specifically, users who have actively worked towards earning a larger boost to their weight are not properly rewarded for their contribution. This also means rewards will likely be given to parties that have less voting weight than they should.

The issue is compounded by the contract's reliance on this incorrect weight calculation for reward distribution. The proportion of rewards a user receives is directly related to their weight relative to the total weight. Therefore, the flawed `getTotalWeight()` function leads to incorrect allocation of rewards.

## Impact

The primary impact of this vulnerability is the **incorrect distribution of rewards** within the RWAGauge system.

* **Under-rewarding of High-Boost Users:** Users with high boosts (e.g., User A in the example) receive fewer rewards than they should, based on their time-weighted stake. This is because their boost is not considered in `getTotalWeight()`.
* **Over-rewarding of Low-Boost Users:** Conversely, users with low or no boosts (e.g., User B in the example) receive more rewards than they should.
* **Inaccurate Governance/Voting:** The gauge is likely used as a voting system where users vote on yield direction. Since `getTotalWeight` is incorrect, the voting power of the users is also incorrect.
* **Discouragement of Desired Behavior:** Users are discouraged from engaging in activities that earn them a boost, as the benefit of the boost is not reflected in the reward distribution.
* **Loss of Trust:** Users may lose confidence in the fairness and accuracy of the reward distribution mechanism, potentially leading to reduced participation.
* **Economic Disadvantage:** Users will be earning lower yields than they should, which may discourage them from staking in the RWAGauge.

## Tools Used

* **Manual Code Review:** The vulnerability was identified through a manual review of the `RWAGauge` contract's source code.
* **Static Analysis (Informal):** An informal static analysis was performed to trace the usage of `getTotalWeight()` and identify its impact on reward distribution.

## Recommendations

1. **Implement** **`calculateTotalBoostedWeight()`:** Implement the function to calculate total boosted weight that takes into account user balances and their respective boost factors. This is in line with the suggested fix:

   ```Solidity
   function getTotalWeight() external view override returns (uint256) {
       return calculateTotalBoostedWeight(); // New function
   }

   function calculateTotalBoostedWeight() public view returns (uint256) {
       uint256 totalBoostedWeight = 0;
       // Iterate through all stakers to calculate their boosted weight
       for (uint256 i = 0; i < stakers.length; i++) {
           address staker = stakers[i];
           uint256 balance = balanceOf(staker);
           uint256 boost = getUserBoost(staker); // Implement this.  This is an example and should be adjusted to the actual boost logic.
           totalBoostedWeight += balance * boost;
       }
       return totalBoostedWeight;
   }

   // Example - Implementation depends on the actual boost logic
   function getUserBoost(address _user) public view returns (uint256) {
       // Placeholder. Needs to be implemented based on the actual boosting mechanism.
       // This example provides a static boost for all addresses.
       // NOTE:  Adjust the boost calculation as necessary (e.g., based on staking duration, token holdings, etc.)
       return 1e18; // Example boost (1x boost)
   }


   ```

   **Note:** The implementation of `getUserBoost()` will depend on the actual boosting logic within the gauge. It should retrieve the boost factor associated with the provided user. The `stakers` array should contain all addresses that have ever staked in the contract. This array should be populated when a user first stakes in the contract.
2. **Update Reward Distribution Logic:** Ensure that the reward distribution logic uses the `calculateTotalBoostedWeight()` function to determine the correct reward allocation for each user.
3. **Audit Contract:** Conduct a formal security audit of the corrected code to identify and address any further potential vulnerabilities.
4. **Test Thoroughly:** Develop comprehensive unit and integration tests to verify the correctness of the `calculateTotalBoostedWeight()` function and the reward distribution logic under various scenarios, including different boost levels.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Core Contracts |
| Report Date | N/A |
| Finders | drlaravel |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2025-02-raac
- **Contest**: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj

### Keywords for Search

`vulnerability`

