---
# Core Classification
protocol: generic
chain: polkadot
category: business_logic
vulnerability_type: state_accounting_error
root_cause_family: missing_state_update
pattern_key: unbalanced-claim-refund | crowdloan vault accounting | contribution not decremented | stale vault totals

# Interaction Scope
interaction_scope: single_contract
involved_contracts:
  - pallets/crowdloans
  - vault storage (vault.contributed)
path_keys:
  - unbalanced-claim-refund | claim | contribution_kill without decrement | inflated vault.contributed
  - unbalanced-claim-refund | refund | contribution_kill without decrement | wrong cap/strategy decisions
  - unbalanced-claim-refund | update_vault no-op | misleading VaultUpdated event | operator desync

# Attack Vector Details
attack_type: logic_flaw
affected_component: crowdloan_claim_refund_accounting

# Technical Primitives
primitives:
  - vault.contributed
  - contribution_kill
  - ChildStorageKind::Contributed
  - VaultPhase
  - ctoken
  - trie_index

# Grep / Hunt-Card Seeds
code_keywords:
  - contribution_kill
  - vault.contributed
  - claim
  - refund
  - update_vault
  - set_vrfs
  - VrfOrigin
  - VaultClaimed

severity: medium
impact: accounting_corruption
language: rust
tags:
  - substrate
  - pallet
  - crowdloan
  - state_management
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [plf7] | reports/substrate-l1_findings/parallel-tob-1.md | UNDETERMINED (Med) | Trail of Bits | 7. Missing calculations in crowdloans extrinsics (TOB-PLF-7) |
| [plf8] | reports/substrate-l1_findings/parallel-tob-1.md | INFORMATIONAL | Trail of Bits | 8. VaultUpdated/VrfsUpdated events emitted when no update happened |
| [plf1p] | reports/substrate-l1_findings/publications-reviews-parallelfinance-pdf.md | UNDETERMINED | Trail of Bits | same TOB-PLF-7 finding (published copy) |
| [plf6] | reports/substrate-l1_findings/parallel-tob-1.md | MEDIUM | Trail of Bits | 6. Failed XCM requests unhandled in crowdloans pallet |
| [x9] | reports/substrate-l1_findings/audit-reports-zeitgeist-2025-01-02-audit-report-zeitgeist-combinatorial-betting-and-futarchy-security-audit-v1-0-pdf.md | HIGH | auditor | Low account costs could facilitate the exhaustion of parachain resources |
| [x11] | reports/substrate-l1_findings/audits-interlay-informal-report-interlay-audit-2021q2-pdf.md | MEDIUM | Informal Systems | Informal Systems InterBTC Parachain IF-INTERLAY-LIQUIDATION: Liquidation event incen- tives unclear |
| [x12] | reports/substrate-l1_findings/audits-interlay-informal-report-interlay-audit-2021q2-pdf.md | HIGH | Informal Systems | InterBTC Parachain IF-INTERLAY-NO-BLOCK: Scenario of "no block being recently submitted" (all relayers offline) not handled grace- fully |
| [x13] | reports/substrate-l1_findings/audits-interlay-informal-report-interlay-audit-2021q2-pdf.md | HIGH | Informal Systems | Informal Systems InterBTC Parachain IF-INTERLAY-THEFT: Theft by redeeming (replacing) too much |
| [x14] | reports/substrate-l1_findings/audits-interlay-informal-report-interlay-audit-2021q2-pdf.md | HIGH | Informal Systems | Informal Systems InterBTC Parachain IF-INTERLAY-TIMEOUT: Timeouts (and races) on sender chain |
| [x15] | reports/substrate-l1_findings/audits-interlay-informal-report-interlay-audit-2021q3-pdf.md | HIGH | Informal Systems | InterBTC Parachain Modules and Vault Client IF-INTERLAY2-EXPIRATION: Possible disagreement on expiration status from request cancellation |
| [x16] | reports/substrate-l1_findings/audits-interlay-informal-report-interlay-audit-2021q3-pdf.md | MEDIUM | Informal Systems | Systems InterBTC Parachain Modules and Vault Client IF-INTERLAY2-MINTING: Vault not banned precondition not enforced on minting tokens |
| [x17] | reports/substrate-l1_findings/interlay-informal-2021q2.md | MEDIUM | Informal Systems | Informal Systems InterBTC Parachain IF-INTERLAY-LIQUIDATION: Liquidation event incen- tives unclear |
| [x18] | reports/substrate-l1_findings/interlay-informal-2021q2.md | HIGH | Informal Systems | InterBTC Parachain IF-INTERLAY-NO-BLOCK: Scenario of "no block being recently submitted" (all relayers offline) not handled grace- fully |
| [x19] | reports/substrate-l1_findings/interlay-informal-2021q2.md | HIGH | Informal Systems | Informal Systems InterBTC Parachain IF-INTERLAY-THEFT: Theft by redeeming (replacing) too much |
| [x20] | reports/substrate-l1_findings/interlay-informal-2021q2.md | HIGH | Informal Systems | Informal Systems InterBTC Parachain IF-INTERLAY-TIMEOUT: Timeouts (and races) on sender chain |
| [x21] | reports/substrate-l1_findings/interlay-informal-2021q3.md | HIGH | Informal Systems | InterBTC Parachain Modules and Vault Client IF-INTERLAY2-EXPIRATION: Possible disagreement on expiration status from request cancellation |
| [x22] | reports/substrate-l1_findings/interlay-informal-2021q3.md | MEDIUM | Informal Systems | Systems InterBTC Parachain Modules and Vault Client IF-INTERLAY2-MINTING: Vault not banned precondition not enforced on minting tokens |

