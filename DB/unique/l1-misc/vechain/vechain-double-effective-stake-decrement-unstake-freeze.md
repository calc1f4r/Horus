---
# Core Classification
protocol: vechain-stargate
chain: vechain
category: state_accounting
vulnerability_type: double_decrement_fund_freeze

# Pattern Identity
root_cause_family: duplicate_state_mutation
pattern_key: duplicated_effective_stake_decrement | unstake-vs-requestDelegationExit | validator-exit-transition | checkpoint-underflow-panic

# Interaction Scope
interaction_scope: multi_contract
involved_contracts:
  - Stargate.sol (requestDelegationExit L~568 / unstake L~266-283)
  - ProtocolStaker (validator status EXITED/PENDING source)
path_keys:
  - duplicated_effective_stake_decrement | requestDelegationExit-then-unstake | Stargate->ProtocolStaker
  - duplicated_effective_stake_decrement | unstake-EXITED-PENDING-branch | Stargate-internal

# Attack Vector Details
attack_type: logical_error
affected_component: effective-stake checkpoint accounting across delegation/validator exit flows

# Technical Primitives
primitives:
  - effective_stake_checkpoints
  - _updatePeriodEffectiveStake(bool add/remove)
  - delegation_status_state_machine
  - validator_status_reflect (ACTIVE/EXITED/PENDING)
  - solidity panic 0x11 arithmetic underflow

# Grep / Hunt-Card Seeds
code_keywords:
  - _updatePeriodEffectiveStake
  - requestDelegationExit
  - unstake
  - delegatorsEffectiveStake
  - DelegationStatus
  - VALIDATOR_STATUS_EXITED
  - updatePeriodEffectiveStake
  - getValidation
  - endPeriod
  - redelegate

# Impact Classification
severity: high
impact: permanent_freezing_of_funds
financial_impact: high

# Context Tags
tags:
  - defi
  - staking
  - delegation
  - dos
  - state_machine
  - l1

# Version Info
language: solidity
version: hayabusa-stargate-release
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [HIGH-1] | reports/vechain-l1_findings/60311-sc-high-double-effective-stake-decrement-freezes-unstake-permanently-after-validator-exit.md | HIGH | immunefi (@TianYu4n) | #60311 |
| [HIGH-2] | reports/vechain-l1_findings/59802-sc-high-double-subtraction-of-validator-effective-stake-will-permanently-lock-other-delegators.md | HIGH | immunefi | #59802 |
| [HIGH-3] | reports/vechain-l1_findings/60419-sc-high-double-decrease-of-effective-stake-leads-to-dos-and-permanent-loss-of-funds.md | HIGH | immunefi | #60419 |
| [HIGH-4] | reports/vechain-l1_findings/59564-sc-high-double-calling-updateperiodeffectivestake-during-the-exit-flow-makes-unstake-revert-tr.md | HIGH | immunefi | #59564 |
| [HIGH-5] | reports/vechain-l1_findings/59904-sc-high-it-s-possible-to-decrease-twice-delegator-stake-in-certain-conditions.md | HIGH | immunefi | #59904 |

## Double Effective-Stake Decrement on Validator Exit Permanently Freezes Unstake

**`requestDelegationExit` decrements effective stake once; later `unstake` in the EXITED/PENDING branch decrements the same period again → underflow (panic 0x11) before any transfer → funds permanently locked**

### Overview

Two separate code paths subtract the same delegator's effective stake for the same period: the exit request and the unstake fallback branch that fires when the validator itself has exited. The second subtraction hits a zero checkpoint and panics with arithmetic underflow before any VET moves, so every `unstake`/`redelegate` attempt reverts forever — staked VET is permanently frozen.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because `_updatePeriodEffectiveStake(..., false)` is applied in `requestDelegationExit` and again in `unstake`'s `currentValidatorStatus == EXITED || status == PENDING` branch without an idempotency guard, so the checkpoint is decremented twice for the same delegation period."
- Pattern key: `duplicated_effective_stake_decrement | unstake-vs-requestDelegationExit | validator-exit-transition | checkpoint-underflow-panic`
- Interaction scope: `multi_contract` (Stargate stake accounting ↔ ProtocolStaker status feed)
- Primary affected component(s): `unstake`, `requestDelegationExit`, `_updatePeriodEffectiveStake`
- Contracts / modules involved: `Stargate.sol`, `ProtocolStaker`
- Path keys: `duplicated_effective_stake_decrement | requestDelegationExit-then-unstake | Stargate->ProtocolStaker`
- High-signal code keywords: `_updatePeriodEffectiveStake`, `requestDelegationExit`, `unstake`, `delegatorsEffectiveStake`, `DelegationStatus`, `VALIDATOR_STATUS_EXITED`
- Typical sink / impact: `permanent fund freeze via deterministic revert (DoS)`
- Validation strength: `strong` (reverting-unstake PoC reproduced 3× consecutively)

