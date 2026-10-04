---
# Core Classification
protocol: generic
chain: everychain
category: liquidation
vulnerability_type: self_liquidation_abuse

# Pattern Identity
root_cause_family: incentive_design_flaw
pattern_key: profitable_or_blocking_self_liquidation | liquidation_engine | owner_self_liquidation | value_extraction_or_evasion

# Interaction Scope
interaction_scope: multi_contract
involved_contracts:
  - LiquidationEngine / Borrower
  - VaultManager (collateral move)
  - Seize module (owner check)
  - Oracle adapters (Redstone / Pyth)
  - Flash loan provider
path_keys:
  - profitable_or_blocking_self_liquidation | liquidate() | Borrower→LiquidationEngine | self_liquidation_clears_warning_state
  - profitable_or_blocking_self_liquidation | seize() | AttackerProxy→Seize | owner_check_bypass_via_proxy
  - profitable_or_blocking_self_liquidation | liquidate() | OracleAdapter→Liquidation | oracle_sandwich_self_liquidation
  - profitable_or_blocking_self_liquidation | liquidate(id,to) | VaultManager→move | flash_loan_guard_bypass_via_liquidation_move

# Attack Vector Details
attack_type: economic_exploit
affected_component: liquidation_engine

# Technical Primitives
primitives:
  - liquidation discount
  - liquidationPenalty
  - owner-seizure check
  - warn / grace period
  - strain value
  - idToBlockOfLastDeposit
  - oracle price update sandwich
  - LTV vs discount factor
  - flash loan

# Grep / Hunt-Card Seeds
code_keywords:
  - liquidate
  - seize
  - CannotSeizeOwnPosition
  - idToBlockOfLastDeposit
  - LIQUIDATION_GRACE_PERIOD
  - unlockCallback
  - healthscore_liquidation
  - liquidationDiscount
  - DepositedInSameBlock

# Impact Classification
severity: high
impact: fund_loss
financial_impact: high

# Context Tags
tags:
  - lending
  - liquidation
  - economic
  - flash_loan
  - defi

# Version Info
language: solidity
version: all
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [L1] | reports/lending_borrowing_findings/h-1-it-is-possible-to-frontrun-liquidations-with-self-liquidation-with-high-stra.md | HIGH | Sherlock (Aloe II) | solodit 27659 / https://github.com/sherlock-audit/2023-10-aloe-judging/issues/29 |
| [L2] | reports/lending_borrowing_findings/proxy-based-self-liquidation-creates-bad-debt-for-lenders.md | HIGH | Cyfrin (Licredity) | solodit 62347 |
| [L3] | reports/lending_borrowing_findings/h-10-flash-loan-protection-mechanism-can-be-bypassed-via-self-liquidations.md | HIGH | Code4rena (DYAD) | solodit 33466 / https://github.com/code-423n4/2024-04-dyad-findings/issues/68 |
| [L4] | reports/lending_borrowing_findings/self-liquidations-of-leveraged-positions-can-be-profitable.md | HIGH | Spearbit (Euler Labs EVK) | solodit 35944 |
| [L5] | reports/lending_borrowing_findings/early-self-liquidations-receive-a-portion-of-future-fees-to-be-paid-by-other-cre.md | HIGH | Spearbit (Size v1) | solodit 35978 |
| [L6] | reports/lending_borrowing_findings/incorrect-implementation-of-self-liquidation.md | HIGH | OtterSec (Blend Capital) | solodit 47445 / https://github.com/blend-capital/blend-contracts |
| [L7] | reports/lending_borrowing_findings/h-02-liquidation-doesnt-account-for-penalty-when-calculating-collateral-to-give-.md | HIGH | Code4rena (Loopfi) | solodit 49024 / https://github.com/code-423n4/2024-07-loopfi-findings/issues/399 |

## Self-Liquidation Abuse in Lending Protocols

**When the borrower can trigger their own liquidation — directly or via a proxy — the liquidation discount, grace-state reset, collateral-move path, or fee split turns into either risk-free value extraction from lenders or a tool to keep unhealthy positions alive.**

### Overview

Self-liquidation is only safe if the economics guarantee the owner cannot profit and the mechanics cannot reset anti-abuse state. Seven unique HIGH findings from 6 audit firms (Sherlock, Cyfrin, Code4rena, Spearbit, OtterSec) show both failure modes: (a) profitable self-liquidation — penalty not applied to seized collateral (Loopfi), oracle-update sandwiches where `LTV_borrow > discountFactor * (1 - priceDrop)` (Euler EVK), owner-seizure checks bypassed with a proxy contract (Licredity), and early self-liquidations harvesting future fees paid by other creditors (Size); (b) blocking self-liquidation — a high-strain self-liquidation clears the warn/grace state (Aloe II), and liquidation's `move` path bypasses same-block deposit/withdraw flash-loan guards (DYAD).

