---
# Core Classification
protocol: generic
chain: everychain
category: liquidation
vulnerability_type: bad_debt_handling

# Pattern Identity
root_cause_family: missing_bad_debt_settlement
pattern_key: unhandled_bad_debt | pool_accounting | collateral_exhaustion | loss_not_socialized

# Interaction Scope
interaction_scope: multi_contract
involved_contracts:
  - LendingPool / Pair
  - LiquidationLogic
  - SupplyLogic (withdraw)
  - DebtToken / share accounting
  - StabilityPool / reserve
path_keys:
  - unhandled_bad_debt | liquidate() | LiquidationLogic→Pool | bad_debt_never_marked_off
  - unhandled_bad_debt | withdraw() | SupplyLogic→liquidityIndex | loss_not_shared_last_withdrawer_loses
  - unhandled_bad_debt | withdrawLiquidityAndClaim() | Collateral→Pool | collateral_exit_without_debt_check
  - unhandled_bad_debt | batchLiquidate() | Liquidation→DebtToken | redistribution_skips_later_batches

# Attack Vector Details
attack_type: logical_error
affected_component: solvency_accounting

# Technical Primitives
primitives:
  - badDebt
  - totalAssets
  - liquidityIndex
  - supplyShares
  - liquidateClean
  - debt socialization
  - reserve settlement
  - interest accrual on defaulted debt
  - collateralRatio check

# Grep / Hunt-Card Seeds
code_keywords:
  - liquidateClean
  - badDebt
  - totalAssets
  - liquidityIndex
  - withdrawLiquidityAndClaim
  - batchLiquidate
  - executeCrossLiquidateERC20
  - _getDebtAmount
  - maxWithdrawableCollateral

# Impact Classification
severity: high
impact: fund_loss
financial_impact: high

# Context Tags
tags:
  - lending
  - bad_debt
  - insolvency
  - liquidation
  - defi

