---
# Core Classification
protocol: generic
chain: everychain
category: interest_rate_model
vulnerability_type: accrual_ordering_error

# Pattern Identity
root_cause_family: stale_index_accounting
pattern_key: accrual_ordering_bug | interest_accrual | borrow_repay_liquidate_withdraw | stale_debt_or_phantom_interest

# Interaction Scope
interaction_scope: multi_contract
involved_contracts:
  - UToken / Market (borrow, repay)
  - LendingPair (liquidateAccount, withdrawUniPosition)
  - BorrowLogic / SupplyLogic (cache + updateState ordering)
  - CrossChainRouter (cross-chain debt mirror)
path_keys:
  - accrual_ordering_bug | borrow() | UToken→borrowIndex | credit_limit_checked_before_accrual
  - accrual_ordering_bug | liquidateAccount() | LendingPair→cumulativeInterestRate | unaccrued_self_liquidation_skips_interest
  - accrual_ordering_bug | executeRepay() | BorrowLogic→updateState | rate_updated_before_debt_update
  - accrual_ordering_bug | withdraw() | LendingPair→debtAccrual | accrued_interest_ignored_on_withdraw

# Attack Vector Details
attack_type: logical_error
affected_component: interest_accrual

# Technical Primitives
primitives:
  - accrueInterest
  - borrowIndex
  - cumulativeInterestRate
  - updateState
  - reserve.cache
  - nextBorrowIndex
  - getDebtBalance
  - accrueAccount
  - credit limit

# Grep / Hunt-Card Seeds
code_keywords:
  - accrueInterest
  - accrueAccount
  - borrowIndex
  - cumulativeInterestRate
  - updateState
  - borrowBalanceView
  - getDebtBalance
  - executeRepay
  - _accrueAccountInterest

# Impact Classification
severity: medium
impact: fund_loss
financial_impact: medium

# Context Tags
tags:
  - lending
  - interest
  - accounting
  - ordering
  - defi

# Version Info
language: solidity
version: all
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [A1] | reports/lending_borrowing_findings/h-01-borrow-must-accrueinterest-first.md | HIGH | Code4rena (Union Finance) | solodit 25592 / https://github.com/code-423n4/2021-10-union-findings/issues/66 |
| [A2] | reports/lending_borrowing_findings/h-02-lendingpairliquidateaccount-does-not-accrue-and-update-cumulativeinterestra.md | HIGH | Code4rena (Wild Credit) | solodit 468 / https://github.com/code-423n4/2021-07-wildcredit-findings/issues/122 |
| [A3] | reports/lending_borrowing_findings/m-02-lendingpairwithdrawuniposition-should-accrue-debt-first.md | MEDIUM | Code4rena (Wild Credit) | solodit 42295 |
| [A4] | reports/lending_borrowing_findings/h-04-accrued-interest-is-not-accounted-for-when-withdrawing.md | HIGH | Pashov Audit Group (Sharwa Finance) | solodit 36479 |
| [A5] | reports/lending_borrowing_findings/h-10-interest-rate-is-updated-before-updating-the-debt-when-repaying-debt.md | HIGH | Sherlock (ZeroLend One) | solodit 41820 / https://github.com/sherlock-audit/2024-06-new-scope-judging/issues/413 |
| [A6] | reports/lending_borrowing_findings/fees-are-wrongly-accrued-when-reducing-collateral.md | HIGH | Zokyo (Filament) | solodit 45604 |
| [A7] | reports/lending_borrowing_findings/h-26-cross-chain-debt-accrues-incorrectly.md | HIGH | Sherlock (LEND) | solodit 58395 |

## Missing Interest Accrual and Stale Index Accounting

**State-changing lending operations (borrow, repay, withdraw, liquidate) that read debt, credit limits, or rate inputs BEFORE accruing interest act on a stale index — letting borrowers exceed limits, skip accrued interest, or mint phantom interest to suppliers.**

