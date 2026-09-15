---
# Core Classification
protocol: generic
chain: polkadot
category: lifecycle
vulnerability_type: upgrade_migration_failure
root_cause_family: unsynchronized_state_migration

# Pattern Identity
pattern_key: untested-storage-migration | runtime upgrade | storage layout / function indices / immutable vars change | stuck funds or wrong-function execution

# Interaction Scope
interaction_scope: multi_contract
involved_contracts:
  - Gateway (upgradable bridge contract)
  - inbound-queue
  - parachain runtime (wasm)
path_keys:
  - untested-storage-migration | Gateway upgrade | storage layout change without migration | token loss / channel immobilization
  - untested-storage-migration | inbound-queue Gateway address | stale hardcoded address after upgrade | stuck bridge
  - untested-storage-migration | function index shift | call indices move across upgrade | wrong function executed
  - untested-storage-migration | immutable vars overwrite | upgrade resets config state | invariant loss

# Attack Vector Details
attack_type: state_corruption
affected_component: runtime upgrade path (on_initialize / on_runtime_upgrade, storage migrations, call indices)

# Technical Primitives
primitives:
  - on_runtime_upgrade
  - storage_migration
  - VersionedMigration
  - function_call_index
  - call_filter
  - inbound_queue
  - gateway_address
  - pallet_macro_defaults
  - try-runtime

# Grep / Hunt-Card Seeds
code_keywords:
  - on_runtime_upgrade
  - migrate
  - StorageVersion
  - on_initialize
  - inbound_queue
  - Gateway
  - call_index
  - try_runtime

