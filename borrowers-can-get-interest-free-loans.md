---
# Core Classification
protocol: Paribus
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37388
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-Paribus.md
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
  - Zokyo
---

## Vulnerability Title

Borrowers can get Interest-free loans

### Overview


The bug report discusses a problem in the Contract PTokens.sol, where the borrowing balance of a borrower is calculated using a formula that can result in a potential attack. This can happen when the principal and ratio of borrow indices are both small, causing the result to equal the principal. This allows users to borrow small loans for short periods with no actual interest, which can be exploited by attackers. The recommendation is to update the method to round up the borrow balance instead of truncating it. This issue is considered high severity and has been acknowledged by the team.

### Original Finding Content

**Severity**: High

**Status**: Acknowledged

**Description**

In Contract PTokens.sol, the borrowing balance of a borrower is calculated as follows:
```solidity
/* Calculate new borrow balance using the interest index:
* recentBorrowBalance = borrower.borrowBalance * market.borrowIndex / borrower.borrowIndex
*/
```
The above formula in Solidity is as following, 
```solidity
uint principalTimesIndex = mul_(borrowSnapshot.principal, borrowIndex);
return div_(principalTimesIndex, borrowSnapshot.interestIndex);
```

Here, when the principal and ratio of borrow indices are both small the result can equal the principal, due to automatic truncation of division within solidity.

If that is the case, then the loan will accrue no actual interest but still be counted as a loan. 

This allows users to borrow small loans for short-term periods with no actual interest which they can deposit back to Paribus to earn interest on that.

Since the client is planning to deploy the contracts on chains where transaction cost is cheap such as Polygon, zkSync, or any other L2 layer chain, the chances of this attack are enhanced as the attacker will not need to care for the small gas fees.

Recommendation: Update the method to calculate the borrow balance being rounded up instead of being truncated.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Paribus |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-Paribus.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

