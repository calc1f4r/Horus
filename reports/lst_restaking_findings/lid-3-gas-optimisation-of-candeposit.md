---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53474
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-04-14-Lido.md
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
  - Hexens
---

## Vulnerability Title

[LID-3] Gas optimisation of canDeposit

### Overview

See description below for full details.

### Original Finding Content

**Severity:** Low

**Path:** DepositSecurityModule.sol:canDeposit, Lido.sol:canDeposit#L385-L395, #L672-L674

**Description:**

The function `canDeposit` in both contracts checks whether it is currently allowed to deposit to the deposit contract. Both checks contain conditionals over multiple variables, including external calls. However, the conditional elements are not ordered by cost or likelihood, so the cost of the functions increases as an early-exit does not improve the cost.

For example, if the first element in a conditional with multiple AND’s, then Solidity will early-exit by returning `false` and the other elements won't be evaluated, saving a lot of gas if those are external calls. The same applies to multiple OR's with `true`.
```
function canDeposit(uint256 stakingModuleId) external view validStakingModuleId(stakingModuleId) returns (bool) {
    bool isModuleActive = STAKING_ROUTER.getStakingModuleIsActive(stakingModuleId);
    uint256 lastDepositBlock = STAKING_ROUTER.getStakingModuleLastDepositBlock(stakingModuleId);
    bool isLidoCanDeposit = LIDO.canDeposit();
    return (
        isModuleActive
        && quorum > 0
        && block.number - lastDepositBlock >= minDepositBlockDistance
        && isLidoCanDeposit
    );
}
```
```
function canDeposit() public view returns (bool) {
    return !IWithdrawalQueue(getLidoLocator().withdrawalQueue()).isBunkerModeActive() && !isStopped();
}
```

**Remediation:**  For `DepositSecurityModule.sol:canDeposit` we would recommend to move the external calls into the conditional of the return statement, instead of first saving it in variables. 

Then these conditionals should be ordered, such that cheaper elements or elements that are more likely to return false are put first, i.e. external calls should always be last.

For example:
```
function canDeposit(uint256 stakingModuleId) external view validStakingModuleId(stakingModuleId) returns (bool) {
    return (
        quorum > 0
        && STAKING_ROUTER.getStakingModuleIsActive(stakingModuleId)
        && block.number - STAKING_ROUTER.getStakingModuleLastDepositBlock(stakingModuleId) >= minDepositBlockDistance
        && LIDO.canDeposit()
    );
}
```
```
function canDeposit() public view returns (bool) {
    return !isStopped() && !IWithdrawalQueue(getLidoLocator().withdrawalQueue()).isBunkerModeActive();
}
```

**Status:**  Acknowledged

- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Hexens |
| Protocol | Lido |
| Report Date | N/A |
| Finders | Hexens |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-04-14-Lido.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

