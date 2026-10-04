---
# Core Classification
protocol: generic
chain: polkadot
category: cross_chain
vulnerability_type: input_validation_bypass
root_cause_family: configuration_error
pattern_key: missing-xcm-fee-or-limit | XCM message delivery | unpriced cross-chain execution | spam and congestion

# Interaction Scope
interaction_scope: cross_chain
involved_contracts:
  - xcm_config / FeeManager
  - pallet_message_queue
  - pallet_call_decompressor
path_keys:
  - missing-xcm-fee-or-limit | XCM delivery fee waived | FeeManager = () | message queue congestion
  - missing-xcm-fee-or-limit | sibling delivery unpriced | NoPriceForMessageDelivery | storage exhaustion
  - missing-xcm-fee-or-limit | nested call decode | decompress_call | stack exhaustion
  - missing-xcm-fee-or-limit | unsigned ISMP relay | handle_incoming_message | free execution

# Attack Vector Details
attack_type: denial_of_service
affected_component: xcm_config_message_delivery

# Technical Primitives
primitives:
  - FeeManager
  - PriceForSiblingDelivery
  - NoPriceForMessageDelivery
  - DecodeLimit
  - Weigher
  - XcmConfig

# Grep / Hunt-Card Seeds
code_keywords:
  - FeeManager
  - PriceForSiblingDelivery
  - NoPriceForMessageDelivery
  - decompress_call
  - DecodeLimit
  - decode_with_depth_limit
  - handle_incoming_message
  - xcm_configs

severity: high
impact: denial_of_service
language: rust
tags:
  - substrate
  - xcm
  - dos
  - misconfiguration
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [oz1] | reports/substrate-l1_findings/polkadot-runtime-templates-oz-2024-04.md | CRITICAL | SRLabs | 3.2.1 Runtime template waives XCM message delivery fee (Closed) |
| [oz2] | reports/substrate-l1_findings/polkadot-runtime-templates-oz-2024-04.md | HIGH | SRLabs | 3.2.2 No XCM delivery fees configured for sibling parachain messages |
| [oz3] | reports/substrate-l1_findings/polkadot-runtime-templates-oz-2024-04.md | HIGH | SRLabs | 3.2.3 Incorrect runtime weights for XCM and Message Queue pallet |
| [hb1] | reports/substrate-l1_findings/hyperbridge-srl-2405.md | HIGH | SRLabs | 6.1 Nexus runtime waives XCM message delivery fee (Risk accepted) |
| [hb2] | reports/substrate-l1_findings/hyperbridge-srl-2405.md | HIGH | SRLabs | 6.2 No XCM delivery fees for sibling parachain messages |
| [hb3] | reports/substrate-l1_findings/hyperbridge-srl-2405.md | HIGH | SRLabs | 6.3 Stack exhaustion due to missing DecodeLimit (Fixed) |
| [hb4] | reports/substrate-l1_findings/hyperbridge-srl-2405.md | HIGH | SRLabs | 6.6 Unsigned extrinsics allow executing ISMP messages for free |
| [plf6] | reports/substrate-l1_findings/parallel-tob-1.md | MEDIUM | Trail of Bits | 6. Unhandled XCM request failures in crowdloans/liquid-staking |
| [x7] | reports/substrate-l1_findings/acala-srl-2021-12.md | HIGH | SRLabs | Integer overflow in the xcm::v1 pallet could result in loss of asset tokens |
| [x8] | reports/substrate-l1_findings/audit-reports-snowbridge-2024-05-24-audit-report-snowbridge-v1-1-pdf.md | CRITICAL | auditor | Attackers can drain sovereign funds and hence DoS the bridge by spamming registerToken transactions |
| [x11] | reports/substrate-l1_findings/moonbeam-srl-2401.md | MEDIUM | SRLabs | Attack impact Block production could be entirely halted without remediation since XCM implies forced execution |

## Waived XCM Delivery Fees and Unbounded Cross-Chain Message Execution Enable Spam Congestion

**XCM configuration mistakes (unit-type FeeManager, NoPriceForSiblingDelivery, missing decode-depth limits, zero-weight/unsigned relay extrinsics) let attackers flood message queues and execute cross-chain messages for free** - representative of runtime XCM misconfigurations that neutralize every fee-based congestion control at once.

### Overview

Multiple SRLabs audits of Polkadot runtimes (OpenZeppelin runtime template, Hyperbridge Nexus) found the same class: the runtime XCM config waives delivery fees, charges nothing for sibling-parachain delivery, uses incorrect weights, or accepts unsigned/unpriced cross-chain message execution. An attacker spams free messages, exhausting queue storage and delaying or dropping honest traffic; related bugs allow deeply nested calls to exhaust the stack during decoding.

