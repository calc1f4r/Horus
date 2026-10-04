---
# Core Classification
protocol: Filament
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45627
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-08-15-Filament.md
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

Positions can not get liquidated when protocol is paused.

### Overview


The bug report describes an issue where a user is unable to pay off their debt and avoid getting liquidated when the protocol is paused. This happens because a function called `increasePosition()` in the `TradeFacet.sol` smart contract is dependent on another function called `lockForAnOrder()` which can only be called when the contract is not paused. This means that if the protocol is paused for any reason, the user will not be able to pay off their debt and may get liquidated. 

To fix this issue, the recommendation is to either remove the `whenNotPaused` modifier for critical functions or create new functions specifically for this purpose. This will ensure that users are able to pay off their debt and avoid getting liquidated even when the protocol is paused. The bug has been resolved and the severity is considered medium.

### Original Finding Content

**Severity**: Medium	

**Status**: Resolved

**Description**

When a position becomes unhealthy a user can call `increasePosition()` within the `TradeFacet.sol`smart contract to pay the debt. However, this `increasePosition()` calls to `lockForAnOrder()` which only callable then the contract is not paused:
```solidity
function lockForAnOrder(address _account, uint256 _amount) external onlyDiamond whenNotPaused {
       if (_amount > balances[_account]) {
           revert LockForOrderFailed(_account);
       }
       locked[_account] += _amount;
       balances[_account] = balances[_account] - _amount;
   }
```


Consider the following scenario:
Alice opens a positions
Alice’s position is healthy.
The protocol is paused for any reason (maintenance/security).
Alice’s position becomes unhealthy.
She can not pay the debt back and will get liquidated.


**Recommendation**:

Remove `whenNotPaused` modifier for critical functions to avoid functions getting liquidated when paused or create new functions for this purpose.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Filament |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-08-15-Filament.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