#### Agent Quick View

- Root cause statement: "This vulnerability exists because the liquidation engine lets the position owner trigger or orchestrate their own liquidation while the discount/penalty math, state-reset logic, or guard coverage still favors them, allowing risk-free extraction of lender value or indefinite evasion."
- Pattern key: `profitable_or_blocking_self_liquidation | liquidation_engine | owner_self_liquidation | value_extraction_or_evasion`
- Interaction scope: `multi_contract`
- Primary affected component(s): `liquidation entry + owner-check + state machine (warn/grace) + collateral move`
- Contracts / modules involved: `Borrower/LiquidationEngine, Seize, VaultManager, AttackerProxy, Oracle adapters`
- Path keys: `self_liquidation_clears_warning_state`, `owner_check_bypass_via_proxy`, `oracle_sandwich_self_liquidation`, `flash_loan_guard_bypass_via_liquidation_move`
- High-signal code keywords: `seize`, `CannotSeizeOwnPosition`, `idToBlockOfLastDeposit`, `LIQUIDATION_GRACE_PERIOD`, `unlockCallback`, `liquidationDiscount`
- Severity: HIGH — 7/7 unique findings rated HIGH by their source auditors
- Typical sink / impact: `lender fund loss (shortfall socialized), risk-free profit, bad debt, liquidation DoS`
- Validation strength: `strong` (7 unique findings, 5+ independent audit firms, 7 protocols, all HIGH)

#### Contract / Boundary Map

- Entry surface(s): `liquidate()` callable by owner (or proxy), `seize()` via helper contract, `liquidate(id, to)` moving collateral between own accounts, `unlockCallback` orchestrations
- Contract hop(s): `AttackerRouter -> unlockCallback -> increaseDebtShare -> AttackerSeizer.seize` (Licredity); `Borrower.liquidate(high strain) -> slot0 warn bits cleared` (Aloe); `flashloan -> deposit A -> mint -> liquidate(A -> B) -> withdraw B -> repay` (DYAD)
- Trust boundary crossed: `owner-identity checks (msg.sender vs position.owner)`, `state-machine bits writable by any liquidation`, `oracle update trigger permission`, `same-block guard scope`
- Shared state or sync assumption: `self-liquidation must never be profitable`; `anti-manipulation guards must cover every fund-moving path, including liquidation`

#### Valid Bug Signals

- Signal 1: Nothing structurally prevents `msg.sender == position.owner` (directly or through a second contract) from calling the liquidation/seize entry.
- Signal 2: A profitability region exists: `discount - penalty > 0` for the configured parameters, or `LTV_borrow > discountFactor * (1 - priceDrop)` when the owner can trigger/choose the oracle update.
- Signal 3: Any liquidation (even one that leaves the position unchanged) resets grace/warn/cooldown state, or the liquidation `move` path skips same-block/flash-loan guards.

#### False Positive Guards

- Not this bug when: self-liquidation is intentionally allowed but provably unprofitable (penalty >= discount on the collateral-out side) and cannot reset any blocking state.
- Not this bug when: `position.owner == msg.sender` checks use identity that survives proxies (e.g. checking the ultimate beneficiary is out of scope for most protocols — most EVM protocols accept this and design economics instead).
- Safe if: liquidation-triggerable state can only be cleared when the position becomes healthy, and all fund-moving paths update manipulation guards.
- Dust-only impact: if the extracted bonus is smaller than gas + flash-loan cost for every reachable collateralization region, the issue collapses (see DYAD judge debate on kerosene acquisition cost).

### Vulnerability Description

#### Root Cause

