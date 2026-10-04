---
# Core Classification
protocol: Kinetiq LST
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58601
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Kinetiq-Spearbit-Security-Review-March-2025.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Kinetiq-Spearbit-Security-Review-March-2025.pdf
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
finders_count: 4
finders:
  - Rvierdiiev
  - Slowfi
  - Hyh
  - Optimum
---

## Vulnerability Title

Lack of liquidity inside StakingManager

### Overview


This bug report is about a medium risk issue in the StakingAccountant.sol contract. The problem is that the exchange rate of kHYPE is calculated based on the total amounts of all StakingManagers in the system, but there is no way to move liquidity between them. This could lead to a lack of liquidity for users trying to withdraw funds from a StakingManager. The recommendation is to ensure and document that institutional usage of the protocol takes place via a separate instance, so all the StakingManagers and ValidatorManager belong to the same party and can manage liquidity effectively. The issue has been acknowledged by the Kinetiq and Cantina Managed teams.

### Original Finding Content

## Medium Risk Report

### Severity
Medium Risk

### Context
StakingAccountant.sol#L142-L147

### Description
The exchange rate of kHYPE is calculated based on the total amounts of all StakingManagers in the system.

```solidity
uint256 rewardsAmount = validatorManager.totalRewards();
uint256 slashingAmount = validatorManager.totalSlashing();
uint256 totalHYPE = totalStaked + rewardsAmount - totalClaimed - slashingAmount; // <<<
// Calculate ratio with 18 decimals precision
return Math.mulDiv(totalHYPE, 1e18, kHYPESupply);
```

Those StakingManager contracts may delegate funds to different validators. Since there is no way to move liquidity between the StakingManagers, there could be a lack of liquidity in case users want to exit StakingManager, as they may not have enough funds on their validator's balance.

To explain the problem, an example is given:
- Suppose that StakingManager1 staked 100 Hype to validator1 and earned 5 Hype in rewards, but StakingManager2 staked 100 Hype to validator2 and earned 15 Hype as rewards. Thus, according to the exchange ratio formula, both StakingManagers should have 110 Hype to withdraw, but StakingManager1 won't be able to withdraw 110 from the validator as it has only 105 on the balance of validator1. In case the stakers of StakingManager1 want to withdraw all funds, there would be a shortage of 5 Hype.
- The protocol team stated that this liquidity should be withdrawn from StakingManager2 and staked to StakingManager1 by any user or protocol admin. While this is indeed possible, if StakingManager2 is created for an institution, it won't be possible to simply interact with it, as it has a whitelist enabled that limits actors who can participate.

### Recommendation
Consider ensuring and documenting that institutional usage of the protocol takes place via a separate instance of it, so all the StakingManagers' `MANAGER_ROLE` and ValidatorManager's `MANAGER_ROLE` belong to the same party, the institution, who was instructed to maintain enough stakes in each StakingManager, monitor the liquidity, and perform the necessary rebalancing between StakingManagers.

### Kinetiq
Acknowledged.

### Cantina Managed
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Kinetiq LST |
| Report Date | N/A |
| Finders | Rvierdiiev, Slowfi, Hyh, Optimum |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Kinetiq-Spearbit-Security-Review-March-2025.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Kinetiq-Spearbit-Security-Review-March-2025.pdf

### Keywords for Search

`vulnerability`

