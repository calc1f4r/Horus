---
# Core Classification
protocol: Steadefi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35561
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-05-15-Steadefi.md
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

FRONT-RUNNING USERS IS POSSIBLE BY THE PROTOCOL TO OBTAIN A HIGHER FEE

### Overview


This bug report discusses a medium severity issue that has been resolved. The problem is related to a variable called performanceFee, which is used to calculate fees for the protocol. This variable can be changed by a specific user through a function called updatePerformanceFee. However, there is a risk that this user can manipulate the fee to be higher, resulting in the protocol earning more fees. The recommendation is to either restrict the ability to change this variable or add a grace period before the change takes effect.

### Original Finding Content

**Severity**: Medium	

**Status**: Resolved

**Description**


The performanceFee variable is a key variable to calculate the fee obtained by the protocol. This variable can be changed by calling the `updatePerformanceFee` function by the `restricted` user/users. 
```solidity
function updatePerformanceFee(uint256 newPerformanceFee) external restricted { 
   _updateVaultWithInterestsAndTimestamp(0);

   performanceFee = newPerformanceFee;

   emit PerformanceFeeUpdated(msg.sender, performanceFee, newPerformanceFee);
 }

```
If a user executes a transaction, the user marked as `restricted` can front-run it and change the `performanceFee` to a higher value resulting on the protocol earning more fees, this could take place specially on large transaction with a huge amount of funds.

**Recommendation:**

Do not allow performanceFee to be changed or add a grace period where the change is not directly applied.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Steadefi |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-05-15-Steadefi.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

