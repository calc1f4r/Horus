---
# Core Classification
protocol: Ebisu
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58115
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Ebisu-security-review.md
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

[M-01] `maxTotalDeposits` is not checked properly inside `_beforeDeposit`.

### Overview


This bug report discusses an issue with the Ebisu vault contract that could potentially allow users to deposit more assets than the maximum limit set by the contract. The severity of this bug is considered medium, as it could have a negative impact on the functionality of the contract. The likelihood of this bug occurring is also considered medium, as it does not require a specific scenario to happen. 

The report explains that the current implementation of the `_beforeDeposit` function in the contract only checks the token balance inside the vault, but does not consider the assets that will be deposited by users. This means that users could potentially deposit assets that exceed the maximum limit set by the contract. 

To fix this issue, the report suggests that the contract should also consider the assets that will be deposited by users when checking against the maximum limit. The recommended code changes are also provided in the report. 

Overall, this bug report highlights an important issue with the Ebisu vault contract and provides a solution to fix it. 

### Original Finding Content

## Severity

**Impact:** Medium, Because it will allow user to deposit more than `maxTotalDeposits`.

**Likelihood:** Medium, Because it doesn't require a specific scenario, the `deposit`/`mint` action at some point can deposit more than `maxTotalDeposits`.

## Description

Ebisu vault implements a `_beforeDeposit` check before users `deposit`/`mint` to ensure it does not exceed the configured `maxPerDeposit` and `maxTotalDeposits`.

```solidity
    function deposit(uint256 assets, address receiver) public virtual override returns (uint256) {
        // require(assets <= maxDeposit(receiver), "ERC4626: deposit more than max");
>>      _beforeDeposit(assets);

        uint256 shares = previewDeposit(assets);
        _deposit(_msgSender(), receiver, assets, shares);

        return shares;
    }
```

However, in the current `_beforeDeposit` implementation, the check against `maxTotalDeposits` only verifies the token balance inside the vault and does not consider the `assets` that will be deposited by users.

```solidity
    function _beforeDeposit(uint256 assets) internal virtual {
        require(assets <= maxPerDeposit, "Vault: deposit amount exceeds per-deposit cap");
>>      require(_tokenBalance() <= maxTotalDeposits, "Vault: deposit amount exceeds total cap");
    }
```

This will allow users to deposit assets that could surpass the `maxTotalDeposits` value.

## Recommendations

Consider `assets` that will be deposited by users when checking against `maxTotalDeposits`.

```diff
    function _beforeDeposit(uint256 assets) internal virtual {
        require(assets <= maxPerDeposit, "Vault: deposit amount exceeds per-deposit cap");
-        require(_tokenBalance() <= maxTotalDeposits, "Vault: deposit amount exceeds total cap");
+        require(_tokenBalance() + assets <= maxTotalDeposits, "Vault: deposit amount exceeds total cap");
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Ebisu |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Ebisu-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

