---
# Core Classification
protocol: Hyperstable_2025-03-19
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57828
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Hyperstable-security-review_2025-03-19.md
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

[M-04] Persistent inflation from uninitialized rates

### Overview


The report states that there is a bug in the `PositionManager.setInterestRateStrategy()` function that allows the protocol owner to update the interest rate strategy contract. However, this operation does not include a way to migrate or initialize the internal state required by the new strategy. This leads to incorrect interest rate calculations due to missing or zero-initialized parameters. The function is controlled by the owner and should only be used in exceptional circumstances. The recommendation is to initialize the new strategy with the current state of each vault or properly migrate relevant parameters from the previous strategy to ensure accuracy.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Low

## Description

The `PositionManager.setInterestRateStrategy()` function enables the protocol owner to update the interest rate strategy contract. However, this operation does not include any mechanism to migrate or initialize the internal state required by the new strategy. Parameters such as `targetUtilization`, `endRateAt`, and `lastUpdate` for each vault remain uninitialized in the new strategy, which leads to inaccurate and inflated interest rate calculations.

```solidity
function setInterestRateStrategy(address _newInterestRateStrategy) external onlyOwner {
    if (_newInterestRateStrategy == address(0)) {
        revert ZeroAddress();
    }

    emit NewInterestRateStrategy(address(interestRateStrategy), address(_newInterestRateStrategy));

    interestRateStrategy = IInterestRateStrategy(_newInterestRateStrategy);
}
```

The interest rate calculation function, `interestRate()`, relies on vault-specific parameters to compute a smooth and adaptive rate curve based on the difference between current utilization and the target utilization. If these parameters are missing or zero-initialized, the function calculates a large error (`err`), resulting in excessive linear adaptation and an artificially high interest rate.

However, this function is strictly controlled by the owner and is expected to be used only in exceptional circumstances.

## Recommendation

The new `interestRateStrategy` contract should either be initialized with the current state of each vault or properly migrate relevant parameters from the previous strategy to ensure accuracy and consistency in interest rate calculations.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Hyperstable_2025-03-19 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Hyperstable-security-review_2025-03-19.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