#### Agent Quick View

- Root cause statement: "FeeManager set to the unit type / PriceForSiblingDelivery set to NoPriceForMessageDelivery / missing DecodeLimit / unsigned relay extrinsics — every economic and structural limit on XCM processing is absent or wrong."
- Pattern key: `missing-xcm-fee-or-limit | XCM message delivery | unpriced cross-chain execution | spam and congestion`
- Interaction scope: `cross_chain`
- Primary affected component(s): `xcm_config, pallet_message_queue, call decompressor, ISMP message handler`
- Contracts / modules involved: `xcm_configs.rs, FeeManager, pallet_call_decompressor, modules/ismp`
- Path keys: `FeeManager = () | queue congestion`, `NoPriceForMessageDelivery | sibling spam`, `decompress_call | stack exhaustion`, `unsigned handle_incoming_message | free execution`
- High-signal code keywords: `FeeManager, PriceForSiblingDelivery, NoPriceForMessageDelivery, decompress_call, DecodeLimit, handle_incoming_message`
- Typical sink / impact: `queue/storage exhaustion, dropped messages, stalled block production, free cross-chain execution`
- Validation strength: `strong` (two independent SRLabs audits; several marked risk-accepted in production)

#### Contract / Boundary Map

- Entry surface(s): XCM message delivery from relay/sibling chains, `decompress_call`, unsigned ISMP message submission
- Contract hop(s): `remote chain -> XCM executor -> pallet_message_queue -> target pallet`
- Trust boundary crossed: `economic spam-control boundary (fees/weights) between foreign message senders and local chain capacity`
- Shared state or sync assumption: fees charged must cover queue weight; decode depth must be bounded

#### Valid Bug Signals

- Signal 1: `FeeManager` type in XCM config is `()` (or any NewFree implementation), or `PriceForSiblingDelivery` is `NoPriceForMessageDelivery`.
- Signal 2: A dispatchable that decodes user-supplied call data (`decompress_call`) uses `decode()` instead of `decode_with_depth_limit(DecodeLimit::new(n))`.
- Signal 3: Unsigned extrinsics accept and execute arbitrary cross-chain/ISMP message types without fee, bond, or per-message nonce.
- Signal 4: XCM/Message Queue weights copied from another runtime without benchmarking ([oz3], [hb4]).

#### False Positive Guards

- Not this bug when: fees are configured with exponential backlog pricing (Kusama-style) and benchmarks exist for the actual runtime.
- Safe if: unsigned paths validate against a tag/nonce and the pool drops invalid submissions (note: Hyperbridge showed repeated FraudProof replay can still circumvent pool checks — [hb4]/6.9 interplay).
- Requires attacker control of: any funded account on a connected chain (cheap; cost is near zero when fees waived).

### Vulnerability Description

#### Root Cause

Runtime configuration templates and production runtimes ship XCM configs with `FeeManager = ()` and sibling delivery priced at zero, alongside unbounded decoding and unpriced unsigned message execution. All fee-based congestion mechanisms become ineffective simultaneously.

#### Attack Scenario / Path Variants

**Path A: Free XCM spam floods the message queue**
Path key: `missing-xcm-fee-or-limit | FeeManager = () | queue congestion`
Entry surface: XCM delivery into the runtime
1. Attacker sends a high volume of XCM messages from a chain with no delivery fee charged.
2. The message queue grows unbounded; storage bloats and delivery slows.
3. Honest messages are delayed or dropped; bridge/threshold liveness degrades.

**Path B: Zero-cost sibling parachain spam**
Path key: `missing-xcm-fee-or-limit | NoPriceForMessageDelivery | storage exhaustion`
1. Attacker relays messages between sibling parachains with `PriceForSiblingDelivery = NoPriceForMessageDelivery`.
2. No fee is charged for delivery across parachains.
3. Queue size exhaustion and delivery delays for other users ([oz2], [hb2]).

**Path C: Stack exhaustion via nested decoded calls**
Path key: `missing-xcm-fee-or-limit | decompress_call | stack exhaustion`
1. Attacker submits a deeply nested compressed call to `decompress_call` (no decode depth limit).
2. Decoding recurses past stack limits and crashes nodes.
3. If routed through a bridge with forced execution, it can permanently stall the receiving chain ([hb3]).

