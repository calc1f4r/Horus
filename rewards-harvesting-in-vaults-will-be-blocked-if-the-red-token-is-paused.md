---
# Core Classification
protocol: Infrared Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49857
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Infrared-Spearbit-Security-Review-January-2025.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Infrared-Spearbit-Security-Review-January-2025.pdf
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
  - 0xRajeev
  - Chinmay Farkya
  - Cryptara
  - Noah Marconi
---

## Vulnerability Title

Rewards harvesting in vaults will be blocked if the RED token is paused

### Overview


This bug report is about a medium risk bug found in the RewardsLib.sol code. The bug affects the Infrared vaults and their ability to harvest rewards from BGT emissions. The issue occurs when the RED token is paused, which can block the harvest calls and prevent new rewards from being claimed. This bug has a high impact as it prevents the harvesting of new rewards, but it has a low likelihood of occurring since the RED token is only paused in rare situations. The recommendation is to either use a try/catch approach or modify the _update() function to exclude mint operations. The bug has been fixed in PR 378 and reviewed by Spearbit.

### Original Finding Content

## Severity: Medium Risk

## Context
RewardsLib.sol#L176-L180

## Summary
All Infrared vaults have a mechanism to harvest rewards from BGT emissions whenever someone tries to claim their rewards, or can be called directly from the Infrared contract. However, these harvest calls will be blocked if the RED token is ever paused.

## Finding Description
The reward claim process calls `RED.mint()` in the `harvestVault()` function. The flow is:
- `getRewardForUser()`
- `onReward()`
- `harvestVault()`
- `RED.mint()`

Whenever there are new BGT rewards (which means some BGT emissions have accrued and claimed from Bera reward vaults), the `harvestVault()` function tries to mint a proportional amount of RED tokens. However, token transfers (including mints, burns, etc.) can be paused on the RED token. If the RED mint fails, the reward harvesting calls will revert.

## Impact Explanation
High, because this will make all `getRewardForUser()` calls revert, preventing the harvesting of new rewards.

## Likelihood Explanation
Low, because this will only happen if the RED token is paused, which is expected to occur in very rare situations.

## Recommendation
Either adopt a try/catch approach when minting RED tokens during `harvestVault()`, or exclude mint operations by modifying the `_update()` function in `ERC20PresetMinterPauser.sol`.

## Infrared
Fixed in PR 378.

## Spearbit
Reviewed that PR 378 resolves the issue as recommended by using a try/catch block.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Infrared Contracts |
| Report Date | N/A |
| Finders | 0xRajeev, Chinmay Farkya, Cryptara, Noah Marconi |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Infrared-Spearbit-Security-Review-January-2025.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Infrared-Spearbit-Security-Review-January-2025.pdf

### Keywords for Search

`vulnerability`

