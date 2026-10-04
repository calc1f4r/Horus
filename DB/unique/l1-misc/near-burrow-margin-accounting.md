---
protocol: burrow-finance
chain: near
category: lending
vulnerability_type: margin_account_missing_checks

root_cause_family: missing_validation
pattern_key: divergent_code_paths | margin_withdraw | parallel_implementation | reserve_drain

interaction_scope: multi_contract
involved_contracts:
  - margin_actions.rs
  - margin_account.rs
  - margin_position.rs
  - actions.rs
  - margin_trading.rs
path_keys:
  - divergent_code_paths | internal_margin_withdraw_supply | reserves_drain
  - no_minimum_debt | internal_borrow | dust_bad_debt_accumulation
  - liquidator_controlled_slippage | process_decrease_margin_position | mev_extraction
  - untracked_storage | internal_set_margin_account | free_state_bloat

attack_type: logical_error
affected_component: margin_trading_module

primitives:
  - margin_account
  - min_token_d_amount
  - max_slippage_rate
  - uahpi (unit accurred holding-position interest)
  - debt_cap
  - storage_staking

code_keywords:
  - internal_margin_withdraw_supply
  - internal_withdraw
  - can_withdraw
  - available_amount
  - min_token_d_amount
  - is_min_amount_out_reasonable
  - max_slippage_rate
  - internal_set_margin_account
  - uahpi_at_open
  - force_closing_enabled
  - std::collections::HashMap

severity: high
impact: fund_loss
tags:
  - lending
  - margin_trading
  - near_sdk
  - rust
language: rust
version: "commit c09a41b (retest fb484de), Oct 2024"
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [BUR] | reports/other-l1_findings/public-audits-reports-near-sigma-prime-near-burrowland-security-assessment-report-v2-0-pdf.md | HIGH (5), MED (5) | Sigma Prime | NEAR Burrow "Burrowland" v2.0, Oct 2024 (22 findings) |
| [BUR-U] | reports/other-l1_findings/public-audits-reports-near-sigma-prime-burrow-finance-burrowland-security-assessment-report-v2-0-pdf.md | — | Sigma Prime | Burrowland Smart Contracts Update (follow-up) |

## NEAR Burrow (Burrowland) — Margin-Module Check Divergence, Dust Bad-Debt, and Liquidator Slippage Extraction

### Overview

Burrow's margin module reimplements lending actions as parallel code paths that omit the safety checks enforced on regular accounts: the margin withdraw path skips `available_amount()` and `can_withdraw` checks (reserves/fees can be withdrawn), there is no minimum debt (dust positions accumulate unliquidatable bad debt), and liquidators control the swap `min_token_d_amount` bound so they can sandwich liquidation swaps up to `max_slippage_rate`. Margin accounts also skip NEAR storage tracking, enabling free state bloat.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because margin-position code paths were implemented as copies of regular lending actions without the original validation checks, and because liquidation swap parameters are attacker-controlled within a slippage bound."
- Pattern key: `divergent_code_paths | margin_withdraw | parallel_implementation | reserve_drain`
- Interaction scope: `multi_contract`
- Primary affected component(s): `margin_actions.rs, margin_account.rs, margin_position.rs, actions.rs, margin_trading.rs`
- Path keys: see `path_keys` above
- High-signal code keywords: `internal_margin_withdraw_supply`, `min_token_d_amount`, `internal_set_margin_account`, `uahpi_at_open`
- Typical sink / impact: `reserve/fee drain, unliquidatable bad debt, MEV extraction from liquidated positions, storage DoS, duplicate fees`
- Validation strength: `strong` (per-finding code excerpts and resolutions in source)

#### Contract / Boundary Map

- Entry surface(s): `liquidate()`, force-close of margin positions, margin withdraw/decrease, `internal_borrow()`
- Contract hop(s): `margin_actions.internal_margin_withdraw_supply -> asset accounting; process_decrease_margin_position -> external DEX swap with liquidator-set min_token_d_amount`
- Trust boundary crossed: `DEX swap during liquidation (liquidator-chosen parameters)`, `margin accounts vs regular accounts (divergent validation)`
- Shared state or sync assumption: `margin accounts must obey the same asset invariants (available_amount, can_withdraw, minimum debt) as regular accounts`

#### Valid Bug Signals

