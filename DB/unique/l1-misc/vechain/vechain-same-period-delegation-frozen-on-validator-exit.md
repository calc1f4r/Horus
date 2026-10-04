---
# Core Classification
protocol: vechain
chain: vechain
category: state_accounting
vulnerability_type: underflow_fund_freeze

# Pattern Identity
root_cause_family: incorrect_state_transition
pattern_key: unchecked_pending_subtraction | staker-aggregation | delegation-added-in-validator-exit-period | uint64-underflow-revert

# Interaction Scope
interaction_scope: multi_contract
involved_contracts:
  - builtin/staker/staker.go (AddDelegation / WithdrawDelegation)
  - builtin/staker/validation/service.go (SignalExit)
  - builtin/staker/aggregation/aggregation.go (exit housekeeping)
  - builtin/staker/delegation/delegation.go (Started)
path_keys:
  - unchecked_pending_subtraction | AddDelegation->SignalExit->housekeeping->WithdrawDelegation | staker->aggregation
  - unchecked_pending_subtraction | WithdrawDelegation-on-unstarted-delegation | staker->aggregation

# Attack Vector Details
attack_type: logical_error
affected_component: delegation withdrawal path (staking exit edge case)

# Technical Primitives
primitives:
  - period_iteration_accounting
  - delegation_lifecycle
  - aggregation_pending_reset_on_exit
  - uint64_arithmetic
  - consensus_houskeeping_hook

# Grep / Hunt-Card Seeds
code_keywords:
  - AddDelegation
  - WithdrawDelegation
  - SubPendingVet
  - SignalExit
  - CompletedPeriods
  - FirstIteration
  - aggregation.Pending
  - RemoveQueued
  - CurrentIteration
  - StatusQueued

# Impact Classification
severity: critical
impact: permanent_freezing_of_funds
financial_impact: high

# Context Tags
tags:
  - l1
  - pos
  - staking
  - delegation
  - edge_case
  - hardfork_required

# Version Info
language: go   # thor native builtin (Go); solidity-dialect VM layer invoked via builtin ABI
version: hayabusa-release
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [CRIT-1] | reports/vechain-l1_findings/55632-bc-critical-delegation-submitted-in-the-same-period-before-a-validator-exit-will-be-permanentl.md | CRITICAL | immunefi (@Haxatron) | #55632 |

## Delegation Submitted in the Same Period as a Validator Exit Is Permanently Frozen

**Same-period delegation + validator exit → wrong `Started()` branch → `SubPendingVet` underflow on zeroed `aggregation.Pending` → permanent freeze (hardfork required)**

### Overview

Any delegation added in the same staking period in which its validator signals exit is never "started" from the protocol's perspective; the withdrawal path then subtracts from an `aggregation.Pending` that exit housekeeping has already reset to zero, underflowing and reverting forever. The delegator's VET is permanently frozen.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because `WithdrawDelegation` selects the pending-subtraction branch based on `Delegation.Started()`, but a delegation whose `FirstIteration` exceeds the validator's frozen `CurrentIteration` (clamped by `CompletedPeriods` at exit) is classified as unstarted even though exit housekeeping already zeroed `aggregation.Pending` — so `SubPendingVet` underflows."
- Pattern key: `unchecked_pending_subtraction | staker-aggregation | delegation-added-in-validator-exit-period | uint64-underflow-revert`
- Interaction scope: `multi_contract` (staker ↔ validation service ↔ aggregation housekeeping)
- Primary affected component(s): `WithdrawDelegation` unstake/withdraw path, aggregation pending accounting
- Contracts / modules involved: `builtin/staker/staker.go`, `builtin/staker/validation/service.go`, `builtin/staker/aggregation/aggregation.go`, `builtin/staker/delegation/delegation.go`
- Path keys: `unchecked_pending_subtraction | AddDelegation->SignalExit->housekeeping->WithdrawDelegation | staker->aggregation`
- High-signal code keywords: `AddDelegation`, `WithdrawDelegation`, `SubPendingVet`, `SignalExit`, `CompletedPeriods`, `FirstIteration`, `aggregation.Pending`, `RemoveQueued`
- Typical sink / impact: `permanent fund freeze / DoS (fix requires hardfork)`
- Validation strength: `strong` (working e2e PoC supplied by reporter)

#### Contract / Boundary Map

- Entry surface(s): `AddDelegation` (delegator), `SignalExit` (validator endorser), `WithdrawDelegation` (delegator)
- Contract hop(s): `staker.AddDelegation -> validation.Service.SignalExit (freezes CompletedPeriods) -> aggregation.exit() housekeeping (Pending=0) -> staker.WithdrawDelegation -> aggregationService.SubPendingVet (revert)`
- Trust boundary crossed: consensus-layer housekeeping mutating builtin-contract aggregate state that user-facing withdrawal logic assumes is still consistent
- Shared state or sync assumption: `aggregation.Pending` must still contain a delegation's queued stake whenever `Delegation.Started() == false`; exit processing breaks this invariant for same-period delegations

