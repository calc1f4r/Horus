---
# Core Classification
protocol: StakeDAO_2025-07-21
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63600
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/StakeDAO-security-review_2025-07-21.md
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

[M-01] `StrategyWrapper.depositAssets()` reverts due to missing approval

### Overview


This bug report is about an issue with the `StrategyWrapper.depositAssets()` function. This function is supposed to deposit LP tokens into a reward vault and wrap the received shares. However, it does not properly approve the reward vault to transfer the tokens, causing the deposit to fail. This means that users cannot use this function and must instead deposit the tokens directly into the reward vault and call the `depositShares()` function. The recommended solution is to add a line of code to force approve the reward vault before the deposit. 

### Original Finding Content


_Resolved_

## Severity

**Impact:** Low

**Likelihood:** High

## Description

`StrategyWrapper.depositAssets()` deposits the underlying LP tokens received by the user into the reward vault and wraps the received shares.

However, before the deposit, the function does not approve the reward vault to transfer the underlying LP tokens from the wrapper contract, causing the deposit to revert.

As a result, the `depositAssets()` function cannot be used, and users are forced to deposit the underlying LP tokens directly into the reward vault and call the `depositShares()` function instead.

## Recommendations

```diff
        SafeERC20.safeTransferFrom(IERC20(REWARD_VAULT.asset()), msg.sender, address(this), amount);
+       SafeERC20.forceApprove(IERC20(REWARD_VAULT.asset()), address(REWARD_VAULT), amount);
        uint256 shares = REWARD_VAULT.deposit(amount, address(this), address(this));
```





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | StakeDAO_2025-07-21 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/StakeDAO-security-review_2025-07-21.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

