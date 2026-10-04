---
# Core Classification
protocol: generic
chain: polkadot
category: access_control
vulnerability_type: missing_access
root_cause_family: missing_validation
pattern_key: missing-relock-balance-verification | staking ledger | unlocked-chunk relock | double-spend staking rewards

# Interaction Scope
interaction_scope: single_contract
involved_contracts:
  - pallet_dapp_staking_v3
  - pallet_balances
path_keys:
  - missing-relock-balance-verification | staking ledger | unlocked-chunk relock | double-spend staking rewards | unlock+transfer+relock_unlocking | DappStaking->Balances

# Attack Vector Details
attack_type: logical_error
affected_component: staking_ledger

# Technical Primitives
primitives:
  - unlocked_chunks
  - ledger_balance
  - relock_unlocking
  - free_balance_transfer
  - lock_registry

# Grep / Hunt-Card Seeds
code_keywords:
  - relock_unlocking
  - unlocked_chunks
  - Ledger::unlock
  - assert_unlock
  - transfer_all
  - staked_amount
  - AccountLedger

severity: critical
impact: fund_loss
language: rust
tags:
  - substrate
  - pallet
  - staking
  - double_spend
  - state_validation
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [astar1] | reports/substrate-l1_findings/astar-srl-2401.md | CRITICAL | SRLabs | Issue 1, dApp staking v3 baseline 2024-01 |
| [astar4] | reports/substrate-l1_findings/astar-srl-2401.md | MEDIUM | SRLabs | Issue 4, loyal staker abuse |
| [astar3] | reports/substrate-l1_findings/astar-srl-2401.md | LOW | SRLabs | Issue 3, unregistered dApps not removed |
| [x5] | reports/substrate-l1_findings/chainflip-backend-audits-2023-04-trailofbits-securityreview-pdf.md | MEDIUM | Trail of Bits | Validators can report nonparticipants in ceremonies |
| [x6] | reports/substrate-l1_findings/composable-audits-halborn-audit20210229-pallets-core-pdf.md | HIGH | Halborn | 3.4 (HAL-04) OFFER CREATION WITH THE SAME ASSET - HIGH Description: Inside the bonded-finance pallet, the do_offer function accepts offers w |
| [x7] | reports/substrate-l1_findings/composable-halborn-core.md | HIGH | Halborn | 3.4 (HAL-04) OFFER CREATION WITH THE SAME ASSET - HIGH Description: Inside the bonded-finance pallet, the do_offer function accepts offers w |
| [x8] | reports/substrate-l1_findings/publicreports-substrate-audits-nodle-nodl-substrate-pallet-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | 3.2 (HAL-02) HAL-02 DENOMINATION LOGIC SHOULD BE IMPROVED - MEDIUM Description: It was observed that if a nominator has a single validator, |
| [x13] | reports/substrate-l1_findings/audit-reports-snowbridge-2025-12-29-audit-report-snowbridge-fiat-shamir-beefy-changes-v1-0-pdf.md | CRITICAL | Oak Security | Fiat-Shamir subsampling does not guarantee the inclusion of any honest validator |
| [x14] | reports/substrate-l1_findings/zenlink-slowmist-bifrost.md | HIGH | SlowMist | erabilities found in this audit: NO Title Category Level Status N1 Inaccurate calculation method used Value Overﬂow Audit |
| [q15] | reports/substrate-l1_findings/composable-audits-solana-restaking-v2-composable-audit-draft-v2-pdf.md | HIGH | OtterSec | Incorrect stake adjustment (OS-CFI-ADV-003) (composable solana restaking v2 draft) |
| [q16] | reports/substrate-l1_findings/composable-audits-solana-restaking-v2-composable-audit-draft-v2-pdf.md | LOW | OtterSec | Potential fund lockup (OS-CFI-ADV-007) (composable solana restaking v2 draft) |
## Staking Ledger Relock of Already-Spent Unlocked Chunks (Double Spend)

**Astar dApp staking v3: `relock_unlocking` re-locks tokens that were already unlocked and transferred away, letting one balance earn staking rewards multiple times** - a classic ledger-vs-free-balance desynchronization in Substrate staking pallets.

### Overview

