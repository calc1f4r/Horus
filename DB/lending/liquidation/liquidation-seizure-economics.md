---
# Core Classification
protocol: generic
chain: everychain
category: liquidation
vulnerability_type: incorrect_seizure_calculation

# Pattern Identity
root_cause_family: liquidation_math_error
pattern_key: wrong_liquidation_amount_math | liquidation_engine | liquidator_call | collateral_over_seizure_or_debt_underclear

# Interaction Scope
interaction_scope: multi_contract
involved_contracts:
  - LiquidationLogic
  - RiskEngine / RiskModule
  - CDPVault
  - CrossChainRouter (bridge messaging)
  - LendingPool / Market
  - DebtToken
path_keys:
  - wrong_liquidation_amount_math | liquidate() | LiquidationLogic→DebtToken | shares_treated_as_assets
  - wrong_liquidation_amount_math | liquidate() | RiskModule→Oracle | over_seizure_via_uint256_max_replay
  - wrong_liquidation_amount_math | liquidatePosition() | CDPVault→PoolV3 | penalty_not_applied_to_seized_collateral
  - wrong_liquidation_amount_math | crosschain liquidation | CrossChainRouter→LayerZero | seize_amount_reused_as_repay_amount

# Attack Vector Details
attack_type: logical_error
affected_component: liquidation_engine

# Technical Primitives
primitives:
  - closeFactor
  - liquidationBonus
  - liquidationPenalty
  - liquidationDiscount
  - seizeTokens
  - repayAmount
  - debtShares
  - borrowIndex
  - computeClosingFactor
  - collateralShare
  - amountDue
  - maxLiquidatableDebt

# Grep / Hunt-Card Seeds
code_keywords:
  - executeLiquidationCall
  - _calculateDebt
  - liquidateCalculateSeizeTokens
  - _validateSeizedAssetValue
  - computeClosingFactor
  - liquidatePosition
  - actualDebtToLiquidate
  - seizeTokens
  - debtToCover
  - maxSeizedAssetValue

# Impact Classification
severity: high
impact: fund_loss
financial_impact: high

# Context Tags
tags:
  - lending
  - liquidation
  - defi
  - accounting
  - cross_chain

# Version Info
language: solidity
version: all
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [S1] | reports/lending_borrowing_findings/h-2-users-can-seize-more-assets-during-liquidation-by-using-typeuintmax.md | HIGH | Sherlock (Sentiment V2) | solodit 41293 / https://github.com/sherlock-audit/2024-08-sentiment-v2-judging/issues/556 |
| [S2] | reports/lending_borrowing_findings/h-3-using-original-principal-amount-as-due-amount-inside-liquidatedefaultedloanw.md | HIGH | Sherlock (Teller Finance) | solodit 44215 / https://github.com/sherlock-audit/2024-11-teller-finance-update-judging/issues/43 |
| [S3] | reports/lending_borrowing_findings/h-19-cross-chain-liquidation-uses-collateral-seize-amount-instead-of-repayment-a.md | HIGH | Sherlock (LEND) | solodit 58388 / https://github.com/sherlock-audit/2025-05-lend-audit-contest-judging/issues/836 |
| [S4] | reports/lending_borrowing_findings/h-02-liquidation-doesnt-account-for-penalty-when-calculating-collateral-to-give-.md | HIGH | Code4rena (Loopfi) | solodit 49024 / https://github.com/code-423n4/2024-07-loopfi-findings/issues/399 |
| [S5] | reports/lending_borrowing_findings/h-03-the-amount-of-debt-removed-during-liquidation-may-be-worth-more-than-the-ac.md | HIGH | Code4rena (Tapioca DAO) | solodit 27493 / https://github.com/code-423n4/2023-07-tapioca-findings/issues/1620 |
| [S6] | reports/lending_borrowing_findings/h-2-full-liquidation-wont-sweep-the-whole-debts-with-leaving-some-and-will-wrong.md | HIGH | Sherlock (ZeroLend One) | solodit 41812 / https://github.com/sherlock-audit/2024-06-new-scope-judging/issues/107 |
| [S7] | reports/lending_borrowing_findings/h-02-risk-of-overpayment-due-to-race-condition-between-repay-and-liquidatewithre.md | HIGH | Code4rena (Size) | solodit 38037 / https://github.com/code-423n4/2024-06-size-findings/issues/181 |
| [S8] | reports/lending_borrowing_findings/h-10-partial-liquidations-are-not-possible.md | HIGH | Sherlock (Notional V3) | solodit 18577 / https://github.com/sherlock-audit/2023-03-notional-judging/issues/204 |

