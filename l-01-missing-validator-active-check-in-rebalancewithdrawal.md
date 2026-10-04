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
solodit_id: 58623
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Kinetiq-security-review_2025-02-26.md
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

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

[L-01] Missing validator active check in `rebalanceWithdrawal()`

### Overview

See description below for full details.

### Original Finding Content


In `ValidatorManager` contract:
`rebalanceWithdrawal()` does not check if a validator is active before processing withdrawals, while `requestEmergencyWithdrawal()` does.
```solidity
    function rebalanceWithdrawal(
        address stakingManager,
        address[] calldata validators,
        uint256[] calldata withdrawalAmounts
    ) external whenNotPaused nonReentrant onlyRole(MANAGER_ROLE) {
        require(validators.length == withdrawalAmounts.length, "Length mismatch");
        require(validators.length > 0, "Empty arrays");

        for (uint256 i = 0; i < validators.length;) {
            require(validators[i] != address(0), "Invalid validator address");

            // Add rebalance request (this will check for duplicates)
            _addRebalanceRequest(validators[i], withdrawalAmounts[i]);

            unchecked {
                ++i;
            }
        }

        // Trigger withdrawals through StakingManager
        IStakingManager(stakingManager).processValidatorWithdrawals(validators, withdrawalAmounts);
    }
```
```solidity
    function requestEmergencyWithdrawal(address stakingManager, address validator, uint256 amount)
        external
        onlyRole(SENTINEL_ROLE)
        whenNotPaused
    {
        require(block.timestamp >= lastEmergencyTime + EMERGENCY_COOLDOWN, "Cooldown period");
        require(amount > 0, "Invalid amount");

        if (emergencyWithdrawalLimit > 0) {
            require(amount <= emergencyWithdrawalLimit, "Exceeds emergency limit");
        }

        (bool exists, uint256 index) = _validatorIndexes.tryGet(validator);
        require(exists, "Validator does not exist");

        Validator storage validatorData = _validators[index];
@>      require(validatorData.active, "Validator not active");

```





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
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

