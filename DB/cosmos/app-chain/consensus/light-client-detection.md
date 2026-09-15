---
protocol: generic
chain: cosmos
category: consensus
vulnerability_type: light_client_detection

# Pattern Identity
root_cause_family: missing_detection_logic
pattern_key: missing_detection | light_client_attack_detector | light_client_detection

# Interaction Scope
interaction_scope: multi_component
involved_contracts:
  - LightClient (verification)
  - Supervisor (cross-header comparison)
  - AttackDetector
  - FullNodeWitnesses (primary/secondary witnesses)
path_keys:
  - missing_cross_header_check | supervisor compares | divergent headers | undetected equivocation
  - faulty_bisection | skippingSearch vs sequentialSearch | wrong verdict | accepted_attack
  - missing_evidence_submission | detector output → EvidencePool | unslashable attacker

# Attack Vector Details
attack_type: consensus_attack|logical_error
affected_component: light_client|light_block_supervisor

# Technical Primitives
primitives:
  - light_client_attack
  - bisection_verification
  - fork_detection
  - witness_comparison
  - evidence_pool_submission
  - trusting_period

# Grep / Hunt-Card Seeds
code_keywords:
  - VerifyNonAdjacent
  - VerifyAdjacent
  - sequentialSearch
  - skippingSearch
  - CompareHeaderBeforeTrustedHeader
  - AlreadyVerified
  - AttackDetector
  - Evidence
  - LightBlock
  - TrustedBlock
  - Source
  - Primary
  - Witnesses
  - ForkDetection

# Impact Classification
severity: critical
impact: state_corruption|fund_loss|consensus_break
exploitability: 0.4
financial_impact: high

# Context Tags
tags:
  - cosmos
  - cometbft
  - tendermint
  - light-client
  - detection
  - bisection
  - fork
  - consensus

language: go
version: CometBFT/Tendermint light client spec (detection-001, detection-003, isolate-attackers-002)

---

## References & Source Reports

> **For Agents**: If you need detailed information, read the referenced report file.

### Light Client Detection Specification
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Light Client Attack Detector spec (sequentialSearch/skippingSearch bisection, detection data structures, evidence) | `reports/cosmos-l1-nodes_findings/cometbft-spec-light-client-detection-detection-001-reviewed-md.md` | SPEC | Informal Systems |
| Detection 003 (continued detector spec — attacker isolation conditions) | `reports/cosmos-l1-nodes_findings/cometbft-spec-light-client-detection-detection-003-reviewed-md.md` | SPEC | Informal Systems |
| Lightclient Attackers Isolation (fork attack model, CMBC-FM-2THIRDS violation) | `reports/cosmos-l1-nodes_findings/cometbft-spec-light-client-attacks-isolate-attackers-002-reviewed-md.md` | SPEC | Informal Systems |
| Detection discussions (design rationale, open questions) | `reports/cosmos-l1-nodes_findings/tendermint-spec-light-client-detection-discussions-md.md` | SPEC | Informal Systems |
| Draft detection functions | `reports/cosmos-l1-nodes_findings/tendermint-spec-light-client-detection-draft-functions-md.md` | SPEC | Informal Systems |
| IBC detection requirements | `reports/cosmos-l1-nodes_findings/tendermint-spec-light-client-detection-req-ibc-detection-md.md` | SPEC | Informal Systems |
| Notes on evidence handling | `reports/cosmos-l1-nodes_findings/tendermint-spec-light-client-attacks-notes-on-evidence-handling-md.md` | SPEC | Informal Systems |

### SEI Instance
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Sei tendermint light-client detection 001 spec | `reports/cosmos-l1-nodes_findings/sei-chain-sei-tendermint-spec-light-client-detection-detection-001-reviewed-md.md` | SPEC | Sei/Informal |
| Sei tendermint detection 003 | `reports/cosmos-l1-nodes_findings/sei-chain-sei-tendermint-spec-light-client-detection-detection-003-reviewed-md.md` | SPEC | Sei/Informal |
| Sei isolate attackers 002 | `reports/cosmos-l1-nodes_findings/sei-chain-sei-tendermint-spec-light-client-attacks-isolate-attackers-002-reviewed-md.md` | SPEC | Sei/Informal |

---

## Light-Client Attack Detection Vulnerabilities [CRITICAL]

### Overview

In a light client attack, correct full nodes agree on the block sequence (no fork), but faulty ex-validators (>1/3 historical voting power) sign a deviating block at some height and feed it to a light client. The CometBFT detection design counters this by (a) bisecting divergent headers (`sequentialSearch` / `skippingSearch`) to find the exact point of conflicting commits and (b) submitting the resulting evidence (conflicting votes) to the Evidence Pool so attackers can be slashed and isolated. Vulnerabilities in this class are *specification-implementation gaps*: forks of the supervisor/detector that skip cross-header comparison, implement bisection incorrectly, or fail to convert detection into submittable evidence.

#### Agent Quick View