When a user unstakes, the amount moves into `unlocked_chunks` pending release. Astar's dApp staking v3 `relock_unlocking` re-locks based on the pending chunk records without verifying the account still holds the free balance, so tokens can be transferred out first and then "re-locked" into staking from nothing.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because `relock_unlocking` trusts `unlocked_chunks` records instead of verifying the corresponding balance still exists in the ledger/free balance."
- Pattern key: `missing-relock-balance-verification | staking ledger | unlocked-chunk relock | double-spend staking rewards`
- Interaction scope: `single_contract` (DappStaking ledger reads Balances free balance)
- Primary affected component(s): `dapp-staking-v3 ledger / unlock / relock extrinsics`
- Contracts / modules involved: `pallets/dapp-staking-v3, pallet_balances`
- Path keys: `missing-relock-balance-verification | unlock+transfer+relock_unlocking | DappStaking->Balances`
- High-signal code keywords: `relock_unlocking, unlocked_chunks, AccountLedger, transfer_all`
- Typical sink / impact: `staking reward inflation / double spend / accounting corruption`
- Validation strength: `moderate` (1 auditor, critical severity, mitigated)

#### Contract / Boundary Map

- Entry surface(s): `unstake()`, `unlock()`, `Balances::transfer_all()`, `relock_unlocking()`, `stake()`
- Contract hop(s): `DappStaking.unlock -> Balances.free_balance (transfer out) -> DappStaking.relock_unlocking -> DappStaking.stake`
- Trust boundary crossed: `pallet-to-pallet shared account state (staking ledger vs balances lock registry)`
- Shared state or sync assumption: `unlocked_chunks total must never exceed the account's actual locked/available balance`

#### Valid Bug Signals

- Signal 1: A relock/claim path that reads `unlocked_chunks` (or equivalent pending-release records) without cross-checking `free_balance` or the Balances lock at execution time.
- Signal 2: Transfer of unlocked funds out of the account between unlock and relock does not reduce the relockable amount.
- Signal 3: The same underlying tokens produce staking rewards on two accounts (or two eras) — measurable reward inflation.

#### False Positive Guards

- Not this bug when: relock amount is recomputed from `T::Currency::free_balance()` / `usable_balance()` at call time, or unlock burns the chunk record atomically on release.
- Safe if: the Balances pallet holds a named lock that is decremented on transfer, making the withdrawn amount unusable.
- Requires attacker control of: only their own account and normal extrinsic ordering (no privileged origin needed).

### Vulnerability Description

#### Root Cause

The dApp staking v3 ledger tracks pending unlocks as `unlocked_chunks`, but `relock_unlocking` converts chunks back into staked balance using the recorded amounts. After `unlock` credits free balance, the chunk records persist; a `transfer_all` moves the funds elsewhere, yet the stale chunk records still authorize relocking (and re-staking) of tokens the account no longer has.

#### Attack Scenario / Path Variants

**Path A: Unlock → Transfer → Relock → Restake (double reward)**
Path key: `missing-relock-balance-verification | unlock+transfer+relock_unlocking | DappStaking->Balances`
Entry surface: `unlock()` then `Balances::transfer_all()` then `relock_unlocking()`
Contracts touched: `DappStaking -> Balances -> DappStaking`
Boundary crossed: `shared account state between pallets`
1. Attacker locks 500 of 1000 tokens and stakes them.
2. `unlock(500)` marks the chunk; free balance becomes spendable after the unlocking period.
3. `transfer_all` moves the 500 to a second account.
4. `relock_unlocking` on the first account re-locks the phantom 500 and re-stakes them — rewards now accrue on both accounts for one real balance.

**Path B: Loyal-staker bonus abuse (related ledger-trust issue)**
Path key: `stale-ledger-records | staking ledger | era-boundary manipulation | unfair loyalty bonus`
Entry surface: `stake/unstake churn at era boundary`
1. Attacker manipulates staking tenure records (Issue 4 of same report) to qualify for loyal-staker rewards they should not receive.

#### Vulnerable Pattern Examples

**Example 1: Astar dApp staking v3 `relock_unlocking` (actual PoC from [astar1])** [Approx Vulnerability : CRITICAL]
```rust
// ❌ VULNERABLE: relock trusts unlocked_chunks records; balance may already be transferred away
// ExtBuilder::build().execute_with(|| {
//     let account = 2;
//     assert_lock(account, 500);        // lock and stake 500
//     assert_unlock(account, 500);      // start unlocking -> chunk record created
//     // transfer ALL free balance to another account
//     assert_ok!(Balances::transfer_all(RuntimeOrigin::signed(account), other_account, true));
//     // Relock_unlocking will "relock" the 500 even though the account no longer holds it
//     DappStaking::relock_unlocking(RuntimeOrigin::signed(account), dapp_id);
//     // -> phantom staked balance earns rewards; tokens double-spent across accounts
// });
```

