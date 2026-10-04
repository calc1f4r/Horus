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
solodit_id: 36476
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/SharwaFinance-security-review.md
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

[H-01] Swaps are available for `MarginAccounts` undergoing liquidation

### Overview


This bug report addresses an issue with the `swap` function in the `MarginTrading` contract. This function is used to execute trades, but it does not properly check the liquidation status of a `MarginAccount` before executing the trade. This means that a malicious user could manipulate the trade and potentially cause asset loss. The report recommends adding a check to ensure that only healthy `MarginAccounts` can use the `swap` function. 

### Original Finding Content

**Severity**

**Impact:** Medium

**Likelihood:** High

**Description**

`MarginTrading.redCoeff` and `MarginTrading.yellowCoeff` are used to determine whether a `MarginAccount` is in a state of liquidation. If an account is under liquidation, operations such as `borrow` and `withdraw` are restricted to preserve the account's integrity for liquidation purposes. However, the current implementation allows for `swaps` to continue without checks for the account's liquidation status.

```solidity
File: MarginTrading.sol
165:     function swap(uint marginAccountID, address tokenIn, address tokenOut, uint amountIn, uint amountOutMinimum) external nonReentrant onlyApprovedOrOwner(marginAccountID) {
166:         emit Swap(marginAccountID, swapID, tokenIn, tokenOut, amountIn);
167:
168:         marginAccount.swap(marginAccountID, swapID, tokenIn, tokenOut, amountIn, amountOutMinimum);
169:
170:         swapID++;
171:     }
```

A malicious user could execute swaps with higher risk by manually setting the `amountOutMinimum`, potentially leading to asset loss that would otherwise be available for liquidation. Additionally, in pools with limited liquidity, the user could manipulate the pool by setting `AmountOutMinimum=0` to execute swaps without receiving anything in return, thus potentially benefiting from slippage.

**Recommendations**

It is recommended to restrict the `swap` function only to `MarginAccounts` that are in a healthy state:

```diff
    function swap(uint marginAccountID, address tokenIn, address tokenOut, uint amountIn, uint amountOutMinimum) external nonReentrant onlyApprovedOrOwner(marginAccountID) {
++      uint marginAccountValue = calculateMarginAccountValue(marginAccountID);
++      uint debtWithAccruedInterest = calculateDebtWithAccruedInterest(marginAccountID);
++      uint marginAccountRatio = _calculatePortfolioRatio(marginAccountValue, debtWithAccruedInterest);
++      require(marginAccountRatio >= yellowCoeff, "Cannot swap");
        emit Swap(marginAccountID, swapID, tokenIn, tokenOut, amountIn);

        marginAccount.swap(marginAccountID, swapID, tokenIn, tokenOut, amountIn, amountOutMinimum);

        swapID++;
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