## Crowdloan Claim/Refund Fails to Decrement vault.contributed, Corrupting Vault Accounting

**The claim and refund extrinsics erase a contributor's child-storage entry but never subtract the amount from vault.contributed, leaving stale totals that drive later cap, phase and strategy decisions** - representative of payout extrinsics that destroy per-user state without updating aggregate state.

### Overview

Parallel Finance's crowdloans pallet tracks both a per-contributor child-trie record and an aggregate `vault.contributed`. `claim` (and `refund`) call `contribution_kill` on the child storage but omit the matching subtraction from `vault.contributed`, so the vault total stays inflated forever. Downstream logic that reads `vault.contributed` (caps, auctions accounting, strategy switches) computes on wrong data. A sibling issue ([plf8]) emits `VaultUpdated`/`VrfsUpdated` events even when `update_vault`/`set_vrfs` changed nothing, desyncing off-chain operators.

#### Agent Quick View

- Root cause statement: "Payout extrinsics mutate per-user contribution records but skip the aggregate `vault.contributed -= amount` bookkeeping, so aggregate and per-user views permanently diverge."
- Pattern key: `unbalanced-claim-refund | crowdloan vault accounting | contribution not decremented | stale vault totals`
- Interaction scope: `single_contract`
- Primary affected component(s): `crowdloans pallet claim/refund, vault aggregate storage`
- Contracts / modules involved: `pallets/crowdloans, vault.contributed`
- Path keys: `claim | contribution_kill without decrement`, `refund | contribution_kill without decrement`, `update_vault no-op | misleading event`
- High-signal code keywords: `contribution_kill, vault.contributed, claim, refund, update_vault, set_vrfs`
- Typical sink / impact: `wrong cap enforcement, wrong refund/claim amounts in later logic, operator desync`
- Validation strength: `moderate` (single auditor; severity undetermined; issue confirmed against source)

#### Contract / Boundary Map

- Entry surface(s): `claim()`, `refund()`, `update_vault()`, `set_vrfs()`
- Contract hop(s): `crowdloans dispatchable -> child trie (Contributed) -> vault storage`
- Trust boundary crossed: `none (logic bug)` — severity comes from downstream trust in vault totals
- Shared state or sync assumption: `vault.contributed must equal sum of live child-trie contributions`

#### Valid Bug Signals

- Signal 1: An extrinsic removes/zeroes a per-user contribution record but the enclosing vault struct's `contributed` field is never mutated in the same call.
- Signal 2: Any code path where `contribution_kill(...)` is not immediately paired with a `checked_sub`/`saturating_sub` on the aggregate.
- Signal 3: Success events (`VaultUpdated`, `VrfsUpdated`) emitted regardless of whether any field actually changed ([plf8]).

#### False Positive Guards

- Not this bug when: the aggregate is recomputed lazily from the child trie (no cached total) — then no stale copy exists.
- Safe if: claim/refund paths are followed by a reconciliation hook or the vault is terminal (phase Ended) before the total is read again.
- Requires attacker control of: none required to corrupt state; ordinary users claiming trigger it.

### Vulnerability Description

#### Root Cause

`claim`/`refund` were written to pay out and clean up the contributor's record but the author forgot the aggregate update: `Self::contribution_kill(vault.trie_index, &who, ChildStorageKind::Contributed)` runs with no `vault.contributed -= amount` before or after ([plf7], Figure 7.1, pallets/crowdloans/src/lib.rs:718-765).

#### Attack Scenario / Path Variants

**Path A: Claim leaves stale aggregate**
Path key: `unbalanced-claim-refund | claim | contribution_kill without decrement`
Entry surface: `claim(crowdloan, lease_start, lease_end)`
1. Contributor calls `claim` after the vault succeeds; ctoken is paid and the child-trie entry is killed.
2. `vault.contributed` still includes the claimed amount.
3. Any later logic keyed on the total (cap checks, `contribution_strategy` decisions, next-crowdloan capacity) overstates real contributions.

**Path B: Refund leaves stale aggregate**
Path key: `unbalanced-claim-refund | refund | contribution_kill without decrement`
1. Same omission in `refund` for failed auctions.
2. Vault totals diverge from refundable liabilities, mispricing the vault's obligations.

