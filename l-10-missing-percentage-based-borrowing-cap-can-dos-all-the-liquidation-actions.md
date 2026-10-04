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
solodit_id: 63415
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

[L-10] Missing percentage based borrowing cap can DoS all the liquidation actions

### Overview

See description below for full details.

### Original Finding Content


_Resolved_

Currently, there is no percentage based borrowing cap in the system. It's not a regular cap type, and it's not required for many protocols, but it's required for RAAC because of it's own unique liquidation design. 

In RAAC liquidation design, debt is covered by lenders, which is a unique way. Stability pool holds RToken, and in liquidations, these RTokens are converted to crvUSD by calling `withdraw` function in Lending Pool:

```solidity
        uint256 rTokenAmountRequired = initialCRVUSDBalance >= scaledPositionDebt ? 0 : scaledPositionDebt - initialCRVUSDBalance;
        if (availableRTokens < rTokenAmountRequired) revert InsufficientBalance(); 

        // We unwind the position
        if (rTokenAmountRequired > 0) {
@>          lendingPool.withdraw(rTokenAmountRequired);
        }

```

This design can't be alive if we reach 100% borrowing utilization rate, because while calling `withdraw` it will revert because of insufficient liquidity. 100% of the funds borrowed by borrowers, and there is no way to liquidate any position in this case.

Borrowers can avoid liquidation by constantly borrowing 100% of the funds in the Lending Pool, and they don't have to pay back that because liquidation is almost impossible.

> Actually, protocol can liquidate positions by transferring crvUSD tokens directly to Stability Pool, and then they can liquidate it. However, these crvUSDs will be lost on protocol side, and it will cause loss of funds anyway.

Due to these reasons, percentage based borrowing cap is crucial for the current RAAC system design. 

**Recommendations**

Consider applying percentage based borrowing cap, such as 80%. 

> Note: This cap has a trade-off. If we leave too much gap in the pool, interest rates will be lower in the Lending Pool. However, if we choose a really tiny value for this gap, big positions cannot be liquidated.




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

