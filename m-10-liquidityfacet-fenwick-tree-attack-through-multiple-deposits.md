---
# Core Classification
protocol: Hyperhyper_2025-03-30
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57753
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Hyperhyper-security-review_2025-03-30.md
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

[M-10] `liquidityFacet`: fenwick tree attack through multiple deposits

### Overview


This bug report discusses a potential issue with the `addLiquidity()` function in the current implementation of the Fenwick Tree structure. This could allow a malicious user to add liquidity multiple times on behalf of another user, filling the tree and preventing legitimate deposits from occurring. This behavior is known as "griefing" and can be exploited to manipulate the system. The Fenwick Tree has a limit on the number of entries that can be added, and once this limit is reached, no more entries can be added. This could result in prolonged periods where malicious behavior can persist. The report recommends checking the `msg.sender` in the `addLiquidity()` function to prevent unauthorized access and suggests withdrawing all liquidity to reset the tree, although this can only be done after the lock duration has passed.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

In the current implementation of the `addLiquidity()` function, a malicious user can exploit the Fenwick Tree structure by adding liquidity multiple times on behalf of another user, effectively filling the tree and potentially preventing legitimate deposits from occurring.
The Fenwick Tree has a `maxDepositEntries` limit, and once this limit is reached, no more entries can be added. This enables griefing behavior, where an attacker could manipulate the system by adding multiple deposits for a single user, thus locking out legitimate users from depositing liquidity until the tree is reset.

```solidity
    function _deposit(FenwicksData storage self, uint256 maxDepositEntries, uint256 lockDuration, uint256 amount)
        internal
    {
        uint256 treeIndex = _registerKey(self, maxDepositEntries, block.timestamp + lockDuration);
        _fenwicksUpdate(self, maxDepositEntries, treeIndex, amount);
        self.totalMintedPLP += amount;
    }

    function _registerKey(FenwicksData storage self, uint256 maxDepositEntries, uint256 newTimestamp)
        internal
        returns (uint256 treeIndex)
    {
        uint256 keyCount = self.sortedKeys.length;

@>      if (keyCount >= maxDepositEntries) revert Fenwicks_TooManyKeys();

        self.sortedKeys.push(newTimestamp);
        self.keyToIndex[newTimestamp] = ++keyCount;

        treeIndex = self.keyToIndex[newTimestamp];
    }
```

Although users can withdraw all liquidity to reset the tree, this action can only be performed after the lock duration has passed, which may lead to prolonged periods where malicious behavior can persist.

## Recommendations

Check `msg.sender` in add liquidity to prevent unauthorized access.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Hyperhyper_2025-03-30 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Hyperhyper-security-review_2025-03-30.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

