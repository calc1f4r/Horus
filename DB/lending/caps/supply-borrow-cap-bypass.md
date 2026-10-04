---
# Core Classification
protocol: generic
chain: everychain
category: risk_parameters
vulnerability_type: cap_enforcement_bypass

# Pattern Identity
root_cause_family: incomplete_cap_validation
pattern_key: wrong_cap_check | cap_validation | deposit_or_borrow | cap_bypass_or_capacity_dos

# Interaction Scope
interaction_scope: single_contract
involved_contracts:
  - Pool / Market / EtherCollateral
  - Margin collateral module
  - Vault (MetaMorpho / ERC4622-style)
  - PoolManager + ReservePool
path_keys:
  - wrong_cap_check | deposit() | Margin→depositCap | per_tx_not_cumulative_check
  - wrong_cap_check | openLoan() | EtherCollateral | cap_checked_before_not_after
  - wrong_cap_check | liquidate() | PoolManager→ReservePool | reserve_funds_exceed_capacity_dos
  - wrong_cap_check | flashloan deposit | MetaMorpho→idleMarket | supply_cap_redirection_grief

# Attack Vector Details
attack_type: logical_error
affected_component: cap_validation

# Technical Primitives
primitives:
  - depositCap
  - supplyCap
  - borrowCap
  - collateral cap
  - maxDeposit
  - totalDeposited accounting
  - reserve funds
  - pool capacity

# Grep / Hunt-Card Seeds
code_keywords:
  - _requireEnoughDepositCap
  - depositCap
  - supplyCap
  - borrowCap
  - maxDeposit
  - _changePoolCollateral
  - openLoan
  - isSupplyCapExceeded
  - maxExternalDeposit

# Impact Classification
severity: medium
impact: risk_limit_bypass
financial_impact: medium

# Context Tags
tags:
  - lending
  - caps
  - risk_parameters
  - dos
  - defi

# Version Info
language: solidity
version: all
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [C1] | reports/lending_borrowing_findings/improper-supply-cap-limitation-enforcement.md | HIGH | SigmaPrime (Synthetix EtherCollateral) | solodit 19668 / https://github.com/sigp/public-audits/blob/master/synthetix/ethercollateral/review.pdf |
| [C2] | reports/lending_borrowing_findings/users-can-easily-bypass-collateral-depositcap-limit-using-multiple-deposits-unde.md | MEDIUM | Cyfrin (Zaros) | solodit 34831 |
| [C3] | reports/lending_borrowing_findings/m-03-bypassing-collateral-cap-check.md | MEDIUM | Pashov Audit Group (Reya Network) | solodit 37833 |
| [C4] | reports/lending_borrowing_findings/m-24-user-collateral-cap-check-issue.md | MEDIUM | Sherlock (Elfi) | solodit 34819 |
| [C5] | reports/lending_borrowing_findings/funds-can-be-redirected-to-the-idle-market-by-reaching-the-metamorpho-supply-cap.md | MEDIUM | Cantina (Morpho) | solodit 40732 |
| [C6] | reports/lending_borrowing_findings/m-6-vault-_maxdeposit-incorrect-calculation-allows-to-bypass-vault-deposit-cap.md | MEDIUM | Sherlock (Perennial V2) | solodit 28957 |
| [C7] | reports/lending_borrowing_findings/pool-at-capacity-cannot-be-liquidated.md | MEDIUM | OpenZeppelin (f(x) v2) | solodit 61793 / https://blog.openzeppelin.com/fx-v2-audit |
| [C8] | reports/lending_borrowing_findings/m-06-denial-of-liquidations-and-redemptions-by-borrowing-all-reserves-from-aave.md | MEDIUM | Code4rena (Ethos Reserve) | solodit 16149 |
| [C9] | reports/lending_borrowing_findings/m-10-jusdbank-users-can-bypass-individual-collateral-borrow-limits.md | MEDIUM | Sherlock (JOJO Exchange) | solodit 18477 |

## Supply / Borrow Cap Enforcement Bypass