## Liquidation Seizure Economics Miscalculation

**Liquidation math that mis-converts between debt/collateral units, ignores penalties, or reuses the wrong amount field lets liquidators over-seize collateral or lets debt survive a "full" liquidation.**

### Overview

Lending liquidation engines must convert a `repayAmount` (debt paid by the liquidator) into a `seizeAmount` (collateral taken by the liquidator) through the bonus/penalty/discount/close-factor configuration. Across 8 unique HIGH findings from 2 audit platforms and 8 protocols, the conversion itself is wrong: debt shares are used where debt assets are expected, the liquidation penalty is not applied to the collateral side, `type(uint256).max` sentinels double-count repayment in validation, the original principal is used where the remaining principal is expected, and cross-chain payloads reuse the seize amount as the repay amount. The result is either borrower collateral loss (over-seizure) or lender loss (debt removed for less than its collateral value / residual debt left behind).

#### Agent Quick View

- Root cause statement: "This vulnerability exists because the liquidation engine's repay-to-seize conversion math mis-handles units, sentinel values, penalties, or payload fields, allowing the liquidator to seize more collateral than the repay amount justifies or leaving debt unliquidated after a full liquidation."
- Pattern key: `wrong_liquidation_amount_math | liquidation_engine | liquidator_call | collateral_over_seizure_or_debt_underclear`
- Interaction scope: `multi_contract`
- Primary affected component(s): `LiquidationLogic / RiskModule / CDPVault.liquidatePosition / CrossChainRouter`
- Contracts / modules involved: `LiquidationLogic, RiskModule, CDPVault, CrossChainRouter, DebtToken, LendingPool`
- Path keys: shares-vs-assets conversion, `type(uint).max` replay, penalty-ignored collateral math, cross-chain payload reuse
- High-signal code keywords: `executeLiquidationCall`, `_calculateDebt`, `seizeTokens`, `liquidationBonus`, `debtToCover`, `closeFactor`
- Severity: HIGH — 8/8 unique findings rated HIGH by their source auditors
- Typical sink / impact: `borrower collateral over-seizure, residual debt / dust debt after full liquidation, corrupted borrowing flags, lender fund loss`
- Validation strength: `strong` (8 unique findings, 2 independent audit platforms, 8 protocols, all rated HIGH)

#### Contract / Boundary Map

- Entry surface(s): `liquidate()`, `liquidatePosition()`, `liquidateDefaultedLoanWithIncentive()`, cross-chain liquidation via `_executeLiquidationCore()`
- Contract hop(s): `PositionManager.liquidate -> RiskModule._validateSeizedAssetValue -> Pool`; `Pool.liquidate -> LiquidationLogic._calculateDebt -> DebtToken`; `CrossChainRouter -> LayerZero -> CrossChainRouter (other chain) -> repayCrossChainBorrowInternal`
- Trust boundary crossed: `oracle valuation inside risk check`, `bridge message payload semantics`, `share/asset index conversion`
- Shared state or sync assumption: `debtShares × borrowIndex == debt assets`; `seizeAmount == repayAmount adjusted by bonus/penalty`; `payload.amount semantics consistent across chains`

#### Valid Bug Signals

- Signal 1: A liquidation amount variable crosses a unit boundary (shares → assets, principal → remaining principal, seize → repay) without the corresponding conversion (`borrowIndex`, minus repaid, explicit field).
- Signal 2: Validation of the seized amount is computed from user-supplied calldata (e.g. `type(uint256).max` sentinel expanded to current balance per array entry) rather than from post-execution state.
- Signal 3: The penalty/discount/bonus is applied on one side of the equation (debt reduction or transfer in) but not the other (collateral out), making self-liquidation or over-seizure profitable.

