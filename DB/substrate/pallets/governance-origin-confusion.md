---
# Core Classification
protocol: generic
chain: polkadot
category: access_control
vulnerability_type: origin_confusion
root_cause_family: misconfigured_privilege_boundary

# Pattern Identity
pattern_key: weak-or-missing-origin | pallet governance/admin extrinsics | governance commands absent, delayed, or template-default | unauthorized or failed privileged ops

# Interaction Scope
interaction_scope: multi_contract
involved_contracts:
  - Snowbridge Gateway (Ethereum side)
  - Polkadot-side runtime/pallet governance surfaces
  - pallet_democracy / OpenGov config
  - runtime templates
path_keys:
  - weak-or-missing-origin | administrative commands | not implemented on Polkadot side | privileged ops unavailable
  - weak-or-missing-origin | governance throttling | delayed governance operations | slow emergency response
  - weak-or-missing-origin | pallet centralized control | single origin controls all functions | privileged concentration
  - weak-or-missing-origin | template WeightInfo | substrate-node-template defaults shipped | mispriced weights
  - weak-or-missing-origin | XCM fee config | waived XCM fees / undocumented OpenGov config | unpriced messaging

# Attack Vector Details
attack_type: configuration_error
affected_component: governance and administrative origin configuration

# Technical Primitives
primitives:
  - ensure_origin
  - Root
  - AddTokenOrigin
  - pallet_democracy
  - OpenGov
  - WeightInfo
  - substrate-node-template
  - XCM delivery fees
  - MaxRemoteLockConsumers
  - governance throttling

# Grep / Hunt-Card Seeds
code_keywords:
  - ensure_root
  - ensure_origin
  - WeightInfo
  - substrate_node_template
  - MaxRemoteLockConsumers
  - OpenGov
  - pallet_democracy
  - transferNativeFromAgent

severity: medium
impact: unauthorized_access
language: rust
tags:
  - substrate
  - pallet
  - governance
  - access_control
  - origin
  - configuration
  - opengov
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [sb4] | reports/substrate-l1_findings/snowbridge-oak-v1-1.md | MAJOR | Oak Security | #4 administrative commands not implemented on Polkadot side |
| [sb5] | reports/substrate-l1_findings/snowbridge-oak-v1-1.md | MAJOR | Oak Security | #5 throttling delays governance operations |
| [sb24] | reports/substrate-l1_findings/snowbridge-oak-v1-1.md | MAJOR | Oak Security | #24 pallet centralized control |
| [aca1] | reports/substrate-l1_findings/acala-srl-2023.md | LOW | SRLabs | pallet_democracy WeightInfo from substrate-node-template |
| [oz7a] | reports/substrate-l1_findings/polkadot-runtime-templates-oz-2024-07.md | HIGH | SRLabs | 4.1 stringent filtering for proxy calls (governance config) |
| [oz7b] | reports/substrate-l1_findings/polkadot-runtime-templates-oz-2024-07.md | INFO | SRLabs | 4.2.2 OpenGov configuration undocumented / MaxRemoteLockConsumers / waived XCM fees findings |
| [oz4x] | reports/substrate-l1_findings/polkadot-runtime-templates-oz-2024-04.md | HIGH | SRLabs | runtime template waives XCM message delivery fee (config-level origin/fee confusion) |
| [x25] | reports/substrate-l1_findings/audit-reports-snowbridge-2025-01-07-audit-report-snowbridge-updates-3-v1-0-pdf.md | HIGH | auditor | Unauthorized minting of PNA assets due to missing origin validation |
| [x26] | reports/substrate-l1_findings/audit-reports-snowbridge-2024-05-24-audit-report-snowbridge-v1-1-pdf.md | HIGH | auditor | Throttling mechanism could delay critical governance operations |
| [q27] | reports/substrate-l1_findings/composable-halborn-byog.md | LOW | Halborn | (HAL-01) CONFIGURATION ORIGIN CAN BE USED TO SET A PAYMENT ASSET FOR AN ARBITRARILY CHOSEN USER |
| [q28] | reports/substrate-l1_findings/avail-halborn.md | INFO | Halborn | HAL-03 UNIMPLEMENTED CUSTOM ORIGIN |
| [q29] | reports/substrate-l1_findings/composable-audits-halborn-audit20220823-pallet-vesting-pdf.md | INFO | Halborn | USAGE OF ROOT ORIGIN |
| [q30] | reports/substrate-l1_findings/composable-audits-halborn-audit20220823-pallet-vesting-pdf.md | INFO | Halborn | USAGE OF SUDO PALLET |
| [q31] | reports/substrate-l1_findings/composable-audits-halborn-audit20220926-pallet-byog-pdf.md | LOW | Halborn | CONFIGURATION ORIGIN CAN BE USED TO SET A PAYMENT ASSET FOR AN ARBITRARILY CHOSEN USER |
| [q32] | reports/substrate-l1_findings/publicreports-substrate-audits-polygon-avail-substrate-pallet-security-audit-report-halborn-final-pdf.md | INFO | Halborn | HAL-03 UNIMPLEMENTED CUSTOM ORIGIN |

