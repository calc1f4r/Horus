---
# Core Classification
protocol: composable
chain: polkadot
category: access_control
vulnerability_type: schedule_validation_bypass
root_cause_family: missing_temporal_validation

# Pattern Identity
pattern_key: unvalidated-time-window | vesting schedule | start/end in the past accepted | vesting terms bypassed

# Interaction Scope
interaction_scope: single_contract
involved_contracts:
  - frame vesting pallet (frame/vesting/src/lib.rs)
path_keys:
  - unvalidated-time-window | vested_transfer | schedule starting in the past | immediate/retroactive vesting
  - unvalidated-time-window | vested_transfer | schedule ending in the past | zero-cliff degenerate schedule
  - unvalidated-time-window | root-origin/sudo config | informational privileged paths | weak governance surface

# Attack Vector Details
attack_type: input_validation_bypass
affected_component: vesting schedule validation (vested_transfer)

# Technical Primitives
primitives:
  - vested_transfer
  - vesting_schedule
  - starting_block
  - ending_block
  - block_number_validation
  - ensure_root
  - sudo_pallet

# Grep / Hunt-Card Seeds
code_keywords:
  - vested_transfer
  - VestingInfo
  - starting_block
  - ending_block
  - vest
  - ensure_root
  - merge_vesting_info

severity: low
impact: policy_bypass
language: rust
tags:
  - substrate
  - pallet
  - vesting
  - access_control
  - temporal_validation
  - frame
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [ves1] | reports/substrate-l1_findings/composable-halborn-vesting.md | LOW | Halborn | HAL-01 `vested_transfer` accepts schedules starting/ending in the past (RISK ACCEPTED, `frame/vesting/src/lib.rs:332-346,412-448`) |
| [ves3] | reports/substrate-l1_findings/composable-halborn-vesting.md | INFO | Halborn | HAL-03 root-origin informational findings on vesting config |
| [ves4] | reports/substrate-l1_findings/composable-halborn-vesting.md | INFO | Halborn | HAL-04 sudo-pallet presence informational findings |
| [q5] | reports/substrate-l1_findings/composable-audits-halborn-audit20220823-pallet-vesting-pdf.md | LOW | Halborn | POSSIBILITY OF CREATING A VESTING SCHEDULE IN THE PAST |

## Vesting Schedules With Past Start/End Blocks Bypass Intended Lock Terms

**FRAME's vesting pallet accepts `vested_transfer` schedules whose start and end blocks lie in the past, so schedules that should gate tokens over a future window instead release them immediately or degenerate to zero vesting** - representative of pallets that validate schedule structure but not schedule temporality against the current block.

### Overview

Halborn's 2022 audit of Composable's vesting pallet usage found HAL-01 (Low, RISK ACCEPTED): `vested_transfer` (`frame/vesting/src/lib.rs:332-346,412-448`) does not check that `starting_block`/`ending_block` are in the future (or sane relative to `now`), allowing retroactive or already-expired schedules. HAL-03/HAL-04 are informational notes on root-origin and sudo-pallet surfaces.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because the vesting schedule validation checks structure (end > start, locked balance sufficiency) but never compares `starting_block`/`ending_block` against the current block number, so past-window schedules are accepted."
- Pattern key: `unvalidated-time-window | vesting schedule | start/end in the past accepted | vesting terms bypassed`
- Interaction scope: `single_contract`
- Primary affected component(s): `vested_transfer schedule validation, vest() unlocking computation`
- Contracts / modules involved: `frame vesting pallet (frame/vesting/src/lib.rs)`
- Path keys: `schedule starting in the past`, `schedule ending in the past`, `root/sudo config surfaces`
- High-signal code keywords: `vested_transfer, VestingInfo, starting_block, ending_block, vest, ensure_root`
- Typical sink / impact: `immediate token unlock / zero-cliff degenerate vesting / policy bypass`
- Validation strength: `moderate` (single auditor; issue RISK ACCEPTED by Composable — low practical impact)

#### Contract / Boundary Map

