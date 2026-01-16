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
solodit_id: 36485
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

[M-05] Borrowers can be left with debt shares after full repayment

### Overview


This bug report discusses an issue in a code file called LiquidityPool.sol. The bug causes borrowers to still have debt shares after fully repaying their debt, due to a rounding error in the calculation of the `shareChange` value. The impact of this bug is considered low, but the likelihood of it occurring is high. The report includes a proof of concept in the form of a code snippet, which shows how the bug can be replicated. The report also includes a recommendation to reevaluate the need for tracking both individual debt amounts and debt shares, as it can lead to unexpected behavior. 

### Original Finding Content

**Severity**

**Impact:** Low

**Likelihood:** High

**Description**

Borrowers can be left with debt shares after full repayment of their debt. This is due to the calculation of the `shareChange` value rounding down.

```solidity
File: LiquidityPool.sol

155:     function repay(uint marginAccountID, uint amount) external onlyRole(MARGIN_ACCOUNT_ROLE) {
(...)
164:  @>     uint shareChange = (amount * debtSharesSum) / newTotalBorrows; // Trader's share to be given away
165:         uint profit = (accruedInterest * shareChange) / shareOfDebt[marginAccountID];
166:         uint profitInsurancePool = (profit * insuranceRateMultiplier) / INTEREST_RATE_COEFFICIENT;
167:         totalInterestSnapshot -= totalInterestSnapshot * shareChange / debtSharesSum;
168:         debtSharesSum -= shareChange;
169:         shareOfDebt[marginAccountID] -= shareChange;
```

**Proof of concept**

```solidity
function test_borrowerKeepsDebtSharesAfterRepay() public {
    provideInitialLiquidity();

    vm.startPrank(alice);
    marginTrading.provideERC20(marginAccountID[alice], address(USDC), 10_000e6);
    marginTrading.provideERC20(marginAccountID[alice], address(WETH), 1e18);
    marginTrading.borrow(marginAccountID[alice], address(WETH), 1e18);
    vm.stopPrank();

    vm.startPrank(bob);
    marginTrading.provideERC20(marginAccountID[bob], address(USDC), 10_000e6);
    marginTrading.borrow(marginAccountID[bob], address(WETH), 0.1e18);
    vm.stopPrank();

    skip(10);

    // Alice repays all debt plus interest
    vm.startPrank(alice);
    marginTrading.repay(marginAccountID[alice], address(WETH), 2e18);

    // Alice keeps debt shares after full repayment
    uint256 aliceDebtAmount = liquidityPoolWETH.portfolioIdToDebt(marginAccountID[alice]);
    uint256 aliceDebtShares = liquidityPoolWETH.shareOfDebt(marginAccountID[alice]);
    assert(aliceDebtAmount == 0);
    assert(aliceDebtShares > 0);
}
```

**Recommendations**

It is recommended to reevaluate the need for tracking both individual debt amounts and individual debt shares, as they can create discrepancies in valuations and lead to unexpected behavior.

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