## Governance/Admin Origins Missing, Throttled, or Left at Template Defaults

**Privileged pallet surfaces fail open when governance commands are not implemented on one side of a bridge, when throttling delays privileged response, when a single origin controls a whole pallet, or when runtime configs ship substrate-node-template defaults** - representative of Substrate runtimes where the governance/admin origin story was never finished or never customized from the template.

### Overview

Composite entry grounded in Snowbridge/Oak 2024 (#4 administrative commands not implemented on the Polkadot side, #5 throttling delays governance ops, #24 pallet centralized control — all Major), Acala/SRLabs 2023 (pallet_democracy WeightInfo copied from substrate-node-template, Low), and SRLabs' Polkadot runtime template reviews 2024-04/07 (waived XCM fees, MaxRemoteLockConsumers, undocumented OpenGov config §4.2.2, proxy-call filtering §4.1).

#### Agent Quick View

- Root cause statement: "This vulnerability exists because the privileged origin plan is incomplete or uncustomized: governance commands are declared but not implemented, throttled, or routed to a single over-powerful origin, and runtime configs (weights, XCM fees, OpenGov params) ship template defaults instead of production values."
- Pattern key: `weak-or-missing-origin | pallet governance/admin extrinsics | governance commands absent, delayed, or template-default | unauthorized or failed privileged ops`
- Interaction scope: `multi_contract`
- Primary affected component(s): `pallet call filters and origins (ensure_root/ensure_origin), pallet_democracy weights, XCM fee config, OpenGov parameters`
- Contracts / modules involved: `Snowbridge Gateway + Polkadot-side runtime, pallet_democracy, runtime templates`
- Path keys: `administrative commands unimplemented`, `governance throttling`, `centralized pallet control`, `template WeightInfo`, `waived XCM fees`
- High-signal code keywords: `ensure_root, ensure_origin, WeightInfo, substrate_node_template, MaxRemoteLockConsumers, OpenGov`
- Typical sink / impact: `privileged operations unavailable / delayed emergency response / underpriced extrinsics / unpriced messaging`
- Validation strength: `moderate` (findings span multiple auditors and protocols; each individually confirmed)

#### Contract / Boundary Map

- Entry surface(s): governance-origin extrinsics (`ensure_root`-gated calls), `BaseFilter`/`call_filter`, democracy/OpenGov dispatch, bridge administrative commands
- Contract hop(s): `OpenGov/democracy referendum -> origin dispatch -> pallet extrinsic`, `bridge admin command -> Gateway -> Polkadot-side handler (possibly missing)`
- Trust boundary crossed: `governance ↔ runtime boundary; bridge ↔ parachain governance boundary`
- Shared state or sync assumption: `both sides of a bridge must implement the same admin command set; weights must match production hardware`

#### Valid Bug Signals

- Signal 1: A pallet exposes governance/admin commands whose dispatchable implementation is absent or `todo!()`/unreachable on one side of the system ([sb4]).
- Signal 2: All (or most) extrinsic entry points in a pallet resolve to the same origin (typically bare `ensure_root`), concentrating control ([sb24]).
- Signal 3: `WeightInfo` trait bound resolves to `substrate_node_template::weights` in a production runtime ([aca1]).
- Signal 4: XCM delivery fees configured to zero/waived, or OpenGov/`MaxRemoteLockConsumers` parameters left undocumented at template defaults ([oz7b], [oz4x]).

#### False Positive Guards

- Not this bug when: every governance command has a symmetric, tested implementation on both sides, and origins follow least-privilege (different roles for different sensitivity tiers).
- Safe if: throttling exists deliberately as rate-limiting with documented emergency bypass, and template weights are benchmarked before mainnet.
- Requires attacker control of: often nothing adversarial — these are fail-open configuration defects; the "attacker" may be time (delayed governance response during an incident).
- Distinguish from `origin-authorization-bypass.md`: that entry is a broken check letting unprivileged callers through; this entry is a missing/weak/unfinished privileged design — checks exist but the origin story itself is wrong.

### Vulnerability Description

#### Root Cause

Governance integration is frequently deferred: Snowbridge shipped with administrative commands that had no Polkadot-side implementation ([sb4]), throttling that delays governance operations ([sb5]), and pallets where a single origin controls every function ([sb24]). Acala's runtime carried pallet_democracy weights inherited from substrate-node-template ([aca1]). SRLabs' template reviews found waived XCM delivery fees, default `MaxRemoteLockConsumers`, and undocumented OpenGov configuration ([oz7b], [oz4x]) — all symptoms of shipping template defaults into production governance.

#### Attack Scenario / Path Variants

**Path A: Governance command has no receiver — privileged action impossible**
Path key: `weak-or-missing-origin | administrative commands | not implemented on Polkadot side | privileged ops unavailable`
Entry surface: governance referendum dispatching a bridge admin command
Contracts touched: `Gateway -> Polkadot-side runtime (missing handler)`
1. An incident requires freezing/adjusting the bridge; governance passes the command.
2. The Polkadot-side implementation does not exist ([sb4]).
3. The mitigation cannot execute; the runtime is stuck with its current parameters.

**Path B: Throttled governance delays emergency response**
Path key: `weak-or-missing-origin | governance throttling | delayed governance operations | slow emergency response`
1. Governance operations are rate-limited/throttled ([sb5]).
2. During an exploit, the required sequence of governance calls exceeds the throttle budget.
3. Response is delayed past the damage window.

**Path C: Single origin controls everything (centralization)**
Path key: `weak-or-missing-origin | pallet centralized control | single origin controls all functions | privileged concentration`
1. Every extrinsic in the pallet requires the same origin ([sb24]).
2. Compromise or misuse of that one origin compromises the entire pallet's functionality.
3. No separation of duties between routine ops and destructive ops.

**Path D: Template defaults in production (weights, fees, OpenGov)**
Path key: `weak-or-missing-origin | template WeightInfo / XCM fee config | substrate-node-template defaults shipped | mispriced weights / unpriced messaging`
1. Runtime ships `WeightInfo = substrate_node_template::weights::...` ([aca1]) or waives XCM fees ([oz4x], [oz7b]).
2. Extrinsics are mispriced (too cheap → DoS economics; too dear → griefing users) and cross-chain messages are free to spam.
3. OpenGov/`MaxRemoteLockConsumers` misconfiguration compounds operational risk.

#### Vulnerable Pattern Examples

**Example 1: Admin command declared but unimplemented (from [sb4])** [Approx Vulnerability : MEDIUM]
```rust
// ❌ VULNERABLE: governance can pass the command, but nothing executes on this side
#[pallet::call]
impl<T: Config> Pallet<T> {
    /// Set bridge operating mode — referenced in docs, missing in dispatch.
    // pub fn set_operating_mode(origin: OriginFor<T>, mode: Mode) -> DispatchResult { ... }
    // ^ absent on the Polkadot side: governance referendum dispatch fails or is a no-op
}
```

**Example 2: Every extrinsic behind the same root origin (from [sb24])** [Approx Vulnerability : MEDIUM]
```rust
// ❌ VULNERABLE: single origin concentration
pub fn set_fees(origin: OriginFor<T>, fees: FeeConfig) -> DispatchResult { ensure_root(origin)?; ... }
pub fn halt_bridge(origin: OriginFor<T>) -> DispatchResult { ensure_root(origin)?; ... }
pub fn rotate_agents(origin: OriginFor<T>, agents: Vec<AgentId>) -> DispatchResult { ensure_root(origin)?; ... }
// routine (set_fees) and catastrophic (halt_bridge, rotate_agents) share ONE origin —
// no separation of duties; compromise of root = total control
```

**Example 3: Template weights in production (from [aca1])** [Approx Vulnerability : LOW]
```rust
// ❌ VULNERABLE: production runtime with template benchmark weights
impl pallet_democracy::Config for Runtime {
    type WeightInfo = substrate_node_template::weights::pallet_democracy::WeightInfo<T>; // Acala finding
    // weights never re-benchmarked for this runtime/hardware → mispriced extrinsics
}
```

**Example 4: Waived XCM fees (from [oz4x], [oz7b])** [Approx Vulnerability : HIGH]
```rust
// ❌ VULNERABLE: free cross-chain messaging
parameter_types! {
    pub const BaseXcmWeight: Weight = Weight::from_parts(1_000_000_000, 1024);
    pub XcmFees: u128 = 0; // delivery fee waived — anyone spams the sibling relay for free
}
// plus undocumented OpenGov config and default MaxRemoteLockConsumers
```

### Impact Analysis

#### Technical Impact

- Unimplementable governance commands and throttled dispatch break the privileged escape hatch exactly when it is needed ([sb4], [sb5]).
- Origin concentration removes separation of duties ([sb24]).
- Template weights misprice extrinsics (DoS economics); waived XCM fees invite message spam ([aca1], [oz4x], [oz7b]).

#### Business Impact

- Major-rated by Oak for Snowbridge: the governance layer cannot guarantee incident response. For templated runtimes, SRLabs rates fee waivers High — free XCM is a spam/DoS economic vector.

#### Affected Scenarios

- Bridges with asymmetric admin command surfaces across chains.
- Parachains spun from substrate-node-template or polkadot-runtime-template without re-benchmarking and config review.
- OpenGov migrations where parameters (track config, `MaxRemoteLockConsumers`, proxy filtering) are undocumented.

### Secure Implementation

**Fix 1: Symmetric, least-privilege governance surfaces**
```rust
// ✅ SECURE: every documented admin command implemented & tested on both sides; tiered origins
pub fn set_fees(origin: OriginFor<T>, fees: FeeConfig) -> DispatchResult {
    T::FeeAdminOrigin::ensure_origin(origin)?;   // routine tier
    ...
}
pub fn halt_bridge(origin: OriginFor<T>) -> DispatchResult {
    T::EmergencyOrigin::ensure_origin(origin)?;  // high-sensitivity tier, separate origin
    ...
}
// runtime test: governance referendum on each command actually changes state on BOTH chains
```

**Fix 2: Production benchmarks and priced messaging**
```rust
// ✅ SECURE: re-benchmark, price XCM, document OpenGov
impl pallet_democracy::Config for Runtime {
    type WeightInfo = runtime_weights::pallet_democracy::WeightInfo<T>; // real benchmarks
}
parameter_types! {
    pub XcmFees: u128 = price_of(BaseXcmWeight::get()); // non-zero delivery fee
}
// document every OpenGov track/param; audit MaxRemoteLockConsumers against actual usage
```

### Detection Patterns

#### High-Signal Grep Seeds
```
- ensure_root
- ensure_origin
- WeightInfo
- substrate_node_template
- MaxRemoteLockConsumers
- OpenGov
- pallet_democracy
- call_filter
```

#### Code Patterns to Look For
```
- Pattern 1: docs/spec mention admin commands absent from #[pallet::call] on one side
- Pattern 2: pallets where grep shows every extrinsic starting with ensure_root(origin)?
- Pattern 3: WeightInfo impl blocks referencing substrate_node_template paths
- Pattern 4: XcmFees / ToTrap defaults set to 0 or commented as "TODO mainnet"
```

#### Audit Checklist
- [ ] For each documented governance/admin command: does a dispatchable exist and pass a functional test on every chain involved?
- [ ] Do routine and destructive extrinsics use different configured origins?
- [ ] Are all WeightInfo values from this runtime's benchmarks (not templates)?
- [ ] Are XCM delivery fees non-zero, and are OpenGov parameters documented?

### Keywords for Search

`governance origin`, `ensure_root`, `origin confusion`, `administrative commands`, `Snowbridge`, `centralized control`, `governance throttling`, `substrate-node-template`, `WeightInfo`, `benchmark weights`, `OpenGov`, `pallet_democracy`, `XCM fees waived`, `MaxRemoteLockConsumers`, `runtime template`, `least privilege`, `separation of duties`

### Related Vulnerabilities

- DB/substrate/pallets/origin-authorization-bypass.md (broken role checks — the sibling entry)
- DB/substrate/pallets/vesting-schedule-bypass.md (root/sudo surfaces)
- DB/substrate/bridges/snowbridge-bridge-accounting.md (Snowbridge fund-custody issues)
- DB/substrate/pallets/xcm-instruction-validation.md (XCM fee waivers)
