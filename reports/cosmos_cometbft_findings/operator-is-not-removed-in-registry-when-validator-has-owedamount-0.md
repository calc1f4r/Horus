---
# Core Classification
protocol: Casimir
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35002
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md
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
finders_count: 2
finders:
  - Hans
  - 0kage
---

## Vulnerability Title

Operator is not removed in Registry when validator has `owedAmount == 0`

### Overview


The `CasimirManager::withdrawValidator()` function is not working properly as it does not update the states of other operators when a validator is fully withdrawn. This means that the collateral for the withdrawn validator will remain locked in the contract and cannot be withdrawn by the operator. To fix this, the function `registry.removeOperatorValidator()` should also be called with a `recoverAmount` of 0 when the owed amount is 0. This bug has been fixed in the latest version of Casimir.

### Original Finding Content

**Description:** `CasimirManager::withdrawValidator()` function is designed to remove a validator after a full withdrawal. It checks whether the final effective balance of the removed validator is sufficient to cover the initial 32 ETH deposit. If for some reason such as slashing, the final effective balance is less than 32 ETH, the operators must recover the missing portion by calling `registry.removeOperatorValidator()`.


```solidity
uint256 owedAmount = VALIDATOR_CAPACITY - finalEffectiveBalance;
if (owedAmount > 0) {
    uint256 availableCollateral = registry.collateralUnit() * 4;
    owedAmount = owedAmount > availableCollateral ? availableCollateral : owedAmount;
    uint256 recoverAmount = owedAmount / 4;
    for (uint256 i; i < validator.operatorIds.length; i++) {
        // @audit if owedAmount == 0, this function is not called
        registry.removeOperatorValidator(validator.operatorIds[i], validatorId, recoverAmount);
    }
}
```

However, the `removeOperatorValidator()` function also has the responsibility to update other operators' states, such as `operator.validatorCount`. If this function is only called when `owedAmount > 0`, the states of these operators will not be updated if the validator fully returns 32 ETH.

**Impact:** The `operator.validatorCount` will not decrease in the `CasimirRegistry` when a validator is removed. As a result, the operator cannot withdraw the collateral for this validator, and the collateral will remain locked in the `CasimirRegistry` contract.

**Recommended Mitigation:** The function `registry.removeOperatorValidator()` should also be called  with `recoverAmount = 0` when `owedAmount == 0`. This will free up collateral for operators.

**Casimir:**
Fixed in [d7b35fc](https://github.com/casimirlabs/casimir-contracts/commit/d7b35fce9925bfa2133fd4e16ae11e483ab4daa4)

**Cyfrin:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Casimir |
| Report Date | N/A |
| Finders | Hans, 0kage |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