- Signal 1: A withdraw/borrow path named or routed as "margin*" lacks checks present in the non-margin equivalent (`internal_withdraw`)
- Signal 2: `min_token_d_amount` (or `min_amount_out`) is supplied by the liquidator, only bounded by oracle price × `max_slippage_rate`
- Signal 3: `internal_set_margin_account` inserts into persistent state without `env::storage_byte_cost()`-style usage tracking while the regular account path tracks it

#### False Positive Guards

- Not this bug when: the margin path delegates to the same checked internal function as the regular path, or checks were added post-fix (commit fb484de resolved BUR-01/02/04/07/08)
- Safe if: minimum debt enforced on open AND close (dust from swaps handled), slippage bound set near zero, storage tracked on all account types
- Requires attacker control of: liquidation transactions (Path C), or simply opening many small positions (Path B); Path A needs any margin user

### Vulnerability Description

#### Root Cause

1. `internal_margin_withdraw_supply()` does not check `asset.available_amount()` (can withdraw reserves/fees → DoS) nor `asset.config.can_withdraw` (circumvents withdrawal restrictions) (BUR-01, High).
2. `internal_borrow()` enforces no minimum debt: dust positions cost more to liquidate than they hold → permanent bad debt (BUR-02, High).
3. Liquidator sets `min_token_d_amount` bounded only by `is_min_amount_out_reasonable()` using oracle price and `max_slippage_rate` → sandwich own liquidation swap, extract up to slippage bound (BUR-05, High, closed-accepted).
4. `internal_set_margin_account()` does no storage tracking → free unlimited margin-account creation → state bloat/DoS (BUR-04, High).
5. `uahpi_at_open` not updated after fee payment → duplicate holding-position fees on every decrease (BUR-08, Medium).

#### Attack Scenario / Path Variants

**Path A: Margin withdraw drains reserves / bypasses can_withdraw** [HIGH]
Path key: `divergent_code_paths | internal_margin_withdraw_supply | reserves_drain`
1. Open margin position with asset whose `can_withdraw == false` or withdraw amount > `available_amount()`
2. Call margin withdraw path which skips both checks
3. Reserves/protocol fees withdrawn or restricted asset exits
4. Accounting corrupted; potential DoS of withdrawals for others

**Path B: Dust debt positions → unliquidatable bad debt** [HIGH]
Path key: `no_minimum_debt | internal_borrow | dust_bad_debt_accumulation`
1. Attacker opens many near-zero debt positions (regular or margin)
2. Each position's collateral < gas/profit to liquidate
3. Positions fall underwater; nobody liquidates
4. Protocol accrues bad debt indefinitely (deflation of share value)

**Path C: Liquidator sandwiches liquidation swap** [HIGH]
Path key: `liquidator_controlled_slippage | process_decrease_margin_position | mev_extraction`
1. Underwater margin position with bad debt is liquidatable
2. Liquidator sets `min_token_d_amount` to the lowest value passing `is_min_amount_out_reasonable()`
3. Sandwich the DEX swap; extract value up to `max_slippage_rate`
4. Liquidations: value taken from position owner; force-closures: bad debt grows, protocol solvency impacted

**Path D: Free storage bloat via margin accounts** [HIGH]
Path key: `untracked_storage | internal_set_margin_account | free_state_bloat`
1. Attacker creates many margin accounts / large accounts
2. No storage fee charged (insert without usage tracking)
3. Contract state grows unboundedly → DoS

#### Vulnerable Pattern Examples

**Example 1: Margin withdraw missing the checks of its sibling path** [Approx Vulnerability : HIGH]
```rust
// ❌ VULNERABLE: BUR-01 — margin withdraw skips available_amount() and can_withdraw
// checks that internal_withdraw() enforces for regular accounts
pub(crate) fn internal_margin_withdraw_supply(&mut self, token_id: &TokenId, amount: Balance) {
    // no asset.available_amount() check -> reserves/fees withdrawable
    // no asset.config.can_withdraw check -> restricted assets withdrawable
    self.internal_remove_liquidity(token_id, amount);
}
```

**Example 2: No minimum debt on borrow** [Approx Vulnerability : HIGH]
```rust
// ❌ VULNERABLE: BUR-02 — dust debt positions are unprofitable to liquidate
pub fn internal_borrow(&mut self, position: &String, account: &mut Account, asset_amount: &AssetAmount) -> Balance {
    // No checks for minimum debt amount
    asset.borrowed.deposit(borrowed_shares, amount);
    // ...
}
```