**Cap validators that compare only the current transaction's amount against the cap — instead of cumulative holdings plus the new amount — let users exceed deposit/borrow/supply caps via multiple transactions, while capacity checks inside liquidation paths can brick liquidations when pools sit at capacity.**

### Overview

Caps are the protocol's exposure limits: per-asset supply caps, per-user collateral caps, borrow caps, vault deposit caps. Nine unique findings (1 HIGH, 8 MEDIUM) from 7 audit firms show two failure families. (1) Bypass: the check compares the increment alone against the cap (Zaros `_requireEnoughDepositCap`, Synthetix `openLoan` enforcing the cap only before issuance, JOJO per-collateral limits, Reya collateral cap, Elfi user collateral cap, Perennial `_maxDeposit` mis-computation), so N deposits each under the cap pass. (2) Capacity-induced DoS: at-capacity pools cannot receive the reserve top-up needed to liquidate bad debt (f(x)), and borrowing all reserves from AAVE denies liquidations and redemptions (Ethos Reserve); a flash loan reaching the MetaMorpho supply cap redirects yield to the idle market (Morpho).

#### Agent Quick View

- Root cause statement: "This vulnerability exists because the cap validation compares the per-transaction amount (or a pre-action snapshot) against the cap instead of cumulative balances plus the increment, or because capacity limits reject funds that core flows (liquidation, reserve top-up) must add, allowing cap bypass or liquidation/withdrawal DoS."
- Pattern key: `wrong_cap_check | cap_validation | deposit_or_borrow | cap_bypass_or_capacity_dos`
- Interaction scope: `single_contract` (with cross-contract reserve/vault variants)
- Primary affected component(s): `cap validators on deposit/borrow/supply paths; capacity checks in liquidation`
- Contracts / modules involved: `Margin collateral, EtherCollateral/Pool, Vault, PoolManager, ReservePool`
- Path keys: `per_tx_not_cumulative_check`, `cap_checked_before_not_after`, `reserve_funds_exceed_capacity_dos`, `supply_cap_redirection_grief`
- High-signal code keywords: `_requireEnoughDepositCap`, `depositCap`, `supplyCap`, `maxDeposit`, `_changePoolCollateral`
- Severity: MEDIUM — 1/9 unique findings rated HIGH, 8 MEDIUM; family severity is the lowest unique rating (MEDIUM) per severity policy
- Typical sink / impact: `risk-limit bypass (concentration risk), liquidation DoS at capacity, yield redirection to idle market`
- Validation strength: `strong` (9 unique findings, 7 independent audit firms — SigmaPrime, Cyfrin, Pashov, Sherlock, Cantina, OpenZeppelin, Code4rena — across 9 protocols)

#### Contract / Boundary Map

- Entry surface(s): `deposit()`, `openLoan()`, `borrow()`, `liquidate()`, `maxDeposit()`
- Contract hop(s): `deposit -> _requireEnoughDepositCap (increment-only check)`; `liquidate -> ReservePool.withdraw -> _changePoolCollateral (capacity revert)`; `flashloan -> vault deposit (cap reached) -> idle market`
- Trust boundary crossed: `per-tx validation vs global accounting`, `reserve-to-pool fund flow hitting pool-level caps`
- Shared state or sync assumption: `cap applies to cumulative totals, enforced atomically with the increment`

#### Valid Bug Signals

- Signal 1: The require statement references only the function's amount argument and the cap constant — no `totalX` storage term.
- Signal 2: The cap is checked as a precondition (before state change) but the state change itself can cross it.
- Signal 3: A core flow (liquidation, reserve injection) adds funds to a capped bucket with no cap-exempt path, so a full bucket reverts the core flow.

#### False Positive Guards

- Not this bug when: validation is `totalDeposited[collateral] + amount <= depositCap` (cumulative, atomically updated).
- Not this bug when: capacity exhaustion merely blocks new deposits (intended behavior) without touching liquidation/redemption paths.
- Safe if: liquidation and reserve flows are exempt from capacity checks or capacity is checked after subtracting outgoing amounts.
- Dust guard: bypassing a cap by dust amounts that cannot meaningfully shift exposure is QA-level; flag when the multiplier (N transactions) is unbounded.

