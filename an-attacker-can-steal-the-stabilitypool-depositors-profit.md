---
# Core Classification
protocol: Threshold Network
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 30191
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Threshold%20Network/Threshold%20USD/README.md#1-an-attacker-can-steal-the-stabilitypool-depositors-profit
github_link: none

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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

An attacker can steal the StabilityPool depositors profit

### Overview


The report discusses a bug in the liquidation flow of a protocol. The bug allows any user to bypass the protocol's liquidity provision and steal profit from the `StabilityPool` provider by using a flash loan. This can result in a loss of profit for `StabilityPool` providers and may cause the currency to unpeg. The report recommends using a time factor to prevent these attacks.

### Original Finding Content

##### Description
The liquidation flow of the protocol is supposed to be as follows:
- users open troves and join `StabilityPool`
- anyone calls the `liquidateTroves` function that iterates the given troves and liquidates them one by one
- `StabilityPool` depositors move collateral gains to their troves and increase the `StabilityPool` ThUSD balance by getting more ThUSD.

By using a flash loan any user can bypass the provision of liquidity to the protocol for a long time and steal some of the `StabilityPool` provider's profit taking the following steps:
1. Let's wait for liquidation opportunities. The following notions are to be introduced: Lsum is the total liquidatable amount of ThUSD and FLusd is the amount of ThUSD that can be accumulated after depositing flashloaned collateral to the protocol; FLfee is the fees the attacker should pay for opening a trove, SPusd is the total ThUSD amount in `StabilityPool`.
The conditions for an attack are:
 Lsum < SPusd + FLusd
 FLfee < Lsum * FLusd / SPusd
2. An attacker gets a flash loan and swaps the Lsum equivalent of the collateral token to ThUSD.
3. The attacker makes a deposit of all remaining collateral tokens to `StabilityPool`.
4. The attacker calls the [`TroveManager::liquidateTroves`](https://github.com/Threshold-USD/dev/blob/800c6c19e44628dfda3cecaea6eedcb498bf0bf3/packages/contracts/contracts/TroveManager.sol#L464) function to liquidate the troves. If the CR system is lower than 150%, the amount of liqudated troves can be significantly bigger.
5. The attacker calls [`withdrawFromSP`](https://github.com/Threshold-USD/dev/blob/800c6c19e44628dfda3cecaea6eedcb498bf0bf3/packages/contracts/contracts/StabilityPool.sol#L283) then ['withdrawCollateralGainToTrove'](https://github.com/Threshold-USD/dev/blob/800c6c19e44628dfda3cecaea6eedcb498bf0bf3/packages/contracts/contracts/StabilityPool.sol#L310) of `StabilityPool` to move collateral to the attacker's trove. The CR System here has to be more than 150%.
   The attacker's trove here contains the initial collateral and collateral gain.
6. The attacker closes the trove providing the rest of ThUSD plus the Lsum equivalent from step 1.
7. The attacker returns the flash loan.

The attack's impact:
- loss of profit from liquidations by `StabilityPool` providers
- decreased motivation to use the Stability Pool which may cause Threshold USD to unpeg

##### Recommendation
We recommend that you use the time factor to prevent flash loan attacks.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Threshold Network |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Threshold%20Network/Threshold%20USD/README.md#1-an-attacker-can-steal-the-stabilitypool-depositors-profit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

