---
# Core Classification
protocol: Saffron
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31509
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Saffron-security-review.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[H-03] Fixed participants will be incorrectly penalized during adminSettleDebt timelock period

### Overview


The bug report describes a problem where fixed participants in a platform may lose money due to a mistake in the code. This bug occurs when an admin settles debt in the system, and a timelock is activated before the admin can transfer funds. However, if fixed participants withdraw their deposit during this timelock period, they will be charged early withdrawal fees, even though they are supposed to be protected during this time. The bug is caused by a calculation error in the code, which applies a scaling fee even after the timelock has started. The recommendation is to fix this error by not applying the scaling fee after the timelock has started.

### Original Finding Content

**Severity**

**Impact:** High, fixed participants will incur losses

**Likelihood:** Medium, occurs when admin settles debt

**Description**

When `initiatingAdminSettleDebt()` is called, the settle debt process is initialized. That will start the timelock of 3 days (based on `adminSettleDebtLockPeriod`), before the admin can call `adminSettleDebt()` and transfer the stETH balance to `AdminLidoAdapter`. I believe the timelock is designed to allow fixed/variable participants to withdraw before `adminSettleDebt()`, when the `settleDebtAmount` set during initialization does not properly compensate them (e.g. a rogue admin try to settle debt with a heavy loss).

However, when fixed participants withdraw their deposit after `initiatingAdminSettleDebt()` and before vault ends, they will be penalized with the early withdrawal fees as calculated in `calculateFixedEarlyExitFees()`. That is incorrect as it defeats the purpose of the timelock, causing fixed participants to be under-compensated regardless of the timelock.

```Solidity
  function calculateFixedEarlyExitFees(
    uint256 upfrontPremium,
    uint256 timestampRequested
  ) internal view returns (uint256) {
    uint256 remainingProportion = (endTime > timestampRequested ? endTime - timestampRequested : 0).mulDiv(
      1e18,
      duration
    );

    //@audit the scaling fees will should not be applied after initiatingAdminSettleDebt() is called
    // Calculate the scaling fee based on the quadratic scaling factor and earlyExitFeeBps
    uint256 earlyExitFees = upfrontPremium.mulDiv(
      earlyExitFeeBps.mulDiv(remainingProportion.mulDiv(remainingProportion, 1e18), 1e18),
      10000
    );

    // Calculate the amount to be paid back of their original upfront claimed premium, not influenced by quadratic scaling
    earlyExitFees += upfrontPremium - upfrontPremium.mulDiv(timestampRequested - startTime, duration);

    return earlyExitFees;
  }
```

**Recommendations**

After `initiatingAdminSettleDebt()` is called, `calculateFixedEarlyExitFees()` should not apply the scaling fee.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Saffron |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Saffron-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