### Vulnerability Description

#### Root Cause

1. **Increment-only check** [C2]: Zaros `_requireEnoughDepositCap(collateralType, amount, depositCap)` reverts only when `amount > depositCap` — total deposited for the type is not part of the expression; each sub-cap deposit passes, N times.
2. **Pre-action-only check** [C1]: Synthetix `openLoan` enforces only that the supply cap is not already reached before opening the loan; the loan itself can exceed the total sETH issuance cap.
3. **Per-user cap gaps** [C3][C4][C9]: Reya collateral cap check bypass; Elfi user collateral cap check issue; JOJO JUSDBank individual collateral borrow-limit bypass.
4. **Derived cap mis-computation** [C6]: Perennial `Vault._maxDeposit` calculates the cap incorrectly, so the effective vault deposit cap is wrong.
5. **Capacity rejects reserve top-up during liquidation** [C7]: f(x) `PoolManager._changePoolCollateral` reverts if the change surpasses capacity; `liquidate` adds reserve funds on top of the current balance — when `balance + bonusFromReserve > capacity`, the liquidation fails.
6. **Liquidity exhaustion DoS** [C8]: Ethos Reserve — borrowing all reserves from AAVE denies liquidations and redemptions (cap-free drain of the liquidity layer).
7. **Cap-reached yield redirection** [C5]: Morpho — a flash loan reaching the MetaMorpho supply cap pushes deposits into the idle market, changing reward/yield routing.

#### Attack Scenario / Path Variants

**Path A: Multiple sub-cap deposits bypass a collateral cap** [C2]
Path key: `wrong_cap_check | deposit() | Margin→depositCap | per_tx_not_cumulative_check`
Entry surface: repeated `deposit()` calls
Contracts touched: `Margin collateral -> _requireEnoughDepositCap`
Boundary crossed: `per-tx validation vs global cap`
1. Protocol sets `depositCap = 1M` for collateral X.
2. Attacker (or any users combined) deposits 900k, then 900k, then 900k...
3. Each tx passes because each `amount <= depositCap`; total deposited grows unbounded.
4. **Impact**: exposure concentration beyond risk limits.

**Path B: Cap checked before, not after, the increment** [C1]
Path key: `wrong_cap_check | openLoan() | EtherCollateral | cap_checked_before_not_after`
Entry surface: `openLoan(loanAmount)`
Contracts touched: `EtherCollateral`
Boundary crossed: `precondition vs postcondition validation`
1. sETH supply cap = C; current issued = C - epsilon.
2. `openLoan` passes the pre-check (`issued < C`).
3. The loan adds `loanAmount`, pushing issued far beyond C.
4. **Impact**: total issuance exceeds the protocol's stated cap (SigmaPrime fix: require post-increment total <= cap).

**Path C: At-capacity pool cannot be liquidated** [C7]
Path key: `wrong_cap_check | liquidate() | PoolManager→ReservePool | reserve_funds_exceed_capacity_dos`
Entry surface: `PoolManager.liquidate(poolId)` with bad debt
Contracts touched: `PoolManager -> ReservePool -> _changePoolCollateral`
Boundary crossed: `reserve-to-pool fund flow vs pool capacity`
1. Pool sits near its collateral capacity with bad debt in a tick.
2. Liquidation pulls `bonusFromReserve` from ReservePool and adds it to pool collateral.
3. `balance + bonusFromReserve > capacity` → `_changePoolCollateral` reverts → liquidation fails.
4. **Impact**: unliquidatable bad debt exactly when reserves are needed (acknowledged-not-fixed by f(x) due to rarity).

**Path D: Cap-reached vault redirects funds to idle market** [C5]
Path key: `wrong_cap_check | flashloan deposit | MetaMorpho→idleMarket | supply_cap_redirection_grief`
Entry surface: `deposit()` on the MetaMorpho vault when the target market cap is hit
Contracts touched: `MetaMorpho vault -> market supply cap -> idle market`
Boundary crossed: `allocation policy vs cap enforcement`
1. Attacker flash-loans enough to fill a market's supply cap exactly.
2. Subsequent deposits (from any user) route to the idle market instead.
3. Yield/reward expectations diverge; allocator griefed.
4. **Impact**: yield redirection and allocator griefing (attacker returns the flash loan).

