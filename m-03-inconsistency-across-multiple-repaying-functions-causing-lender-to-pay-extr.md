---
# Core Classification
protocol: The Wildcat Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41704
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-08-wildcat
source_link: https://code4rena.com/reports/2024-08-wildcat
github_link: https://github.com/code-423n4/2024-08-wildcat-findings/issues/62

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
finders_count: 6
finders:
  - Takarez
  - Udsen
  - deadrxsezzz
  - 0xNirix
  - Infect3d
---

## Vulnerability Title

[M-03] Inconsistency across multiple repaying functions causing lender to pay extra fees

### Overview


This bug report discusses an inconsistency in the Wildcat Market protocol where funds are pulled from users at different times in different functions. This results in borrowers paying extra fees in some cases. The report includes a Proof of Concept (PoC) and recommended mitigation steps, which include always pulling funds first and refunding them later if needed. The Wildcat team has acknowledged and resolved the issue in their code.

### Original Finding Content


Within functions such as `repay` and `repayAndProcessUnpaidWithdrawalBatches`, funds are first pulled from the user in order to use them towards the currently expired, but not yet unpaid batch, and then the updated state is fetched.

```solidity
  function repay(uint256 amount) external nonReentrant sphereXGuardExternal {
    if (amount == 0) revert_NullRepayAmount();

    asset.safeTransferFrom(msg.sender, address(this), amount);
    emit_DebtRepaid(msg.sender, amount);

    MarketState memory state = _getUpdatedState();
    if (state.isClosed) revert_RepayToClosedMarket();

    // Execute repay hook if enabled
    hooks.onRepay(amount, state, _runtimeConstant(0x24));

    _writeState(state);
  }
```

However, this is not true for functions such as `closeMarket`, `deposit`, `repayOutstandingDebt` and `repayDelinquentDebt`, where the state is first fetched and only then funds are pulled, forcing borrower into higher fees.

```solidity
  function closeMarket() external onlyBorrower nonReentrant sphereXGuardExternal {
    MarketState memory state = _getUpdatedState();    // fetches updated state

    if (state.isClosed) revert_MarketAlreadyClosed();

    uint256 currentlyHeld = totalAssets();
    uint256 totalDebts = state.totalDebts();
    if (currentlyHeld < totalDebts) {
      // Transfer remaining debts from borrower
      uint256 remainingDebt = totalDebts - currentlyHeld;
      _repay(state, remainingDebt, 0x04);             // pulls user funds
      currentlyHeld += remainingDebt;
```

This inconsistency will cause borrowers to pay extra fees which they otherwise wouldn't.

**PoC:**

```solidity
  function test_inconsistencyIssue() external {
      parameters.annualInterestBips = 3650;
      _deposit(alice, 1e18);
      uint256 borrowAmount = market.borrowableAssets();
      vm.prank(borrower);
      market.borrow(borrowAmount);
      vm.prank(alice);
      market.queueFullWithdrawal();
      fastForward(52 weeks);

      asset.mint(borrower, 10e18);
      vm.startPrank(borrower);
      asset.approve(address(market), 10e18);
      uint256 initBalance = asset.balanceOf(borrower); 

      asset.transfer(address(market), 10e18);
      market.closeMarket();
      uint256 finalBalance = asset.balanceOf(borrower);
      uint256 paid = initBalance - finalBalance;
      console.log(paid);

  } 

    function test_inconsistencyIssue2() external {
      parameters.annualInterestBips = 3650;
      _deposit(alice, 1e18);
      uint256 borrowAmount = market.borrowableAssets();
      vm.prank(borrower);
      market.borrow(borrowAmount);
      vm.prank(alice);
      market.queueFullWithdrawal();
      fastForward(52 weeks);

      asset.mint(borrower, 10e18);
      vm.startPrank(borrower);
      asset.approve(address(market), 10e18);
      uint256 initBalance = asset.balanceOf(borrower); 


      market.closeMarket();
      uint256 finalBalance = asset.balanceOf(borrower);
      uint256 paid = initBalance - finalBalance;
      console.log(paid);

  }
```

and the logs:

    Ran 2 tests for test/market/WildcatMarket.t.sol:WildcatMarketTest
    [PASS] test_inconsistencyIssue() (gas: 656338)
    Logs:
      800455200405885337

    [PASS] test_inconsistencyIssue2() (gas: 680537)
    Logs:
      967625143234433533

### Recommended Mitigation Steps

Always pull the funds first and refund later if needed.

**[d1ll0n (Wildcat) acknowledged and commented](https://github.com/code-423n4/2024-08-wildcat-findings/issues/62#issuecomment-2388275386):**
 > The listed functions which incur higher fees all require the current state of the market to accurately calculate relevant values to the transfer. Because of that, the transfer can't happen until after the state is updated, and it would be expensive (and too large to fit in the contract size) to redo the withdrawal payments post-transfer.
> 
> For the repay functions this is more of an issue than the others, as that represents the borrower specifically taking action to repay their debts, whereas the other functions are actions by other parties (and thus we aren't very concerned if they fail to cure the borrower's delinquency for them). We may end up just removing these secondary repay functions.

**[laurenceday (Wildcat) commented](https://github.com/code-423n4/2024-08-wildcat-findings/issues/62#issuecomment-2403678176):**
 > Resolved by [wildcat-finance/v2-protocol@e7afdc9](https://github.com/wildcat-finance/v2-protocol/commit/e7afdc9312ec672df2a9d03add18727a4c774b88).


***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | The Wildcat Protocol |
| Report Date | N/A |
| Finders | Takarez, Udsen, deadrxsezzz, 0xNirix, Infect3d, Bigsam |

### Source Links

- **Source**: https://code4rena.com/reports/2024-08-wildcat
- **GitHub**: https://github.com/code-423n4/2024-08-wildcat-findings/issues/62
- **Contest**: https://code4rena.com/reports/2024-08-wildcat

### Keywords for Search

`vulnerability`

