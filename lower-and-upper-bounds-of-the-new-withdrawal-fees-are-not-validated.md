---
# Core Classification
protocol: Vaultka
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44910
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-08-30-Vaultka.md
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
  - Zokyo
---

## Vulnerability Title

Lower and upper bounds of the new withdrawal fees are not validated

### Overview

See description below for full details.

### Original Finding Content

**Severity**: Informational

**Status**: Resolved

**Description**

SakeVaultV2.sol - In function changeProtocolFee, the argument newWithdrawalFee should be within certain determined bounds. In the body of the function the newWithdrawalFee is not being validated to be a proper input to be the new value of feeConfiguration.withdrawalFee.
```solidity
function changeProtocolFee(address newFeeReceiver, uint256 newWithdrawalFee) external onlyOwner {
    feeConfiguration.withdrawalFee = newWithdrawalFee;
    feeConfiguration.feeReceiver = newFeeReceiver;
    emit ProtocolFeeChanged(newFeeReceiver, newWithdrawalFee);
}
```
**Recommendation** 

Add require statement to validate the newWithdrawalFee to be a proper value. Also, check newFeeReceiver to assert that it is a non-zero address.
Fix: In commit 9b0f573, function name has changed to setProtocolFee.  Address input is validated to be non-zero address, but numerical uint values are not validated despite expected to be within a certain range.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Vaultka |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-08-30-Vaultka.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