#### Vulnerable Pattern Examples

**Example 1: Increment-only cap check (Zaros)** [MEDIUM]
```solidity
// ❌ VULNERABLE: compares ONLY this deposit against the cap
function _requireEnoughDepositCap(address collateralType, UD60x18 amount, UD60x18 depositCap) internal pure {
    if (amount.gt(depositCap)) { // @audit totalDeposited[collateralType] missing
        revert Errors.DepositCap(collateralType, amount.intoUint256(), depositCap.intoUint256());
    }
}
// Fix: if (totalDeposited[collateralType].add(amount).gt(depositCap)) revert ...
```

**Example 2: Pre-check only (Synthetix EtherCollateral)** [HIGH]
```solidity
// ❌ VULNERABLE: cap enforced only as a precondition
function openLoan(uint256 loanAmount) external {
    require(totalIssuedPynthDebt < supplyCap, "cap reached"); // @audit loan itself can blow past cap
    // ... issue loanAmount, totalIssued += loanAmount
}
// Fix: require(totalIssuedPynthDebt + loanAmount <= supplyCap)
```

**Example 3: Capacity revert inside liquidation (f(x))** [MEDIUM]
```solidity
// ❌ VULNERABLE: reserve top-up can exceed pool capacity and revert the liquidation
function liquidate(uint256 poolId, ...) external {
    uint256 bonusFromReserve = reservePool.withdraw(shortfall);
    _changePoolCollateral(poolId, int256(bonusFromReserve)); // @audit reverts if balance + bonus > capacity
}
function _changePoolCollateral(uint256 poolId, int256 delta) internal {
    require(poolCollateral[poolId] + uint256(delta) <= poolCapacity[poolId], "capacity");
}
```

**Example 4: Borrow-limit bypass per collateral (JOJO)** [MEDIUM]
```solidity
// ❌ VULNERABLE (shape): per-collateral borrow limit not aggregated
// users route borrows across collateral types, each under its individual limit,
// while total borrowing exceeds the intended global/user exposure
function _validateBorrowLimit(address collateral, uint256 amount) internal view {
    require(amount <= perCollateralBorrowLimit[collateral]); // @audit no per-user cumulative term
}
```

### Impact Analysis

#### Technical Impact

- Risk-limit bypass: exposure concentration beyond governance-set caps (6/9 unique findings: C1-C4, C6, C9)
- Liquidation/withdrawal DoS at capacity (2/9: C7, C8)
- Yield routing griefing via cap exhaustion (1/9: C5)

#### Business Impact

- Caps exist to bound oracle-error and tail risk; bypassing them silently re-concentrates that risk
- Liquidation failure at capacity is worst exactly during stress (bad debt + full pool)
- Idle-market redirection degrades expected returns for depositors and complicates allocator operations

#### Affected Scenarios

- Multi-transaction deposit flows against per-asset collateral caps
- CDP/synth issuance with pre-action cap checks
- Vaults layering caps (MetaMorpho market caps under a vault cap)
- Protocols whose liquidation path injects reserve funds into a capacity-limited bucket

### Secure Implementation

**Fix 1: Cumulative, atomic cap check (Zaros fix, commit 0d37299)**
```solidity
// ✅ SECURE: cumulative total + increment vs cap, checked at state change
function _requireEnoughDepositCap(address collateralType, uint256 amount) internal view {
    uint256 newTotal = totalDeposited[collateralType] + amount;
    if (newTotal > depositCaps[collateralType]) {
        revert Errors.DepositCap(collateralType, newTotal, depositCaps[collateralType]);
    }
}
```

**Fix 2: Post-increment invariant (Synthetix fix)**
```solidity
// ✅ SECURE: validate the state you are about to create
require(totalIssuedPynthDebt + loanAmount <= supplyCap, "exceeds supply cap");
totalIssuedPynthDebt += loanAmount;
```

