---
# Core Classification
protocol: Kinetiq LST
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58597
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Kinetiq-Spearbit-Security-Review-March-2025.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Kinetiq-Spearbit-Security-Review-March-2025.pdf
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
  - Rvierdiiev
  - Slowfi
  - Hyh
  - Optimum
---

## Vulnerability Title

Sentinel can block core operations for any validator chosen due to missing input control in re-

### Overview


The bug report is about a problem in the code of `questEmergencyWithdrawal()` function in the `ValidatorManager.sol` file. This function is used to withdraw funds from a validator. The bug allows someone with a specific role to block the withdrawal process permanently. This can be done by calling a specific function with a fake contract and a specific amount of money. This will cause the withdrawal process to fail and prevent the removal of the validator from the system. The bug has been fixed in a recent update.

### Original Finding Content

## questEmergencyWithdrawal()

**Severity:** Medium Risk  
**Context:** `ValidatorManager.sol#L326-L342`  

**Description:**  
The `generatePerformance(targetValidator)`, `reactivateValidator(targetValidator)`, `requestEmergencyWithdrawal(..., targetValidator,...)`, and `rebalanceWithdrawal(..., [..., targetValidator, ...], ...)` operations for any `targetValidator` chosen can be blocked permanently by any sentinel. 

For that end, a holder of `SENTINEL_ROLE` can call `requestEmergencyWithdrawal(fakeStakingManager, targetValidator, amount)` with `amount > 0` when `block.timestamp >= lastEmergencyTime + EMERGENCY_COOLDOWN`. In this instance, `fakeStakingManager` is a tailor-made contract such that `IStakingManager(fakeStakingManager).processValidatorWithdrawals(validators, amounts)` is a noop, while `IStakingManager(fakeStakingManager).processValidatorRedelegation(...)` reverts. The latter will make `closeRebalanceRequests(fakeStakingManager, ...)` also revert permanently, making the removal of `targetValidator` from `_validatorsWithPendingRebalance` impossible due to the `request.staking == stakingManager` control.

### Relevant Code Fragment:
```solidity
function closeRebalanceRequests(address stakingManager, address[] calldata validators)
    external
    whenNotPaused
    nonReentrant
    onlyRole(MANAGER_ROLE)
{
    // ...
    uint256 totalAmount = 0;
    for (uint256 i = 0; i < validators.length;) {
        address validator = validators[i];
        require(_validatorsWithPendingRebalance.contains(validator), "No pending request");
        // Add amount to total for redelegation
        RebalanceRequest memory request = validatorRebalanceRequests[validator];
        require(request.staking == stakingManager, "Invalid staking manager for rebalance"); // @audit if `request.staking` is hoax, !
        totalAmount += request.amount;
        // Clear the rebalance request
        delete validatorRebalanceRequests[validator];
        _validatorsWithPendingRebalance.remove(validator);
        emit RebalanceRequestClosed(validator, request.amount);
        unchecked {
            ++i;
        }
    }
    // Trigger redelegation through StakingManager if there's an amount to delegate
    if (totalAmount > 0) {
        IStakingManager(stakingManager).processValidatorRedelegation(totalAmount); // @audit then `closeRebalanceRequests()` can be blocked, !
    }
}
```

Then, `generatePerformance(targetValidator)` will fail due to the `L204 !validatorManager.hasPendingRebalance(targetValidator)` check, as `validatorManager.hasPendingRebalance(targetValidator) == _validatorsWithPendingRebalance.contains(validator) == true`. The `reactivateValidator(targetValidator)` will fail due to the `!_validatorsWithPendingRebalance.contains(validator)` `L206` check. 

The calls to `requestEmergencyWithdrawal(..., targetValidator,...)` and `rebalanceWithdrawal(..., [..., targetValidator, ...], ...)` will fail due to `_addRebalanceRequest(...)` reverting on the same `!_validatorsWithPendingRebalance.contains(validator)` check.

**Recommendation:**  
Consider adding a stakingManager whitelist as an input control in `requestEmergencyWithdrawal()`.

**Kinetiq:** Fixed in PR 11.  
**Cantina Managed:** Fix verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Kinetiq LST |
| Report Date | N/A |
| Finders | Rvierdiiev, Slowfi, Hyh, Optimum |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Kinetiq-Spearbit-Security-Review-March-2025.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Kinetiq-Spearbit-Security-Review-March-2025.pdf

### Keywords for Search

`vulnerability`

