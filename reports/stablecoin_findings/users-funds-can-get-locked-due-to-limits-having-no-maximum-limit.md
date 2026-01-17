---
# Core Classification
protocol: Vaultcraft
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45896
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-12-31-VaultCraft.md
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
  - Zokyo
---

## Vulnerability Title

User’s funds can get locked due to ‘limits’ having no maximum limit.

### Overview


This bug report is about a problem in the `AsyncVault.sol` contract where the `Limits` struct contains two variables: `depositLimit` and `minAmount`. These variables can be modified by the owner using the `setLimits()` function, but there are no limits set for these variables. This means that they can be set to very high or very low values, causing users to not be able to deposit or withdraw their funds. To fix this, the report suggests defining maximum and minimum limits for these variables and checking that the new limits set by the owner are within these limits. The bug has been resolved.

### Original Finding Content

**Severity**: Medium	

**Status**: Resolved

**Description**

The ´Limits´ struct within the `AsyncVault.sol` contract contains 2 variables:
`depositLimit`: Maximum amount of assets that can be deposited into the vault
`minAmount`: Minimum amount of shares that can be minted / redeemed from the vault

The owner can execute the `setLimits()` function to modify these limit variables.
```solidity
function setLimits(Limits memory limits_) external onlyOwner {
       _setLimits(limits_);
   }


   /// @dev Internal function to set the limits
   function _setLimits(Limits memory limits_) internal { 
       emit LimitsUpdated(limits, limits_);


       limits = limits_;
   }
```
The problem is that there are not any maximum upper or lower limits for these variables, meaning that they can be set to 0 or to 99999999999999999… leading to users not being able to deposit or withdraw their funds, therefore getting them locked in the contract.

**Recommendation**:

Define 2 immutable variables representing the maximum and minimum upper limits and check that the new limits set within the `setLimits()` function are between the mentioned limits variables.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Vaultcraft |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-12-31-VaultCraft.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

