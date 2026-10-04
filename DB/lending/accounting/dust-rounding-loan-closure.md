---
# Core Classification
protocol: generic
chain: everychain
category: arithmetic
vulnerability_type: rounding_dust_breakage

# Pattern Identity
root_cause_family: rounding_direction_error
pattern_key: dust_rounding_closure_break | debt_share_accounting | dust_repay_or_precision_loss | repay_liquidate_revert_or_unprofitable

# Interaction Scope
interaction_scope: single_contract
involved_contracts:
  - V3Vault / LendingPair (repay, liquidate)
  - CDP redemption / liquidation incentive math
  - healthFactor vs repay routers
  - fee accounting in liquidation flows
path_keys:
  - dust_rounding_closure_break | repay() | V3Vault→debtShares | exact_share_match_revert_grief
  - dust_rounding_closure_break | liquidate() | V3Vault→DebtChanged | front_run_share_delta_revert
  - dust_rounding_closure_break | openCDP(dust) | CDP→redemption | dust_positions_unprofitable_to_clear
  - dust_rounding_closure_break | healthFactor() | Router→Morpho | rounding_discrepancy_migration_failure

# Attack Vector Details
attack_type: logical_error
affected_component: debt_share_accounting

# Technical Primitives
primitives:
  - debtShares rounding
  - RepayExceedsDebt
  - DebtChanged
  - dust CDP
  - liquidation profitability
  - fee precision
  - token-to-USD conversion precision
  - rounding direction (ceil vs floor)
  - share-to-amount conversion

# Grep / Hunt-Card Seeds
code_keywords:
  - RepayExceedsDebt
  - DebtChanged
  - debtShares
  - convertToShares
  - convertToAssets
  - ceilDiv
  - roundUp
  - healthFactor
  - minProfit

# Impact Classification
severity: medium
impact: dos
financial_impact: medium

# Context Tags
tags:
  - lending
  - rounding
  - precision
  - dust
  - liquidation
  - defi

# Version Info
language: solidity
version: all
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [D1] | reports/lending_borrowing_findings/m-16-repayments-and-liquidations-can-be-forced-to-revert-by-an-attacker-that-rep.md | MEDIUM | Code4rena (Revert Lend) | solodit 32282 / https://github.com/code-423n4/2024-03-revert-lend-findings |
| [D2] | reports/lending_borrowing_findings/allowing-the-creation-of-dust-cdps-could-lead-redeemersliquidators-to-be-not-pro.md | HIGH | Cantina (BadgerDAO) | solodit 54625 |
| [D3] | reports/lending_borrowing_findings/h-1-fee-precision-loss-disrupts-liquidations-and-causes-loss-of-funds.md | HIGH | Sherlock (Velar Artha PerpDEX) | solodit 41278 |
| [D4] | reports/lending_borrowing_findings/bigger-precision-loss-in-tokenamount-to-usd-conversion-will-lead-incorrect-liqui.md | MEDIUM | Cantina (HyperLabs Inc) | solodit 46402 |
| [D5] | reports/lending_borrowing_findings/m-7-rounding-discrepancy-between-morpholendingrouterhealthfactor-and-morphorepay.md | MEDIUM | Sherlock (Notional Exponent) | solodit 62499 |
| [D6] | reports/lending_borrowing_findings/fng-16-loans-with-cerc721-collateral-can-be-made-unliquidatable.md | HIGH | Hexens (Fungify) | solodit 62382 (whole-NFT rounding variant — see liquidation-evasion entry) |

## Dust and Rounding Breakage of Loan Closure and Liquidation

**Rounding direction errors and dust debt let third parties or the protocol itself make repayments and liquidations revert (exact-share-match requirements) or render clearing positions unprofitable — dust positions become unpayable, unclearable debt.**

### Overview

