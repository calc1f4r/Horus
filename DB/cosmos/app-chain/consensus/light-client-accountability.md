---
protocol: generic
chain: cosmos
category: consensus
vulnerability_type: light_client_accountability

# Pattern Identity
root_cause_family: missing_accountability_mechanism
pattern_key: missing_accountability | fork_accountability | light_client_accountability

# Interaction Scope
interaction_scope: multi_component
involved_contracts:
  - Consensus (Tendermint/CometBFT)
  - EvidencePool
  - SlashingModule
  - Fork accountability invariants (inductive invariant)
path_keys:
  - equivocation_undetected | two votes same round | no slash | repeated attacks
  - amnesia_unhandled | lock changed without justification | invariant violated | unslashable
  - evidence_gap | f+1 byzantine provable | less than f+1 provable | accountability hole

# Attack Vector Details
attack_type: consensus_attack
affected_component: fork_accountability|evidence_pool|slashing

# Technical Primitives
primitives:
  - fork_accountability
  - equivocation
  - amnesia
  - inductive_invariant
  - tendermint_paper_invariants
  - apalache_model_checking

# Grep / Hunt-Card Seeds
code_keywords:
  - TendermintAcc
  - TypedInv
  - equivocation
  - amnesia
  - DuplicateVoteEvidence
  - LightClientAttackEvidence
  - EvidencePool
  - MaxEvidenceAge
  - slashFractionDoubleSign
  - byzantine
  - voting_power
  - f+1

# Impact Classification
severity: high
impact: consensus_break|repeated_attacks|slash_evasion
exploitability: 0.3
financial_impact: high

# Context Tags
tags:
  - cosmos
  - tendermint
  - cometbft
  - consensus
  - accountability
  - slashing
  - formal-methods
  - tla+

language: go
version: Tendermint/CometBFT spec — fork accountability (001indinv apalache)

---

## References & Source Reports

> **For Agents**: If you need detailed information, read the referenced report file.

### Fork Accountability Formal Verification
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| TLA+ fork accountability synopsis (simplified one-shot Tendermint, equivocation + amnesia, f+1 provable) | `reports/cosmos-l1-nodes_findings/tendermint-spec-light-client-accountability-synopsis-md.md` | SPEC | Informal Systems |
| Results 001indinv-apalache (model checking runs, inductive invariant TypedInv, MC_n4/n5 configs) | `reports/cosmos-l1-nodes_findings/tendermint-spec-light-client-accountability-results-001indinv-apalache-report-md.md` | SPEC | Informal Systems |
| Notes on evidence handling (evidence pool semantics) | `reports/cosmos-l1-nodes_findings/tendermint-spec-light-client-attacks-notes-on-evidence-handling-md.md` | SPEC | Informal Systems |
| SEI instance: accountability apalache results | `reports/cosmos-l1-nodes_findings/sei-chain-sei-tendermint-spec-light-client-accountability-results-001indinv-apalache-report-md.md` | SPEC | Sei/Informal |
| SEI isolate attackers 001 (draft) | `reports/cosmos-l1-nodes_findings/tendermint-spec-light-client-attacks-isolate-attackers-001-draft-md.md` | SPEC | Informal Systems |

---

## Light-Client / Fork Accountability Vulnerabilities [HIGH]

### Overview

Fork accountability is the property that, given a fork, the evidence held by correct processes suffices to prove at least `f+1` processes Byzantine (via **equivocation** — two different votes in the same round — or **amnesia** — locking a value inconsistent with prior locks). Informal Systems specified this in TLA+ (`TendermintAcc_004_draft` + inductive invariant `TypedInv`) and checked it with Apalache (10h budgets, n4/n5, f1/f2 configs). The vulnerability class for auditors: chains whose evidence pool / slashing rules implement only *part* of the accountability relation (e.g., detect DuplicateVoteEvidence but not amnesia-style conflicts, or expire evidence too early), leaving attackers unslashed and attacks repeatable.

#### Agent Quick View

- Root cause statement: "Accountability is an on-chain *encoding* of an off-chain proof relation; any mismatch between the TLA+-verified relation (equivocation ∪ amnesia, f+1 provable) and the implemented evidence types/slash rules lets fork participants escape slashing and re-attack."
- Pattern key: `missing_accountability | fork_accountability | light_client_accountability`
- Interaction scope: `multi_component`
- Primary affected component(s): `evidence pool admission rules, slashing module double-sign handlers, light-client attack evidence path`
- High-signal code keywords: `DuplicateVoteEvidence`, `LightClientAttackEvidence`, `MaxEvidenceAge`, `TendermintAcc`, `equivocation`, `amnesia`, `slashFractionDoubleSign`
- Typical sink / impact: `unslashable forgers → repeated light client attacks / consensus safety failures without economic consequence`
- Validation strength: `strong (formal spec + bounded model checking)`

