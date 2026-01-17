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
solodit_id: 40722
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
finders_count: 2
finders:
  - neumo
  - gmhacker
---

## Vulnerability Title

While ‘particlePositionManager contract is paused, positions could go liquidatable 

### Overview


The ParticlePositionManager contract has a bug where certain functions, such as closing positions and adding premium, can still be called while the contract is paused. This could result in some borrowers having their positions liquidated unfairly. The recommendation is to add a storage variable to set a grace period before the contract is unpaused, allowing borrowers to handle their positions before they become liquidatable. The bug has been fixed by removing the pausable pattern and using a server side signature instead.

### Original Finding Content

## Context
(No context files were provided by the reviewer)

## Description
The `Contract ParticlePositionManager` uses the modifier `whenNotPaused` from the inherited contract `PausableUpgradeable` to disallow calling certain functions if the contract is paused. The following functions, among others, use this modifier:

- `closePosition(DataStruct.ClosePositionParams calldata params)`
- `addPremium(DataStruct.AddPremiumParams calldata params)`

This way, borrowers with open positions for which the LP owner has called `reclaimLiquidity` and started the three-day period could see the period end before the contract is unpaused, making their positions liquidatable without having had the chance of closing their positions. Additionally, positions could become liquidatable while the contract is paused due to insufficient premium, and the borrower will not be able to add premium before it's unpaused. 

This would make the moment the contract is unpaused an unfair moment for some borrowers, who would see their positions liquidated.

## Recommendation
I'm unsure whether it's a good idea to allow closing positions or adding premium while the contract is paused. One possibility would be to add a storage variable to set when the contract is unpaused to give time to borrowers to handle their positions before they are liquidatable. Something like this:

```solidity
uint64 public minLiquidationTimestamp;
uint64 constant LIQUIDATION_UNPAUSE_GRACE_PERIOD = 6 hours;
// ...
function unpause() public onlyOwner {
    minLiquidationTimestamp = block.timestamp + LIQUIDATION_UNPAUSE_GRACE_PERIOD;
    _unpause();
}
// ...
function liquidatePosition(
    DataStruct.ClosePositionParams calldata params,
    address borrower
) external override nonReentrant whenNotPaused {
    require(block.timestamp >= minLiquidationTimestamp);
    // ...
}
```

## Particle
Fixed. We don't use the pausable pattern anymore (instead we use server-side signature).

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Particle |
| Report Date | N/A |
| Finders | neumo, gmhacker |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_particle_feb2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/83468b34-954f-4650-b16d-7d72c5477780

### Keywords for Search

`vulnerability`