Lending math constantly converts between assets and shares and between token amounts and USD values; each conversion rounds. Six unique findings (3 HIGH, 3 MEDIUM) from 3 audit firms across 6 protocols show the two failure shapes. (1) Griefing via dust deltas: Revert Lend's `repay`/`liquidate` revert with `RepayExceedsDebt` / `DebtChanged` when the requested shares exceed outstanding shares, so an attacker repaying 1 share front-runs the victim's full repayment and then liquidates them; Fungify's whole-NFT rounding-up underflows on fractional collateral. (2) Unprofitable/broken clearing: BadgerDAO dust CDPs make redemption and liquidation unprofitable (debt below gas + minimum incentive); Velar fee precision loss disrupts liquidation math causing fund loss; HyperLabs token→USD precision flips liquidation outcomes; Notional Exponent rounding disagreement between `healthFactor` and `repay` breaks position migration.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because repay/liquidate paths require exact share matches (revert on any dust delta another user can create) or because rounding in debt/fee/USD conversions is in the wrong direction, making dust positions impossible to repay profitably and flipping liquidation decisions."
- Pattern key: `dust_rounding_closure_break | debt_share_accounting | dust_repay_or_precision_loss | repay_liquidate_revert_or_unprofitable`
- Interaction scope: `single_contract`
- Primary affected component(s): `repay/liquidate share validation; CDP dust creation gates; fee and USD conversion rounding`
- Contracts / modules involved: `V3Vault, CDP redemption, healthFactor router vs repay engine`
- Path keys: `exact_share_match_revert_grief`, `front_run_share_delta_revert`, `dust_positions_unprofitable_to_clear`, `rounding_discrepancy_migration_failure`
- High-signal code keywords: `RepayExceedsDebt`, `DebtChanged`, `debtShares`, `convertToShares`, `ceilDiv`
- Severity: MEDIUM — 3/6 unique findings rated HIGH, 3 MEDIUM; family severity is the lowest unique rating (MEDIUM) per severity policy
- Typical sink / impact: `repay/liquidate DoS near thresholds, unpayable dust debt, unprofitable liquidations, fund loss from fee rounding`
- Validation strength: `strong` (6 unique findings, 3 independent audit firms — Code4rena, Cantina, Sherlock, Hexens — across 6 protocols)

#### Contract / Boundary Map

- Entry surface(s): `repay(tokenId, shares)`, `liquidate(params)`, CDP open (dust), `healthFactor` routers
- Contract hop(s): `attacker.repay(1 share) -> debtShares-1 -> victim.repay(debtShares) revert`; `openCDP(dust) -> redemption profitability < gas`
- Trust boundary crossed: `anyone-can-repay semantics vs exact-match validation`; `two independent roundings of the same quantity (healthFactor vs repay)`
- Shared state or sync assumption: `repay amount >= outstanding debt must succeed (clamp, not revert)`; `dust positions must be openable-but-clearable or disallowed`

#### Valid Bug Signals

- Signal 1: `require(shares <= debtShares)` style validation where anyone can decrement `debtShares` between the victim's simulation and execution.
- Signal 2: Dust-sized CDPs/loans can be opened (no minimum) while redemption/liquidation pays fixed costs (gas, minimum profit).
- Signal 3: The same quantity (debt, health) is rounded independently in two functions with different directions (`floor` in one, `ceil` in the other) and the flows must agree.

#### False Positive Guards

- Not this bug when: repay clamps to outstanding debt (repaying `type(uint256).max` or more than debt succeeds and burns all shares).
- Not this bug when: dust loss is bounded below gas cost AND no griefing vector exists (pure QA-level rounding).
- Safe if: protocols enforce minimum position sizes at open AND closure paths accept over-repayment with refund.
- Cross-link guard: vault share-price inflation attacks (first-depositor) are a different pattern — `DB/general/vault-inflation-attack/vault-inflation-attack.md`.

### Vulnerability Description

#### Root Cause

1. **Exact-share-match revert** [D1]: Revert Lend `V3Vault.repay`/`liquidate` revert when requested shares exceed outstanding (`RepayExceedsDebt`, `DebtChanged`). Anyone can repay 1 share of another's position; the victim's pre-computed full-repay transaction then reverts, and during the confusion the attacker liquidates.
2. **Dust CDP economics** [D2]: BadgerDAO allows opening dust CDPs; redeemers/liquidators of such positions cannot cover gas + minimum incentive, so dust debt survives forever.
3. **Fee precision in liquidation** [D3]: Velar fee accounting loses precision, corrupting liquidation amounts — liquidations disrupted plus direct fund loss.
4. **USD conversion precision flips outcomes** [D4]: HyperLabs tokenAmount→USD conversion loses precision for some decimals, producing incorrect liquidation results.
5. **Divergent roundings** [D5]: Notional Exponent `MorphoLendingRouter.healthFactor` and `Morpho.repay` round the same debt differently; positions that appear closable by HF fail in repay, breaking migrations.
6. **Rounding to indivisible units** [D6]: Fungify rounds seized NFT collateral UP to whole tokens the borrower may not hold — underflow revert (full writeup in the evasion entry).

#### Attack Scenario / Path Variants

**Path A: 1-share repay front-run griefs repayment and enables liquidation** [D1]
Path key: `dust_rounding_closure_break | repay() | V3Vault→debtShares | exact_share_match_revert_grief`
Entry surface: `vault.repay(tokenId, shares, true)` by anyone
Contracts touched: `V3Vault -> debtShares`
Boundary crossed: `anyone-can-repay + exact-match validation`
1. Victim is near the liquidation threshold; plans a full repay of `debtShares`.
2. Attacker front-runs with `repay(tokenId, 1, true)` — debtShares drops by 1.
3. Victim's tx reverts `RepayExceedsDebt`; likewise `liquidate(debtShares)` reverts `DebtChanged`.
4. Attacker (or anyone) liquidates at `debtShares - 1` while the victim is defenseless.
5. **Impact**: forced liquidations of savable positions; DoS of repay/self-liquidate.