- Entry surface(s): `vested_transfer()`, `vest()`, vesting config extrinsics (root)
- Contract hop(s): `vested_transfer -> VestingInfo construction -> vest() lock computation`
- Trust boundary crossed: `sender-intent boundary — schedule fields supplied by the transfer sender are trusted for temporal sanity`
- Shared state or sync assumption: `vest() derives unlocked amounts from (now, starting_block, ending_block); the tuple must represent a future window at creation`

#### Valid Bug Signals

- Signal 1: `vested_transfer` constructs `VestingInfo::new(starting_block, ending_block, ...)` with no `ensure!(starting_block >= frame_system::block_number())` style check (`lib.rs:332-346,412-448`).
- Signal 2: A schedule whose `ending_block` already passed still locks tokens (they are immediately 100% unlocked via `vest()`), defeating the lock's purpose.
- Signal 3: Privileged vesting configuration reachable through root/sudo without additional governance scrutiny (HAL-03/04 context).

#### False Positive Guards

- Not this bug when: the pallet (or a wrapper) enforces `starting_block >= now` and `ending_block > starting_block + min_duration` at schedule creation.
- Safe if: past-dated schedules are an accepted product decision (as Composable RISK ACCEPTED) and no downstream logic (airdrops, investor locks, legal terms) depends on future windows.
- Requires attacker control of: the schedule fields in `vested_transfer` — i.e., any account sending a vested transfer (typically the treasury/issuer, so impact is often self-inflicted or a tooling bug).

### Vulnerability Description

#### Root Cause

`vested_transfer` validates the schedule's arithmetic (per-block amounts, locked ≤ balance) but accepts any block numbers, including windows entirely in the past. When `ending_block <= now`, `vest()` immediately unlocks everything; when `starting_block` is far in the past, the cliff is retroactively satisfied. The result: the vesting lock's intended temporal policy is bypassed ([ves1], `lib.rs:332-346,412-448`).

#### Attack Scenario / Path Variants

**Path A: Retroactive schedule = instant unlock**
Path key: `unvalidated-time-window | vested_transfer | schedule ending in the past | immediate full unlock`
Entry surface: `vested_transfer()`
Contracts touched: `vesting pallet storage -> vest()`
1. Sender (or a buggy payroll/airdrop tool) submits `vested_transfer` with `ending_block` already behind `now`.
2. The pallet accepts and locks the tokens, recording the past-dated schedule.
3. Recipient calls `vest()` — everything is unlocked immediately; the intended lock period never happened.

**Path B: Backdated start skips the cliff**
Path key: `unvalidated-time-window | vested_transfer | schedule starting in the past | retroactive cliff satisfaction`
1. Schedule sets `starting_block` well in the past with a long cliff.
2. Cliff elapsed time is credited retroactively from creation.
3. Recipient unlocks earlier than the intended product terms allow.

**Path C: Privileged config surface (informational)**
Path key: `unvalidated-time-window | root-origin/sudo config | informational privileged paths | weak governance surface`
1. Vesting-related configuration extrinsics run under root/sudo (HAL-03/04).
2. Any compromise or misuse of root/sudo directly rewrites vesting state without further gates.

#### Vulnerable Pattern Examples

**Example 1: vested_transfer without temporal validation (from [ves1])** [Approx Vulnerability : LOW]
```rust
// ❌ VULNERABLE: frame/vesting/src/lib.rs:332-346, 412-448
pub fn vested_transfer(
    origin: OriginFor<T>,
    target: T::AccountId,
    schedule: VestingInfo<T::BlockNumber, BalanceOf<T>>,
) -> DispatchResult {
    let who = ensure_signed(origin)?;
    // validates locked <= balance, schedule arithmetic ... but NEVER:
    // ensure!(schedule.starting_block() >= frame_system::Pallet::<T>::block_number());
    // ensure!(schedule.ending_block() > frame_system::Pallet::<T>::block_number());
    Self::apply_vesting_schedule(&who, &target, schedule)?; // past-dated schedule accepted
    Ok(())
}
```

**Example 2: vest() releases everything for expired windows** [Approx Vulnerability : LOW]
```rust
// ❌ VULNERABLE (as consumed): degenerate schedule unlocks fully on first vest()
pub fn vest(origin: OriginFor<T>) -> DispatchResult {
    let now = frame_system::Pallet::<T>::block_number();
    let vested = VestingInfo::<T>::unlocking_balance(now); // ending_block <= now → full amount
    // recipient of a past-dated schedule gets 100% immediately
}
```

