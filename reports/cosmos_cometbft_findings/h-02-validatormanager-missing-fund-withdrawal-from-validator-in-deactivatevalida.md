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
solodit_id: 58610
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Kinetiq-security-review_2025-02-26.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[H-02] ValidatorManager: missing fund withdrawal from validator in `deactivatevalidator` function

### Overview


This bug report discusses an issue with a function called `deactivateValidator()` in the StakingManager contract. This function is used to stop a validator from participating in the network. However, the function currently has a bug that prevents it from withdrawing funds from the validator's account. This means that funds will be stuck in the validator's account, causing problems for the network. To fix this issue, the report recommends adding a line of code to withdraw funds from the validator's account.

### Original Finding Content


## Severity

**Impact:** Medium

**Likelihood:** High

## Description
`StakingManager.deactivateValidator()` creates a withdrawal request but does not undelegate/withdraw funds from validator by calling `processValidatorWithdrawals()`:
```solidity
    function deactivateValidator(address validator) external whenNotPaused nonReentrant validatorExists(validator) {
        // Oracle manager will also call this, so limit the msg.sender to both MANAGER_ROLE and ORACLE_ROLE
        require(hasRole(MANAGER_ROLE, msg.sender) || hasRole(ORACLE_ROLE, msg.sender), "Not authorized");

        (bool exists, uint256 index) = _validatorIndexes.tryGet(validator);
        require(exists, "Validator does not exist");

        Validator storage validatorData = _validators[index];
        require(validatorData.active, "Validator already inactive");

        // Create withdrawal request before state changes
        if (validatorData.balance > 0) {
            _addRebalanceRequest(validator, validatorData.balance);
        }

        // Update state after withdrawal request
        validatorData.active = false;

        emit ValidatorDeactivated(validator);
    }
```
Because of this issue, funds will stuck in the validator’s account:
1. Manager call to `closeRebalanceRequests()` to remove the rebalance request will revert because there is not enough balance in staking manager.
2. Manager call to `rebalanceWithdrawal()` will revert because the validator is added to the pending list.
3. Sentinel call to `requestEmergencyWithdrawal()` will revert too for the same reason

## Recommendations
In `deactivateValidator()` function, withdraw funds from validator by calling: 
```IStakingManager(stakingManager).processValidatorWithdrawals();```





### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

