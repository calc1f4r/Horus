---
# Core Classification
protocol: Particle
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40725
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/83468b34-954f-4650-b16d-7d72c5477780
source_link: https://cdn.cantina.xyz/reports/cantina_competition_particle_feb2024.pdf
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
  - Sujith Somraaj
---

## Vulnerability Title

Premature liquidation in liquidateposition() due to improper isliquidatable validation 

### Overview


The bug report is about a function called liquidatePosition() in a file called ParticlePositionManager.sol. This function is used to liquidate an open position under two conditions: if the premium is not enough and if the cutoff time exceeds the loan term. However, there is a bug in the code that causes premature liquidation even if the premium is enough. This is because the function checks for liquidation before deducting the liquidation fee, resulting in an incorrect check. The recommendation is to move the liquidation check before deducting the fee and then deduct the fee if the premium is not enough. The bug has been fixed by correcting the logic.

### Original Finding Content

## Liquidation Logic Issue in ParticlePositionManager.sol

## Context
`ParticlePositionManager.sol#L358`

## Description
The function `liquidatePosition()` in `ParticlePositionManager.sol` is used to liquidate an open position under two conditions: firstly, if the premium is not enough and secondly, if the cutoff time exceeds the loan term.

### isLiquidatable Function
```solidity
function isLiquidatable() {
    // ...
    return
        (tokenFromPremium < tokenFromOwed || tokenToPremium < tokenToOwed) ||
        (cutoffTime > 0 && cutoffTime + LOAN_TERM < block.timestamp);
}
```

However, during the liquidation process, `tokenFromPremium` includes the liquidation fee, resulting in premature liquidation even if `tokenFromPremium` is equal to or greater than `tokenFromOwed`.

### LiquidatePosition Function
```solidity
function liquidatePosition() {
    // ...
    closeCache.tokenFromPremium -= liquidateCache.liquidationRewardFrom;
    closeCache.tokenToPremium -= liquidateCache.liquidationRewardTo;
    if (!isLiquidatable(
        closeCache.tokenFromPremium,
        closeCache.tokenToPremium,
        liquidateCache.tokenFromOwed,
        liquidateCache.tokenToOwed,
        lien.tokenId
    )) {
        revert Errors.LiquidationNotMet();
    }
}
```

### Example Scenario
An example scenario would be as follows: if the user has a premium of 100 USDC and the liquidation reward is 2 USDC, whereas the token owed is 100 USDC, liquidation shouldn't be allowed since the user has enough premium. However, due to the incorrect check, the user will get liquidated.

## Recommendation
Move the `isLiquidatable` check before the adjustment of `liquidationReward`, and then deduct the reward if the premium is not enough.

### Updated LiquidatePosition Function
```solidity
function liquidatePosition() {
    // ...
    - closeCache.tokenFromPremium -= liquidateCache.liquidationRewardFrom;
    - closeCache.tokenToPremium -= liquidateCache.liquidationRewardTo;
    if (!isLiquidatable(
        closeCache.tokenFromPremium,
        closeCache.tokenToPremium,
        liquidateCache.tokenFromOwed,
        liquidateCache.tokenToOwed,
        lien.tokenId
    )) {
        revert Errors.LiquidationNotMet();
    }
    + closeCache.tokenFromPremium -= liquidateCache.liquidationRewardFrom;
    + closeCache.tokenToPremium -= liquidateCache.liquidationRewardTo;
    // ...
}
```

## Particle
Fixed. Corrected the logic.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Particle |
| Report Date | N/A |
| Finders | Sujith Somraaj |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_particle_feb2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/83468b34-954f-4650-b16d-7d72c5477780

### Keywords for Search

`vulnerability`

