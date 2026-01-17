---
# Core Classification
protocol: Nexus_2024-11-29
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44982
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Nexus-security-review_2024-11-29.md
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

[H-02] Lack of approval before depositing DAI into DSR contract

### Overview


This bug report discusses an issue with the DSRStrategy contract's `deposit` function. The contract is attempting to deposit DAI tokens into the DSR contract to receive sDAI, but it fails to include the required ERC20 approval step. This means that the contract is unable to transfer the tokens on behalf of the owner, leading to failed deposit transactions. The report recommends adding the necessary approval step before attempting the deposit to resolve the issue.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** High

## Description

The DSRStrategy contract's `deposit` function attempts to deposit DAI tokens into the DSR (Dai Savings Rate) contract to receive sDAI, but fails to implement the required ERC20 approval step. Since ERC20 tokens require approval before a contract can transfer them on behalf of the owner, it leads to deposit transactions to revert.

```solidity
   function deposit(uint256 _value) public returns(uint256){
        sDAI(DSR_DEPOSIT_ADDRESS).deposit(_value,address(this));
        return 100;
    }
```

## Recommendations

Add the necessary approval step before attempting the deposit:

```diff
   function deposit(uint256 _value) public returns(uint256){
+       IERC20(DAI_ADDRESS).approve(DSR_DEPOSIT_ADDRESS, _value);
        sDAI(DSR_DEPOSIT_ADDRESS).deposit(_value,address(this));
        return 100;
    }

```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Nexus_2024-11-29 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Nexus-security-review_2024-11-29.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

