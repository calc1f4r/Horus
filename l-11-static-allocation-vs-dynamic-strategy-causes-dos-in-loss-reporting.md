---
# Core Classification
protocol: Elytra_2025-07-27
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63589
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Elytra-security-review_2025-07-27.md
github_link: none

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
  - Pashov Audit Group
---

## Vulnerability Title

[L-11] Static allocation vs dynamic strategy causes DoS in loss reporting

### Overview

See description below for full details.

### Original Finding Content


_Resolved_

The `reportStrategyLoss()` function validates slashing amounts against statically tracked allocations (`assetStrategyAllocations`) rather than real-time strategy balances, causing complete denial of service when strategies earn rewards before slashing events occur. This validation logic prevents legitimate slashing losses from being reported, leading to permanent accounting corruption and potential protocol insolvency.

The core issue stems from Elytra's dual tracking system: TVL calculations correctly use real-time strategy balances (fixing H-04 from the previous audit), but slashing validation still relies on stale static allocation tracking. When strategies generate yield, their real balances grow beyond the originally tracked allocation amounts, making any significant slashing event impossible to report.

```solidity
function reportStrategyLoss(address asset, address strategy, uint256 amount) external onlyElytraAdmin {
    // Validates against stale static tracking
    if (assetStrategyAllocations[asset][strategy] < amount) revert LossExceedsStrategyAllocation();
    
    // Updates only static tracking, creating further discrepancies
    assetsAllocatedToStrategies[asset] -= amount;
    assetStrategyAllocations[asset][strategy] -= amount;
}
```

This creates a fundamental mismatch where slashing calculations are performed against real-time balances (as they should be), but validation uses outdated static allocations. The protocol includes a manual `syncStrategyAllocations()` function to reconcile discrepancies, but this creates a fragile two-step process that fails under emergency conditions.

**Vulnerable Scenario:**
The following steps demonstrate how normal protocol operations lead to a complete slashing reporting breakdown:

1. **Initial Allocation**: Protocol allocates 100 ETH to Strategy A, tracked as `assetStrategyAllocations[WETH][StrategyA] = 100 ETH`.

2. **Strategy Growth**: Over 6 months, Strategy A earns 25% yield through normal restaking rewards, reaching 125 ETH real balance while tracked allocation remains 100 ETH.

3. **Slashing Event**: Validator experiences 20% slashing (realistic scenario), resulting in 20 ETH loss that needs to be reported.

4. **DoS Trigger**: Admin attempts `reportStrategyLoss(WETH, StrategyA, 20)` but transaction reverts because `20 ETH > 0 ETH` (20 ETH loss amount exceeds the 0 ETH growth margin between 125 ETH real balance and 100 ETH tracked allocation).

5. **Protocol Breakdown**: Slashing cannot be reported, internal accounting remains incorrect, users can withdraw at inflated rates based on pre-slash accounting, leading to potential insolvency.

6. **Emergency Complexity**: Under slashing event pressure, admin must remember to call `syncStrategyAllocations()` first, then `reportStrategyLoss()`, creating operational risk and human error potential.

This scenario becomes highly likely with even conservative parameters: 15% strategy growth over 3-6 months combined with 15-20% slashing events, both of which are realistic in liquid restaking environments.

**Recommendations**

Implement the following solution to eliminate the static validation dependency:

Modify `reportStrategyLoss()` to validate against the current strategy balance rather than stale allocations:
```solidity
function reportStrategyLoss(address asset, address strategy, uint256 amount) external onlyElytraAdmin {
    uint256 realTimeBalance = IElytraStrategy(strategy).getBalance(asset);
    require(amount <= realTimeBalance, "Loss exceeds current strategy balance");
    // Process loss reporting
}
```





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Elytra_2025-07-27 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Elytra-security-review_2025-07-27.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