# Version Info
language: solidity
version: all
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [B1] | reports/lending_borrowing_findings/h-02-liquidate-doesnt-mark-off-bad-debt-leading-to-a-last-lender-to-withdraw-los.md | HIGH | Code4rena (Frax Finance) | solodit 24829 / https://github.com/code-423n4/2022-08-frax-findings/issues/141 |
| [B2] | reports/lending_borrowing_findings/h-05-bad-debt-is-never-handled-which-places-insolvency-risks-on-benddao.md | HIGH | Code4rena (BendDAO) | solodit 36879 / https://github.com/code-423n4/2024-07-benddao-findings/issues/23 |
| [B3] | reports/lending_borrowing_findings/h-09-bad-debts-should-not-continue-to-accrue-interest.md | HIGH | Code4rena (JPEG'd) | solodit 1915 |
| [B4] | reports/lending_borrowing_findings/bad-debt-redistribution-not-happening-between-liquidations-in-batch-mode.md | HIGH | Cantina (Bima) | solodit 46267 |
| [B5] | reports/lending_borrowing_findings/collateral-can-be-withdrawn-without-repaying-usds-loan.md | HIGH | TrailOfBits (Salty.IO) | solodit 29617 |
| [B6] | reports/lending_borrowing_findings/h-7-when-bad-debt-is-accumulated-the-loss-is-not-shared-amongst-all-suppliers-in.md | HIGH | Sherlock (ZeroLend One) | solodit 41817 / https://github.com/sherlock-audit/2024-06-new-scope-judging/issues/275 |
| [B7] | reports/lending_borrowing_findings/h-01-collateral-can-be-claimed-back-without-repaying-its-corresponding-loan-due-.md | HIGH | Code4rena (Lavarage) | solodit 33176 |
| [B8] | reports/lending_borrowing_findings/m-03-users-can-prevent-absorbing-bad-debt-by-sandwiching-liquidations.md | MEDIUM | Pashov Audit Group (Roots) | solodit 55119 |
| [B9] | reports/lending_borrowing_findings/h-2-reserves-can-be-stolen-by-settling-artificially-created-bad-debt-from-them.md | HIGH | Sherlock (Ajna #2) | solodit 27652 |
| [B10] | reports/lending_borrowing_findings/m-04-liquidationoperationsbatchliquidatetroves-redistributes-bad-debt-and-collat.md | MEDIUM | Recon Audits (Apollon) | solodit 53844 |

## Bad Debt Socialization and Missing Write-Off

**When collateral is exhausted and debt remains, the pool must write off and socialize the loss immediately — protocols that skip the write-off, keep accruing interest on dead debt, or let borrowers exit collateral without repaying convert insolvency into a last-lender-loses bank run.**

### Overview

Bad debt is the terminal state of a lending market: collateral value < debt, no liquidator profit exists, and someone must eat the shortfall. Ten unique findings (8 HIGH, 2 MEDIUM) from 8 audit firms show the recurring failure shapes: the liquidation path never marks bad debt off the pool's `totalAssets` (Frax), withdrawal math (`shares * liquidityIndex`) ignores realized losses so early withdrawers escape at par while the last withdrawers absorb everything (ZeroLend), defaulted debt keeps accruing interest and even mints new stablecoin (JPEG'd), batch liquidations forget to redistribute to later batches (Bima, Apollon), and open collateral-exit functions let borrowers remove collateral while keeping the loan (Salty, Lavarage) — creating bad debt on demand.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because the pool accounting never writes off unbacked debt when collateral is exhausted (or lets collateral exit without debt repayment), so the loss is silently held in inflated `totalAssets`/`liquidityIndex`, interest keeps compounding on dead debt, and early withdrawers drain real assets leaving the last lenders insolvent."
- Pattern key: `unhandled_bad_debt | pool_accounting | collateral_exhaustion | loss_not_socialized`
- Interaction scope: `multi_contract`
- Primary affected component(s): `pool solvency accounting, liquidation finalization, withdraw path`
- Contracts / modules involved: `LendingPool, LiquidationLogic, SupplyLogic, DebtToken, StabilityPool/reserve`
- Path keys: `bad_debt_never_marked_off`, `loss_not_shared_last_withdrawer_loses`, `collateral_exit_without_debt_check`, `redistribution_skips_later_batches`
- High-signal code keywords: `liquidateClean`, `badDebt`, `totalAssets`, `liquidityIndex`, `withdrawLiquidityAndClaim`
- Severity: HIGH — 8/10 unique findings rated HIGH, 2 MEDIUM; lowest unique rating MEDIUM, dominant consensus HIGH
- Typical sink / impact: `insolvent pool, withdrawal bank run, unbacked stablecoin minting, reserve theft`
- Validation strength: `strong` (10 unique findings, 8 independent audit firms — Code4rena, Cantina, TrailOfBits, Sherlock, Pashov, Recon — across 10 protocols)

#### Contract / Boundary Map

- Entry surface(s): `liquidate()` / `liquidateClean()`, `withdraw()`, `withdrawLiquidityAndClaim()`, `claimCollateral()`, `batchLiquidate()`
- Contract hop(s): `LiquidationLogic -> Pool totalAssets`; `SupplyLogic.withdraw -> shares * liquidityIndex`; `Collateral.withdrawCollateralAndClaim -> withdrawLiquidityAndClaim (public bypass)`; `NFTVault liquidation -> stablecoin.burnFrom`
- Trust boundary crossed: `internal solvency assumption vs external collateral value`, `public vs internal function visibility`
- Shared state or sync assumption: `totalAssets == real recoverable assets`; `share price must reflect realized losses at the moment they occur, not at the moment liquidity runs out`

#### Valid Bug Signals

- Signal 1: Liquidation transfers all remaining collateral but leaves `userDebt > 0` with no code path that reduces pool-level `totalAssets`/`totalBorrows` by the shortfall.
- Signal 2: Withdrawal payout is `shares * liquidityIndex` where `liquidityIndex` never absorbs bad debt; the pool has no `badDebt` accumulator at all.
- Signal 3: A public function moves collateral/liquidity out without invoking the collateralization check used by its sibling wrapper.

#### False Positive Guards

- Not this bug when: the protocol has an explicit bad-debt mechanism — treasury coverage documented in-scope, a socialization step in the liquidation finalizer, or a `badDebt` accumulator that decrements `totalAssets` atomically (Aave-style reserve write-off).
- Not this bug when: the "loss" is only unrealized mark-to-market variance that ordinary interest spread covers.
- Safe if: every path that removes collateral (withdraw, claim, auction settlement) reverts when outstanding debt would exceed remaining collateral value.
- Dust guard: near-zero residual debt on closed positions is typically dust accounting, not socialization failure — check whether withdrawers can extract value above par before flagging.

### Vulnerability Description

#### Root Cause

1. **No write-off on liquidation** [B1]: Frax `liquidate()` pays the liquidator from collateral but never marks the unbacked remainder off `totalAssets.amount`; `liquidateClean()` (which would) has no economic incentive to call, especially with near-zero collateral left.
2. **Withdraw math ignores realized losses** [B6]: ZeroLend `SupplyLogic.withdraw` computes `amount = shares * liquidityIndex`; the index only tracks interest, never bad debt, so first withdrawers exit at par while the pool silently went insolvent.
3. **No mechanism at all** [B2]: BendDAO — ERC20 partial liquidation clears debt only up to available collateral and further liquidation reverts (no collateral left); ERC721 liquidation is unprofitable below debt; nothing reduces the outstanding debt; withdrawals then depend on liquidity that never returns.
4. **Interest accrues on dead debt** [B3]: JPEG'd NFTVault requires the liquidator to repay the FULL `debtAmount` to take the NFT; once the NFT is worth less than debt, nobody liquidates, the debt keeps compounding at 10% APR, and each DAO interest collection mints new unbacked stablecoin.
5. **Batch redistribution gap** [B4][B10]: Bima — bad-debt redistribution between liquidations doesn't happen in batch mode; Apollon — `batchLiquidateTroves` redistributes bad debt and collateral only across the troves in the current batch, not the ones later in the list.
6. **Collateral exit without debt check** [B5][B7]: Salty `withdrawLiquidityAndClaim` is public with no collateralization check (the check lives only in the `withdrawCollateralAndClaim` wrapper); Lavarage lets collateral be claimed back without repaying the corresponding loan.
7. **Loss-dodging by sandwiching** [B8]: Roots — users front-run their own bad-debt absorption by sandwiching liquidations so other suppliers take the loss.
8. **Artificial bad debt drains reserves** [B9]: Ajna — settling artificially created bad debt draws from reserves, letting an attacker extract reserve value.

#### Attack Scenario / Path Variants

**Path A: Last lender to withdraw loses** [B1][B6]
Path key: `unhandled_bad_debt | withdraw() | SupplyLogic→liquidityIndex | loss_not_shared_last_withdrawer_loses`
Entry surface: `withdraw()` after collateral crash
Contracts touched: `SupplyLogic -> DebtToken -> Pool cash`
Boundary crossed: `solvency assumption behind share pricing`
1. Pair holds 10 lenders × $1k; borrower's collateral crashes to $7k value.
2. A liquidator seizes the $7k; `totalAssets` still reads $10k + interest (no write-off).
3. Six lenders redeem at par; the 7th gets partial; the last three get nothing.
4. **Impact**: value transfer from slow lenders to fast ones; bank-run incentive.

**Path B: Collateral exit bypasses debt check** [B5]
Path key: `unhandled_bad_debt | withdrawLiquidityAndClaim() | Collateral→Pool | collateral_exit_without_debt_check`
Entry surface: public `withdrawLiquidityAndClaim(tokenA, tokenB, ...)`
Contracts touched: `Collateral -> Pool._decreaseUserShare -> pools.removeLiquidity`
Boundary crossed: `function visibility (wrapper check bypassed)`
1. Borrower holds USDS debt backed by WBTC/WETH collateral shares.
2. Instead of `withdrawCollateralAndClaim` (which enforces `collateralToWithdraw <= maxWithdrawableCollateral`), the borrower calls `withdrawLiquidityAndClaim` directly.
3. Collateral leaves the protocol; the USDS loan remains outstanding and now unbacked.
4. **Impact**: instant bad debt creation, repeatable.

**Path C: Dead debt compounds and mints** [B3]
Path key: `unhandled_bad_debt | liquidation (skipped) | NFTVault→stablecoin | interest_on_dead_debt`
Entry surface: nobody liquidates (unprofitable)
Contracts touched: `NFTVault accrual -> DAO interest collection -> stablecoin mint`
Boundary crossed: `debt ceiling vs real asset backing`
1. NFT worth $30k backs $10k borrowed (limit 60%/50%); NFT drops to $10k.
2. Liquidator would need to repay $11k (debt + interest) for a $10k NFT — never happens.
3. Debt keeps accruing 10% APR; every DAO interest collection mints new stablecoin against it.
4. **Impact**: unbacked stablecoin supply; depeg pressure.

**Path D: Batch redistribution misses later troves** [B4][B10]
Path key: `unhandled_bad_debt | batchLiquidate() | Liquidation→DebtToken | redistribution_skips_later_batches`
Entry surface: `batchLiquidate(troves[])`
Contracts touched: `LiquidationLogic -> batch loop -> DebtToken`
Boundary crossed: `loop-boundary accounting`
1. Operator liquidates a batch of underwater troves; shortfall redistribution is computed only within the current batch.
2. Troves later in the queue (or in the next batch) never receive their share of the bad debt.
3. Accounting diverges from the socialization invariant.
4. **Impact**: uneven loss allocation; exploitable ordering (see [B8] sandwich).

#### Vulnerable Pattern Examples

**Example 1: Withdraw at index that never absorbed losses (ZeroLend One)** [HIGH]
```solidity
// ❌ VULNERABLE: liquidityIndex tracks interest only — bad debt never enters the formula
function executeWithdraw(..., DataTypes.ExecuteWithdrawParams memory params) internal {
    // ...
    uint256 amountToWithdraw = params.shares.rayMul(cache.nextLiquidityIndex); // @audit insolvent pool pays par
    if (amountToWithdraw > userBalance) revert();
    // no check: pool cash vs totalAssets (bad debt unaccounted)
}
```

**Example 2: Public path skips the wrapper's collateral check (Salty)** [HIGH]
```solidity
// ❌ VULNERABLE: check lives in the wrapper only; inner function is public
function withdrawCollateralAndClaim(uint256 collateralToWithdraw, ...) public returns (...) {
    require(userShareForPool(msg.sender, collateralPoolID) > 0, "User does not have any collateral");
    require(collateralToWithdraw <= maxWithdrawableCollateral(msg.sender), "Excessive collateralToWithdraw"); // @audit bypassed below
    (reclaimedWBTC, reclaimedWETH) = withdrawLiquidityAndClaim(wbtc, weth, collateralToWithdraw, ...);
}
// attacker calls withdrawLiquidityAndClaim() directly — no collateralization check inside
```

**Example 3: Full-repay requirement strands dead debt (JPEG'd)** [HIGH]
```solidity
// ❌ VULNERABLE: liquidator must repay the ENTENT debt to take collateral worth less
uint256 debtAmount = _getDebtAmount(_nftIndex);
require(debtAmount >= _getLiquidationLimit(_nftIndex), "position_not_liquidatable");
stablecoin.burnFrom(msg.sender, debtAmount); // @audit nobody pays 11k for a 10k NFT -> debt accrues forever
```

**Example 4: Batch loop forgets later troves (Apollon)** [MEDIUM]
```solidity
// ❌ VULNERABLE: redistribution computed only within the current batch
function batchLiquidateTroves(address[] calldata troves) external {
    for (uint256 i; i < troves.length; ++i) {
        // shortfall socialized across THIS batch's troves only — troves later in the list never absorb
    }
}
```

### Impact Analysis

#### Technical Impact

- Insolvent pools with par-paying withdrawals until cash runs out (3/10 unique findings: B1, B6, B2)
- Unbacked debt compounding and, in CDP designs, unbacked stablecoin minting (1/10: B3)
- On-demand bad-debt creation via unchecked collateral exit (2/10: B5, B7)
- Uneven/arbitrary loss allocation across suppliers and reserve theft (3/10: B4, B8, B9, B10)

#### Business Impact

- Bank-run dynamics: sophisticated lenders monitor solvency and exit first, retail absorbs the loss
- Stablecoin depeg risk when interest keeps minting against dead debt (JPEG'd)
- Treasury drain when reserves are the settlement layer for artificial bad debt (Ajna)

#### Affected Scenarios

- Collateral price crashes that push positions past full liquidation value
- NFT/ERC721 collateral where partial liquidation is impossible
- P2P pair lending without a global pool bad-debt accumulator
- Batch liquidation operations with per-batch accounting
- Protocols exposing low-level liquidity/collateral movement functions publicly

### Secure Implementation

**Fix 1: Atomic write-off when collateral is exhausted (Aave-style)**
```solidity
// ✅ SECURE: shortfall reduces totalAssets immediately at liquidation finalization
uint256 badDebt = vars.userDebt - vars.actualDebtRepaidFromCollateral;
if (badDebt > 0) {
    // socialize across suppliers via the index, or book to a reserve, but do it NOW:
    IDebtToken(debtToken).burn(user, vars.userDebt);
    reserve.accumulateBadDebt(badDebt); // or cache.nextLiquidityIndex -= lossPerShare
    emit BadDebtWrittenOff(user, badDebt);
}
```

**Fix 2: Every collateral-exit path re-checks outstanding debt**
```solidity
// ✅ SECURE: the check lives in the innermost fund-moving function
function withdrawLiquidityAndClaim(IERC20 tokenA, IERC20 tokenB, uint256 amount, ...) public nonReentrant {
    _decreaseUserShare(msg.sender, poolID, amount);
    require(amount <= maxWithdrawableCollateral(msg.sender), "Excessive withdrawal"); // @audit fix: enforce here
    (reclaimedA, reclaimedB) = pools.removeLiquidity(...);
}
```

**Fix 3: Stop accruing and start marking (JPEG'd fix)**
```solidity
// ✅ SECURE: track bad debt explicitly; reward marking; accrue interest on live debt only
if (_isBadDebt(_nftIndex)) {
    totalBadDebt += debtAmount;             // excluded from interest accrual
    stablecoinMinting.skip(debtAmount);     // no minting against dead debt
}
function markBadDebt(uint256 nftIndex) external { _markIfBadDebt(nftIndex); rewardMark(msg.sender); }
```

**Fix 4: Socialize across ALL suppliers, not the current batch**
```solidity
// ✅ SECURE: global accumulator, batch-agnostic
function batchLiquidateTroves(address[] calldata troves) external {
    uint256 totalShortfall;
    for (...) { totalShortfall += _liquidateOne(troves[i]); }
    if (totalShortfall > 0) _socializeLoss(totalShortfall); // decrements every supplier's claim via index
}
```

### Detection Patterns

#### Contract / Call Graph Signals
```
- liquidation finalizer transfers collateral but no path decrements pool totalAssets/totalBorrows by shortfall
- withdraw payout = f(shares, liquidityIndex) with no badDebt state anywhere in the codebase
- public/internal function that moves collateral or liquidity out, whose safety check exists only in a wrapper
- interest accrual loops over totalDebt including positions with zero remaining collateral
- batch operations that redistribute losses only among their own elements
```

#### High-Signal Grep Seeds
```
- liquidateClean
- badDebt
- totalAssets
- liquidityIndex
- withdrawLiquidityAndClaim
- batchLiquidate
- maxWithdrawableCollateral
- executeCrossLiquidateERC20
- burnFrom
```

#### Code Patterns to Look For
```
- Pattern 1: `shares.rayMul(liquidityIndex)` payout with zero occurrences of a bad-debt accumulator
- Pattern 2: `require(amount <= maxWithdrawableCollateral(...))` present in one entry, absent in the sibling entry that moves the same funds
- Pattern 3: `stablecoin.burnFrom(msg.sender, debtAmount)` as the only liquidation mode (full-repay-only)
- Pattern 4: `for (uint256 i; i < batch.length; ++i)` around loss redistribution
- Pattern 5: `totalBorrows += interest` with no `if (collateral == 0) skip` branch
```

#### Audit Checklist
- [ ] Trace collateral-to-zero: when a position's collateral hits 0 with debt remaining, which storage variable changes, in which function, atomically with what?
- [ ] Does any withdrawal path let a user exit collateral while debt stays outstanding?
- [ ] Is interest accrual excluded for positions flagged/known bad? Does anything mint against them?
- [ ] Do batch/ multicall liquidations socialize losses globally or only within the batch?
- [ ] Simulate: pool insolvent by X — first withdrawer gets par? Then the mechanism is missing.

### Real-World Examples

#### Known Exploits
- Platypus (2023, $10.5M) — flash-loan-created bad debt the liquidation/solvency layer failed to price (see `DB/general/defihacklabs-business-logic-2023-patterns.md` Pattern 8).
- BendDAO (2022) NFT-collateral bad debt episode — unprofitable ERC721 liquidations froze withdrawals market-wide (context for [B2]).

#### Related CVEs/Reports
- Code4rena 2022-08-frax issue #141 (judge-kept HIGH for `liquidate()` no-write-off)
- Sherlock 2024-06-new-scope issue #275 (ZeroLend loss-socialization)

### Prevention Guidelines

#### Development Best Practices
1. Bad debt is a state, not an event to ignore: write it off atomically at the moment collateral exhausts — socialize via index or book to a visible reserve.
2. Every function that moves collateral or liquidity out must independently enforce the debt-safety check (defense in depth against visibility mistakes).
3. Exclude dead debt from interest accrual and from any minting path.
4. Make loss socialization global and order-independent; property-test it with adversarial batch orderings.

#### Testing Requirements
- Unit tests for: collateral-to-zero liquidation decrements totalAssets by exactly the shortfall; direct call to inner withdraw functions reverts when debt outstanding
- Integration tests for: batch liquidation with troves split across batches; withdrawal racing after insolvency
- Fuzzing targets: invariant `sum(supplier claims) <= real recoverable assets` after arbitrary liquidation sequences

### References

#### Technical Documentation
- Aave V2 bad debt settlement (treasury + index socialization history)
- MakerDAO MCD `sin` (bad debt) queue design

#### Security Research
- TrailOfBits Salty.IO report (visibility-based collateral exit)
- Cantina Bima review (batch-mode redistribution)

### Keywords for Search

`bad debt`, `bad debt socialization`, `insolvency`, `last lender loses`, `write-off`, `unbacked debt`, `liquidityIndex loss`, `totalAssets overstated`, `collateral exit without repay`, `withdrawLiquidityAndClaim`, `bank run`, `unbacked stablecoin mint`, `batch liquidation redistribution`, `reserve theft`, `dead debt interest`, `liquidateClean`, `undercollateralized withdrawal`, `insolvent pool`

### Related Vulnerabilities

- [Liquidation Evasion and Borrower-Triggered Liquidation DoS](../liquidation/liquidation-evasion-dos.md)
- [Liquidation Seizure Economics Miscalculation](../liquidation/liquidation-seizure-economics.md)
- [Health Factor and Collateral Ratio Miscalculation](../risk-params/health-factor-miscalculation.md)
- `DB/general/business-logic/defi-business-logic-flaws.md` (Category 5: insolvency/HF bypasses, exploit-side)
