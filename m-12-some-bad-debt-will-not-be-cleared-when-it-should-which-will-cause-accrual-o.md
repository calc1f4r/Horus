---
# Core Classification
protocol: Exactly Protocol Update - Stacking Contract
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36675
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/396
source_link: none
github_link: https://github.com/sherlock-audit/2024-07-exactly-stacking-contracts-judging/issues/74

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
  - 0x73696d616f
---

## Vulnerability Title

M-12: Some bad debt will not be cleared when it should which will cause accrual of bad debt decreasing the protocol's solvency

### Overview


This bug report discusses an issue with the protocol that can lead to bad debt not being cleared when it should. This can cause a decrease in the protocol's solvency and increase the risk of insolvency for users. The bug has been acknowledged by the protocol and its root cause has been identified. The issue occurs because the accumulator is checked before it is increased, which means that it may not be enough to cover the bad debt even though it could be with the added unassigned earnings. This can happen when a user borrows maturities but does not pay them back, causing their debt to increase. To mitigate this issue, the earnings accumulator should be increased before comparing it against the bad debt. A code snippet is provided to confirm the issue and steps are suggested to fix it.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-07-exactly-stacking-contracts-judging/issues/74 

The protocol has acknowledged this issue.

## Found by 
0x73696d616f
### Summary

In `Market::clearBadDebt()`, it only clears bad debt if the `earningsAccumulator` is bigger than the bad debt to clear, but the fixed pool in question may have unassigned earnings which would be added to the earnings accumulator. Thus, the accumulator would have funds to handle the bad debt, but due to checking if it is enough before taking into account its increase, it will not clear the bad debt and will decrease protocol solvency.

### Root Cause

In `Market:641`, it first [checks](https://github.com/sherlock-audit/2024-07-exactly-stacking-contracts/blob/main/protocol/contracts/Market.sol#L641C13-L641C35) if `accumulator >= badDebt` and then in `Market:653` it [increases](https://github.com/sherlock-audit/2024-07-exactly-stacking-contracts/blob/main/protocol/contracts/Market.sol#L653) the accumulator. This should be done in the opposite order as the accumulator may actual be big enough with the added unassigned earnings to clear the bad debt.

### Internal pre-conditions

1. Fixed pool has unassigned earnings.
2. User is liquidated.
3. Accumulator is bigger than the bad debt if it takes into account unassigned earnings.

### External pre-conditions

None.

### Attack Path

1. User borrows maturities but lets them expire and accrues more debt than collateral.
2. User is liquidated, but the accumulator is not enough to cover the bad debt without the unassigned earnings increase, so bad debt keeps accruing.

### Impact

Bad debt accrual which harms protocol users as it increases the risk of insolvency.

### PoC

The following code snippet can be verified to confirm the issue:
```solidity
function clearBadDebt(address borrower) external {
  {
    {
      ...
      if (accumulator >= badDebt) {
        ...
        if (fixedPools[maturity].borrowed == position.principal) {
          earningsAccumulator += fixedPools[maturity].unassignedEarnings;
          fixedPools[maturity].unassignedEarnings = 0;
        }
        ...
      }
    }
  }
  ...
}
```

### Mitigation

Increase the earnings accumulator first and only then compare it against the bad debt.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Exactly Protocol Update - Stacking Contract |
| Report Date | N/A |
| Finders | 0x73696d616f |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-07-exactly-stacking-contracts-judging/issues/74
- **Contest**: https://app.sherlock.xyz/audits/contests/396

### Keywords for Search

`vulnerability`