**Example 3: Liquidator-controlled swap bound** [Approx Vulnerability : HIGH]
```rust
// ❌ VULNERABLE: BUR-05 — min_token_d_amount set by liquidator; bound is oracle×max_slippage_rate
fn process_decrease_margin_position(...) {
    // is_min_amount_out_reasonable() only checks min_token_d_amount against
    // current oracle prices and max_slippage_rate; liquidator sets the minimum,
    // then sandwiches the swap up to that bound
}
```

**Example 4: Untracked storage insert** [Approx Vulnerability : HIGH]
```rust
// ❌ VULNERABLE: BUR-04 — no storage usage tracked for margin accounts
pub(crate) fn internal_set_margin_account(&mut self, account_id: &AccountId, account: MarginAccount) {
    self.margin_accounts.insert(account_id, &account.into()); // no storage charge
}
```

### Impact Analysis

#### Technical Impact
- Reserve/fee drain and withdrawal-restriction bypass
- Permanent dust bad debt (share deflation for lenders)
- MEV extraction from liquidated users; worsened bad debt on force-closures
- Unbounded contract state growth

#### Business Impact
- Protocol insolvency risk via bad-debt accumulation and reserve loss
- User funds extracted during liquidations

#### Affected Scenarios
- Any NEAR (or general) protocol with parallel "margin/X accounts" reimplementing core actions
- Liquidation flows routing through AMMs with user-supplied min-out

### Secure Implementation

**Fix 1: Unify checked paths (upstream fix, commit fb484de)**
```rust
// ✅ SECURE: single withdraw implementation enforcing available_amount and can_withdraw,
// regardless of account type; margin paths added the missing checks
pub(crate) fn internal_margin_withdraw_supply(&mut self, token_id: &TokenId, amount: Balance) {
    let asset = self.internal_get_asset(token_id);
    assert!(amount <= asset.available_amount(), "ERR_EXCEEDS_AVAILABLE");
    assert!(asset.config.can_withdraw, "ERR_WITHDRAW_DISABLED");
    // ...
}
```

**Fix 2: Minimum debt + tighter slippage governance**
```text
// ✅ SECURE: enforce minimum debt on open and close (min_token_d_amount checked so
// repaying leaves no dust), and set max_slippage_rate low enough that sandwich
// extraction is negligible while liquidations still go through (Sigma Prime rec)
```

### Detection Patterns

#### High-Signal Grep Seeds
```
- internal_margin_withdraw_supply
- internal_withdraw
- min_token_d_amount
- is_min_amount_out_reasonable
- max_slippage_rate
- internal_set_margin_account
- uahpi_at_open
- force_closing_enabled
```

#### Code Patterns to Look For
```
- "margin_*"/"internal_*_margin_*" functions that duplicate non-margin logic minus validation
- Borrow functions with no minimum-debt assert
- Liquidation/force-close paths taking min-out from msg.sender
- near_sdk LookupMap/UnorderedMap inserts with no storage_usage accounting
- Fee accrual snapshots (uahpi_at_open-style) never updated after fee settlement
```

#### Audit Checklist
- [ ] Diff every margin path against its regular-account twin for missing asserts
- [ ] Is minimum debt enforced on open AND close for both account types?
- [ ] Who supplies min-out on liquidation swaps, and what bounds it?
- [ ] Is NEAR storage tracked for every account-type insert?
- [ ] Are interest/fee snapshots updated when fees are charged?

### Real-World Examples

#### Related Reports
- Sigma Prime, NEAR Burrow (Burrowland) v2.0 Oct 2024: BUR-01/02/03/04/05 High; BUR-07/08/09 Medium (03 closed-accepted as intentional rollbacks; 05 closed with "max_slippage_rate will be set appropriately")

### Keywords for Search

`near`, `burrow`, `burrowland`, `margin trading`, `margin account`, `dust debt`, `bad debt`, `minimum debt`, `liquidation`, `min_token_d_amount`, `slippage`, `sandwich`, `storage tracking`, `near_sdk`, `uahpi`, `holding position fee`, `force close`, `can_withdraw`, `available_amount`, `divergent code paths`

### Related Vulnerabilities

- DB/unique/l1-misc/near-aurora-rainbow-bridge-light-client.md
- DB/general/missing-validations/ entries (minimum-borrow checks)