#### Valid Bug Signals

- Signal 1: delegation's `FirstIteration == validatorExitPeriod + 1` (added in the same period the validator signaled exit)
- Signal 2: `WithdrawDelegation` hits the `!started` branch and calls `SubPendingVet` after `aggregation.exit()` has already run (Pending reset to `&stakes.WeightedStake{}`)
- Signal 3: transaction reverts deterministically on every withdraw attempt — funds unreachable without a hardfork/state override

#### False Positive Guards

- Not this bug when: the delegation was added at least one full period *before* the validator's exit signal (the reporter's own PoC passes when a one-period wait is uncommented)
- Not this bug when: the validator is merely QUEUED/UNKNOWN at delegation time and never exits in that same period
- Safe if: `SubPendingVet` performs a zero-check / clamping subtraction, or `WithdrawDelegation` re-checks aggregation state post-exit before choosing the branch
- Requires attacker control of: nothing adversarial — any ordinary delegator + ordinary validator exit timing triggers it

### Vulnerability Description

#### Root Cause

`AddDelegation` records `FirstIteration = CurrentIteration + 1`. `SignalExit` in the same period pins `validation.CompletedPeriods = current`, which permanently clamps `CurrentIteration` for that validator. At the start of the next period, `aggregation.exit()` resets `Pending` (and `Locked`) to zero. When the delegator withdraws, `Delegation.Started()` returns `false` (current staking period 5 < `FirstIteration` 6), so `WithdrawDelegation` takes the queued-stake branch and calls `aggregationService.SubPendingVet` against an already-zeroed aggregate → underflow → revert.

#### Attack Scenario / Path Variants

**Path A: Same-period delegation then exit (primary freeze)**
Path key: `unchecked_pending_subtraction | AddDelegation->SignalExit->housekeeping->WithdrawDelegation | staker->aggregation`
1. Period 5: delegator calls `AddDelegation` → `FirstIteration = 6`.
2. Period 5: validator calls `SignalExit` → `CompletedPeriods = 5`.
3. Period 6 start: housekeeping runs `aggregation.exit()` → `Pending = 0`.
4. Period 6+: delegator calls `WithdrawDelegation` → `Started()==false` → `SubPendingVet` underflow → permanent revert. Stake frozen.

**Path B: Withdraw attempt timing variants**
Path key: `unchecked_pending_subtraction | WithdrawDelegation-on-unstarted-delegation | staker->aggregation`
1. Same state as Path A; any repeated withdraw/redelegate in later periods reverts identically.
2. No alternative release path exists (`RemoveQueued` also assumes the pending aggregate is intact).

#### Vulnerable Pattern Examples

**Example 1: WithdrawDelegation pending branch (thor release/hayabusa)** [Approx Vulnerability : CRITICAL]
```go
// ❌ VULNERABLE: branch chosen on Started() while aggregation.Pending was zeroed by exit housekeeping
func (s *Staker) WithdrawDelegation(delegationID *big.Int, currentBlock uint32) (uint64, error) {
    ...
    if !started {
        weightedStake := stakes.NewWeightedStakeWithMultiplier(withdrawableStake, del.Multiplier)
        if err = s.aggregationService.SubPendingVet(del.Validation, weightedStake); err != nil {
            return 0, err // underflow: Pending already reset to 0 by aggregation.exit()
        }
        if err = s.globalStatsService.RemoveQueued(withdrawableStake); err != nil {
            return 0, err
        }
    } else { ... }
}
```

**Example 2: Started() clamped by exit-frozen CompletedPeriods** [Approx Vulnerability : CRITICAL]
```go
// ❌ VULNERABLE: CurrentIteration is derived from a validation frozen at exit, so a
// next-period delegation can never become "started"
func (d *Delegation) Started(val *validation.Validation, currentBlock uint32) (bool, error) {
    if val.Status == validation.StatusQueued || val.Status == validation.StatusUnknown {
        return false, nil
    }
    currentStakingPeriod, err := val.CurrentIteration(currentBlock) // clamped to CompletedPeriods==5
    if err != nil { return false, err }
    return currentStakingPeriod >= d.FirstIteration, nil // 5 >= 6 is false forever
}
```

**Example 3: Exit housekeeping zeroes the shared aggregate** [Approx Vulnerability : CRITICAL]
```go
// ❌ VULNERABLE: aggregation reset orphans every same-period pending delegation
func (a *Aggregation) exit() *globalstats.Exit {
    exit := globalstats.Exit{ ExitedTVL: a.Locked.Clone(), QueuedDecrease: a.Pending.VET }
    a.Exiting = &stakes.WeightedStake{}
    a.Locked  = &stakes.WeightedStake{}
    a.Pending = &stakes.WeightedStake{} // Pending zeroed; later SubPendingVet underflows
    return &exit
}
```

