---
# Core Classification
protocol: Sharwafinance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36491
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/SharwaFinance-security-review.md
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

[M-11] Debt calculation should be rounded up during repayment

### Overview


The bug report discusses a problem with a function called `repay` in a smart contract called `LiquidityPool`. The severity of the bug is low, but the likelihood of it happening is high. The function is designed to calculate the remaining debt of a user when they partially repay their debt. However, the calculation is rounded down, which means that over time, small amounts of debt can accumulate and cause losses for depositors in the pool. The recommendation is to round up the calculation instead to prevent this issue.

### Original Finding Content

**Severity**

**Impact:** Low

**Likelihood:** High

**Description**

In case of partial repayment of the debt `LiquidityPool#repay` function calculates the user's debt that is left based on current debt and amount of repayment (line 171):

```solidity
File: LiquidityPool.sol
155:     function repay(uint marginAccountID, uint amount) external onlyRole(MARGIN_ACCOUNT_ROLE) {
156:         uint newTotalBorrows = totalBorrows();
157:         uint newTotalInterestSnapshot = newTotalBorrows - netDebt;
158:         uint accruedInterest = (newTotalInterestSnapshot * shareOfDebt[marginAccountID]) / debtSharesSum; // Accrued interest only
159:         uint debt = portfolioIdToDebt[marginAccountID] + accruedInterest;
160:         if (debt < amount) {
161:             // If you try to return more tokens than were borrowed, the required amount will be taken to repay the debt, the rest will remain untouched
162:             amount = debt;
163:         }
164:         uint shareChange = (amount * debtSharesSum) / newTotalBorrows; // Trader's share to be given away
165:         uint profit = (accruedInterest * shareChange) / shareOfDebt[marginAccountID];
166:         uint profitInsurancePool = (profit * insuranceRateMultiplier) / INTEREST_RATE_COEFFICIENT;
167:         totalInterestSnapshot -= totalInterestSnapshot * shareChange / debtSharesSum;
168:         debtSharesSum -= shareChange;
169:         shareOfDebt[marginAccountID] -= shareChange;
170:         if (debt > amount) {
171:             uint tempDebt = (portfolioIdToDebt[marginAccountID] * (debt - amount)) / debt;
172:             netDebt = netDebt - (portfolioIdToDebt[marginAccountID] - tempDebt);
173:             portfolioIdToDebt[marginAccountID] = tempDebt;
174:         } else {
175:             netDebt -= portfolioIdToDebt[marginAccountID];
176:             portfolioIdToDebt[marginAccountID] = 0;
177:         }
178:         poolToken.transferFrom(msg.sender, address(this), amount);
179:         if (profitInsurancePool > 0) {
180:             poolToken.transfer(insurancePool, profitInsurancePool);
181:         }
182:
183:         emit Repay(marginAccountID, amount, profit);
184:     }
```

However, this calculation is rounded down, which means that users could repay less debt each time for some dust amount. This dust would accumulate into pool depositors' losses.

**Recommendations**

Consider rounding up the `tempDebt` variable in the `LiquidityPool#repay` function.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Sharwafinance |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/SharwaFinance-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