**Path B: Dust positions nobody can profitably clear** [D2]
Path key: `dust_rounding_closure_break | openCDP(dust) | CDP→redemption | dust_positions_unprofitable_to_clear`
Entry surface: opening minimum-size CDPs
Contracts touched: `CDP engine -> redemption/liquidation incentive math`
Boundary crossed: `open-time minimum vs close-time economics`
1. Protocol imposes no minimum CDP size.
2. Attackers (or organic users) create many dust CDPs.
3. For each, redemption/liquidation reward < gas cost — nobody clears them.
4. Dust debt accumulates as permanent protocol slack.
5. **Impact**: growing unbacked dust; redemption dilution.

**Path C: Two roundings disagree** [D5]
Path key: `dust_rounding_closure_break | healthFactor() | Router→Morpho | rounding_discrepancy_migration_failure`
Entry surface: position migration (repay old, borrow new)
Contracts touched: `MorphoLendingRouter.healthFactor -> Morpho.repay`
Boundary crossed: `independent rounding of the same quantity`
1. Router computes HF with one rounding; repay converts shares→assets with another.
2. Migration plans a full repay that the engine rejects by 1 wei (or leaves 1 wei of debt).
3. Migration reverts or leaves dust debt behind.
4. **Impact**: broken automation; stuck positions.

#### Vulnerable Pattern Examples

**Example 1: Exact-match repay validation (Revert Lend)** [MEDIUM]
```solidity
// ❌ VULNERABLE: reverts instead of clamping when shares > outstanding
function repay(uint256 tokenId, uint256 shares, bool isShare) external {
    uint256 debtShares = loans[tokenId];
    if (isShare) {
        if (shares > debtShares) revert IErrors.RepayExceedsDebt(tokenId, shares, debtShares); // @audit 1-share grief
    }
    // ...
}
```

**Example 2: No minimum CDP size (BadgerDAO shape)** [HIGH]
```solidity
// ❌ VULNERABLE: dust CDPs openable; closing them costs more than it pays
function openCdp(uint256 drawnAmount) external returns (uint256 id) {
    // no require(drawnAmount >= MIN_CDP_SIZE)
    id = ++count;
    cdps[id] = Cdp({ debt: drawnAmount, ... });
}
// redeemer/liquidator: reward = f(debt) < gas for dust => never cleared
```

**Example 3: Fee precision lost in liquidation payout (Velar shape)** [HIGH]
```solidity
// ❌ VULNERABLE: fee terms truncated before subtraction
uint256 fee = (amount * feeRate) / 1e18;            // rounds down
uint256 liquidatorPayout = amount - fee - otherFee; // compounding truncation
// repeated liquidations drift: payout < intended, or math reverts at boundaries
```

**Example 4: Inconsistent rounding across views (Notional Exponent shape)** [MEDIUM]
```solidity
// ❌ VULNERABLE: two engines round the same debt differently
function healthFactor(address user) external view returns (uint256) {
    return collateralValue.divRound(debtValue); // rounding A
}
function repay(uint256 assets) external {
    uint256 shares = convertToShares(assets);   // rounding B (different direction)
    if (assets != convertToAssets(shares)) revert(); // 1-wei disagreement
}
```

### Impact Analysis

#### Technical Impact

- Third-party-forced revert of repay and liquidation near thresholds (2/6 unique findings: D1, D6)
- Permanently unclearable dust debt (1/6: D2)
- Direct fund loss or disrupted liquidation from fee/USD precision (2/6: D3, D4)
- Broken composability (migration/automation) from divergent roundings (1/6: D5)

#### Business Impact

- Users pushed into liquidation they could have avoided (Revert Lend confirmed + mitigated)
- Redemption dilution and growing protocol slack from dust positions (BadgerDAO)
- Integration failures for routers/automation that depend on HF/repay agreement

#### Affected Scenarios

- Vaults where anyone can repay on behalf of a position combined with strict share validation
- CDP protocols without minimum position sizes
- Liquidation flows with multi-step fee arithmetic on small amounts
- Router/aggregator stacks reading HF from one contract and repaying through another

### Secure Implementation