#### Contract / Boundary Map

- Entry surface(s): `CheckEvidence` (evidence pool), `ApplyPenalties`/slashing keeper, light-client attack evidence submission
- Component hop(s): `off-chain conflicting commits → evidence struct → pool validity window → slashing`
- Trust boundary crossed: `off-chain proof objects → on-chain penalty execution` (the encoding is the attack surface)
- Shared state or sync assumption: `evidence must be submittable while still valid (MaxEvidenceAge); validator set changes must not orphan vote signatures`

#### Valid Bug Signals

- Signal 1: Evidence pool admits `DuplicateVoteEvidence` only; no handling for light-client-attack evidence (amnesia-class or conflicting-header conflicts) — accountability relation under-encoded
- Signal 2: Evidence validity window (`MaxEvidenceAge`) shorter than the time to detect+broadcast light client attacks (esp. with slow bisection) — attackers outlive the window
- Signal 3: Slashing of light client attack evidence attributes blame to *all* validators of the conflicting header rather than the provable f+1 subset (over/under-slashing)
- Signal 4: Vote-signature validation ignores validator-set changes across the two conflicting votes (wrong pubkey set used)
- Signal 5: On-chain "invalid evidence" handling panics or halts consensus instead of rejecting (evidence itself is attacker-controlled input)

#### False Positive Guards

- Not this bug when: evidence admission matches the spec relation and the chain halts rather than finalizing on conflicting evidence (accountability-preserving)
- Safe if: double-sign slashing includes both equivocation types and evidence from detection (see detection card) flows into the same pool
- Requires attacker control of: validator set participation (≥1/3 historical power for the attack; ≥1 Byzantine for equivocation evidence)

### Vulnerable Pattern Examples

**Example 1: The accountability relation implementations must satisfy** [SPEC]
> 📖 Reference: `reports/cosmos-l1-nodes_findings/tendermint-spec-light-client-accountability-synopsis-md.md`
"Byzantine processes can demonstrate arbitrary behavior... However, we have to show that under the collective evidence collected by the correct processes, at least `f+1` Byzantine processes demonstrate one of the following behaviors: **Equivocation**: a Byzantine process sends two different values in the same round. **Amnesia**: a Byzantine process locks a value, although it has locked another value in the past."

**Example 2: Model-checked invariant (`TypedInv`)** [SPEC]
> 📖 Reference: `reports/cosmos-l1-nodes_findings/tendermint-spec-light-client-accountability-results-001indinv-apalache-report-md.md`
Runs `MC_n4_f1.tla / MC_n5_f1.tla ... apalache 10h --length=1 --cinit=ConstInit` with `TypedInv` as both init-inv and next-inv — the inductive invariant auditors can treat as the reference correctness claim for one-shot fork accountability.

**Example 3: Evidence-handling gap primer**
> 📖 Reference: `reports/cosmos-l1-nodes_findings/tendermint-spec-light-client-attacks-notes-on-evidence-handling-md.md` — notes on how detection outputs must map into evidence-pool admissible objects (window, heights, validator sets).

### Secure Implementation

```go
// ✅ SECURE: accountability-complete evidence admission
func (pool *EvidencePool) CheckEvidence(ctx, ev Evidence) error {
    switch e := ev.(type) {
    case *DuplicateVoteEvidence:        // equivocation
        return pool.verifyDuplicateVote(e)     // both sigs, same height+round+valset
    case *LightClientAttackEvidence:    // amnesia/ conflicting-header class
        return pool.verifyLightClientAttack(e) // blame = provable conflicting signers
    default:
        return ErrUnknownEvidence               // never panic on attacker input
    }
    // enforce: height - evidenceHeight <= MaxEvidenceAge (spec window)
    // slashing attributes ONLY signers of conflicting commits (f+1 provable subset)
}
```

### Impact Analysis

- **Frequency**: specification + verification results (2 core docs, 2 SEI/v1 drafts, evidence-handling notes)
- **Severity Distribution**: SPEC/HIGH class when under-implemented
- **Affected Protocols**: CometBFT/Tendermint chains, SEI's tendermint fork, IBC Tendermint client misbehaviour → slashing pipeline
- **Validation Strength**: Strong (formal methods: TLA+/Apalache)

**Cross-references**: `consensus/light-client-detection.md` (evidence generation), `slashing/slashing-accounting-errors.md`, `slashing/slashing-evasion-frontrunning.md`, `consensus/consensus-finality-vulnerabilities.md`.
