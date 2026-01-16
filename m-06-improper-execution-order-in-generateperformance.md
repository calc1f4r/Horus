---
# Core Classification
protocol: Kinetiq_2025-02-26
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58622
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Kinetiq-security-review_2025-02-26.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-06] Improper execution order in `generatePerformance`

### Overview


The report discusses a bug in the OracleManager software that affects the performance of validators. The problem occurs when the software checks the behavior of a validator and deactivates it if it does not meet expectations. However, the software fails to update the latest slash, reward, and balance amounts before deactivating the validator. This can result in incorrect calculations and withdrawals of HYPE (a type of currency). The report recommends updating the amounts before deactivating the validator to avoid these issues. 

### Original Finding Content


## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

In OracleManager, the operator role will generate validators' performance result periodically. When we get the performance result, we will check the validator's behavior. If this validator's behavior is below expectation, we will deactivate this validator.

The problem is that we will trigger to deactivate the validator directly, missing updating the latest slash/reward/balance amount.

There are some possible impacts:
1. If there are more rewards than slash in the latest period, we will withdraw less HYPE than we expect.
2. If there are more slash than rewards in the latest period, we will withdraw more HYPE than we delegate in the validator. This will cause the un-delegate failure.
3. In StakingManager, we will make use of `slash` and `reward` amount to calculate the exchange ratio. The calculation will be inaccurate.

```solidity
    function generatePerformance() external whenNotPaused onlyRole(OPERATOR_ROLE) returns (bool) {
        if (
            !_checkValidatorBehavior(
                validator, previousSlashing, previousRewards, avgSlashAmount, avgRewardAmount, avgBalance
            )
        ) {
            validatorManager.deactivateValidator(validator);
            continue;
        }

        if (avgSlashAmount > previousSlashing) {
            uint256 newSlashAmount = avgSlashAmount - previousSlashing;
            validatorManager.reportSlashingEvent(validator, newSlashAmount);
        }

        if (avgRewardAmount > previousRewards) {
            uint256 newRewardAmount = avgRewardAmount - previousRewards;
            validatorManager.reportRewardEvent(validator, newRewardAmount);
        }

        validatorManager.updateValidatorPerformance(
            validator, avgBalance, avgUptimeScore, avgSpeedScore, avgIntegrityScore, avgSelfStakeScore
        );
    }
```


## Recommendations

Update the balance/reward/slash to the latest amount, then deactivate this validator.





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Kinetiq_2025-02-26 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Kinetiq-security-review_2025-02-26.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