- Root cause statement: "Light clients that verify single chains of headers (VerifyAdjacent/VerifyNonAdjacent) without comparing the resulting header against a second witness source and without generating slashable evidence accept fabricated headers signed by ex-validator cabals — detection is a required second algorithm, not an optional feature."
- Pattern key: `missing_detection | light_client_attack_detector | light_client_detection`
- Interaction scope: `multi_component`
- Primary affected component(s): `light client supervisor, attack detector, evidence pool bridge`
- High-signal code keywords: `sequentialSearch`, `skippingSearch`, `VerifyNonAdjacent`, `CompareHeaderBeforeTrustedHeader`, `Evidence`, `Witnesses`
- Typical sink / impact: `light client accepts invalid state root → IBC packet proven against false state → cross-chain fund theft; attackers never slashed`
- Validation strength: `strong (formal spec, TLA+ companion models, multiple reviewed versions)`

#### Contract / Boundary Map

- Entry surface(s): `UpdateLightBlock(headerFromPrimary)`, witness responses, `VerifyToTarget`
- Component hop(s): `verification (single chain) → supervisor (primary vs witnesses compare) → detector (bisection to find conflicting pair) → evidence submission (on-chain EvidencePool)`
- Trust boundary crossed: `untrusted full node → light client trusted state`; `off-chain detection output → on-chain evidence` (format/height-window validity)
- Shared state or sync assumption: `CMBC-FM-2THIRDS (>2/3 correct voting power per block); evidence must be submitted within the evidence window; trusted state within trusting period`

#### Valid Bug Signals

- Signal 1: Light client verifies headers from a single source only (no witness comparison in supervisor) — detection impossible by construction
- Signal 2: Bisection implemented only as `sequentialSearch` without the log-time `skippingSearch` or vice versa, or `CompareHeaderBeforeTrustedHeader` returns "pending" cases not handled (liveness/deadlock or missed forks)
- Signal 3: Detection produces conflicting headers but the code never constructs `DuplicateVoteEvidence`/`LightClientAttackEvidence` or submits past the evidence age window
- Signal 4: `AlreadyVerified` short-circuit compares only height, not header hash (accepts distinct header at same height)
- Signal 5: Trusting period / clock drift checks absent around verification (stale trust reused)

#### False Positive Guards

- Not this bug when: the deployment is a *full node* (verification via consensus, not light client) or uses a ZK client where detection is replaced by proof validity
- Safe if: supervisor compares primary against ≥1 independent witness and spec-conformant bisection runs on divergence with evidence submission tested end-to-end
- Requires attacker control of: >1/3 *historical* (ex-)validator voting power + network position to feed the target light client (hence exploitability 0.4 — costly but catastrophic)

### Vulnerable Pattern Examples

**Example 1: Detection spec semantics (what to verify against)** [SPEC — the contract]
> 📖 Reference: `reports/cosmos-l1-nodes_findings/cometbft-spec-light-client-detection-detection-001-reviewed-md.md`
"In a light client attack, all the correct Cosmos full nodes agree on the sequence of generated blocks (no fork), but a set of faulty full nodes attack a light client by generating (signing) a block that deviates from the block of the same height on the blockchain... An attack detector (or detector for short) is a mechanism that is used by the light client supervisor after verification of a new light block."

**Example 2: Attacker isolation requirement**
> 📖 Reference: `reports/cosmos-l1-nodes_findings/cometbft-spec-light-client-attacks-isolate-attackers-002-reviewed-md.md`
"As Tendermint consensus and light client verification is safe under the assumption of more than 2/3 of correct voting power per block, this implies that if there was an attack then [CMBC-FM-2THIRDS] was violated" — detection must produce evidence identifying the violators so they can be isolated (slashed), otherwise attacks are cost-free and repeatable.

**Example 3: Implementation pitfalls catalogued in spec TODOs**
> 📖 Reference: `reports/cosmos-l1-nodes_findings/cometbft-spec-light-client-detection-detection-001-reviewed-md.md`
Spec TODOs mark exactly where forks go wrong: LightStore state semantics (`LatestVerified`), `VerifyToTarget` second-parameter semantics, and "if it returns TimeoutError it can be assumed faulty" — implementations that ignore these cases silently accept or loop on attacker data.

### Secure Implementation

```go
// ✅ SECURE: spec-conformant supervision + evidence emission
func (s *Supervisor) Update(ctx, primaryHeader) error {
    if err := s.verifyFromPrimary(primaryHeader); err != nil { return err }
    for _, w := range s.witnesses {                    // cross-source compare
        wh, err := s.fetchLatest(w)
        if err != nil { continue /* witness unavailable: track, alert */ }
        if cmp := CompareHeaders(primaryHeader, wh); cmp == Divergent {
            ev, err := s.detector.Detect(primaryHeader, wh)  // bisection
            if err == nil && ev != nil {
                s.evidenceBroadcaster.Broadcast(ev)      // slashable evidence
                s.markWitnessesCompromised(...)
            }
        }
    }
}
```

### Impact Analysis

- **Frequency**: specification family (7 spec documents + 3 SEI instances); historical attacks (e.g., Binance fork incident class) motivated the spec
- **Severity Distribution**: SPEC/CRITICAL class (impact when unimplemented)
- **Affected Protocols**: CometBFT/Tendermint light clients, IBC Tendermint clients (07-tendermint), exchange/bridge light clients, SEI's tendermint fork
- **Validation Strength**: Strong (formal methods team, TLA+ models, reviewed versions 001–003)

**Cross-references**: `consensus/light-client-accountability.md` (who gets slashed), `ibc/ibc-v2-eureka-client-status.md` (frozen-client gating downstream of misbehaviour), `consensus/consensus-finality-vulnerabilities.md`.
