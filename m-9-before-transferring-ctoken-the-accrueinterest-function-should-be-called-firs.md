---
# Core Classification
protocol: Numa
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45286
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/554
source_link: none
github_link: https://github.com/sherlock-audit/2024-12-numa-audit-judging/issues/168

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
  - KupiaSec
---

## Vulnerability Title

M-9: Before transferring `CToken`, the `accrueInterest()` function should be called first.

### Overview


This bug report discusses an issue with the `CToken` function in the Numa protocol. Before transferring `CToken`, the `accrueInterest()` function should be called first. However, in the current code, `accrueInterest()` is not called before `transferAllowed()`, leading to inaccurate checks and potentially allowing illegitimate transfers to succeed. This could result in an imbalance between a user's collateral and debt value, potentially leading to liquidation. To fix this issue, the `accrueInterest()` function should be called before any transfers are made.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-12-numa-audit-judging/issues/168 

## Found by 
KupiaSec

### Summary

Before transferring `CToken`, the `NumaComptroller.transferAllowed()` function is called first to prevent any imbalance between the user's collateral and debt value.

However, since `accrueInterest()` is not called before `transferAllowed()`, the imbalance check is performed incorrectly, using outdated data.

As a result, legitimate transfers may be reverted, and illegitimate transfers could succeed.

### Root Cause

Before transferring `CToken`, the [transferTokens()](https://github.com/sherlock-audit/2024-12-numa-audit/blob/main/Numa/contracts/lending/CToken.sol#L149) function is invoked without first calling `accrueInterest()`.

Within the `transferTokens()` function, `transferAllowed()` is called.

The `NumaComptroller.transferAllowed()` function checks for potential imbalances between the user's collateral and debt value. However, this check is inaccurate, as it relies on outdated data because `accrueInterest()` has not been invoked.

As a result, legitimate transfers may be reverted, and illegitimate transfers could succeed.

The reversal of legitimate transfers is particularly concerning, as it can be time-sensitive, especially in liquidation situations for the receiver. And illegitimate transfers can lead to an imbalance between the sender's collateral and the value of their debt, potentially resulting in the sender facing liquidation after the transfer.

```solidity
    function transfer(
        address dst,
        uint256 amount
    ) external override nonReentrant returns (bool) {
149     return transferTokens(msg.sender, msg.sender, dst, amount) == NO_ERROR;
    }

--------------------

    function transferTokens(
        address spender,
        address src,
        address dst,
        uint tokens
    ) internal returns (uint) {
        /* Fail if transfer not allowed */
90      uint allowed = comptroller.transferAllowed(
            address(this),
            src,
            dst,
            tokens
        );
        if (allowed != 0) {
            revert TransferComptrollerRejection(allowed);
        }

        ...
    }
```

### Internal pre-conditions

### External pre-conditions

### Attack Path

### Impact

Legitimate transfers may be reverted, and illegitimate transfers could succeed.

If the receiver is on the verge of liquidation, the reversal of legitimate transfers to this receiver becomes a time-sensitive issue.

And illegitimate transfers can lead to an imbalance between the sender's collateral and the value of their debt, potentially resulting in the sender facing liquidation after the transfer.

### PoC

### Mitigation

Invoke `accrueInterest()` before the transfer.

## Discussion

**tibthecat**

This is coming from compound V2 fork. Is compound V2 vulnerable to that too?

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Numa |
| Report Date | N/A |
| Finders | KupiaSec |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-12-numa-audit-judging/issues/168
- **Contest**: https://app.sherlock.xyz/audits/contests/554

### Keywords for Search

`vulnerability`