#### False Positive Guards

- Not this bug when: shares are converted via `rayMul(borrowIndex)` / `toAmount()` before entering the liquidation math (Aave-style `LiquidationLogic` with proper `debtSharesToAmount` is safe).
- Not this bug when: the seized-value cap is validated against actual transferred amounts after state updates, or each poolId may appear at most once in the liquidation calldata.
- Safe if: penalty is applied symmetrically — collateral out and debt cleared both scale with `repayAmount - penalty`, and full-liquidation sweeps `userDebt` computed in assets, not shares.
- Requires attacker control of: liquidation calldata (repay amounts, seize amounts, array contents), or an oracle/boundary making positions liquidatable.

### Vulnerability Description

#### Root Cause

The liquidation repayment-to-seizure pipeline performs several unit and semantic conversions. Each finding breaks one conversion:

1. **Shares vs assets** [S6]: `ZeroLend One._calculateDebt` returns `debtShares` (never multiplied by `borrowIndex`) and `supplyShares` are fed as `userCollateralBalance` into `_calculateAvailableCollateralToLiquidate`; every downstream step treats these shares as asset amounts, so a "full" liquidation leaves `((borrowIndex - 1) / borrowIndex) * debtShares` uncovered and wrongly clears the borrowing flag.
2. **Sentinel-value replay** [S1]: `Sentiment V2._validateSeizedAssetValue` expands `amt == type(uint256).max` to `pool.getBorrowsOf(...)` per calldata entry; a first entry partially repaying plus a `type(uint256).max` entry double-counts the same debt in `maxSeizedAssetValue`, allowing seizure of the entire collateral.
3. **Original vs remaining principal** [S2]: `Teller.liquidateDefaultedLoanWithIncentive` uses `_getAmountOwedForBid` (full original principal) as `amountDue`; partially repaid loans double-count principal in `totalPrincipalTokensRepaid`, causing underflow in `totalPrincipalTokensLended - totalPrincipalTokensRepaid` and lost withdrawal accounting.
4. **Penalty asymmetry** [S4]: `Loopfi CDPVault.liquidatePosition` computes `takeCollateral = wdiv(repayAmount, discountedPrice)` from the *gross* `repayAmount` while only `repayAmount - penalty` covers debt — the penalty exists but never reduces seized collateral, so `deposit -> borrow -> go unsafe -> self-liquidate` is profitable.
5. **Collateral-share cap vs bonus inflation** [S5]: `Tapioca Singularity._updateBorrowAndCollateralShare` derives `collateralShare` from `borrowPart + liquidationBonusAmount`; when that exceeds the user's actual collateral it is silently clamped down, so debt worth more than the collateral is removed — the contract loses the difference.
6. **Cross-chain payload field reuse** [S3]: `LEND CrossChainRouter` sends `seizeTokens` as the generic `Payload.amount`; `_handleLiquidationSuccess` on the debt chain then calls `repayCrossChainBorrowInternal(payload.amount)`, repaying debt with the collateral-seize amount instead of `repayFinalAmount`.

#### Attack Scenario / Path Variants

**Path A: Share/asset unit confusion in full liquidation** [S6]
Path key: `wrong_liquidation_amount_math | liquidate() | LiquidationLogic→DebtToken | shares_treated_as_assets`
Entry surface: `Pool.liquidate()`
Contracts touched: `Pool -> LiquidationLogic -> DebtToken`
Boundary crossed: `share/asset index conversion (internal accounting)`
1. Borrower accrues debt with `borrowIndex > 1` (interest accrued).
2. Liquidator calls `liquidate()` with `debtToCover = userDebt` intending full coverage.
3. `_calculateDebt` compares `debtShares` against close-factor limits without index conversion.
4. Remaining `((borrowIndex - 1) / borrowIndex) * debtShares` debt survives; `setBorrowing(false)` wrongly marks the asset as no longer borrowed.
5. **Impact**: dust debt blocks position closure, accounting corruption, borrower stuck flags.