### Overview

Every money-market operation must first bring the interest index up to date. Seven unique findings (6 HIGH, 1 MEDIUM; severity set to the lowest unique rating) from 4 audit firms show the ordering bug in both directions: checks-before-accrual (Union Finance `borrow` validating the credit limit against `borrowBalanceView` before `accrueInterest` — borrowers exceed `maxBorrow` in quiet markets), accrual-skipping on action paths (Wild Credit `liquidateAccount` calling `_accrueAccountInterest` without updating `cumulativeInterestRate` — an underwater borrower self-liquidates instead of repaying and skips the interest; Sharwa withdrawals ignoring accrued interest; Wild Credit `withdrawUniPosition` before debt accrual), update-order inversions (ZeroLend `executeRepay` updating the interest rate before the debt, so suppliers accrue interest on repaid debt — even with zero outstanding borrows; Filament fee accrual on collateral reduction), and cross-chain mirrors accruing independently (LEND).

#### Agent Quick View

- Root cause statement: "This vulnerability exists because a state-changing operation validates or mutates debt/rate state using a stale interest index — accrual is skipped, ordered after the check, or applied to pre-update balances — so limits are checked against outdated debt and interest is either skipped by borrowers or over-accrued to suppliers."
- Pattern key: `accrual_ordering_bug | interest_accrual | borrow_repay_liquidate_withdraw | stale_debt_or_phantom_interest`
- Interaction scope: `multi_contract`
- Primary affected component(s): `accrual call sites in borrow/repay/withdraw/liquidate flows`
- Contracts / modules involved: `UToken/Market, LendingPair, BorrowLogic/SupplyLogic, CrossChainRouter debt mirror`
- Path keys: `credit_limit_checked_before_accrual`, `unaccrued_self_liquidation_skips_interest`, `rate_updated_before_debt_update`, `accrued_interest_ignored_on_withdraw`
- High-signal code keywords: `accrueInterest`, `borrowIndex`, `cumulativeInterestRate`, `updateState`, `borrowBalanceView`
- Severity: MEDIUM — 6/7 unique findings rated HIGH, 1 MEDIUM; family severity is the lowest unique rating (MEDIUM) per severity policy
- Typical sink / impact: `over-borrowing past limits, skipped interest payments, phantom supplier interest, wrong utilization/rates`
- Validation strength: `strong` (7 unique findings, 4 independent audit firms — Code4rena, Pashov, Sherlock, Zokyo — across 6 protocols)

#### Contract / Boundary Map

- Entry surface(s): `borrow()`, `executeRepay()`, `liquidateAccount()`, `withdraw()` / `withdrawUniPosition()`, collateral reduction
- Contract hop(s): `UToken.borrow -> borrowBalanceView (old index) -> accrueInterest` ; `LendingPair.liquidateAccount -> _accrueAccountInterest (no rate update)` ; `BorrowLogic.executeRepay -> reserve.updateState (rate) -> debt update`
- Trust boundary crossed: `time-based state (index) vs transaction-local state`, `cross-chain debt mirror sync`
- Shared state or sync assumption: `any read of debt/limit/rate must be preceded by accrual to the current timestamp in the same call`

#### Valid Bug Signals

- Signal 1: A require/comparison over debt or credit-limit values appears textually BEFORE the `accrueInterest`/`updateState` call in the same function.
- Signal 2: An action path calls a partial accrual helper that updates user balances but not the global rate/index (or vice versa).
- Signal 3: Interest-bearing state is mutated while the cache (`nextBorrowIndex`, `cumulativeInterestRate`) reflects a pre-mutation snapshot, then feeds the rate update.

#### False Positive Guards