**Path C: No-op update events desync operators**
Path key: `unbalanced-claim-refund | update_vault no-op | misleading VaultUpdated event`
1. Privileged `update_vault`/`set_vrfs` called with unchanged parameters.
2. `VaultUpdated`/`VrfsUpdated` emitted anyway; monitoring assumes state changed ([plf8]).

#### Vulnerable Pattern Examples

**Example 1: claim without aggregate subtraction (from [plf7])** [Approx Vulnerability : MEDIUM]
```rust
// ❌ VULNERABLE: child entry killed but vault.contributed untouched
pub fn claim(origin: OriginFor<T>, crowdloan: ParaId,
             lease_start: LeasePeriod, lease_end: LeasePeriod) -> DispatchResult {
    // ... payout to `who` ...
    Self::contribution_kill(vault.trie_index, &who, ChildStorageKind::Contributed);
    // MISSING: vault.contributed = vault.contributed.saturating_sub(amount);
    Self::deposit_event(Event::<T>::VaultClaimed(/*..*/));
    Ok(())
}
```

**Example 2: refund with same omission (from [plf7])** [Approx Vulnerability : MEDIUM]
```rust
// ❌ VULNERABLE: refund mirrors claim's missing subtraction
pub fn refund(origin: OriginFor<T>, crowdloan: ParaId, lease: (LeasePeriod, LeasePeriod)) -> DispatchResult {
    // ... refund transferred ...
    Self::contribution_kill(vault.trie_index, &who, ChildStorageKind::Contributed);
    Ok(()) // vault.contributed never decremented
}
```

**Example 3: unconditional update events (from [plf8])** [Approx Vulnerability : LOW]
```rust
// ❌ VULNERABLE: event emitted even when nothing changed
pub fn update_vault(origin: OriginFor<T>, crowdloan: ParaId, cap: Option<BalanceOf<T>>,
                    end_block: Option<BlockNumberFor<T>>, /* ... */) -> DispatchResult {
    T::UpdateVaultOrigin::ensure_origin(origin)?;
    let mut vault = Self::current_vault(crowdloan).ok_or(Error::<T>::VaultDoesNotExist)?;
    if let Some(cap) = cap { vault.cap = cap; }   // may be a no-op
    Self::deposit_event(Event::<T>::VaultUpdated(/* always emitted */));
    Ok(())
}
```

### Impact Analysis

#### Technical Impact

- Permanent divergence between aggregate and per-user accounting; wrong cap enforcement and downstream amount calculations; unhandled XCM failures in the same pallet can strand contributions ([plf6]).

#### Business Impact

- Crowdloan capacity and refund liability misstated; operator automation acting on false VaultUpdated signals.

#### Affected Scenarios

- Any vault/crowdloan-style pallet caching an aggregate total of per-user records paid out by claim/refund extrinsics.

### Secure Implementation

**Fix 1: Balance every payout with an aggregate update**
```rust
// ✅ SECURE: kill child entry AND decrement vault total atomically
Self::contribution_kill(vault.trie_index, &who, ChildStorageKind::Contributed);
Vaults::<T>::mutate(crowdloan, lease, |v| {
    let vault = v.as_mut().expect("vault checked above");
    vault.contributed = vault.contributed.saturating_sub(amount);
});
Self::deposit_event(Event::<T>::VaultClaimed(/* ..amount.. */));
```

**Fix 2: only emit update events on real diffs**
```rust
// ✅ SECURE: diff old/new before emitting
let changed = old != new;
if changed { Vaults::<T>::insert(crowdloan, lease, new.clone()); }
if changed { Self::deposit_event(Event::<T>::VaultUpdated(/* .. */)); }
```

### Detection Patterns

#### High-Signal Grep Seeds
```
- contribution_kill
- vault.contributed
- fn claim(
- fn refund(
- VaultClaimed
- VaultUpdated
```

#### Code Patterns to Look For
```
- Pattern 1: contribution_kill / child-trie removal not followed by aggregate mutate in same function
- Pattern 2: payout events carrying amounts while storage totals are not adjusted
- Pattern 3: emit-before-check update extrinsics (events on no-ops)
```

#### Audit Checklist
- [ ] For every payout extrinsic: is every stored total that the payout affects decremented?
- [ ] Is there an invariant test `vault.contributed == sum(child_trie)` after claim/refund?
- [ ] Do update extrinsics emit events only when state actually changed?

### Keywords for Search

`crowdloan`, `claim`, `refund`, `contribution_kill`, `vault.contributed`, `child trie`, `trie_index`, `ctoken`, `VaultPhase`, `contribution cap`, `auction refund`, `Parallel Finance`, `state accounting`, `missing subtraction`, `stale total`, `VaultUpdated`, `set_vrfs`

### Related Vulnerabilities

- DB/substrate/pallets/multi-asset-reserve-accounting.md
- DB/substrate/pallets/vesting-schedule-bypass.md
