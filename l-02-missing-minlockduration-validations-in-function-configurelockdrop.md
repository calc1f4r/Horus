---
# Core Classification
protocol: Munchables
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33601
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-05-munchables
source_link: https://code4rena.com/reports/2024-05-munchables
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
finders_count: 0
finders:
---

## Vulnerability Title

[L-02] Missing minLockDuration validations in function configureLockdrop()

### Overview

See description below for full details.

### Original Finding Content


[Link to instance](https://github.com/code-423n4/2024-05-munchables/blob/57dff486c3cd905f21b330c2157fe23da2a4807d/src/managers/LockManager.sol#L98)

First validation:
The function should ensure `_lockdropData.end - _lockdropData.start >= _lockdropData.minLockDuration`. This ensures the lockdrop event is longer than the minimum lock times user need to lock their tokens for.

Second validation:
The function should ensure `_lockdropData.minLockDuration < configStorage.getUint(StorageKey.MaxLockDuration)`. This ensure function setLockDuration() does not revert [due to the check here](https://github.com/code-423n4/2024-05-munchables/blob/57dff486c3cd905f21b330c2157fe23da2a4807d/src/managers/LockManager.sol#L246C25-L246C74) and lock() as well due to the check [here](https://github.com/code-423n4/2024-05-munchables/blob/57dff486c3cd905f21b330c2157fe23da2a4807d/src/managers/LockManager.sol#L358).
```solidity
File: LockManager.sol
099:     function configureLockdrop(
100:         Lockdrop calldata _lockdropData
101:     ) external onlyAdmin {
102:         if (_lockdropData.end < block.timestamp)
103:             revert LockdropEndedError(
104:                 _lockdropData.end,
105:                 uint32(block.timestamp)
106:             ); // , "LockManager: End date is in the past");
107:         if (_lockdropData.start >= _lockdropData.end)
108:             revert LockdropInvalidError();
109:         
111:         lockdrop = _lockdropData;
112: 
113:         emit LockDropConfigured(_lockdropData);
114:     }
```



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Munchables |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2024-05-munchables
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2024-05-munchables

### Keywords for Search

`vulnerability`

