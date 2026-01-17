---
# Core Classification
protocol: Dpnmdefi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44543
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-03-13-DPNMDEFI.md
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

Transfer of busd to same recipient is unnecessarily repeated in loops

### Overview


This bug report is about a repeated code in a file called dpnm_sc.sol. The code is related to transferring money using a method called safeTransfer. This method is being used multiple times in a loop, which is not efficient and can cause delays. The recommendation is to declare a variable for the amount to be transferred and increase it each time instead of repeating the safeTransfer method. This will make the transfer faster and more efficient. The bug has been resolved by making changes to the code in a recent update.

### Original Finding Content

**Severity**: Medium

**Status**: Resolved

**Description**

dpnm_sc.sol - busd.safeTransfer(feeCollector, ...) is repeated in loop in both methods: _TreePayment and depositFordPNMBuy, safeTransfer is a costly operation, and it can be called only once on the total amount to be transferred, rather than repeating it unnecessarily.

**Recommendation** 

Declare a variable for the amountToBeTransferred and increase it each time you need to make the transfer. After reaching the target amountToBeTransferred do the actual transfer.
```solidity
uint256 amountToBeTransferred;

for (uint i=0; i <10; i++)  
   amountToBeTransferred += amountToBeAdded
busd.safeTransfer(feeCollector, amountToBeTransferred);
```
**Fix** - Codefix in 60761c1 introduced amountToBeTransferredToFeeCollector in _TreePayment. Also we have feeCollectorBonus in method depositBonusFordPNMBuy.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Dpnmdefi |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-03-13-DPNMDEFI.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