**Example 3: Wrapper trusting caller-supplied block numbers** [Approx Vulnerability : LOW]
```rust
// ❌ VULNERABLE: payroll/airdrop wrapper forwards user-supplied windows unchecked
pub fn batch_vested_transfer(origin: OriginFor<T>, items: Vec<(AccountId, VestingInfo)>) -> DispatchResult {
    for (target, schedule) in items {
        Self::vested_transfer(origin.clone(), target, schedule)?; // no now-check anywhere in the stack
    }
    Ok(())
}
```

### Impact Analysis

#### Technical Impact

- Vesting locks created with past windows provide zero temporal protection — tokens are immediately unlocked.
- Backdated starts credit elapsed cliff time, shortening locks below intended terms.
- Root/sudo config surfaces (HAL-03/04) concentrate vesting mutation power.

#### Business Impact

- Low severity, RISK ACCEPTED by Composable: primary risk is tooling/error-induced bypass of investor/team lock terms rather than adversarial theft. If vesting schedules back legal agreements (investor locks), a bypass can have contractual consequences.

#### Affected Scenarios

- Parachains using FRAME's vesting pallet with caller-supplied schedule fields.
- Airdrop/payroll tooling that computes block numbers incorrectly (off-by-eras bugs producing past windows).
- Any consumer that treats the existence of a vesting lock as proof of future-dated obligations.

### Secure Implementation

**Fix 1: Validate the temporal window at schedule creation**
```rust
// ✅ SECURE: reject past-dated and degenerate schedules
pub fn vested_transfer(
    origin: OriginFor<T>,
    target: T::AccountId,
    schedule: VestingInfo<T::BlockNumber, BalanceOf<T>>,
) -> DispatchResult {
    let who = ensure_signed(origin)?;
    let now = frame_system::Pallet::<T>::block_number();
    ensure!(schedule.starting_block() >= now, Error::<T>::StartingBlockInPast);
    ensure!(schedule.ending_block() > schedule.starting_block(), Error::<T>::EmptyWindow);
    ensure!((schedule.ending_block() - schedule.starting_block()) >= T::MinVestingDuration::get(), Error::<T>::WindowTooShort);
    Self::apply_vesting_schedule(&who, &target, schedule)
}
```

**Fix 2: Clamp derived schedules server-side (wrapper responsibility)**
```rust
// ✅ SECURE: wrapper computes windows from now, never from caller input
let now = frame_system::Pallet::<T>::block_number();
let schedule = VestingInfo::new(
    now + T::DefaultCliff::get(),        // cliff strictly future
    now + T::DefaultDuration::get(),     // end strictly future
    total,
);
```

### Detection Patterns

#### High-Signal Grep Seeds
```
- vested_transfer
- VestingInfo
- starting_block
- ending_block
- unlock_lockable_currency
- ensure_root
```

#### Code Patterns to Look For
```
- Pattern 1: VestingInfo::new(...) where either block argument is caller-controlled and never compared to block_number()
- Pattern 2: batch vesting tooling passing through raw schedule structs
- Pattern 3: wrappers deriving schedules from stale off-chain computed block heights
```

#### Audit Checklist
- [ ] Does schedule creation compare start/end against the current block?
- [ ] What happens on vest() the same block a past-dated schedule is created?
- [ ] Can any non-root path modify or merge existing schedules (merge_vesting_info) to shift windows?

### Keywords for Search

`vesting`, `vested_transfer`, `VestingInfo`, `starting_block`, `ending_block`, `past schedule`, `temporal validation`, `block number validation`, `token lock bypass`, `cliff retroactive`, `FRAME vesting pallet`, `Composable`, `Halborn`, `schedule validation`, `vesting bypass`, `lock period bypass`

### Related Vulnerabilities

- DB/substrate/pallets/governance-origin-confusion.md (root/sudo privileged surfaces)
- DB/substrate/pallets/staking-unlock-relock-double-spend.md (unlock-path abuse family)
