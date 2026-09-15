---
# Core Classification
protocol: Lido Csm
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44095
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Lido-CSM-Security-Review.md
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
  - Shieldify Security
---

## Vulnerability Title

[L-02] Potential Overflow on `_lock()` Method

### Overview

See description below for full details.

### Original Finding Content

## Submitted By

[bloqarl](https://x.com/TheBlockChainer)

## Severity

Low Risk

## Description

There is a potential for overflow in the `_lock()` function from the `CSBondLock` contract. The unchecked block in `_lock()` is problematic because it adds the new amount to any existing locked amount.

Even if individual calls don't use extremely large values, repeated calls could potentially lead to an overflow over time.

## Impact

The `lockBondETH()` function in `CSModule` (which calls `_lock()` in `CSBondLock`) is indeed restricted to `onlyCSM`, meaning it can only be called by the CSM contract itself. This significantly reduces the risk of malicious exploitation. However, there is still theoretical risk even in unintentional circumstances.

## Location of Affected Code

File [CSBondLock.sol](https://github.com/lidofinance/community-staking-module/blob/8ce9441dce1001c93d75d065f051013ad5908976/src/abstract/CSBondLock.sol)

```solidity
function _lock(uint256 nodeOperatorId, uint256 amount) internal {
  ...
  unchecked {
      if ($.bondLock[nodeOperatorId].retentionUntil > block.timestamp) {
          amount += $.bondLock[nodeOperatorId].amount;
      }
      _changeBondLock({
          nodeOperatorId: nodeOperatorId,
          amount: amount,
          retentionUntil: block.timestamp + $.bondLockRetentionPeriod
      });
  }
}
```

## Recommendation

Consider applying either of the following mitigations:

- Add an explicit check for overflow:

```diff
if ($.bondLock[nodeOperatorId].retentionUntil > block.timestamp) {
+   require(amount <= type(uint256).max - $.bondLock[nodeOperatorId].amount, "Lock amount too high");
    amount += $.bondLock[nodeOperatorId].amount;
}
```

- Add an upper limit to the amount that can be locked, based on realistic maximum values for the protocol:

```diff
if ($.bondLock[nodeOperatorId].retentionUntil > block.timestamp) {
+   require(amount <= MAX_LOCKABLE_AMOUNT, "Lock amount exceeds maximum");
    amount += $.bondLock[nodeOperatorId].amount;
}
```

## Team Response

Will be fixed, the `unchecked` block will be removed to ensure native solidity revert in case of overflow.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Lido Csm |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Lido-CSM-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

