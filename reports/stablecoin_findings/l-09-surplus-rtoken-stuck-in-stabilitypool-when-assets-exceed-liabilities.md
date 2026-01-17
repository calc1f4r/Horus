---
# Core Classification
protocol: RegnumAurum_2025-08-12
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63414
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/RegnumAurum-security-review_2025-08-12.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[L-09] Surplus `rToken` stuck in `StabilityPool` when assets exceed liabilities

### Overview

See description below for full details.

### Original Finding Content


_Resolved_

During liquidation, the strategy pays the borrower’s debt in `crvUSD` and then **re-deposits any leftover `crvUSD` back into the LendingPool**, which mints additional **`rToken` to the `StabilityPool`**:

```solidity
// LiquidationStrategyProxy (simplified)
uint256 finalCRVUSDBalance = crvUSDToken.balanceOf(address(this));
if (finalCRVUSDBalance > 0) {
    lendingPool.deposit(finalCRVUSDBalance); // mints rToken to StabilityPool
}
```

User withdrawals from the StabilityPool always send **exactly the user’s scaled amount** and do **not** pro-rata any surplus:

```solidity
// StabilityPool.withdraw(...)
deToken.burn(msg.sender, scaledAmount);
rToken.safeTransfer(msg.sender, scaledAmount); // exactly "scaledAmount", no share of surplus
```

`DEToken` is **index-denominated**, not share-of-pool. Its balances (and total supply) are derived from raw deposits × index, **independent of** `rToken.balanceOf(StabilityPool)`.
Therefore, if liquidation leaves extra `crvUSD` that is re-deposited, the pool’s **assets** can exceed the **liabilities** to DEToken holders:

* **Assets (scaled):** `A = rToken.balanceOf(StabilityPool)`
* **Liabilities (scaled):** `L = deToken.getRawTotalDeposits() * getNormalizedIncome()`

If `A > L`, the difference `A - L` is a **surplus** that:

* is **not distributable** to DEToken holders (no PPS/vault math, no surplus index);
* cannot be withdrawn by users (no matching DEToken to burn);
* has **no admin sweep** in the current code (so it effectively sits on the contract indefinitely),
* and will only be consumed opportunistically by future liquidations.

This creates **capital lock** and mis-accounting risk (assets parked without an explicit policy), and can confuse accounting/metrics (TVL vs. claimable).

**Recommendations**

**A. Cap the post-liquidation re-deposit to avoid growing surplus.**
Before depositing the leftover `crvUSD`, compute how much (in scaled terms) the pool can accept without exceeding a target (liabilities or liabilities + small buffer).

**B. Add an explicit `sweepSurplus()` admin function (with events & policy).**
Allow moving only the *excess* safely.





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | RegnumAurum_2025-08-12 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/RegnumAurum-security-review_2025-08-12.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