1. **State reset on any liquidation** [L1]: `Aloe Borrower.liquidate` clears the warn bits (`slot0 = (slot0_ & SLOT0_MASK_POSITIONS) | SLOT0_DIRT`) regardless of how much is repaid; a self-liquidation with a very high strain value keeps the position essentially unchanged but clears the warning, re-arming the 2-minute grace period forever.
2. **Owner check bypassed by proxy** [L2]: `Licredity.seize` only checks `position.owner == msg.sender`; an `AttackerRouter` calls `unlock`, and inside `unlockCallback` takes debt and self-seizes via a separate `AttackerSeizer` contract — atomically undercollateralizing and liquidating to capture the bonus while socializing the shortfall.
3. **Guard not covering the liquidation path** [L3]: DYAD's `idToBlockOfLastDeposit` same-block guard is updated in `deposit` and checked in `withdraw`, but `liquidate` calls `vault.move(id, to, collateral)` without updating the destination's guard — flash-loaned collateral can enter account A and exit account B in one block.
4. **Economic region where self-liquidation pays** [L4]: Euler EVK — with user-triggerable oracle adapters (Redstone, Pyth), the attacker max-borrows at `LTV_borrow`, triggers the price drop, and self-liquidates from a subaccount; profit is positive whenever `LTV_borrow > discountFactor * (1 - priceDrop)`; several smaller liquidations deepen the effective discount.
5. **Fee-stream capture** [L5]: Size v1 — early self-liquidations receive a portion of future fees that other creditors would have paid, rewarding exactly the wrong actor.
6. **Penalty asymmetry** [L7]: Loopfi — collateral out is computed from gross `repayAmount` while debt is reduced by `repayAmount - penalty`, so the anti-self-liquidation penalty has no effect.
7. **Broken self-liquidation implementation** [L6]: Blend Capital — the self-liquidation routine itself mis-implemented (OtterSec), enabling mispriced outcomes.

#### Attack Scenario / Path Variants

**Path A: Self-liquidation clears the warning state (evasion)** [L1]
Path key: `profitable_or_blocking_self_liquidation | liquidate() | Borrower→LiquidationEngine | self_liquidation_clears_warning_state`
Entry surface: `account.liquidate(this, "", 1e10, ...)` (owner calling own liquidation with huge strain)
Contracts touched: `Borrower (slot0 state)`
Boundary crossed: `liquidation state machine bits`
1. Open a huge borrow with minimal margin; account becomes unhealthy and is warned.
2. Wait out `LIQUIDATION_GRACE_PERIOD` (2 min), then self-liquidate with a very high strain value — position stays unhealthy but the warning bits are cleared.
3. Every liquidator attempt now reverts ("Aloe: grace") for another 2 minutes.
4. Repeat forever.
5. **Impact**: bad debt grows; bank-run dynamics for lenders.

**Path B: Proxy bypass of the owner-seizure check (extraction)** [L2]
Path key: `profitable_or_blocking_self_liquidation | seize() | AttackerProxy→Seize | owner_check_bypass_via_proxy`
Entry surface: `unlock` + `unlockCallback`
Contracts touched: `AttackerRouter -> Licredity.unlock -> unlockCallback -> AttackerSeizer.seize`
Boundary crossed: `msg.sender identity check`
1. Deploy two contracts: router (position owner) and seizer.
2. Router opens a position, deposits minimal collateral, calls `unlock`.
3. In the callback: `increaseDebtShare` to make the position unhealthy, then `seizer.seize(positionId)` — `msg.sender` is the seizer, not the owner, so `CannotSeizeOwnPosition` never fires.
4. Bonus is captured; shortfall socialized to lenders; repeatable and atomic.
5. **Impact**: protocol value drain with no price movement required.

**Path C: Oracle-update sandwich self-liquidation (extraction)** [L4]
Path key: `profitable_or_blocking_self_liquidation | liquidate() | OracleAdapter→Liquidation | oracle_sandwich_self_liquidation`
Entry surface: user-triggered oracle update + liquidation from a subaccount
Contracts touched: `Oracle adapter (Redstone/Pyth) -> Liquidation engine`
Boundary crossed: `oracle update permission`
1. Flashloan collateral; build (1000 collateral, 900 debt) at `LTV_borrow = 90%`.
2. Trigger the oracle update moving collateral price to $0.90.
3. Self-liquidate from a subaccount repaying `maxRepayAssets = 810`; seize all 1000 collateral.
4. Repay flashloan; keep the 90-debt-asset difference.
5. **Impact**: risk-free profit; bad debt left for the protocol when repeated at scale.

**Path D: Liquidation `move` bypasses the same-block guard (extraction)** [L3]
Path key: `profitable_or_blocking_self_liquidation | liquidate(id,to) | VaultManager→move | flash_loan_guard_bypass_via_liquidation_move`
Entry surface: `liquidate(A, B)` between attacker accounts
Contracts touched: `VaultManager -> Vault.move`
Boundary crossed: `flash-loan guard scope (deposit/withdraw only)`
1. Flashloan into account A; kerosene price inflates; mint dyad at inflated CR.
2. Deflate kerosene price (account C action); account A becomes liquidatable.
3. Self-liquidate A, directing collateral to account B — `move` never updates `idToBlockOfLastDeposit[B]`.
4. Withdraw from B in the same block; repay flashloan.
5. **Impact**: positions opened at true CR ~1.0; systemic bad debt.

#### Vulnerable Pattern Examples