- Not this bug when: the market uses lazy-accrual-with-strict-CEI and every external read path (`balanceOf`-equivalents) accrues internally (Compound-style `exchangeRateCurrent` semantics) — verify the actual read, not just the writer.
- Not this bug when: dust-level interest between blocks is the only delta (same-block operations) — the bug bites in low-activity markets with long accrual gaps.
- Safe if: the first statement of every state-changing function is accrual (or the entry router accrues for all touched reserves).
- Cross-link guard: rate-model math errors (utilization formulas, wrong reserves) are a different pattern — see `DB/general/lending-rate-model/LENDING_RATE_MODEL_VULNERABILITIES.md`.

### Vulnerability Description

#### Root Cause

1. **Check before accrual** [A1]: Union Finance `UToken.borrow` runs `require(borrowBalanceView(msg.sender) + amount + fee <= maxBorrow)` and the credit-limit check with the OLD `borrowIndex`; `accrueInterest()` only runs afterward. In low-activity markets the gap between accruals is long, so borrowers exceed both `maxBorrow` and their credit limit. Judge: "fundamentally breaks the accounting of the protocol."
2. **Partial accrual on liquidation** [A2]: Wild Credit `liquidateAccount` calls `_accrueAccountInterest` which does NOT update `cumulativeInterestRate`; an underwater borrower self-liquidates and skips all interest accrued since the last global accrual (cheaper than repaying).
3. **Withdraw ignores accrued interest** [A3][A4]: Wild Credit `withdrawUniPosition` and Sharwa withdrawals operate before debt/interest accrual — accounting reads stale amounts.
4. **Rate updated before debt** [A5]: ZeroLend `BorrowLogic.executeRepay` computes new rates from the cached (pre-repay) total debt — suppliers keep accruing interest on already-repaid debt, even when borrows drop to zero; users can withdraw more than entitled at other suppliers' expense.
5. **Fee accrual on the wrong event** [A6]: Filament accrues fees when collateral is reduced instead of on debt-bearing state.
6. **Cross-chain divergence** [A7]: LEND cross-chain debt accrues incorrectly (mirror indexes out of sync with the source chain).

#### Attack Scenario / Path Variants

**Path A: Borrow against a stale index** [A1]
Path key: `accrual_ordering_bug | borrow() | UToken→borrowIndex | credit_limit_checked_before_accrual`
Entry surface: `borrow(amount)`
Contracts touched: `UToken -> borrowIndex`
Boundary crossed: `time-based index vs call-local check`
1. Borrower takes a loan; market is quiet — no `accrueInterest` for weeks.
2. Accrued interest has raised true debt well above the last index snapshot.
3. `borrow` validates against the stale snapshot; the borrower draws funds beyond `maxBorrow`/credit limit.
4. **Impact**: undercollateralized borrowing; accounting breaks.

**Path B: Self-liquidate to skip interest** [A2]
Path key: `accrual_ordering_bug | liquidateAccount() | LendingPair→cumulativeInterestRate | unaccrued_self_liquidation_skips_interest`
Entry surface: `liquidateAccount` (from an associate of the borrower)
Contracts touched: `LendingPair -> cumulativeInterestRate`
Boundary crossed: `user-level accrual vs market-level accrual`
1. Borrower is underwater with interest accrued since the last global accrual.
2. Instead of `repay` (which would accrue), they trigger `liquidateAccount`.
3. Only `_accrueAccountInterest` runs — the market `cumulativeInterestRate` stays stale.
4. The liquidation clears debt without paying the accrued interest slice.
5. **Impact**: interest revenue lost to lenders; liquidation cheaper than repayment.

**Path C: Rate update on pre-repay debt** [A5]
Path key: `accrual_ordering_bug | executeRepay() | BorrowLogic→updateState | rate_updated_before_debt_update`
Entry surface: `repay()`
Contracts touched: `BorrowLogic -> reserve.updateState -> rate model`
Boundary crossed: `operation ordering within one call`
1. User repays the entire debt; `updateState` computes the new interest rate BEFORE the debt subtraction.
2. Utilization and supply rate still reflect the old (higher) total borrows.
3. Suppliers accrue interest as if the debt still existed — with zero outstanding borrows.
4. **Impact**: phantom supplier yield funded by other suppliers / reserves; withdrawal over-entitlement.

