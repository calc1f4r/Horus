---
# Core Classification
protocol: Blastoff
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37480
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-14-BlastOff.md
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
  - Zokyo
---

## Vulnerability Title

Unauthorized Withdrawal of Staked ETH via `repayWithStakeToken` Function

### Overview


This bug report describes a critical vulnerability in a function called `repayWithStakeToken` that allows attackers to withdraw staked ETH without proper authorization. This means that someone could take ETH that belongs to other users without their permission. The bug has been fixed, but it is important to add an ownership check to the function to prevent this from happening in the future. To reproduce the bug, someone would need to know a specific stake ID and calculate the required fee. To fix the bug, the function should be updated to verify that the caller is the owner of the stake ID before allowing the withdrawal to occur.

### Original Finding Content

**Severity**: Critical

**Status**: Resolved


**Affected Function:** repayWithStakeToken

**Description: **

A critical vulnerability allowing attackers to withdraw ETH staked by other users without proper authorization. The function fails to verify the ownership of the stake ID (`stakeId`) before processing the repayment and unstaking process, enabling anyone who knows the `stakeId` and the required fee calculation to withdraw the full staked amount by paying only a fraction of its value.

**Impact**: 

Allows unauthorized withdrawal of staked ETH, leading to potential loss of funds for users.

**Steps to Reproduce**:

- Identify a target stake ID (`stakeId`) with a significant amount of staked ETH.
- Calculate the required fee to repay the stake based on the yield amount and the accumulated yield per staked token. This can be done using the formula provided in the bug description.
- Call the `repayWithStakeToken` function with the target `poolId`, `stakeId`, and the calculated fee as the transaction value.
- Observe that the full amount of ETH staked under the target `stakeId` is transferred to the attacker's address, while only the calculated fee is deducted.

**Expected Behavior**: 

The `repayWithStakeToken` function should verify that the caller (`msg.sender`) is the owner of the stake ID (`stakeId`) before allowing the repayment and unstaking process to proceed. This ensures that only the rightful owner can withdraw the staked ETH.

**Actual Behavior**: 

The function does not perform any ownership verification, allowing any user to withdraw ETH staked by others by exploiting the vulnerability.

**Recommendation**: 

To mitigate this vulnerability, it is recommended to add an ownership check at the beginning of the `repayWithStakeToken` function. The following line of code should be inserted to ensure that the caller is the owner of the stake:
```solidity
if (staking.user != msg.sender) revert NotStaker(staking.user);
```
This check will prevent unauthorized users from exploiting the function to withdraw staked ETH that does not belong to them.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Blastoff |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-14-BlastOff.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

