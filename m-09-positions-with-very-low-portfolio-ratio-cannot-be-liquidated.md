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
solodit_id: 36489
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

[M-09] Positions with very low portfolio ratio cannot be liquidated

### Overview


Severity: High
Impact: The bug can have a significant effect on the functioning of the contract.
Likelihood: The chances of this bug occurring are low.

Description:
The `_calculatePortfolioRatio` function in the `MarginTrading.sol` file calculates the ratio between the margin account value and the debt with accrued interest. However, if the margin account value is significantly lower than the debt, the function will revert and prevent the liquidation of positions with low portfolio ratios. This can result in the remaining collateral being locked in the contract.

Recommendations:
To fix this bug, the code in the `MarginTrading.sol` file needs to be modified. The `require` statement in lines 200-201 should be removed and replaced with a check for a minimum portfolio ratio. Additionally, the `return` statement in line 198 should be replaced with a return of the maximum value of the `uint256` type. These changes will ensure that the liquidation function can still be executed even if the margin account value is significantly lower than the debt.

Overall, this bug is severe and can have a significant impact on the functioning of the contract. However, the chances of it occurring are low. To fix it, the code needs to be modified as recommended. 

### Original Finding Content

**Severity**

**Impact:** High

**Likelihood:** Low

**Description**

In `MarginTrading.sol`, the `_calculatePortfolioRatio` function calculates the ratio between the margin account value and the debt with accrued interest. In case the margin account value is 5 orders of magnitude lower than the debt accrued, this function reverts.

```solidity
File: MarginTrading.sol

196:     function _calculatePortfolioRatio(uint marginAccountValue, uint debtWithAccruedInterest) private pure returns (uint marginAccountRatio) {
197:         if (debtWithAccruedInterest == 0) {
198:             return 0;
199:         }
200:   @>    require(marginAccountValue*COEFFICIENT_DECUMALS > debtWithAccruedInterest, "Margin Account value should be greater than debt with accrued interest");
201:         marginAccountRatio = marginAccountValue*COEFFICIENT_DECUMALS/debtWithAccruedInterest;
202:     }
```

As the function is executed in the `liquidate` function, the liquidation of positions with very low portfolio ratios is not possible, locking the remaining collateral in the contract.

```solidity
File: MarginTrading.sol

181:     function liquidate(uint marginAccountID) external {
182:   @>    require(getMarginAccountRatio(marginAccountID) <= redCoeff, "Margin Account ratio is too high to execute liquidation");
```

**Recommendations**

```diff
File: MarginTrading.sol

-       if (portfolioRatio != 0) {
            require(portfolioRatio > yellowCoeff, "portfolioRatio is too low");
-       }

(...)

-       if (portfolioRatio != 0) {
            require(portfolioRatio > yellowCoeff, "portfolioRatio is too low");
-       }

(...)

    function _calculatePortfolioRatio(uint marginAccountValue, uint debtWithAccruedInterest) private pure returns (uint marginAccountRatio) {
        if (debtWithAccruedInterest == 0) {
-           return 0;
+           return type(uint256).max;
        }
-        require(marginAccountValue*COEFFICIENT_DECUMALS > debtWithAccruedInterest, "Margin Account value should be greater than debt with accrued interest");
        marginAccountRatio = marginAccountValue*COEFFICIENT_DECUMALS/debtWithAccruedInterest;
    }
```

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