### Impact Analysis

#### Technical Impact
- Deterministic underflow revert in `WithdrawDelegation` for every affected delegation
- Aggregation/global-stats state desynchronized from per-delegation records
- No in-protocol remediation; recovery requires a hardfork or manual state surgery

#### Business Impact
- Permanent loss of user VET staked in the window; critical reputational damage to the staking launch

#### Affected Scenarios
- High-traffic exit windows where delegations and validator exits race within one period
- Compounds with any other exit-path accounting bug (see double-decrement family) to widen the freeze set

### Secure Implementation

**Fix 1: Reject same-period delegations to exiting validators / clamp-then-subtract**
```go
// ✅ SECURE: two-layer defense
// (a) In AddDelegation: refuse or defer delegation when validator has signaled exit in this period
if validation.Exiting != nil || validation.CompletedPeriods >= current {
    return nil, ErrDelegationDuringExit // or queue with FirstIteration validated against post-exit state
}
// (b) In WithdrawDelegation / SubPendingVet: saturating subtraction with explicit error taxonomy
func (s *Service) SubPendingVet(v thor.Address, w *stakes.WeightedStake) error {
    agg := s.load(v)
    if agg.Pending.Cmp(w) < 0 {
        return ErrPendingUnderflowNoCharge // revert WITHOUT mutating state; surface distinct error
    }
    agg.Pending.Sub(w)
    return nil
}
```

**Fix 2: Reconcile per-delegation queues with aggregates at exit time**
```go
// ✅ SECURE: during aggregation.exit(), also settle/refund every delegation whose
// FirstIteration > exit period so no orphaned pending entries survive the reset
for _, d := range pendingDelegationsWithFirstIterationAfter(exitPeriod) {
    settleAsUnstarted(d) // removes from per-delegation queue AND global queued stats atomically
}
```

### Detection Patterns

#### Contract / Call Graph Signals
```
- Aggregation/global state reset on lifecycle exit while per-entity records referencing it persist
- Branch selection predicate (Started) computed from a *different* state source than the mutated aggregate
- Saturating-vs-reverting subtraction semantics unverified across a housekeeping boundary
```

#### High-Signal Grep Seeds
```
- SubPendingVet
- AddPendingVet
- aggregation.Pending
- SignalExit
- CompletedPeriods
- FirstIteration
- WithdrawDelegation
- RemoveQueued
```

#### Code Patterns to Look For
```
- Pattern 1: lifecycle exit handlers that zero shared aggregates without sweeping dependent queues
- Pattern 2: "started/active" predicates derived from frozen counters (CompletedPeriods clamps)
- Pattern 3: uint64 stake arithmetic with no underflow guard on cross-module state
```

#### Audit Checklist
- [ ] Fuzz delegation-add vs exit-signal ordering within the same period (all interleavings)
- [ ] Verify every subtraction site has a matching, still-consistent aggregate after housekeeping
- [ ] Confirm a reclaim path exists for each delegation state after validator exit processing

### Real-World Examples

#### Known Exploits
- **VeChain thor (hayabusa release)** — Same-period delegation permanently frozen on validator exit — Oct 2025 — no exploit (contest finding)
  - Link: https://reports.immunefi.com/vechain-hayabusa-upgrade-or-attackathon (report #55632)
  - Root cause: `SubPendingVet` underflow after `aggregation.exit()` reset

#### Related CVEs/Reports
- Same staker exit-window family: #59564, #59723, #59727, #59742, #59756 (Stargate-side exit freezes)

### Prevention Guidelines

#### Development Best Practices
1. Model lifecycle edges (add/exit same period) as explicit state-machine transitions with tests
2. Never let a reset of shared aggregate state orphan per-entity records

#### Testing Requirements
- e2e tests: every (delegation action × validator lifecycle event) pair within a single period
- Fuzzing targets: iteration arithmetic around `CompletedPeriods` clamps

### Keywords for Search

`vechain`, `hayabusa`, `staker`, `delegation`, `validator exit`, `SignalExit`, `WithdrawDelegation`, `SubPendingVet`, `aggregation pending`, `underflow`, `fund freeze`, `FirstIteration`, `CompletedPeriods`, `staking period`, `housekeeping`, `hardfork`, `PoS transition`

### Related Vulnerabilities

- vechain-double-effective-stake-decrement-unstake-freeze.md (Stargate-side exit freeze family)
- vechain-post-exit-delegation-reward-drain-off-by-one.md (same exit window, reward-side sink)
