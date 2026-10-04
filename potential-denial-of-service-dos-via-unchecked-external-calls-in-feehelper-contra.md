---
# Core Classification
protocol: Rollie
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35485
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-04-16-Rollie.md
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

Potential Denial of Service (DoS) via Unchecked External Calls in `FeeHelper` Contract

### Overview


The FeeHelper contract has a function called `dealReferralAward` that can cause a problem where funds may get locked and prevent other operations from happening. This is because the function does not check if the values it receives from another contract are valid. To fix this, a validation step should be added to make sure the values are not too high. If they are, the function should use a different method to continue without causing any issues.

### Original Finding Content

**Severity**: Medium

**Status**: Resolved

**Location**: FeeHelper.sol

**Description**:

The `dealReferralAward` function in the `FeeHelper` contract makes external calls to the referral contract without validating the return values (rebase and discount). This oversight can lead to a situation where the sum of rebase and discount exceeds `totalFee`, resulting in a negative balance calculation. This scenario can potentially lock funds, as the contract attempts to transfer more tokens than available, leading to a Denial of Service (DoS) condition for subsequent operations.

**Recommendation**:

Implement a validation step in the `dealReferralAward` function to check if the sum of rebase and discount exceeds totalFee. If the condition is true, execute an alternative logic path that avoids a DoS scenario. For example:

```solidity
function dealReferralAward(uint256 totalFee, address trader, uint256 position) private returns (uint256 left) {
    if (address(referral) == address(0)) return totalFee;
    (uint256 rebase, uint256 discount) = referral.distributeRefReward(trader, totalFee, position);
    
    // Validate the sum of rebase and discount does not exceed totalFee
    if (rebase + discount > totalFee) {
        // Implement alternative logic here
        // For example, log the incident and continue without transferring funds
        emit ReferralRewardExceedsTotalFee(trader, rebase, discount, totalFee);
        return totalFee;
    }

    if (discount != 0) {
        SafeERC20.safeTransfer(standardToken, trader, discount);
    }
    if (rebase != 0) {
        SafeERC20.safeTransfer(standardToken, address(referral), rebase);
    }
    left = totalFee - discount - rebase;
}

```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Rollie |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-04-16-Rollie.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