**Path D: Free ISMP message execution**
Path key: `missing-xcm-fee-or-limit | unsigned handle_incoming_message | free execution`
1. ISMP messages are unsigned extrinsics; attacker submits Request/Response/Consensus messages for free.
2. Execution consumes real weight/storage with no punishment or blacklisting ([hb4]).

#### Vulnerable Pattern Examples

**Example 1: FeeManager waived (from [oz1]/[hb1])** [Approx Vulnerability : CRITICAL]
```rust
// ❌ VULNERABLE: unit-type FeeManager waives all XCM delivery fees
pub struct XcmConfig;
impl xcm_executor::Config for XcmConfig {
    type FeeManager = (); // polkadot-sdk: unit type == fees never charged
}
// fix per polkadot runtime v1.3: implement FeeManager charging BuyExecution
```

**Example 2: Free sibling delivery** [Approx Vulnerability : HIGH]
```rust
// ❌ VULNERABLE: sibling messages priced at zero (from [oz2])
parameter_types! {
    pub const PriceForSiblingDelivery: PriceForSiblingParachainDelivery =
        PriceForSiblingParachainDelivery::NoPriceForMessageDelivery;
}
// attacker spams sibling queues without paying; use exponential pricing (Kusama config)
```

**Example 3: Unbounded decode of user calls** [Approx Vulnerability : HIGH]
```rust
// ❌ VULNERABLE: no decode depth limit (from [hb3], pallet-call-decompressor)
pub fn decompress_call(origin, compressed: Vec<u8>) -> DispatchResult {
    let call = <T as Config>::RuntimeCall::decode(&mut compressed.as_slice())?; // unbounded recursion
    call.dispatch(origin)
}
```

### Impact Analysis

#### Technical Impact

- Queue/storage exhaustion, long delivery delays, dropped messages; permanent chain stall when forced-execution bridges carry the nesting bomb ([hb3]).
- Zero-cost execution of cross-chain state changes ([hb4]); unhandled XCM failures strand contributed funds in crowdloan/liquid-staking flows ([plf6]).

#### Business Impact

- Bridge and parachain liveness degradation; templates propagate the flaw to every downstream runtime built from the template.

#### Affected Scenarios

- New parachains copying runtime templates; ISMP/bridge runtimes; any runtime that has not benchmarked XCM + message queue weights.

### Secure Implementation

**Fix 1: Price all delivery and bound all decoding**
```rust
// ✅ SECURE: charge fees with exponential backlog + bound decode depth
pub struct ChargeFees;
impl FeeManager for ChargeFees { /* burn/credit weight_to_fee(msg.weight()) */ }
type PriceForSiblingDelivery = ExponentialPrice<
    min_price, max_price, decay_interval, max_inbound_to_queue,
>;
pub fn decompress_call(origin, compressed: Vec<u8>) -> DispatchResult {
    let call = <T as Config>::RuntimeCall::decode_with_depth_limit(
        DecodeLimit::new(T::MaxCallDepth::get()), &mut compressed.as_slice())?;
    call.dispatch(origin)
}
```

### Detection Patterns

#### High-Signal Grep Seeds
```
- type FeeManager = ()
- NoPriceForMessageDelivery
- PriceForSiblingDelivery
- decompress_call
- decode(&mut  (call decoding sites)
- handle_incoming_message
```

#### Code Patterns to Look For
```
- Pattern 1: XCM config blocks with unit-type FeeManager or free sibling pricing
- Pattern 2: decode() of RuntimeCall from user input without decode_with_depth_limit
- Pattern 3: unsigned extrinsics executing arbitrary message types without per-message nonce/deposit
- Pattern 4: weights declared via estimate instead of runtime benchmarks for XCM/message-queue
```

#### Audit Checklist
- [ ] Does every inbound XMP/XCM path charge a fee covering worst-case weight?
- [ ] Is sibling-parachain delivery priced (exponentially)?
- [ ] Are all user-controlled decodes depth-limited?
- [ ] Can unsigned relay messages be replayed for free?

### Keywords for Search

`XCM`, `FeeManager`, `message delivery fee`, `NoPriceForMessageDelivery`, `PriceForSiblingDelivery`, `message queue congestion`, `DecodeLimit`, `stack exhaustion`, `decompress_call`, `unsigned extrinsic`, `ISMP`, `hyperbridge nexus`, `runtime template`, `xcm_configs`, `spam`, `storage exhaustion`

### Related Vulnerabilities

- DB/substrate/pallets/bridge-light-client-header-validation.md
- DB/substrate/pallets/origin-authorization-bypass.md
