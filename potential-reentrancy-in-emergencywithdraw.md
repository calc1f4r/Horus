---
# Core Classification
protocol: Radiant Riz Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35150
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/radiant-riz-audit
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
  - OpenZeppelin
---

## Vulnerability Title

Potential Reentrancy in emergencyWithdraw

### Overview


The emergencyWithdraw function in the Riz system has a bug that allows users to withdraw multiple times. This is because the check to prevent double withdrawals is placed at the top of the function, but the status of "has withdrawn" is only set at the bottom of the function after assets are transferred. This means that if the asset has a hook on transfer, users can reenter the function and withdraw again. To fix this, the status should be set directly after the check at the top of the function or a non-reentrant modifier should be implemented. Additionally, all tokens in the Riz system should be checked to ensure they do not have hooks on transfer and cannot be upgraded to have them in the future. This bug has been resolved in a recent update to the system.

### Original Finding Content

In the [`emergencyWithdraw` function](https://github.com/radiant-capital/riz/blob/65ca7bb55550d30388e2b2277fefe5686ab7e4e8/src/libraries/EmergencyWithdraw.sol#L31), the [check which prevents double withdrawals](https://github.com/radiant-capital/riz/blob/65ca7bb55550d30388e2b2277fefe5686ab7e4e8/src/libraries/EmergencyWithdraw.sol#L39-L40) is at the top of the function. However, the value representing "has withdrawn" is only set [at the bottom of the function](https://github.com/radiant-capital/riz/blob/65ca7bb55550d30388e2b2277fefe5686ab7e4e8/src/libraries/EmergencyWithdraw.sol#L90), after [the assets are transferred to the user](https://github.com/radiant-capital/riz/blob/65ca7bb55550d30388e2b2277fefe5686ab7e4e8/src/libraries/EmergencyWithdraw.sol#L85-L87). Importantly, since `RizATokens` [are not burned](https://github.com/radiant-capital/riz/blob/65ca7bb55550d30388e2b2277fefe5686ab7e4e8/src/tokenization/RizAToken.sol#L32-L34) at this step, if the underlying asset has a hook on transfer, a user could potentially reenter this function and withdraw again, multiple times.


Consider [setting the user's withdrawn status](https://github.com/radiant-capital/riz/blob/65ca7bb55550d30388e2b2277fefe5686ab7e4e8/src/libraries/EmergencyWithdraw.sol#L90) directly below the [check at the top of the function](https://github.com/radiant-capital/riz/blob/65ca7bb55550d30388e2b2277fefe5686ab7e4e8/src/libraries/EmergencyWithdraw.sol#L39-L41). Alternatively, consider implementing a non\-reentrant modifier onto the `emergencyWithdraw` function. Finally, consider vetting all tokens and ensuring that any tokens added to the Riz system do not have hooks on transfer and cannot be upgraded to have them in the future.


***Update:** Resolved in [pull request \#61](https://github.com/radiant-capital/riz/pull/61) at commit [bd13afe](https://github.com/radiant-capital/riz/pull/61/commits/bd13afe28ec52023536dcfd822469857dbce44d6). The `emergencyWithdraw` function now sets the status on the holder just after checking it.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Radiant Riz Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/radiant-riz-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

