---
# Core Classification
protocol: Stader Labs
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20185
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-06-stader
source_link: https://code4rena.com/reports/2023-06-stader
github_link: https://github.com/code-423n4/2022-06-stader-findings/issues/84

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
  - rvierdiiev
---

## Vulnerability Title

[M-12] `ValidatorWithdrawalVault.settleFunds` doesn't check amount that user has inside `NodeELRewardVault` to pay for penalty

### Overview


The bug report describes an issue with the `ValidatorWithdrawalVault.settleFunds` function, which is called when a validator withdraws from the beacon chain. This function calculates the amount that a validator has earned for attestations as a validator, and only considers the balance of this contract. The function also fetches the penalty amount, which consists of 3 points: `_mevTheftPenalty`, `_missedAttestationPenalty` and `_missedAttestationPenalty`. If the penalty amount is greater than the validator's earning on `ValidatorWithdrawalVault`, the SD collateral is slashed.

The bug report explains that the `NodeELRewardVault` balance should also be checked in order to find out how many earnings a validator has and these should be counted when applying the penalty. This is because all attestation payments come to `ValidatorWithdrawalVault`, while `mev`/`block` proposal funds are coming to `SocializingPool` or `NodeELRewardVault`. 

This bug report was acknowledged by manoj9april (Stader) who said that rewards are treated separately between CL and EL and they will take this suggestion into account for future upgrades. Picodes (judge) commented that this should be kept as medium severity as it shows how an operator could be slashed, despite having earned more than the penalty if we combine EL and CL rewards, which could lead to a loss of funds.

The recommended mitigation step is to calculate the operator's rewards inside `NodeELRewardVault` when accruing `_mevTheftPenalty` inside `ValidatorWithdrawalVault`.

### Original Finding Content


`ValidatorWithdrawalVault.settleFunds` doesn't check amount that user has inside `NodeELRewardVault` to pay for penalty. That value can increase operator's earned amount, which can avoid slashing.

### Proof of Concept

When a validator withdraws from beacon chain the `ValidatorWithdrawalVault.settleFunds` function is called. This function calculates amount that a validator [has earned](https://github.com/code-423n4/2023-06-stader/blob/main/contracts/ValidatorWithdrawalVault.sol#L62) for attestations as a validator. So only the balance of this contract [is considered](https://github.com/code-423n4/2023-06-stader/blob/main/contracts/ValidatorWithdrawalVault.sol#L99).

The function [fetches penalty amount](https://github.com/code-423n4/2023-06-stader/blob/main/contracts/ValidatorWithdrawalVault.sol#L64). This penalty amount contains [of 3 points](https://github.com/code-423n4/2023-06-stader/blob/main/contracts/Penalty.sol#L111): `_mevTheftPenalty`, `_missedAttestationPenalty` and `_missedAttestationPenalty`.

In this case, if the penalty amount is bigger than the validator's earning on `ValidatorWithdrawalVault`, the [SD collateral is slashed](https://github.com/code-423n4/2023-06-stader/blob/main/contracts/ValidatorWithdrawalVault.sol#L66-L69).

Now, we need to understand how validator receives funds in this system. All attestation payments come to `ValidatorWithdrawalVault`, while `mev`/`block` proposal funds are coming to `SocializingPool` or `NodeELRewardVault` (depends on user's choice). So actually, `_missedAttestationPenalty` is responding to `ValidatorWithdrawalVault` earning, while `_mevTheftPenalty` is responding to `NodeELRewardVault` earnings.

That means, `NodeELRewardVault` balance should also be checked in order to find out how many earnings a validator has and they should be also counted when applying the penalty.

Simple example:
1. A validator wants to exit.
2. An operator earning is 0.1 eth inside `ValidatorWithdrawalVault`.
3. The accrued penalty is 0.11, which means the user will be slashed.
4. The operator also has `NodeELRewardVault` where their operator's reward is 0.05 eth.
5. As result, the user has enough balance to cover penalty, but they were still penalized.

### Tools Used

VsCode

### Recommended Mitigation Steps

As you accrue `_mevTheftPenalty` inside `ValidatorWithdrawalVault`, you also should calculate the operator's rewards inside `NodeELRewardVault`.

### Assessed type

Error

**[manoj9april (Stader) acknowledged and commented](https://github.com/code-423n4/2022-06-stader-findings/issues/84#issuecomment-1596567203):**
 > Rewards are treated separately between CL and EL. We will take this suggestion into account for next upgrades.

**[Picodes (judge) commented](https://github.com/code-423n4/2022-06-stader-findings/issues/84#issuecomment-1616855027):**
 > Keeping medium severity as this report shows how an operator could be slashed, despite having earned more than the penalty if we combine EL and CL rewards, which could lead to a loss of funds.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Stader Labs |
| Report Date | N/A |
| Finders | rvierdiiev |

### Source Links

- **Source**: https://code4rena.com/reports/2023-06-stader
- **GitHub**: https://github.com/code-423n4/2022-06-stader-findings/issues/84
- **Contest**: https://code4rena.com/reports/2023-06-stader

### Keywords for Search

`vulnerability`