**Path B: `type(uint256).max` sentinel replay in seize validation** [S1]
Path key: `wrong_liquidation_amount_math | liquidate() | RiskModule→Oracle | over_seizure_via_uint256_max_replay`
Entry surface: `PositionManager.liquidate(position, debtData[], assetData[])`
Contracts touched: `PositionManager -> RiskModule._validateSeizedAssetValue -> Pool -> Oracle`
Boundary crossed: `calldata validation vs post-execution state`
1. Position has 1e18 debt; liquidator passes two debt entries: `0.9e18` and `type(uint256).max` for the same poolId.
2. Validation expands the sentinel to the *pre-repayment* balance (1e18), counting 1.9e18 repaid.
3. `maxSeizedAssetValue` inflates; execution actually transfers only 1e18 total (0.9e18 + remaining 0.1e18).
4. Liquidator seizes the entire collateral of the position.
5. **Impact**: borrower loses excess collateral; direct fund loss.

**Path C: Penalty-ignored collateral math enables profitable self-liquidation** [S4]
Path key: `wrong_liquidation_amount_math | liquidatePosition() | CDPVault→PoolV3 | penalty_not_applied_to_seized_collateral`
Entry surface: `CDPVault.liquidatePosition(position, repayAmount)`
Contracts touched: `CDPVault -> PoolV3`
Boundary crossed: `internal math between debt-reduction and collateral-out`
1. Attacker deposits 100e collateral, borrows 80e underlying.
2. Waits (or manipulates spot price) until position is unsafe but with no bad debt.
3. Calls `liquidatePosition` on self: pays `repayAmount - penalty` of debt but receives `repayAmount / discountedPrice` of collateral.
4. Discount (2%) exceeds penalty effect (1%) — attacker profits by the spread.
5. **Impact**: theft of lender/protocol funds via repeated borrow-selfliquidate cycles.

**Path D: Cross-chain seize/repay amount swap** [S3]
Path key: `wrong_liquidation_amount_math | crosschain liquidation | CrossChainRouter→LayerZero | seize_amount_reused_as_repay_amount`
Entry surface: cross-chain `liquidate()` on the debt chain
Contracts touched: `CrossChainRouter (chain B) -> LayerZero -> CrossChainRouter (chain A) -> repayCrossChainBorrowInternal (chain B)`
Boundary crossed: `bridge message payload semantics`
1. Liquidation initiated on chain B computes `seizeTokens` via `liquidateCalculateSeizeTokens`.
2. `seizeTokens` is encoded as generic `Payload.amount` to chain A.
3. Chain A echoes `payload.amount` back; chain B repays the borrower's debt with `seizeTokens`.
4. Debt reduced by collateral amount instead of repayment amount — under- or over-repayment depending on price ratio.
5. **Impact**: borrower debt accounting corrupted; protocol insolvency when seize > repay value.

#### Vulnerable Pattern Examples

**Example 1: Debt shares used as debt assets (ZeroLend One)** [HIGH]
```solidity
// ❌ VULNERABLE: userDebt/actualDebtToLiquidate are SHARES, never converted by borrowIndex
function _calculateDebt(
    DataTypes.ExecuteLiquidationCallParams memory params,
    uint256 healthFactor,
    mapping(address => mapping(bytes32 => DataTypes.PositionBalance)) storage balances
) internal view returns (uint256, uint256) {
    uint256 userDebt = balances[params.debtAsset][params.position].debtShares; // @audit shares, not assets
    uint256 closeFactor = healthFactor > CLOSE_FACTOR_HF_THRESHOLD
        ? DEFAULT_LIQUIDATION_CLOSE_FACTOR : MAX_LIQUIDATION_CLOSE_FACTOR;
    uint256 maxLiquidatableDebt = userDebt.percentMul(closeFactor);
    uint256 actualDebtToLiquidate = params.debtToCover > maxLiquidatableDebt
        ? maxLiquidatableDebt : params.debtToCover;
    return (userDebt, actualDebtToLiquidate); // downstream treats these as asset amounts
}
```

