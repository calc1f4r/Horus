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
solodit_id: 58612
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

[H-04] `ReportSlashingEvent` reverts if outdated balance is below slashing amount

### Overview


The report discusses a bug in the code where the function `OracleManager::generatePerformance` is supposed to update the stats of every validator and their total balance. However, if there are any rewards or slashing amounts, the code will revert if the new slashing amount is greater than the validator’s previously reported balance. This can easily happen due to the intervals between updates and can lead to errors in the first few days after a validator is activated. The recommendation is to implement a mechanism for handling slashing amounts similar to how rewards are handled or compare the new slashing amount with the validator’s actual up-to-date balance.

### Original Finding Content


## Severity

**Impact:** High

**Likelihood:** Medium

## Description

`OracleManager::generatePerformance` is supposed to be called once every hour (or at any other interval specified by `MIN_UPDATE_INTERVAL`). It updates the stats of every validator and also updates the `totalBalance`. If there are any rewards or slashing amounts, they are supposed to be accounted for and `ValidatorManager` should be updated accordingly.
```solidity
    function generatePerformance() external whenNotPaused onlyRole(OPERATOR_ROLE) returns (bool) {
        // ..

        // Update validators with averaged values
        for (uint256 i = 0; i < validatorCount; i++) {
            // ...

            // Handle slashing
            if (avgSlashAmount > previousSlashing) {
                uint256 newSlashAmount = avgSlashAmount - previousSlashing;
@>                validatorManager.reportSlashingEvent(validator, newSlashAmount);
            }

            // ...
        }

        // ...

        return true;
    }
```
As we can see, if the accumulated slashing amount for this particular validator has increased, `reportSlashingEvent` will be triggered with the increase passed as a parameter.
```solidity
    function reportSlashingEvent(address validator, uint256 amount)
       // ...
    {
        require(amount > 0, "Invalid slash amount");

        Validator storage val = _validators[_validatorIndexes.get(validator)];
@>        require(val.balance >= amount, "Insufficient stake for slashing");

        // Update balances
        unchecked {
            // These operations cannot overflow:
            // - val.balance >= amount (checked above)
            // - totalBalance >= val.balance (invariant maintained by the contract)
            val.balance -= amount;
            totalBalance -= amount;
        }

       // ...
    }
```
As shown in the highlighted section, the entire `reportSlashingEvent` (and therefore `generatePerformance` as well) will revert if the new slashing amount is greater than the validator’s previously reported balance. However, this is actually a very likely scenario and could easily happen due to the intervals between updates.

For example, at time `T`, the validator’s balance could be `100`. At `T + 1 hour`, the validator’s balance could grow to `500`, and the `slashingAmount` could be `110`. Due to this bug, the code will require `oldBalance > newSlashingAmount`, which would revert since `slashingAmount` is `110` and `oldBalance` is only `100`. Situations like this are especially likely to occur in the first few days after a validator is activated.

## Recommendations

Consider implementing a mechanism for handling slashing amounts similar to how rewards are handled, or compare the new slashing amount with the validator’s actual up to-date-balance.





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

