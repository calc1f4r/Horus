---
# Core Classification
protocol: Ion Protocol Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32714
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/ion-protocol-audit
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
  - OpenZeppelin
---

## Vulnerability Title

Inconsistency When Accruing Interest for a Single ILK vs. All ILKs

### Overview


The `IonPool` contract has two internal functions for accruing interest: `_accrueInterestForIlk` for a single collateral type and `_accrueInterest` for all collateral types. These functions update the `supplyFactor` which tracks interest accrued on the underlying token. However, there is a bug where accruing interest for a single collateral type and then accruing interest for another collateral type in the future does not accurately reflect the changes in interest. This can result in an incorrect interest rate being applied to users' debt positions. The suggested solution is to accrue interest for all collateral types each time there is an action made on any of the collateral types. The bug has been resolved in a recent update.

### Original Finding Content

The `IonPool` contract contains two internal functions for accruing interest: the [`_accrueInterestForIlk` function](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/IonPool.sol#L413) for accruing interest for a single collateral type, and the [`_accrueInterest` function](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/IonPool.sol#L368) for accruing interest for all collateral types. Both of these functions update the [`supplyFactor`](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/reward/RewardModule.sol#L72) which is used for tracking interest accrued on the underlying token.


The `supplyFactor` is used by the `balanceOf` and `totalSupply` functions in the `RewardModule` contract for converting from normalized balance to the true balances. Both the `_accrueInterestForIlk` and the `_accrueInterest` functions pass the current `totalSupply` to the `_calculateRewardAndDebtDistribution` function to determine the respective changes to the `supplyFactor`, the total debt, and the new interest rate for debt positions.


`_accrueInterestForIlk` only accumulates interest for a single collateral type. As such, the changes to the `supplyFactor`, the total debt, and the new interest rate will take into consideration only the accrued interest, for that collateral type, since the last time interest was accrued. When interest is accrued for another collateral type in the future, either with `_accrueInterestForIlk` or `_accrueInterest`, the `supplyFactor`, and thus the `totalSupply` will reflect changes since the last time the first collateral type was updated, but will be applied since the last time the second collateral type was updated.


As a result, accruing interest for a single collateral type, followed by accruing interest for another collateral type in the future is not equivalent to accruing interest for all collateral types each time interest is accrued. This will result in an inaccurate interest rate being applied to users' debt positions.


Consider accruing interest for all collateral types each time there is an action made on any of the collateral types that should result in interest accrual.


***Update:** Resolved in [pull request #27](https://github.com/Ion-Protocol/ion-protocol/pull/27).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Ion Protocol Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/ion-protocol-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