**Example 2: Sentinel replay inflating the seize cap (Sentiment V2)** [HIGH]
```solidity
// ❌ VULNERABLE: type(uint).max expanded per calldata entry double-counts repaid debt
function _validateSeizedAssetValue(
    address position, DebtData[] calldata debtData, AssetData[] calldata assetData, uint256 discount
) internal view {
    uint256 debtRepaidValue;
    for (uint256 i; i < debtData.length; ++i) {
        uint256 amt = debtData[i].amt;
        if (amt == type(uint256).max) amt = pool.getBorrowsOf(debtData[i].poolId, position); // @audit replayed balance
        debtRepaidValue += IOracle(riskEngine.getOracleFor(pool.getPoolAssetFor(debtData[i].poolId)))
            .getValueInEth(pool.getPoolAssetFor(debtData[i].poolId), amt);
    }
    uint256 maxSeizedAssetValue = debtRepaidValue.mulDiv(1e18, (1e18 - discount));
    if (assetSeizedValue > maxSeizedAssetValue) revert RiskModule_SeizedTooMuch(assetSeizedValue, maxSeizedAssetValue);
}
```

**Example 3: Penalty applied to debt but not to collateral out (Loopfi CDPVault)** [HIGH]
```solidity
// ❌ VULNERABLE: takeCollateral derived from gross repayAmount — penalty has no effect
uint256 discountedPrice = wmul(spotPrice_, liqConfig_.liquidationDiscount);
uint256 takeCollateral = wdiv(repayAmount, discountedPrice);          // @audit uses FULL repayAmount
uint256 deltaDebt = wmul(repayAmount, liqConfig_.liquidationPenalty); // debt reduced by repayAmount*penalty
uint256 penalty = wmul(repayAmount, WAD - liqConfig_.liquidationPenalty);
...
poolUnderlying.safeTransferFrom(msg.sender, address(pool), repayAmount - penalty); // pays penalty...
poolUnderlying.safeTransferFrom(msg.sender, address(pool), penalty);               // ...but collateral unchanged
```

**Example 4: Collateral clamp silently discounts debt removal (Tapioca Singularity)** [HIGH]
```solidity
// ❌ VULNERABLE: bonus-inflated collateralShare exceeds user collateral, clamped instead of re-derived
if (collateralShare > userCollateralShare[user]) {
    collateralShare = userCollateralShare[user]; // @audit borrowPart (debt removed) keeps full value
}
userCollateralShare[user] -= collateralShare;
userBorrowPart[user] -= borrowPart; // debt removed exceeds collateral actually taken
```

**Example 5: Original principal used as amount due (Teller)** [HIGH]
```solidity
// ❌ VULNERABLE: amountDue is the ORIGINAL principal, not remaining principal
function _getAmountOwedForBid(uint256 _bidId) internal view virtual returns (uint256 amountDue) {
    (,,,, amountDue, , , ) = ITellerV2(TELLER_V2).getLoanSummary(_bidId); // @audit full principal
}
// liquidateDefaultedLoanWithIncentive then does:
uint256 amountDue = _getAmountOwedForBid(_bidId);
// -> totalPrincipalTokensRepaid double-counts already-repaid principal -> underflow + lost withdrawals
```

### Impact Analysis

#### Technical Impact

- Borrower collateral over-seizure beyond the bonus-justified amount (2/8 unique findings: S1, S4-family)
- Debt survives a "full" liquidation as dust shares, blocking closure and corrupting `setBorrowing` flags (1/8: S6)
- Debt removed for less collateral than it is worth — protocol/lender shortfall (2/8: S5, S3)
- Global accounting corruption: repaid-principal double counting, underflow reverts on new borrows, zero-share mints (1/8: S2)
- Liquidation incentive elimination when seize math underpays liquidators in adverse conditions (supporting: S7, S8 — overpayment race and impossible partial liquidations)

#### Business Impact