**Example 1: Warning cleared by any liquidation (Aloe II)** [HIGH]
```solidity
// ❌ VULNERABLE: even a no-op liquidation clears the liquidation warning
function liquidate(address recipient, bytes memory data, uint256 strain, uint256 nonce) external {
    // ...
    _repay(repayable0, repayable1);                       // high strain => ~nothing repaid
    slot0 = (slot0_ & SLOT0_MASK_POSITIONS) | SLOT0_DIRT; // @audit clears warn unconditionally
}
```

**Example 2: Owner check defeated by a second contract (Licredity)** [HIGH]
```solidity
// ❌ VULNERABLE: msg.sender identity is not the position owner when routed through a proxy
if (position.owner == msg.sender) {
    assembly ("memory-safe") { mstore(0x00, 0x7c474390) revert(0x1c, 0x04) } // CannotSeizeOwnPosition()
}
// AttackerRouter.unlockCallback:
//   licredity.increaseDebtShare(positionId, delta, address(this)); // make unhealthy
//   seizer.seize(positionId);                                      // msg.sender = seizer ≠ owner
```

**Example 3: Guard misses the liquidation move (DYAD)** [HIGH]
```solidity
// ❌ VULNERABLE: same-block guard only wired to deposit/withdraw
function deposit(uint id, uint amount) external { idToBlockOfLastDeposit[id] = block.number; ... }
function withdraw(uint id, uint amount) external {
    if (idToBlockOfLastDeposit[id] == block.number) revert DepositedInSameBlock(); // @audit not set by move
    ...
}
function liquidate(uint id, uint to) external {
    vault.move(id, to, collateral); // @audit receiving account 'to' never marked
}
```

**Example 4: Profitable region for leveraged self-liquidation (Euler EVK)** [HIGH]
```text
// ❌ VULNERABLE ECONOMICS: profitable iff LTV_borrow > discountFactor * (1 - priceDrop)
// with user-triggerable oracle updates (Redstone/Pyth) the priceDrop is chosen by the attacker:
//   maxBorrowAssets = LTV_borrow * collateral * price_0 / debtPrice      // 900
//   maxRepayAssets  = collateral * discountFactor * price_1 / debtPrice  // 810
//   profit = maxBorrowAssets - maxRepayAssets                            // 90, risk-free
```

### Impact Analysis

#### Technical Impact

