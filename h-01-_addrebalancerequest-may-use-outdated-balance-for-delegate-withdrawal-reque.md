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
solodit_id: 58609
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

[H-01] `_AddRebalanceRequest` may use outdated balance for delegate withdrawal request

### Overview


The report highlights a bug in the `ValidatorManager._addRebalanceRequest()` function. This function is responsible for checking a validator's balance and recording a withdrawal request. However, due to the dynamic nature of balance changes, there are two potential problems when the `closeRebalanceRequest()` function is called. Firstly, if the validator's balance decreases after the request is made, the withdrawal may fail. Secondly, if the balance increases, some funds may remain in the validator's account. This is especially concerning during emergency withdrawals or when deactivating a validator, as the manager needs to retrieve all funds. To fix this bug, the report recommends implementing two solutions: 1) ensuring that the `closeRebalanceRequest()` function checks the validator's balance to reflect the most up-to-date amount before processing the withdrawal request, and 2) adding a mechanism to `closeRebalanceRequest()` so that the manager can withdraw all available funds at the moment in the validator's balance.

### Original Finding Content


## Severity

**Impact:** High

**Likelihood:** Medium

## Description

`ValidatorManager._addRebalanceRequest()` checks validator's balance and records a withdrawal request:

```solidity
    function _addRebalanceRequest(address validator, uint256 withdrawalAmount) internal {
        require(!_validatorsWithPendingRebalance.contains(validator), "Validator has pending rebalance");
        require(withdrawalAmount > 0, "Invalid withdrawal amount");

        (bool exists, uint256 index) = _validatorIndexes.tryGet(validator);
        require(exists, "Validator does not exist");
        require(_validators[index].balance >= withdrawalAmount, "Insufficient balance");

        validatorRebalanceRequests[validator] = RebalanceRequest({validator: validator, amount: withdrawalAmount});
        _validatorsWithPendingRebalance.add(validator);

        emit RebalanceRequestAdded(validator, withdrawalAmount);
    }
```
However, a validator’s balance can change at any time due to rewards or slashing. This creates two potential problems when manager calls `closeRebalanceRequest()`:
1. Balance Decreases: If the validator’s balance decreases after the request is made, the delegation removal or withdrawal will fail.
2. Balance Increases: If the balance increases, some funds may remain in the validator’s account.

This is especially critical during emergency withdrawals or when deactivating a validator, as the manager needs to retrieve all funds.

## Recommendations

1. Ensure that the `closeRebalanceRequest()` function checks the validator’s balance to reflect the most up-to-date amount before processing the withdrawal request.
2. Add a mechanism to `closeRebalanceRequest()` so that manager can withdraw all available funds at the moment in validator balance





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