**Fix 3: Exempt or reorder capacity checks for core flows**
```solidity
// ✅ SECURE: subtract outgoing collateral before adding reserve funds (OZ suggestion)
function liquidate(uint256 poolId, uint256 collateralOut, uint256 reserveIn) external {
    _changePoolCollateral(poolId, -int256(collateralOut)); // reduce first
    _changePoolCollateral(poolId, int256(reserveIn));      // then top up; no revert
}
```

### Detection Patterns

#### Contract / Call Graph Signals
```
- require statements pairing (amount, capConstant) without a totals storage read
- cap checks positioned before the state mutation they are supposed to bound
- liquidation / reserve functions calling a shared capacity validator with additive-only deltas
- derived caps (_maxDeposit-style) computed from stale or partial inputs
```

#### High-Signal Grep Seeds
```
- _requireEnoughDepositCap
- depositCap
- supplyCap
- borrowCap
- maxDeposit
- _changePoolCollateral
- isSupplyCapExceeded
- maxExternalDeposit
```

#### Code Patterns to Look For
```
- Pattern 1: `if (amount > depositCap) revert` — no `totalDeposited[...]` term
- Pattern 2: `require(total < cap)` followed by `total += amount` with no postcondition
- Pattern 3: `_changePoolCollateral(id, +reserveBonus)` inside liquidate with a capacity require
- Pattern 4: per-asset limit maps without a per-user or global aggregate companion
```

#### Audit Checklist
- [ ] For every cap: which storage variable holds the cumulative total, and is it in the same expression as the increment?
- [ ] Is the cap checked before or after the mutation? Re-derive the post-state.
- [ ] Do liquidation/reserve/redemption flows add funds into capped buckets? What happens when the bucket is full?
- [ ] Can a single flash loan push a market to its cap and change routing for other users?

### Real-World Examples

#### Known Exploits
- Cap-bypass incidents typically surface as risk-limit failures rather than direct exploits; the observable harm is concentration during depegs (see oracle manipulation entries for the compounding case).

#### Related CVEs/Reports
- SigmaPrime Synthetix EtherCollateral review (implemented fix)
- OpenZeppelin f(x) v2 audit (acknowledged capacity/liquidation edge case)

### Prevention Guidelines

#### Development Best Practices
1. Express every cap as a cumulative invariant: `total_after <= cap`, checked in the same expression as the increment.
2. Treat liquidation, reserve, and redemption flows as privileged with respect to capacity — or order deltas so reductions precede additions.
3. Fuzz caps with multi-transaction deposit sequences, not just single maximal deposits.

#### Testing Requirements
- Unit tests for: N sequential sub-cap deposits must revert at N+1 when the cumulative cap is crossed; liquidation succeeds on a full-capacity pool with bad debt
- Integration tests for: flash-loan to exact cap; idle-market routing behavior
- Fuzzing targets: cap invariant over random deposit/withdraw interleavings, including reverts on the exact boundary

### References

#### Technical Documentation
- Aave V2 supply/borrow caps implementation (`SupplyLogic` / `BorrowLogic` enforcement)
- Morpho MetaMorpho market cap + idle market semantics

#### Security Research
- Cyfrin Zaros report 2024-07-13 (verified fix)
- Cantina Morpho review (supply-cap idle redirection)

### Keywords for Search

`supply cap`, `borrow cap`, `deposit cap`, `collateral cap`, `cap bypass`, `multiple deposits bypass`, `cap enforcement`, `cumulative cap check`, `pool capacity`, `liquidation capacity DoS`, `reserve top up revert`, `maxDeposit`, `idle market`, `supply cap flash loan`, `risk limits`, `exposure limits`, `per-user limit bypass`

### Related Vulnerabilities

- [Bad Debt Socialization and Missing Write-Off](../bad-debt/bad-debt-socialization.md)
- [Liquidation Evasion and Borrower-Triggered Liquidation DoS](../liquidation/liquidation-evasion-dos.md)
- [Health Factor and Collateral Ratio Miscalculation](../risk-params/health-factor-miscalculation.md)