#### Vulnerable Pattern Examples

**Example 1: Credit limit checked before accrual (Union Finance)** [HIGH]
```solidity
// ❌ VULNERABLE: both checks use the old borrowIndex
function borrow(uint256 amount, ...) external {
    require(borrowBalanceView(msg.sender) + amount + fee <= maxBorrow, "UToken: amount large than borrow size max"); // @audit stale
    require(uint256(_getCreditLimit(msg.sender)) >= amount + fee, "UToken: The loan amount plus fee is greater than credit limit"); // @audit stale
    require(accrueInterest(), "UToken: accrue interest failed"); // accrual AFTER checks
}
```

**Example 2: Liquidation without market-rate accrual (Wild Credit)** [HIGH]
```solidity
// ❌ VULNERABLE: partial accrual — user balances updated, market rate not
function liquidateAccount(...) external {
    _accrueAccountInterest(liquidatee); // @audit does NOT update cumulativeInterestRate
    // ... seize/repay using stale cumulativeInterestRate
}
// Fix: call accrueAccount() (user + market accrual) first.
```

**Example 3: Rate computed from pre-repay debt (ZeroLend One)** [HIGH]
```solidity
// ❌ VULNERABLE: rate update uses cached debt before the repay mutates it
function executeRepay(...) external returns (DataTypes.SharesType memory payback) {
    DataTypes.ReserveCache memory cache = reserve.cache(totalSupplies);
    reserve.updateState(params.reserveFactor, cache); // @audit rates updated on PRE-repay debt
    payback.assets = balances.getDebtBalance(cache.nextBorrowIndex);
    // ... debt reduced only after the rate snapshot
}
```

### Impact Analysis

#### Technical Impact

- Borrowing beyond limits/credit lines (1/7 unique findings: A1)
- Skipped interest via unaccrued liquidation/withdrawal paths (3/7: A2, A3, A4)
- Phantom supplier interest and wrong utilization/rates from update-order inversions (2/7: A5, A6)
- Cross-chain debt divergence (1/7: A7)

#### Business Impact