**Fix 1: Clamp, never revert, on over-repayment (Revert Lend fix)**
```solidity
// ✅ SECURE: repay caps at outstanding debt; excess is refunded
function repay(uint256 tokenId, uint256 shares, bool isShare) external {
    uint256 debtShares = loans[tokenId];
    uint256 toRepay = isShare ? Math.min(shares, debtShares) : shares; // clamp
    uint256 paid = _burnSharesAndCollect(tokenId, toRepay);
    if (paid < msg.valueEquivalent) _refundExcess(msg.sender);          // give back overage
}
```

**Fix 2: Enforce minimum position sizes**
```solidity
// ✅ SECURE: dust cannot enter the system
function openCdp(uint256 drawnAmount) external returns (uint256 id) {
    require(drawnAmount >= MIN_CDP_SIZE, "dust cdp");
    // ...
}
```

**Fix 3: Single rounding authority**
```solidity
// ✅ SECURE: one library function, one direction, used by every consumer
using DebtMath for uint256;
uint256 hfDebt = debtValue.roundUpToShares();
uint256 repayShares = assets.toSharesCeil(); // same helper, same direction
```

### Detection Patterns

#### Contract / Call Graph Signals
```
- repay/liquidate validation of the form `require(requested <= outstanding)` where outstanding is
  decrementable by third parties
- position-open paths with no minimum-size check while close paths pay fixed costs
- fee/USD arithmetic chains with multiple sequential divisions
- the same quantity computed in two contracts/routers with different rounding helpers
```

#### High-Signal Grep Seeds
```
- RepayExceedsDebt
- DebtChanged
- convertToShares
- convertToAssets
- ceilDiv
- divRound
- minDebt / MIN_CDP
- debtShares
```

#### Code Patterns to Look For
```
- Pattern 1: `if (shares > debtShares) revert` in a repay path callable with anyone's position
- Pattern 2: open functions lacking `require(amount >= MIN)` while redemption pays per-position costs
- Pattern 3: `amount - fee1 - fee2` with each fee independently floored
- Pattern 4: `healthFactor()` in one contract and `repay()` share math in another with different rounding
```

#### Audit Checklist
- [ ] Can anyone decrement a position's debt shares/amount between a victim's quote and execution? What happens on mismatch — clamp or revert?
- [ ] Is there a minimum position size at open? Compute redeemer/liquidator profit at that size vs gas.
- [ ] Do all consumers of debt/health round through one helper in one direction?
- [ ] Fuzz repay/liquidate at 1-share and 1-wei boundaries for every decimal combination.

### Real-World Examples

#### Known Exploits
- Dust-driven closure failures compound with liquidation evasion — see the Fungify and Gains Network variants in [Liquidation Evasion](../liquidation/liquidation-evasion-dos.md).

#### Related CVEs/Reports
- Code4rena 2024-03-revert-lend issue (confirmed + mitigated by team)
- Cantina BadgerDAO review (dust CDP profitability)

### Prevention Guidelines

#### Development Best Practices
1. Closure paths clamp over-payments and refund the excess; never revert on "too much repayment".
2. Enforce minimum position sizes at open; recalculate clearability economics whenever gas or incentive parameters change.
3. Centralize rounding: one math library, explicit direction per use case, shared by views and mutations.

#### Testing Requirements
- Unit tests for: repay(debtShares) after external repay(1) succeeds; repay(type(uint256).max) closes position with refund; migration succeeds when HF says closable
- Boundary fuzzing: 1-wei/1-share edges across decimals 6/8/18
- Property tests: no reachable state where a position cannot be fully closed by its owner

### References

#### Technical Documentation
- OpenZeppelin/Solmate ERC4626 rounding guidance (round against the user, clamp closures)
- Morpho share math documentation

#### Security Research
- Revert Lend PoCs `testRepaymentFrontrun` / `testLiquidationFrontrun`
- Cantina dust-economics analysis (BadgerDAO)

### Keywords for Search

`dust debt`, `dust CDP`, `rounding direction`, `repay revert`, `RepayExceedsDebt`, `DebtChanged`, `repay front-run`, `share conversion rounding`, `liquidation profitability`, `unprofitable liquidation`, `fee precision loss`, `USD conversion precision`, `health factor rounding`, `migration failure`, `1 wei debt`, `min position size`, `clamp overpayment`, `dust griefing`

### Related Vulnerabilities

- [Liquidation Evasion and Borrower-Triggered Liquidation DoS](../liquidation/liquidation-evasion-dos.md)
- [Liquidation Seizure Economics Miscalculation](../liquidation/liquidation-seizure-economics.md)
- [Missing Interest Accrual and Stale Index Accounting](../interest-accrual/missing-accrual-stale-index.md)
- `DB/general/precision/precision-loss-rounding-vulnerabilities.md` (general precision class)
- `DB/general/rounding-precision-loss/rounding-precision-loss.md`
