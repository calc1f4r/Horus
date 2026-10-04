---
protocol: dydx
chain: dydx
category: consensus
vulnerability_type: proposer_set_correctness

# Pattern Identity
root_cause_family: assumption_mismatch
pattern_key: assumption_mismatch | proposer_selection | no_correct_proposer_scenario

# Interaction Scope
interaction_scope: multi_component
involved_contracts:
  - ProposerSelectionModule (dYdX v4)
  - StakingKeeper (redelegation/slashing/jailing)
  - CometBFT validator set
path_keys:
  - staking_drain | redelegation+slashing+jailing | proposer count below fault bound | no proposer
  - missing_invariant | proposer set voting power > 1/3 total | unenforced assumption | chain stall

# Attack Vector Details
attack_type: logical_error|dos
affected_component: proposer_selection|validator_set_composition

# Technical Primitives
primitives:
  - proposer_selection_updates
  - msg_set_proposers
  - redelegation_effects
  - voting_power_bound
  - cometbft_fault_assumption

# Grep / Hunt-Card Seeds
code_keywords:
  - MsgSetProposers
  - proposer set
  - NumProposers
  - redelegate
  - jail
  - slash
  - voting power
  - proposer_rewards
  - ValidateProposerSet

# Impact Classification
severity: high
impact: chain_stall|liveness_failure|missed_blocks
exploitability: 0.4
financial_impact: medium

# Context Tags
tags:
  - dydx
  - cosmos
  - appchain
  - consensus
  - proposer-selection
  - validator-set
  - liveness

language: go
version: dYdX v4 (Q3 2025 proposer selection updates audit)

---

## References & Source Reports

> **For Agents**: If you need detailed information, read the referenced report file.

### dYdX Proposer Selection Audit
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Redelegations, slashing and jailing can lead to scenarios where there is no correct proposer (Design, High, Acknowledged) | `reports/cosmos-l1-nodes_findings/audits-dydx-dydx-q3-2025-proposer-selection-updates-audit-report-final-pdf.md` | HIGH | Informal Systems |
| Recommendation to enforce uniqueness in proposer set validation (Implementation, Informational) | `reports/cosmos-l1-nodes_findings/audits-dydx-dydx-q3-2025-proposer-selection-updates-audit-report-final-pdf.md` | INFO | Informal Systems |
| Miscellaneous code improvements | `reports/cosmos-l1-nodes_findings/audits-dydx-dydx-q3-2025-proposer-selection-updates-audit-report-final-pdf.md` | INFO | Informal Systems |

---

## dYdX Proposer-Set Correctness Vulnerabilities [HIGH]

### Overview

dYdX v4's Q3-2025 "proposer selection updates" introduce a designated proposer set (chosen via governance `MsgSetProposers`) that runs alongside the CometBFT validator set. Informal Systems' audit found a **design-level High**: nothing prevents redelegations, slashing, and jailing from draining the proposer set below the point where *all remaining proposers* could be faulty — i.e., the "at least one correct proposer" assumption is strictly stronger than CometBFT's standard <1/3 fault assumption and is not enforced on-chain. Status: Acknowledged.

#### Agent Quick View

- Root cause statement: "The proposer-selection feature implicitly assumes ≥1 honest active proposer, but staking dynamics (redelegation, slashing, jailing) outside the feature's control can push the proposer set's correct voting power below the safety bound — the invariant 'proposer set voting power > 1/3 of total' is never checked."
- Pattern key: `assumption_mismatch | proposer_selection | no_correct_proposer_scenario`
- Interaction scope: `multi_component`
- Primary affected component(s): `proposer selection module ↔ staking keeper (redelegation/slashing/jail) ↔ CometBFT proposer scheduling`
- High-signal code keywords: `MsgSetProposers`, `proposer set`, `redelegate`, `jail`, `slash`, `voting power`, `ValidateProposerSet`
- Typical sink / impact: `no valid proposer for blocks → chain stall / missed blocks / proposer-reward failure`
- Validation strength: `strong (dedicated Formal Methods audit; issue tracked as Acknowledged)`

#### Component / Boundary Map

- Entry surface(s): governance `MsgSetProposers` (rare, long-term), continuous staking txs (redelegate/unjail), slashing events (fast, outside dev control)
- Component hop(s): `staking state changes → validator power updates → proposer set membership/power → CometBFT proposer election`
- Trust boundary crossed: `permissionless staking operations → protocol-critical proposer availability`
- Shared state or sync assumption: `proposer set must always contain ≥1 correct validator with the assumption it holds >1/3 of total voting power (sufficient condition per audit)`

#### Valid Bug Signals

- Signal 1: Proposer set admission/retention does not verify members' *current* (post-redelegation) bonded power stays above the 1/3-of-total bound
- Signal 2: No reaction (halt/halt-proposal/alert) when jailing+slashing drives active proposer count toward 0
- Signal 3: Proposer set validation allows duplicates or non-unique membership (companion Info finding: "enforce uniqueness in proposer set validation")
- Signal 4: Governance-set proposer lists are point-in-time snapshots with no expiry/re-validation against validator set changes

#### False Positive Guards

- Not this bug when: chain enforces the sufficient condition (proposer total power > 1/3 of validator total at every block) or proposer selection is purely CometBFT-default
- Acknowledged-risk guard: dYdX accepted the assumption ("at least one active proposer... at any time") — report as design-acknowledged, not as an unpatched code bug
- Requires: natural staking dynamics (no single attacker needed) or coordinated unstaking from proposer set

### Vulnerable Pattern Examples

**Example 1: Staking dynamics break the proposer-availability assumption** [HIGH, Design, Acknowledged]
> 📖 Reference: `reports/cosmos-l1-nodes_findings/audits-dydx-dydx-q3-2025-proposer-selection-updates-audit-report-final-pdf.md`
"Without further assumptions, because of redelegations, slashing or jailing, the number of proposers may fall below a value where according to their stake and the normal fault assumptions of CometBFT all of them may fail... the acceptance of a MsgSetProposer by a governance proposal is a rare and long-term event, while redelegations and slashing might happen faster and are not in the hands of the developers and operators of the chain."

**Example 2: Weak proposer-set validation** [INFO]
> 📖 Reference: same report — "Recommendation to enforce uniqueness in proposer set validation" (duplicates not rejected at validation).

### Secure Implementation

```go
// ✅ SECURE: enforce the availability invariant at every power-changing event
func (k Keeper) AssertProposerSetHealthy(ctx sdk.Context) error {
    total := k.staking.GetLastTotalPower(ctx)
    proposerPower := sumPowerOf(ctx, k.GetProposers(ctx)) // current, post-redelegate
    if proposerPower.GT(total.Quo(sdk.NewInt(3))) == false {
        return ErrProposerSetBelowSafetyBound // halt gov action / trigger alert & re-selection
    }
    return nil
}
// call sites: MsgSetProposers handler, AfterValidatorSlashed / BeforeDelegationRemoved hooks
// ValidateBasic: reject duplicate validators in MsgSetProposers
```

### Impact Analysis

- **Frequency**: 1 dedicated audit → 1 High design + 2 Info
- **Severity Distribution**: HIGH: 1 (acknowledged), INFO: 2
- **Affected Protocols**: dYdX v4 proposer-selection updates; any chain adopting a designated-proposer design
- **Validation Strength**: Strong (Informal Systems)

**Cross-references**: `consensus/consensus-finality-vulnerabilities.md`, `staking/validator-management-vulnerabilities.md`, `dos/chain-halt-consensus-dos.md`.