**Example 2: Generic pattern — relock from records, not from balance** [Approx Vulnerability : HIGH]
```rust
// ❌ VULNERABLE: amount derived from stale chunk record instead of usable balance
pub fn relock_unlocking(origin: OriginFor<T>) -> DispatchResult {
    let who = ensure_signed(origin)?;
    let ledger = AccountLedger::<T>::get(&who);
    for chunk in ledger.unlocked_chunks {          // stale records
        let amount = chunk.amount;                  // never re-verified against free_balance
        Self::stake_locked(&who, amount)?;          // mints staking power from possibly-spent funds
    }
    Ok(())
}
```

**Example 3: Unlock releases balance but keeps chunk records** [Approx Vulnerability : HIGH]
```rust
// ❌ VULNERABLE: unlock credits spendable balance while the pending record survives
pub fn unlock(origin: OriginFor<T>, amount: BalanceOf<T>) -> DispatchResult {
    let who = ensure_signed(origin)?;
    UnlockedChunks::<T>::append(&who, Chunk { amount, era: current_era() });
    T::Currency::remove_lock(STAKING_ID, &who);     // balance now freely transferable
    Ok(())  // chunk record intentionally kept for relock — desynchronized state
}
```

### Impact Analysis

#### Technical Impact

- Staking rewards are minted against non-existent balance (inflation theft).
- Total staked counter diverges from real locked collateral; era reward distribution corrupted.
- Cascades into loyal-staker bonus abuse and inaccurate dApp reward shares.

#### Business Impact

- Direct treasury/reward-pool drain scaled by attacker capital and churn rate; severity rated Critical by SRLabs.

#### Affected Scenarios

- Any parachain staking pallet where "unlock" and "relock" are separate extrinsics and unlock credits transferable free balance.

### Secure Implementation

**Fix 1: Verify usable balance at relock time (applied mitigation)**
```rust
// ✅ SECURE: cap relock by the account's actually locked/usable balance
pub fn relock_unlocking(origin: OriginFor<T>) -> DispatchResult {
    let who = ensure_signed(origin)?;
    let ledger = AccountLedger::<T>::get(&who);
    let usable = T::Currency::usable_balance(&who);          // ground truth at execution time
    let to_relock: BalanceOf<T> = ledger.unlocked_chunks.iter()
        .map(|c| c.amount).sum::<BalanceOf<T>>().min(usable); // never exceed real balance
    ensure!(!to_relock.is_zero(), Error::<T>::NothingToRelock);
    Self::do_stake(&who, to_relock)                          // then clear consumed chunk records
}
```

**Fix 2: Keep funds locked until claim (atomic release)**
```rust
// ✅ SECURE: unlocked funds stay under a named lock until explicitly withdrawn
pub fn unlock(origin: OriginFor<T>, amount: BalanceOf<T>) -> DispatchResult {
    let who = ensure_signed(origin)?;
    T::Currency::set_lock(UNLOCKING_ID, &who, amount, WithdrawReasons::all()); // not transferable
    PendingUnlocks::<T>::append(&who, amount);
    Ok(())
}
// relock can then safely trust the records: funds never left the lock registry
```

### Detection Patterns

#### High-Signal Grep Seeds
```
- relock_unlocking
- unlocked_chunks
- AccountLedger
- transfer_all
- assert_unlock
```

#### Code Patterns to Look For
```
- Pattern 1: extrinsic that converts pending-unlock records into locked/staked balance without reading free_balance/usable_balance
- Pattern 2: unlock path that calls remove_lock or credits spendable balance while persisting the chunk record
- Pattern 3: staking reward payout that uses ledger records rather than the pallet's Currency lock as collateral proof
```

#### Audit Checklist
- [ ] After unlock + full transfer_out, does relock of the same amount fail?
- [ ] Is relock amount min(recorded_chunks, usable_balance)?
- [ ] Do era rewards reference locks or ledger copies? (locks = truth)

### Keywords for Search

`relock_unlocking`, `unlocked_chunks`, `dapp staking`, `staking ledger desync`, `double spend staking`, `phantom stake`, `unlock transfer relock`, `AccountLedger`, `staking rewards inflation`, `free_balance transfer_all`, `lock registry`, `era rewards`, `substrate staking pallet`, `chunk records stale`

### Related Vulnerabilities

- DB/substrate/pallets/origin-authorization-bypass.md (same report family, access-control class)