- Risk-free value extraction from lenders/protocol (4/7 unique findings: L2, L3, L4, L7)
- Liquidation DoS and unbounded bad-debt accrual (2/7: L1, and L3's CR~1.0 positions)
- Misdirected fee streams from honest creditors to self-liquidators (1/7: L5)

#### Business Impact

- Repeatable, atomic drains (Licredity PoC repeats within liquidity/config limits) — no market movement needed
- Protocol insolvency: DYAD accounts left at CR ~1.0; Aloe-style bank runs where late withdrawers eat the bad debt
- Spearbit flagged the Euler EVK variant as leave-behind bad debt per attack

#### Affected Scenarios

- Any protocol where the liquidation entry lacks owner-adjacency restrictions AND the bonus economics can favor the borrower
- Warn/grace-period state machines where "any liquidation" resets the timer
- CDPs with internal-value collateral (e.g. kerosene) and flash-loan guards scoped to deposit/withdraw only
- Oracle adapters where users trigger or choose price updates (Redstone, Pyth)

### Secure Implementation

**Fix 1: Self-liquidation only via a provably fair path**
```solidity
// ✅ SECURE: dedicated self-liquidation entry without bonus, or owner-restricted economics
function liquidate(address borrower, ...) external {
    if (borrower == msg.sender) {
        // no discount for self-liquidation; penalty set so net cost >= market repayment
        discount = 1e18; // or revert to a dedicated closePosition() path
    }
}
```

**Fix 2: Clear warning state only when healthy**
```solidity
// ✅ SECURE: warn bits reset only if the position is healthy after the action
_repay(repayable0, repayable1);
if (_isHealthy()) {
    slot0 = (slot0_ & SLOT0_MASK_POSITIONS) | SLOT0_DIRT; // clear warn only on health
}
```

**Fix 3: Guards cover every fund-moving path**
```solidity
// ✅ SECURE: liquidation move marks the receiving account too
function liquidate(uint id, uint to) external {
    vault.move(id, to, collateral);
    idToBlockOfLastDeposit[to] = block.number; // same-block flash guard preserved
}
```

**Fix 4: Parameterize away the profitable region**
```solidity
// ✅ SECURE: ensure discountFactor * (1 - maxOracleMove) >= LTV_borrow for all markets,
// or make oracle updates keeper-only so priceDrop cannot be chosen by the attacker
require(liqConfig.discountFactor <= WAD - maxLTVBuffer, "self-liq profitable region");
```

### Detection Patterns

#### Contract / Call Graph Signals
```
- liquidate/seize entry with only a direct msg.sender identity check (defeated by proxy contracts)
- liquidation handler unconditionally clearing warn/cooldown/grace state
- fund-moving operations (move, transfer during liquidation) outside the same-block/manipulation guard set
- user-triggerable oracle updates on the same chain as liquidation with LTV close to discount factor
- fee/penalty configuration where discount - penalty > 0 for self-liquidators
```

#### High-Signal Grep Seeds
```
- CannotSeizeOwnPosition
- idToBlockOfLastDeposit
- LIQUIDATION_GRACE_PERIOD
- unlockCallback
- liquidationDiscount
- DepositedInSameBlock
- healthscore_liquidation
- slot0
```

#### Code Patterns to Look For
```
- Pattern 1: `if (position.owner == msg.sender) revert` as the only self-liquidation defense
- Pattern 2: `slot0 = (slot0_ & SLOT0_MASK...) | SLOT0_DIRT` (or any unconditional state reset) in liquidate
- Pattern 3: `vault.move(` inside liquidate with no guard update on the receiving id
- Pattern 4: `1e18 - liquidationDiscount` vs configured LTV — compute the profitable region
- Pattern 5: `takeCollateral = wdiv(repayAmount, discountedPrice)` with penalty applied only on the debt side
```

#### Audit Checklist
- [ ] Can the owner (or any contract they deploy) reach the liquidation/seize entry for their own position?
- [ ] Does any liquidation reset anti-abuse state regardless of resulting health?
- [ ] Do same-block / flash-loan guards cover liquidation `move` and every other fund-moving path?
- [ ] Is there a parameter region where `LTV_borrow > discountFactor * (1 - priceDrop)`? Who controls `priceDrop`?
- [ ] Where do liquidation penalties/discounts flow when the liquidator is related to the borrower?

### Real-World Examples

#### Known Exploits
- Euler (2022, $197M) — the donate-to-reserves self-liquidation is the canonical exploit instance of this family (see `DB/general/defihacklabs-business-logic-2023-patterns.md` Pattern 1).

#### Related CVEs/Reports
- Cyfrin Licredity review (proxy-based self-seize, fixed)
- Spearbit Euler EVK review (profitability formula `LTV_borrow > discountFactor * (1 - priceDrop)`)

### Prevention Guidelines

#### Development Best Practices
1. Decide explicitly: ban self-liquidation (identity checks are weak on EVM) or make it provably unprofitable (penalty >= discount on the collateral-out side).
2. State machines: only transitions to "not liquidatable" when the position is actually healthy post-action.
3. Manipulation guards must be property-based (all value entry/exit points), not function-name-based.
4. Model self-liquidation PnL as a function of configurable parameters and user-controllable inputs before launch.

#### Testing Requirements
- Unit tests for: self-liquidate with max strain keeps position unhealthy and does NOT clear warn; proxy-routed seize reverts or nets zero bonus; same-block flashloan -> deposit -> self-liquidate -> withdraw reverts
- Property/fuzz tests: for all (LTV, discount, penalty, priceDrop) in configured ranges, self-liquidation profit <= 0

### References

#### Technical Documentation
- Aave V3 liquidation discount parameterization
- Euler EVK eBTC-style liquidation incentives

#### Security Research
- Sherlock 2023-10-aloe issue #29 (warn-state reset escalation to HIGH)
- Spearbit Size/Euler reviews (fee-stream capture and leveraged self-liquidation economics)

### Keywords for Search

`self liquidation`, `self-liquidation profit`, `liquidation discount abuse`, `owner seizure`, `proxy bypass owner check`, `CannotSeizeOwnPosition`, `warn state reset`, `grace period reset`, `liquidation DoS`, `oracle sandwich`, `flash loan guard bypass`, `liquidation move`, `idToBlockOfLastDeposit`, `strain value`, `liquidation penalty asymmetry`, `bad debt creation`, `Euler donate to reserves`

### Related Vulnerabilities

- [Liquidation Seizure Economics Miscalculation](../liquidation/liquidation-seizure-economics.md)
- [Liquidation Evasion and Borrower-Triggered Liquidation DoS](../liquidation/liquidation-evasion-dos.md)
- [Oracle-Driven Liquidation Mispricing](../liquidation/oracle-driven-liquidation-mispricing.md)
- `DB/general/flash-loan/FLASH_LOAN_VULNERABILITIES.md`
