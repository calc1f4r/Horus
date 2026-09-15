---
# Core Classification
protocol: Hyperlend_2025-01-11
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64821
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Hyperlend-security-review_2025-01-11.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-01] StrategyManager functions are not `payable`

### Overview


This bug report discusses a low severity bug in the code of StrategyManager, which is used by users to perform their strategies in one transaction. The bug allows users to send ETH for transactions, but the issue is that none of the functions of StrategyManager are marked as `payable` and there is no `fallback()` or `receive()` function to transfer ETH to the StrategyManager address. The recommendation is to mark the functions as `payable` to fix this bug.

### Original Finding Content


## Severity

**Impact:** Low

**Likelihood:** High

## Description

Users can use StrategyManager to perform their strategies in one transaction and the code allows sending ETH for the transactions:
```solidity
    function executeCall(address target, uint256 value, bytes memory data, bool allowRevert) public onlyOwner() returns (bytes memory) {
        (bool success, bytes memory returnData) = target.call{value: value}(data);
        if (!allowRevert) require(success, 'execution reverted');
        return returnData;
    }
```
The issue is that none of the functions of the StrategyManager are payable and there's no payable `fallback()` or `receive()` function so there's no way to transfer ETH to StrategyManager address and perform transactions that require sending ETH.

## Recommendations
Mark StrategyManager functions as `payable`.





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Hyperlend_2025-01-11 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Hyperlend-security-review_2025-01-11.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

