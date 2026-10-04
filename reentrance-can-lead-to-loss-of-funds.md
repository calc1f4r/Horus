---
# Core Classification
protocol: Zap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35415
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-04-11-Zap.md
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

Reentrance can lead to loss of funds

### Overview


This bug report is about a critical issue in a contract called Contract Vesting.sol. The method `claim()` in this contract allows users to claim their deposited tokens once a certain time period has passed. However, there is a problem where users can repeatedly call the `claim()` method and steal all the ETH or native tokens from the contract. This is because the contract does not have protection against reentrancy and does not follow the CEI (Check-Effects-Interaction) pattern. The recommendation is to update the contract to fix these issues and add OZ Reentrancy guard.

### Original Finding Content

**Severity**: Critical

**Status**: Resolved

**Description**

In Contract Vesting.sol, the method `claim()` allows users to claim the deposited tokens once the vesting time is over.

Since the deposited asset can be ETH/Native token as well, it will be sent to the user as per the following logic:
```solidity
if (pctAmount != 0) {
           if (address(token) == address(1)) {
               (bool sent, ) = payable(sender).call{value: pctAmount}(""); 
               require(sent, "Failed to send BNB to receiver");
           } else {
               token.safeTransfer(sender, pctAmount);
           }
           s.index = uint128(i);
           s.amountClaimed += pctAmount;
       }
```
Here, Sending Ether is transferring the access of execution to the `sender` account, and then the `sender` account can call the `claim` method again. Since `s.index` is still not updated, the `pctAmount` will be calculated again and the same amount of ETH will be sent to the `sender`.

The sender can repeat this process until no ETH/native token is left in the contract. This way `sender` can steal all the ETH/native tokens from the contract.

This happens due to no reentrancy protection and not following the CEI (Check-Effects-Interaction) pattern.

**Recommendation**: 

Update the `s.index` and `s.amountClaimed` before sending assets to the user. Also, check `s.amountClaimed` if necessary before the claim. Finally, add OZ Reentrancy guard as well.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Zap |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-04-11-Zap.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