#### Contract / Boundary Map

- Entry surface(s): `requestDelegationExit(tokenId)` (user), `unstake(tokenId)` (user), `redelegate(...)`
- Contract hop(s): `Stargate.requestDelegationExit -> _updatePeriodEffectiveStake(false) [1st]; Stargate.unstake -> getValidation(validator).status==EXITED -> _updatePeriodEffectiveStake(false) [2nd] -> panic 0x11`
- Trust boundary crossed: stake-ledger mutation keyed on *external* validator lifecycle status crossing into user withdraw path
- Shared state or sync assumption: each (validator, period) effective-stake checkpoint must be decremented at most once per delegation

#### Valid Bug Signals

- Signal 1: a delegation whose exit was requested (first decrement recorded) and whose validator later reports EXITED/PENDING status
- Signal 2: `unstake` reverts with panic 0x11 (arithmetic underflow) inside `_updatePeriodEffectiveStake` before any VET transfer
- Signal 3: repeated unstake attempts revert identically — no self-healing state transition

#### False Positive Guards

- Not this bug when: the delegator never called `requestDelegationExit` (single decrement path only)
- Not this bug when: the validator remains ACTIVE through unstake (branch not taken)
- Safe if: `_updatePeriodEffectiveStake` is idempotent per (tokenId, period) or the unstake branch checks delegation status EXITED-already-decremented and skips
- Not fund *theft*: stakes are frozen, not stolen — impact class is freeze/DoS, matching "Permanent freezing of funds"

### Vulnerability Description

#### Root Cause

Effective-stake checkpoints (`delegatorsEffectiveStake[validator][period]`) are decremented in two independent flows that can both execute for one delegation: (1) `requestDelegationExit` applies the decrement for the next period at L~568; (2) when the validator's status later reads EXITED (or the delegation is PENDING), `unstake` L~266-283 unconditionally applies the decrement again. The second call subtracts from an already-zero checkpoint → Solidity panic 0x11 → revert before funds move.

#### Attack Scenario / Path Variants

**Path A: Delegator-exit then validator-exit (primary freeze)**
Path key: `duplicated_effective_stake_decrement | requestDelegationExit-then-unstake | Stargate->ProtocolStaker`
1. User stakes → NFT → delegates to validator; delegation becomes ACTIVE.
2. `requestDelegationExit(tokenId)` — first `_updatePeriodEffectiveStake(false)`.
3. Validator transitions to EXITED (its own exit flow).
4. User calls `unstake(tokenId)` — EXITED/PENDING branch fires second decrement → underflow panic → revert. Stake locked permanently; `redelegate` equally bricked.

**Path B: Validator-exit first, delegator unwind second**
Path key: `duplicated_effective_stake_decrement | unstake-EXITED-PENDING-branch | Stargate-internal`
1. Validator exits while delegations are ACTIVE (validator-side housekeeping may already adjust aggregates).
2. Delegator's later `unstake`/exit flow applies its own decrement for the same periods.
3. Same double-subtraction sink: underflow revert, frozen VET.

#### Vulnerable Pattern Examples

**Example 1: Unstake's unconditional second decrement (Stargate.sol ~L266-283)** [Approx Vulnerability : HIGH]
```solidity
// ❌ VULNERABLE: no check that requestDelegationExit already decremented this period
function unstake(uint256 _tokenId) external {
    (, , , , uint256 currentValidatorStatus, ) = $.protocolStakerContract.getValidation(_validator);
    if (
        currentValidatorStatus == VALIDATOR_STATUS_EXITED ||
        $.delegations[_tokenId].status == DelegationStatus.PENDING
    ) {
        _updatePeriodEffectiveStake(_validator, _tokenId, endPeriod, false); // 2nd decrement → panic 0x11
    }
    ...
}
```

**Example 2: First decrement in the exit request (~L568)**
```solidity
// ❌ VULNERABLE: decrement recorded here is not flagged as consumed
function requestDelegationExit(uint256 _tokenId) external {
    ...
    _updatePeriodEffectiveStake(_validator, _tokenId, completedPeriods + 1, false); // 1st decrement
    $.delegations[_tokenId].endPeriod = completedPeriods;
    $.delegations[_tokenId].status = DelegationStatus.EXITING;
}
```

**Example 3: Non-idempotent checkpoint helper**
```solidity
// ❌ VULNERABLE: plain subtraction, no per-(token,period) once-guard
function _updatePeriodEffectiveStake(address v, uint256 id, uint32 period, bool add) internal {
    uint256 cur = $.delegatorsEffectiveStake[v][period];
    $.delegatorsEffectiveStake[v][period] = add ? cur + stakeOf(id) : cur - stakeOf(id); // underflows
}
```