- Direct loss of lender funds when debt is cleared below value (Tapioca-style clamping)
- Borrower lawsuits-level harm from collateral over-seizure (Sentiment V2 escalation to HIGH confirmed by Sherlock judge discussion)
- Liquidation markets break: overpayment races (Size S7) and impossible partial liquidations (Notional V3 S8, where whole-currency positions cannot be partially liquidated, letting huge positions accrue bad debt)

#### Affected Scenarios

- Any market with accrued interest (`borrowIndex > 1`) at liquidation time
- Calldata-driven liquidation bundles where sentinel values (`type(uint256).max`) expand balances
- CDP vaults with self-liquidation penalty mechanisms where penalty < discount
- Cross-chain liquidations reusing a generic `amount` field in bridge payloads

### Secure Implementation

**Fix 1: Convert shares to assets before liquidation math (Aave-style)**
```solidity
// ✅ SECURE: every liquidation quantity is an asset amount
vars.userDebt = _calculateDebt(...) ;                    // shares
vars.userDebt = DebtToken(debtToken).rayMul(vars.userDebt, debtReserveCache.nextBorrowIndex); // -> assets
vars.actualDebtToLiquidate = Math.min(vars.actualDebtToLiquidate, vars.userDebt);
// Full-liquidation sweep only when actualDebtToLiquidate == userDebt (both in assets):
if (vars.userDebt == vars.actualDebtToLiquidate) {
    userConfig.setBorrowing(debtReserve.id, false);
}
```

**Fix 2: Deny duplicate pool entries and validate post-execution**
```solidity
// ✅ SECURE: one debt entry per pool, cap checked against actual transferred amounts
for (uint256 i; i < debtData.length; ++i) {
    if (i > 0) require(debtData[i].poolId > debtData[i-1].poolId, RiskModule_DuplicatePool());
}
// after execution: assert actualRepaid == validatedRepaid before transferring seized assets
```

**Fix 3: Apply penalty symmetrically (Loopfi fix)**
```solidity
// ✅ SECURE: collateral out must be computed from the NET effective repayment
uint256 netRepay = repayAmount - penalty;
uint256 takeCollateral = wdiv(netRepay, discountedPrice);
require(liqConfig_.liquidationPenalty >= WAD - liqConfig_.liquidationDiscount + minBuffer, "unprofitable self-liq guaranteed");
```

**Fix 4: Distinct payload fields per semantic (cross-chain)**
```solidity
// ✅ SECURE: never reuse one generic amount field for both seize and repay semantics
struct LZPayload { uint256 amount; uint256 repayFinalAmount; ... }
_send(srcEid, seizeTokens, /*repayFinalAmount=*/ params.repayAmount, 0, 0, ...);
// debt chain repays with payload.repayFinalAmount, never payload.amount
```

### Detection Patterns

#### Contract / Call Graph Signals
```
- liquidate()/liquidatePosition() reads debtShares or supplyShares and the result flows into
  transfer/collateral math without a borrowIndex/liquidityIndex multiplication on the path
- user-supplied amount arrays validated against balances expanded inside a loop (sentinel expansion)
- penalty/discount applied to debt-reduction line but absent from the collateral-out line (or vice versa)
- bridge payload struct with a single generic `amount` reused across liquidation handshake steps
- amountDue sourced from loan summary (original principal) rather than remaining principal
```

#### High-Signal Grep Seeds
```
- executeLiquidationCall
- _calculateDebt
- liquidateCalculateSeizeTokens
- _validateSeizedAssetValue
- computeClosingFactor
- actualDebtToLiquidate
- seizeTokens
- debtToCover
- liquidationPenalty
- setBorrowing
```

#### Code Patterns to Look For
```
- Pattern 1: `debtShares` variable consumed by `percentMul(closeFactor)` with no `rayMul(borrowIndex)` on any path
- Pattern 2: `if (amt == type(uint256).max) amt = <balance lookup>` inside a validation loop over calldata arrays
- Pattern 3: `takeCollateral = repayAmount / discountedPrice` while transfer-in uses `repayAmount - penalty`
- Pattern 4: `collateralShare = userCollateralShare[user]` clamping after bonus inflation
- Pattern 5: `_getAmountOwed` returning `getLoanSummary(...)` principal for defaulted-loan liquidation
```

