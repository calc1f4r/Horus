---
# Core Classification
protocol: Sushi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19611
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/sushi/bentobox-strategies-staking-contract/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/sushi/bentobox-strategies-staking-contract/review.pdf
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

protocol_categories:
  - dexes
  - cdp
  - yield
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

Unstaking stkAave Extends Cooldown Time

### Overview


A bug has been reported with the Aave Lending Pool on mainnet when depositing tokens such as USDC. When stkAave tokens are rewarded to the depositors, staking stkAave should allow relevant parties to unstake and receive AAVE tokens as a result. This is done by calling the _harvestRewards function twice. The first time when the stakerCooldowns is at 0 and needs to be set to the relevant block timestamp, and the second time to unstake and redeem relevant rewards.

However, the conditions for unstaking are difficult to satisfy due to Aave's specific logic, triggered during incentiveController.claimRewards() which updates the stakerCooldown through STAKE_TOKEN.stake(). This internal logic can then set the stakerCooldown to a value that will not meet the requirements of unstaking. Each time rewards are claimed, the stakerCooldown is increased proportionally to the amount of new rewards, making it take longer before the rewards can be claimed and redeemed.

The testing team recommends moving incentiveController.claimRewards() to only occur outside of the claim window in order to fix this bug.

### Original Finding Content

## Description

When depositing tokens like USDC into Aave Lending Pool on mainnet, stkAave tokens are rewarded to the depositors. Staking stkAave should allow relevant parties to unstake and receive AAVE tokens as a result. This behaviour requires the `harvestRewards` function to be called twice:

- The first time when `stakerCooldowns` is at 0 and needs to be set to the relevant block timestamp.
- The second time to unstake and redeem relevant rewards.

The conditions for unstaking (i.e. `cooldown + COOLDOWN_SECONDS < block.timestamp` and `block.timestamp < cooldown + COOLDOWN_SECONDS + UNSTAKE_WINDOW`) are difficult to satisfy. This is as a result of Aave’s specific logic, triggered during `incentiveController.claimRewards()`, which updates the `stakerCooldown` through `STAKE_TOKEN.stake()`. Internal logic can then set the `stakerCooldown` to a value that will not meet the requirements of unstaking.

Each time rewards are claimed, the `stakerCooldown` is increased proportionally to the amount of new rewards. Therefore, it will take longer before the rewards can be claimed and redeemed.

## Recommendations

The testing team recommends moving `incentiveController.claimRewards()` to only occur outside of the claim window.

```solidity
if (cooldown == 0) {
    incentiveController.claimRewards(rewardTokens, type(uint256).max, address(this));
    stkAave.cooldown();
} else if (cooldown + COOLDOWN_SECONDS < block.timestamp) {
    if (block.timestamp < cooldown + COOLDOWN_SECONDS + UNSTAKE_WINDOW) {
        // We claim any AAVE rewards we have from staking AAVE.
        stkAave.claimRewards(address(this), type(uint256).max);
        // We unstake stkAAVE and receive AAVE tokens.
        // Our cooldown timestamp resets to 0.
        stkAave.redeem(address(this), type(uint256).max);
    } else {
        incentiveController.claimRewards(rewardTokens, type(uint256).max, address(this));
        // We missed the unstake window - we have to reset the cooldown timestamp.
        stkAave.cooldown();
    }
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Sushi |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/sushi/bentobox-strategies-staking-contract/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/sushi/bentobox-strategies-staking-contract/review.pdf

### Keywords for Search

`vulnerability`