- Quiet markets are the attack window: longer gaps between natural accruals magnify the stale delta (Union judge note)
- Lender revenue leakage and cross-supplier transfers (ZeroLend PoC shows over-withdrawal at other suppliers' expense)

#### Affected Scenarios

- Low-activity markets / long-tail assets with sparse transactions
- Protocols with per-user lazy accrual but global rate variables
- Repay/withdraw/liquidate flows assembled from helpers with mixed accrual responsibility
- Cross-chain deployments mirroring debt without synchronizing accrual timestamps

### Secure Implementation

**Fix 1: Accrue first, act second (Union fix)**
```solidity
// ✅ SECURE: accrual is the first statement of every state-changing entry
function borrow(uint256 amount, ...) external {
    require(accrueInterest(), "UToken: accrue interest failed"); // FIRST
    require(borrowBalanceView(msg.sender) + amount + fee <= maxBorrow, "...");
    require(uint256(_getCreditLimit(msg.sender)) >= amount + fee, "...");
    // ...
}
```

**Fix 2: Accrual helpers update both levels (Wild Credit fix)**
```solidity
// ✅ SECURE: action paths use the full accrual
function liquidateAccount(...) external {
    accrueAccount(liquidatee); // user balances AND market cumulativeInterestRate
    // ...
}
```

**Fix 3: Mutate debt before computing rates (ZeroLend fix)**
```solidity
// ✅ SECURE: repay mutates total debt, then rates reflect post-action utilization
function executeRepay(...) external returns (DataTypes.SharesType memory payback) {
    DataTypes.ReserveCache memory cache = reserve.cache(totalSupplies);
    payback.assets = balances.getDebtBalance(cache.nextBorrowIndex);
    _reduceDebt(totalSupplies, params.amount, cache); // debt FIRST
    reserve.updateState(params.reserveFactor, cache); // rates SECOND
}
```

### Detection Patterns

#### Contract / Call Graph Signals
```
- debt/limit comparisons or rate computations textually preceding accrueInterest/updateState in the same function
- two accrual helpers (user-level vs market-level) where action paths call the weaker one
- caches built before a mutation but consumed by a rate/index update after it
- cross-chain debt mirrors with independent accrual timestamps
```

#### High-Signal Grep Seeds
```
- accrueInterest
- accrueAccount
- _accrueAccountInterest
- borrowIndex
- cumulativeInterestRate
- updateState
- borrowBalanceView
- getDebtBalance
```

#### Code Patterns to Look For
```
- Pattern 1: `require(borrowBalanceView(...) + amount <= max` appearing above `accrueInterest()`
- Pattern 2: `liquidate` calling `_accrueAccount*` (partial) instead of `accrueAccount` (full)
- Pattern 3: `updateState(...)` before the debt mutation in repay/liquidate handlers
- Pattern 4: withdraw paths reading debt balances without any accrual call in scope
```

#### Audit Checklist
- [ ] For each of borrow/repay/withdraw/liquidate: which line accrues, and does any earlier line read debt or limits?
- [ ] Do partial accrual helpers exist, and do action paths use them?
- [ ] Are rate updates computed from pre- or post-mutation total debt?
- [ ] In cross-chain setups, do both chains accrue from the same timestamp source?

### Real-World Examples

#### Known Exploits
- Stale-index over-borrowing is a recurring precondition in lending incidents; the rate-side mechanics are covered in `DB/general/lending-rate-model/LENDING_RATE_MODEL_VULNERABILITIES.md` Section 4.

#### Related CVEs/Reports
- Code4rena 2021-10-union issue #66 (judge: "fundamentally breaks the accounting")
- Sherlock 2024-06-new-scope issue #413 (14 finders — strong consensus)

### Prevention Guidelines

#### Development Best Practices
1. Make accrual the first (non-reentrant) statement of every state-changing market function; route-level multi-asset accrual for batch operations.
2. Maintain exactly one accrual helper with full semantics; forbid partial-accrual helpers from action paths.
3. Order operations: mutate quantities, then update indexes/rates from post-mutation state.

#### Testing Requirements
- Unit tests for: borrow after long `vm.warp` (stale window) must revert past limit; self-liquidation pays accrued interest; repay-to-zero stops supplier accrual immediately
- Property tests: debt reads are monotonic in timestamps across all entry points
- Fuzzing targets: interleavings of warp + operations asserting `totalDebt == Σ userDebt` at all times

### References

#### Technical Documentation
- Compound V2 accrual semantics (`accrueInterest` in every accrue-then-interact entry)
- Aave V3 `updateState` usage ordering

#### Security Research
- cmichel's Wild Credit finding (quality 5/5 — model report for this pattern)
- Sherlock ZeroLend issue #413 (update-order inversion)

### Keywords for Search

`accrueInterest`, `stale index`, `borrowIndex`, `accrual ordering`, `interest accrual`, `cumulativeInterestRate`, `updateState`, `credit limit stale`, `over-borrow`, `skip interest`, `self liquidation interest`, `phantom interest`, `suppliers accrue`, `repay ordering`, `cross-chain debt accrual`, `lazy accrual`, `stale debt`, `interest index`

### Related Vulnerabilities

- [Liquidation Seizure Economics Miscalculation](../liquidation/liquidation-seizure-economics.md)
- [Self-Liquidation Abuse](../liquidation/self-liquidation-abuse.md)
- `DB/general/lending-rate-model/LENDING_RATE_MODEL_VULNERABILITIES.md` (rate-model math — distinct from ordering bugs)
