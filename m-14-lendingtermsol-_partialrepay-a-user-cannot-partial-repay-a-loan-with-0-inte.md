---
# Core Classification
protocol: Ethereum Credit Guild
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 30234
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-12-ethereumcreditguild
source_link: https://code4rena.com/reports/2023-12-ethereumcreditguild
github_link: https://github.com/code-423n4/2023-12-ethereumcreditguild-findings/issues/756

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
finders_count: 5
finders:
  - carrotsmuggler
  - Silvermist
  - rbserver
  - ElCid
  - Topmark
---

## Vulnerability Title

[M-14] LendingTerm.sol `_partialRepay()` A user cannot partial repay a loan with `0` interest

### Overview


The bug report discusses an issue with a function called `_partialRepay()` that allows users to partially repay a loan. The function has a parameter called `debtToRepay` which determines how much of the loan debt will be repaid. However, there is a problem with the `interestRepaid != 0` requirement in the function, which causes issues when trying to partially repay a loan with 0 interest. This can be fixed by removing the requirement and adding a check to ensure the interest is not 0 before transferring it. A possible solution has been suggested and confirmed by the Ethereum Credit Guild.

### Original Finding Content


A user is allowed to partial repay a loan via the `_partialRepay()` function. It has a `debtToRepay` parameter which determines how much of the loan debt will be repaid. The `debtToRepay` amount should repay part of the borrowed amount and also a part of the fees and interest.

`interestRepaid` is calculated when from `debtToRepay` is subtracted the `principalRepaid`. It is made like that because we assume when we subtract the `principalRepaid` from the `debtToRepay`, the remaining amount from the  `debtToRepay`  is the interest.

```js
    uint256 interestRepaid = debtToRepay - principalRepaid;
```

So far so good, but there is one require or more specifically the `interestRepaid != 0` part of the require that causes a problem:

```js
    require(principalRepaid != 0 && interestRepaid != 0, "LendingTerm: repay too small");
```

That check is used to ensure that the amount the user is repaying is not too small; however, the `interestRepaid` would be `0` when there is `0` amount interest. A loan can be configured with `0` interest so it is a possible case. We can see it is not a problem to repay it through `_repay()` but it is impossible to partial repay it.

### Proof of Concept

Paste the following test inside `test/unit/loan/LendingTerm.t.sol`:

```js
    function testPartialRepayWithZeroInterestFail() public {
        LendingTerm term2 = LendingTerm(
            Clones.clone(address(new LendingTerm()))
        );
        term2.initialize(
            address(core),
            term.getReferences(),
            LendingTerm.LendingTermParams({
                collateralToken: address(collateral),
                maxDebtPerCollateralToken: _CREDIT_PER_COLLATERAL_TOKEN,
                interestRate: 0,
                maxDelayBetweenPartialRepay: _MAX_DELAY_BETWEEN_PARTIAL_REPAY,
                minPartialRepayPercent: _MIN_PARTIAL_REPAY_PERCENT,
                openingFee: 0,
                hardCap: _HARDCAP
            })
        );
        vm.label(address(term2), "term2");
        guild.addGauge(1, address(term2));
        guild.decrementGauge(address(term), _HARDCAP);
        guild.incrementGauge(address(term2), _HARDCAP);
        vm.startPrank(governor);
        core.grantRole(CoreRoles.RATE_LIMITED_CREDIT_MINTER, address(term2));
        core.grantRole(CoreRoles.GAUGE_PNL_NOTIFIER, address(term2));
        vm.stopPrank();

        // prepare & borrow
        uint256 borrowAmount = 20_000e18;
        uint256 collateralAmount = 12e18;
        collateral.mint(address(this), collateralAmount);
        collateral.approve(address(term2), collateralAmount);
        bytes32 loanId = term2.borrow(borrowAmount, collateralAmount);
        assertEq(term2.getLoan(loanId).collateralAmount, collateralAmount);

        vm.warp(block.timestamp + 10);
        vm.roll(block.number + 1);
        
        // check that the loan amount is the same as the initial borrow amount to ensure there are no accumulated interest
        assertEq(term2.getLoanDebt(loanId), 20_000e18);

        credit.mint(address(this), 10_000e18);
        credit.approve(address(term2), 10_000e18);

        vm.expectRevert("LendingTerm: repay too small");
        term2.partialRepay(loanId, 10_000e18);
    }
```

### Recommended Mitigation Steps

A possible solution would be to remove the `interestRepaid != 0` from the require in `_partialRepay()`:

```diff
-       require(principalRepaid != 0 && interestRepaid != 0, LendingTerm: repay too small");
+       require(principalRepaid != 0, LendingTerm: repay too small");
```

And a check to confirm the interest is not `0` before transferring it:

```diff
-        CreditToken(refs.creditToken).transfer(
-            refs.profitManager,
-            interestRepaid
-        );
-
-        ProfitManager(refs.profitManager).notifyPnL(
-            address(this),
-            int256(interestRepaid)
-        );

+       if (interest != 0) {
+           CreditToken(refs.creditToken).transfer(
+               refs.profitManager,
+               interestRepaid
+           );
+
+           ProfitManager(refs.profitManager).notifyPnL(
+               address(this),
+               int256(interestRepaid)
+           );
+      }
```

**[eswak (Ethereum Credit Guild) confirmed via duplicate issue #782](https://github.com/code-423n4/2023-12-ethereumcreditguild-findings/issues/782#issuecomment-1892051508)**

**[TrungOre (judge) commented](https://github.com/code-423n4/2023-12-ethereumcreditguild-findings/issues/756#issuecomment-1921617059):**
 > I chose this to be the primary issue since it has a very high quality; including clear and insightful context, PoC, and recommendations.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Ethereum Credit Guild |
| Report Date | N/A |
| Finders | carrotsmuggler, Silvermist, rbserver, ElCid, Topmark |

### Source Links

- **Source**: https://code4rena.com/reports/2023-12-ethereumcreditguild
- **GitHub**: https://github.com/code-423n4/2023-12-ethereumcreditguild-findings/issues/756
- **Contest**: https://code4rena.com/reports/2023-12-ethereumcreditguild

### Keywords for Search

`vulnerability`