severity: high
impact: fund_loss
language: rust
tags:
  - substrate
  - lifecycle
  - runtime_upgrade
  - storage_migration
  - snowbridge
  - parachain
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [sb12] | reports/substrate-l1_findings/snowbridge-oak-v1-1.md | MAJOR | Oak Security | #12 token loss / channel immobilization after Gateway upgrade |
| [sb14] | reports/substrate-l1_findings/snowbridge-oak-v1-1.md | MAJOR | Oak Security | #14 Gateway address update in inbound-queue → stuck bridge |
| [sb22] | reports/substrate-l1_findings/snowbridge-oak-v1-1.md | MAJOR | Oak Security | #22 function index shift during parachain upgrades executes wrong functions |
| [sb23] | reports/substrate-l1_findings/snowbridge-oak-v1-1.md | MAJOR | Oak Security | #23 upgrade overwrites immutable vars |
| [oz12] | reports/substrate-l1_findings/polkadot-runtime-templates-oz-2024-12.md | INFO/LOW | SRLabs | pallet-macro abstraction defaults (migration hazards in templated runtimes) |
| [pen1] | reports/substrate-l1_findings/pendulum-docs-pen-migration-review-handover-md.md | INFO | Pendulum docs | Pen migration review handover (migration process reference) |
| [pen2] | reports/substrate-l1_findings/pendulum-docs-pen-migration-internal-review-md.md | INFO | Pendulum docs | Pen migration internal review (migration process reference) |
| [x24] | reports/substrate-l1_findings/hydradx-c4-2401.md | MEDIUM | Code4rena | [M-08] Storage can be bloated with low value liquidity positions |
| [x25] | reports/substrate-l1_findings/phala-c4-2401.md | MEDIUM | Code4rena | [M-02] An attacker can bloat the Pink runtime storage with zero costs |
| [x26] | reports/substrate-l1_findings/publicauditreports-nm0286-final-nodle-pdf.md | HIGH | auditor | NM-0286 Nodle - SECURITY REVIEW 6 Issues 6.1 [High] User grants migration can be blocked by exploiting the MAX_SCHEDULES limit File(s): Gran |
| [x30] | reports/substrate-l1_findings/manta-veridise-chain.md | MEDIUM | Veridise | Inc. 10 4 Vulnerability Report 4.1 Detailed Description of Issues 4.1.1 V-MANC-VUL-001: Static fee charged despite dynamic storage accesses |
| [x31] | reports/substrate-l1_findings/acala-c4-2401.md | MEDIUM | Code4rena | Storage can be bloated with low liquidity positions • Low Risk and Non-Critical Issues • 01 Admin is a single point of failure • 02 Consider adding be |
| [x32] | reports/substrate-l1_findings/acala-c4-2401.md | MEDIUM | Code4rena | Storage can be bloated with low liquidity positions Acala https://code4rena.com/reports/2024-03-acala 22 of 52 09/06/2024, 14:14 Submitted by ZanyBonz |
| [x33] | reports/substrate-l1_findings/phala-blockchain-audit-code4rena-phat-contract-runtime-pdf.md | MEDIUM | auditor | An attacker can bloat the Pink runtime storage with zero costs |
| [x36] | reports/substrate-l1_findings/audit-reports-snowbridge-2025-05-29-audit-report-snowbridge-v2-v1-0-pdf.md | HIGH | Oak Security | State collision after upgrade of the Gateway contract |
| [x37] | reports/substrate-l1_findings/moonbeam-srl-2401.md | MEDIUM | SRLabs | Location runtime/* Attack impact Underweighted extrinsic calls may result block rejection upon relay-chain validation |
| [x39] | reports/substrate-l1_findings/acala-slowmist-2021.md | MEDIUM | SlowMist | URL: https://rustsec.org/advisories/RUSTSEC-2021-0115 Solution: Upgrade to >=1.2.0 Dependency tree: zeroize_derive 1.1.0 5.2 Risk of calculation error |
| [q40] | reports/substrate-l1_findings/audit-reports-snowbridge-2025-05-06-audit-report-snowbridge-updates-4-v1-0-pdf.md | LOW | Oak Security | Incomplete reward funds migration in Gateway upgrade |

## Untested Runtime Upgrades Shift Layout/Indices and Strand Bridge Funds

**Runtime and Gateway upgrades that change storage layouts, hardcoded addresses, call indices, or "immutable" variables without complete migrations cause token loss, channel immobilization, stuck bridges, and dispatch of wrong functions** - representative of parachain lifecycle defects where the upgrade path itself is the attack surface.

### Overview

Oak Security's Snowbridge audits found four Major lifecycle issues: #12 Gateway upgrades can lose tokens / immobilize channels when storage migrations are incomplete; #14 the inbound-queue's Gateway address update strands the bridge; #22 function-index shifts across parachain upgrades execute the wrong functions; #23 upgrades overwrite supposedly immutable variables. SRLabs' 2024-12 template review flagged pallet-macro abstraction defaults that make migrations hazardous in templated runtimes. Pendulum's Pen migration reviews document real migration-review process.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because upgrades mutate storage layout, external addresses, call indices, or config state without a complete, tested migration, so post-upgrade code reads moved/stale slots and dispatches shifted indices."
- Pattern key: `untested-storage-migration | runtime upgrade | storage layout / function indices / immutable vars change | stuck funds or wrong-function execution`
- Interaction scope: `multi_contract`
- Primary affected component(s): `on_runtime_upgrade hooks, storage migrations, inbound-queue address wiring, call index tables`
- Contracts / modules involved: `Gateway, inbound-queue, parachain runtime`
- Path keys: `Gateway storage layout change`, `inbound-queue stale address`, `function index shift`, `immutable var overwrite`
- High-signal code keywords: `on_runtime_upgrade, migrate, StorageVersion, inbound_queue, call_index, try_runtime`
- Typical sink / impact: `bridged token loss / channel freeze / wrong extrinsic execution / config reset`
- Validation strength: `strong` (auditor-confirmed Majors with concrete failure modes)

#### Contract / Boundary Map

- Entry surface(s): `set_code` / runtime upgrade extrinsic, Gateway contract upgrade path, inbound-queue config update
- Contract hop(s): `upgrade -> on_runtime_upgrade migrations -> storage reads (new layout) -> dispatch (new indices)`
- Trust boundary crossed: `code-version ↔ storage-version boundary; external contract address wiring (inbound-queue ↔ Gateway)`
- Shared state or sync assumption: `storage layout must match code expectations after upgrade; queue's Gateway pointer must match the live Gateway; call indices must remain stable or messages must be versioned`

#### Valid Bug Signals

- Signal 1: An upgrade changes pallet storage items or Gateway contract storage layout without a `StorageVersion`-gated migration ([sb12]).
- Signal 2: The inbound-queue holds a Gateway address that the upgrade flow can change (or forget to change), desynchronizing the pair ([sb14]).
- Signal 3: Extrinsic call indices (pallet index / call index) shift between runtime versions while stored or in-flight messages reference the old encoding ([sb22]).
- Signal 4: Values documented as immutable/set-once are recomputed or overwritten during upgrade initialization ([sb23]).

#### False Positive Guards

- Not this bug when: every migration is `VersionedMigration`-gated, exercised with `try-runtime` on a fork of real state, and call-index changes ship with a deprecation/translation period.
- Safe if: the Gateway address is fixed at genesis and the queue's pointer is proven equal in an integration test each release.
- Requires attacker control of: usually none — these are operator/lifecycle-triggered; "attack" = scheduling an upgrade (governance/ sudo). External attackers exploit the window only insofar as in-flight messages hit shifted indices.

### Vulnerability Description

#### Root Cause

Upgrades are code replacements over live state. Snowbridge's upgrade flow had four gaps: Gateway storage migrations were incomplete (tokens/channel state stranded, [sb12]); the inbound-queue's Gateway address update desynchronized the message path ([sb14]); call indices shifted across parachain runtime versions so pre-upgrade-encoded calls dispatched to the wrong functions post-upgrade ([sb22]); and upgrade hooks rewrote variables assumed immutable ([sb23]). Templated runtimes inherit pallet-macro defaults that quietly omit migration scaffolding ([oz12]).

#### Attack Scenario / Path Variants

**Path A: Gateway upgrade strands tokens/channels**
Path key: `untested-storage-migration | Gateway upgrade | storage layout change without migration | token loss / channel immobilization`
Entry surface: Gateway contract upgrade
Contracts touched: `Gateway storage -> channel accounting`
1. Operator upgrades the Gateway with a new storage layout.
2. Migration does not cover all channel/token mappings ([sb12]).
3. Tokens mapped under old slots become unreachable; channels freeze.

**Path B: Inbound-queue points at the wrong Gateway**
Path key: `untested-storage-migration | inbound-queue Gateway address | stale hardcoded address after upgrade | stuck bridge`
1. Gateway upgrade includes an address change; the inbound-queue's stored pointer is updated (or missed) as part of the flow ([sb14]).
2. Queue and Gateway disagree on the address binding.
3. Inbound messages fail to reach the new Gateway — the bridge sticks.

**Path C: Function-index shift executes wrong code**
Path key: `untested-storage-migration | function index shift | call indices move across upgrade | wrong function executed`
1. A runtime upgrade inserts/removes extrinsics, shifting (pallet_index, call_index) pairs ([sb22]).
2. In-flight or stored messages encoded against the old table dispatch to different functions after the upgrade.
3. Unintended state changes execute — potentially privileged operations reached via shifted indices.

**Path D: Immutable variables overwritten**
Path key: `untested-storage-migration | immutable vars overwrite | upgrade resets config state | invariant loss`
1. Upgrade's `on_initialize`/genesis-like reset recomputes "set-once" config ([sb23]).
2. Custom settings revert to defaults.
3. Invariants (fee configs, role bindings) silently vanish.

#### Vulnerable Pattern Examples

**Example 1: Migrationless layout change (from [sb12])** [Approx Vulnerability : HIGH]
```rust
// ❌ VULNERABLE: storage item renamed/moved with no versioned migration
// v1: #[pallet::storage] pub type Channels<T> = StorageMap<_, Blake2_128Concat, ChannelId, Channel>;
// v2: renamed/retyped, old prefix not migrated
#[pallet::storage]
pub type ChannelStates<T> = StorageMap<_, Blake2_128Concat, ChannelId, ChannelState>;
// upgrade ships; old Channels data orphaned under the old prefix → token loss / frozen channels
```

**Example 2: Queue's Gateway pointer drift (from [sb14])** [Approx Vulnerability : HIGH]
```rust
// ❌ VULNERABLE: address update not atomic across the pair
pub fn on_runtime_upgrade() -> Weight {
    // Gateway upgraded to new implementation address...
    // ...but InboundQueue::<T>::gateway() still returns the OLD address
    // inbound messages route to the dead contract → bridge stuck
}
```

**Example 3: Call index shift (from [sb22])** [Approx Vulnerability : HIGH]
```rust
// ❌ VULNERABLE: extrinsic inserted above existing calls
// v1 call order: [transfer, register_token, halt]
// v2 call order: [transfer, register_token, set_fees, halt]   // halt shifted 2 -> 3
// an in-flight XCM encoded as call index 2 now executes set_fees instead of halt
```

**Example 4: Immutable var reset (from [sb23])** [Approx Vulnerability : MEDIUM]
```rust
// ❌ VULNERABLE: upgrade hook rewrites set-once config
pub fn on_runtime_upgrade() -> Weight {
    // Config::<T>::set(GenesisConfig::default_config()); // "immutable" params reset
    // customized fee/role settings silently lost
}
```

### Impact Analysis

#### Technical Impact

- Bridged token loss and channel immobilization ([sb12]); full bridge liveness failure via address desync ([sb14]).
- Wrong-function execution from shifted indices — a correctness and security hazard, potentially reaching privileged calls ([sb22]).
- Silent config/invariant loss ([sb23]).

#### Business Impact

- Major-rated: upgrades are routine operations on parachains; a defective upgrade path means any scheduled upgrade can strand user funds or brick the bridge. Recovery typically requires a second, carefully-crafted upgrade — days of downtime.

#### Affected Scenarios

- Any parachain that renames/moves pallet storage without `VersionedMigration` + `try-runtime` checks.
- Bridges where external contract addresses are wired into runtime storage.
- Runtimes that insert/remove extrinsics without call-index stability review.
- Templated runtimes relying on pallet-macro defaults rather than explicit migration scaffolding ([oz12]).

### Secure Implementation

**Fix 1: Versioned migrations with try-runtime validation**
```rust
// ✅ SECURE: gate migrations on storage version; prove them against real state
pub type MigrateV3ToV4<T> = VersionedMigration<
    3, 4,
    v4::migrate::LazyMigration<V3, T, Registry<T>>,
    Pallet<T>,
    DefaultVersion,
>;
// pre-release: try-runtime check-state on a fork of production storage;
// migration completeness test asserts no orphaned keys under the old prefix
```

**Fix 2: Address-binding and call-index integrity checks**
```rust
// ✅ SECURE: prove queue<->Gateway binding and index stability per release
#[test]
fn upgrade_preserves_gateway_binding_and_indices() {
    // 1. after upgrade, InboundQueue::gateway() == live Gateway address (integration test)
    // 2. deprecated call indices dispatch to a translate-call error, not a shifted function
    // 3. immutable config snapshot before == after upgrade
}
```

### Detection Patterns

#### High-Signal Grep Seeds
```
- on_runtime_upgrade
- migrate
- StorageVersion
- VersionedMigration
- inbound_queue
- call_index
- try_runtime
```

#### Code Patterns to Look For
```
- Pattern 1: storage item renames/type changes with no corresponding migrate() or VersionedMigration
- Pattern 2: external contract addresses stored in runtime/queue storage without upgrade-time equality tests
- Pattern 3: extrinsic insertions/deletions in #[pallet::call] blocks between releases (diff call order)
- Pattern 4: on_runtime_upgrade/on_initialize bodies that write config values documented as immutable
- Pattern 5: runtimes assembled from templates with default migration scaffolding commented out
```

#### Audit Checklist
- [ ] Diff storage layouts (names, types, prefixes) between runtime versions — is every delta migrated?
- [ ] Was try-runtime executed against a snapshot of production state for this upgrade?
- [ ] Do any stored/in-flight messages embed call indices that shifted?
- [ ] Which "set-once" values can the upgrade path write?
- [ ] Are external addresses (Gateway) referenced by queues re-validated post-upgrade?

### Keywords for Search

`runtime upgrade`, `storage migration`, `on_runtime_upgrade`, `StorageVersion`, `VersionedMigration`, `try-runtime`, `call index shift`, `extrinsic index`, `inbound queue`, `Gateway address`, `Snowbridge`, `token loss`, `channel immobilization`, `stuck bridge`, `immutable variable overwrite`, `pallet macro defaults`, `parachain upgrade`, `set_code`

### Related Vulnerabilities

- DB/substrate/bridges/snowbridge-bridge-accounting.md (Snowbridge custody failures)
- DB/substrate/pallets/governance-origin-confusion.md (who controls the upgrade)
- DB/substrate/lifecycle/ (sibling lifecycle entries)