#### Audit Checklist
- [ ] Trace every liquidation amount variable end-to-end: is it shares or assets at each step? Is the index conversion present exactly once?
- [ ] Can the same debt position appear twice in liquidation calldata? What does `type(uint256).max` expand to per entry?
- [ ] Is the liquidation penalty/discount applied to BOTH the debt cleared and the collateral transferred?
- [ ] In a "full" liquidation with accrued interest, does any dust debt remain? Is `setBorrowing(false)` correct?
- [ ] For cross-chain liquidation: does each bridge payload field keep one semantic meaning across all hops?

### Real-World Examples

#### Known Exploits
- **Euler (2022, $197M)** - donate-to-reserves self-liquidation variant: liquidation economics allowed a self-liquidation to extract collateral at a discount (see `DB/general/defihacklabs-business-logic-2023-patterns.md` Pattern 1 for the exploit-side view).
- **Platypus (2023, $10.5M)** - flash-loan-assisted bad debt creation that liquidation math failed to price (see `DB/general/defihacklabs-business-logic-2023-patterns.md` Pattern 8).

#### Related CVEs/Reports
- Sherlock Sentiment V2 issue #556 (over-seizure escalation to HIGH) — [S1]
- Code4rena Loopfi issue #399 (self-liquidation penalty bypass) — [S4]

### Prevention Guidelines

#### Development Best Practices
1. Use typed wrappers (`DebtAssets`, `DebtShares`) or naming conventions (`debtAmt` vs `debtShares`) enforced in review — never let raw shares enter transfer math.
2. Validate liquidation calldata structurally (sorted, unique pool ids) before expanding sentinel values.
3. Property-test the invariant: `collateralOut_value == repayEffective_value * (1 + bonus) - penalty` for every liquidation, including at `borrowIndex` extremes and boundary HF values.
4. For cross-chain flows, define one payload struct per message type with named fields per semantic.

#### Testing Requirements
- Unit tests for: full liquidation with `borrowIndex > 1` (no dust debt left), duplicate-pool calldata reverts, self-liquidation profitability at configured discount/penalty
- Integration tests for: cross-chain liquidation handshake field consistency
- Fuzzing targets: `seizeAmount/repayAmount` ratio vs configured bonus over random price/index combinations; assert no profitable self-liquidation region exists

### References

#### Technical Documentation
- Aave V3 LiquidationLogic (reference secure shares-to-assets conversion)
- Compound V2 `liquidateCalculateSeizeTokens` (reference repay-to-seize conversion)

#### Security Research
- Sherlock 2024-08-sentiment-v2 issue #556 judge escalation discussion (severity of over-seizure)
- Code4rena 2024-07-loopfi issue #399 (self-liquidation penalty asymmetry)

### Keywords for Search

`liquidation`, `seize collateral`, `seizeTokens`, `liquidation bonus`, `liquidation penalty`, `close factor`, `debt shares`, `borrowIndex`, `shares vs assets`, `over-seizure`, `self liquidation profit`, `debtToCover`, `cross-chain liquidation`, `payload amount reuse`, `dust debt`, `setBorrowing`, `full liquidation sweep`, `computeClosingFactor`, `collateralShare clamp`

### Related Vulnerabilities

- [Liquidation Evasion and Borrower-Triggered Liquidation DoS](../liquidation/liquidation-evasion-dos.md)
- [Oracle-Driven Liquidation Mispricing](../liquidation/oracle-driven-liquidation-mispricing.md)
- [Self-Liquidation Abuse](../liquidation/self-liquidation-abuse.md)
- [Bad Debt Socialization and Missing Write-Off](../bad-debt/bad-debt-socialization.md)
- `DB/general/lending-rate-model/LENDING_RATE_MODEL_VULNERABILITIES.md` (rate-side liquidation input errors)