### Impact Analysis

#### Technical Impact
- Deterministic panic-0x11 reverts on every withdraw/redelegate for affected delegations
- Effective-stake history corrupted (undercounted), distorting reward shares of remaining delegators
- Freeze is state-permanent: no user-side sequence recovers the funds

#### Business Impact
- Frozen user VET, support burden, trust damage; mass freezes possible when a large validator exits

#### Affected Scenarios
- Any validator exit touching delegations that already requested exit (default unwind ordering)
- Compounds with #60210/#60334/#60372 variants (underflow in unstake after validator exit) and the native-side aggregation freeze (#55632)

### Secure Implementation

**Fix 1: Status-aware decrement gating (reporter's suggested fix)**
```solidity
// ✅ SECURE: skip the decrement already applied by requestDelegationExit
bool shouldDecrement =
    ($.delegations[_tokenId].status == DelegationStatus.PENDING) ||
    (currentValidatorStatus == VALIDATOR_STATUS_EXITED &&
     $.delegations[_tokenId].status == DelegationStatus.NONE);
if (shouldDecrement) {
    _updatePeriodEffectiveStake(_validator, _tokenId, endPeriod, false);
} // status == EXITED has already been decreased in requestDelegationExit — skip
```

**Fix 2: Idempotent checkpoint mutation**
```solidity
// ✅ SECURE: once-only decrement per (tokenId, period)
if (!$.stakeDecremented[_tokenId][period]) {
    $.delegatorsEffectiveStake[_validator][period] -= stakeOf(_tokenId);
    $.stakeDecremented[_tokenId][period] = true;
}
```

### Detection Patterns

#### Contract / Call Graph Signals
```
- Same mutating helper (add/remove stake) reachable from ≥2 lifecycle flows without a shared once-flag
- Withdraw-path branching on external protocol status (validator EXITED) duplicating exit-path mutations
- Underflow-prone uint subtraction on checkpoint maps
```

#### High-Signal Grep Seeds
```
- _updatePeriodEffectiveStake
- updatePeriodEffectiveStake
- delegatorsEffectiveStake
- requestDelegationExit
- VALIDATOR_STATUS_EXITED
- DelegationStatus.PENDING
- redelegate
```

#### Code Patterns to Look For
```
- Pattern 1: `_update*(..., false)` appearing in both an exit-request function and an unstake function
- Pattern 2: state-machine status values (NONE/PENDING/ACTIVE/EXITING/EXITED) used as decrement triggers without exhaustive coverage
- Pattern 3: panic 0x11 in test teardown after forced validator status flips
```

#### Audit Checklist
- [ ] For every lifecycle transition pair (delegator exit × validator exit, both orders), trace each checkpoint mutation exactly once
- [ ] Assert idempotency: calling unstake twice changes state identically to once
- [ ] Verify no code path decrements a period already settled by exit housekeeping

### Real-World Examples

#### Known Exploits
- **VeChain Stargate (hayabusa audit comp)** — double decrement froze unstake after validator exit — Nov 2025 — contest finding
  - Link: https://reports.immunefi.com/vechain-or-stargate-hayabusa (reports #60311, #59802, #60419, #59564, #59904)
  - Root cause: duplicate `_updatePeriodEffectiveStake(false)` across exit + unstake flows

#### Related CVEs/Reports
- Variant family (30+ highs): #59386, #59723, #59727, #59730, #59742, #59751, #59756, #59809, #59850, #60004, #60027, #60049, #60080, #60151, #60210, #60282, #60298, #60334, #60372, #60373, #60429, #60470, #60506, #60533, #60548, #60553, #60557, #60575, #60586, #60592

### Prevention Guidelines

#### Development Best Practices
1. Centralize effective-stake mutations in one function guarded by a per-entity once-flag
2. Model validator status as an input to the delegation state machine, not as scattered branch conditions

#### Testing Requirements
- Integration: full matrix stake → delegate → (delegator exit | validator exit | both, both orders) → unstake
- Fuzz: invariant `Σ decrements == 1` per (delegation, period) across random lifecycle interleavings

### Keywords for Search

`vechain`, `stargate`, `effective stake`, `double decrement`, `double subtraction`, `underflow`, `panic 0x11`, `unstake revert`, `fund freeze`, `validator exit`, `requestDelegationExit`, `_updatePeriodEffectiveStake`, `delegatorsEffectiveStake`, `checkpoint`, `delegation status`, `redelegate bricked`, `DoS`, `state machine`, `exit flow`, `staking`

### Related Vulnerabilities

- vechain-same-period-delegation-frozen-on-validator-exit.md (native-side aggregation underflow freeze)
- vechain-post-exit-delegation-reward-drain-off-by-one.md (reward-side ghost stake after exit)
