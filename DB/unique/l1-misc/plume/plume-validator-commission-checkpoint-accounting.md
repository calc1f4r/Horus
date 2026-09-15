---
# Core Classification
protocol: plume
chain: plume
category: accounting
vulnerability_type: retroactive_commission_miscalculation

# Pattern Identity
root_cause_family: missing_checkpoint
pattern_key: missing_commission_checkpoint | reward_per_token_settlement | commission_rate_change | retroactive_reward_distortion

# Interaction Scope
interaction_scope: multi_contract
involved_contracts:
  - ValidatorFacet (requestCommissionClaim, forceSettleValidatorCommission, addValidator)
  - RewardsFacet (user reward claims)
  - ManagementFacet (setMaxAllowedValidatorCommission, removeRewardToken)
  - PlumeRewardLogic (getEffectiveCommissionRateAt, _settleCommissionForValidatorUpToNow, updateRewardPerTokenForValidator)
  - PlumeStakingStorage (validators, commission checkpoints, rewardTokens)
path_keys:
  - missing_commission_checkpoint | addValidator | PlumeRewardLogic.getEffectiveCommissionRateAt | user over-reward
  - rounding_direction_mismatch | forceSettleValidatorCommission | PlumeRewardLogic.updateRewardPerTokenForValidator | commission loss/drift
  - removed_token_gate | requestCommissionClaim | ValidatorFacet._validateIsToken | frozen commission

# Attack Vector Details
attack_type: logical_error
affected_component: validator_commission_and_reward_settlement

# Technical Primitives
primitives:
  - commission rate checkpoints per validator
  - reward-per-token cumulative indices
  - getEffectiveCommissionRateAt fallback to current commission
  - ceil vs floor division in segment settlement
  - reward token enable/disable registry (isRewardToken)
  - validator slash timestamp handling (validatorLastUpdateTimes)

# Grep / Hunt-Card Seeds
code_keywords:
  - getEffectiveCommissionRateAt
  - _settleCommissionForValidatorUpToNow
  - updateRewardPerTokenForValidator
  - requestCommissionClaim
  - forceSettleValidatorCommission
  - _validateIsToken
  - isRewardToken
  - setMaxAllowedValidatorCommission

# Impact Classification
severity: critical
impact: theft_of_unclaimed_yield_and_frozen_commission
exploitability: 0.6
financial_impact: high

# Context Tags
tags:
  - l1
  - rwa
  - staking
  - validator-commission
  - solidity
  - diamond-facets
  - checkpoint-accounting

# Version Info
language: solidity
version: "Plume Network Attackathon (immunefi-team/attackathon-plume-network), plume/src, Jul-Aug 2025"
---

## References & Source Reports

> All paths verified to exist under `reports/plume-l1_findings/`. Largest high-severity cluster in the corpus (~50 commission/reward-accounting highs + 1 critical out of 141 high+critical).

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [PL1] | reports/plume-l1_findings/53037-sc-critical-commission-changes-can-retroactively-affect-user-rewards.md | CRITICAL | Immunefi (Attackathon) | Report #53037, Plume Network Attackathon, RewardsFacet.sol |
| [PL2] | reports/plume-l1_findings/53070-sc-high-validator-commission-update-during-max-allowed-commission-change-causes-incorrect-rewa.md | HIGH | Immunefi | Report #53070, ManagementFacet.sol |
| [PL3] | reports/plume-l1_findings/53072-sc-high-ceil-vs-floor-rounding-mismatch-causes-systematic-underpayment-and-unclaimed-yield-lea.md | HIGH | Immunefi | Report #53072, PlumeRewardLogic.sol |
| [PL4] | reports/plume-l1_findings/51961-sc-high-attackers-can-deny-commission-rewards-to-validators-by-repeatedly-calling-forcesettlev.md | HIGH | Immunefi | Report #51961, PlumeRewardLogic.sol |
| [PL5] | reports/plume-l1_findings/50924-sc-high-validators-are-not-able-to-claim-their-accrued-commission-when-the-reward-token-is-rem.md | HIGH | Immunefi | Report #50924, ValidatorFacet.sol |

## Plume Validator Commission Checkpoint and Settlement Accounting Failures

### Overview

Plume's staking diamonds settle validator commission and staker rewards via per-validator commission-rate checkpoints and cumulative reward-per-token indices. The checkpoint machinery is incomplete at the boundaries: no commission checkpoint is pushed when a validator is added (retroactive commission application), settlement rounds user deductions up but validator accruals down (systematic drift), anyone can force settlement at tiny time deltas to round commission to zero, and commission on reward tokens later removed by admin becomes permanently unclaimable because `requestCommissionClaim` reverts on non-active tokens. This family produced the single critical (#53037) and the largest block of high-severity findings (~50) in the Plume attackathon corpus.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because commission-rate history is not checkpointed at every state transition (validator add, max-rate change, slash), and settlement math mixes rounding directions and token-liveness gates, so rewards computed for past intervals use present-day rates, round inconsistently, or become permanently frozen."
- Pattern key: `missing_commission_checkpoint | reward_per_token_settlement | commission_rate_change | retroactive_reward_distortion`
- Interaction scope: `multi_contract` (ValidatorFacet + RewardsFacet + ManagementFacet over shared PlumeStakingStorage)
- Primary affected component(s): `PlumeRewardLogic settlement, commission checkpoints, commission claim gating`
- Contracts / modules involved: `ValidatorFacet, RewardsFacet, ManagementFacet, PlumeRewardLogic, PlumeStakingStorage`
- Path keys: `missing_commission_checkpoint | addValidator | getEffectiveCommissionRateAt | user over-reward` · `rounding_direction_mismatch | forceSettleValidatorCommission | updateRewardPerTokenForValidator | commission loss/drift` · `removed_token_gate | requestCommissionClaim | _validateIsToken | frozen commission`
- High-signal code keywords: `getEffectiveCommissionRateAt, _settleCommissionForValidatorUpToNow, updateRewardPerTokenForValidator, requestCommissionClaim, forceSettleValidatorCommission, _validateIsToken, isRewardToken, setMaxAllowedValidatorCommission`
- Typical sink / impact: `theft of unclaimed yield (stakers over- or under-paid), validator commission permanently frozen, protocol insolvency via retroactive rate games`
- Validation strength: `strong` (critical #53037, #53070, #53072, #51961, #50924 all read with code excerpts and PoC steps)

#### Contract / Boundary Map

- Entry surface(s): `addValidator()`, `setValidatorCommission()`, `setMaxAllowedValidatorCommission()`, `removeRewardToken()`, `forceSettleValidatorCommission()`, `requestCommissionClaim()`, user reward claims in RewardsFacet
- Contract hop(s): `ManagementFacet/ValidatorFacet -> PlumeRewardLogic._settleCommissionForValidatorUpToNow -> updateRewardPerTokenForValidator -> RewardsFacet user claim reads getEffectiveCommissionRateAt`
- Trust boundary crossed: `admin-controlled facet (token removal, max commission) silently changes value of user-accrued-but-unclaimed balances across the boundary`
- Shared state or sync assumption: `validator.commission scalar and commission checkpoint array must agree for every past interval; user-side and validator-side settlement must round consistently`

#### Valid Bug Signals

- Signal 1: `addValidator()` sets only `$.validators[id].commission` and pushes no checkpoint — `getEffectiveCommissionRateAt()` returns the *current* scalar for the first interval (verified in #53037, #52667, #52955, #52500).
- Signal 2: User-side commission deduction uses ceiling division while validator-side accrual uses floor division in the same segment (#53072, #53061, #52424) — deductions exceed accruals; excess belongs to no one.
- Signal 3: `forceSettleValidatorCommission()` is permissionless and can be called with an arbitrarily small time delta, making per-segment commission round to zero forever (#51961).
- Signal 4: `requestCommissionClaim()` carries `_validateIsToken`, which reverts for tokens removed via `removeRewardToken()` — accrued commission becomes unclaimable (#50924, #52931, #53025, #52104 — at least 8 near-duplicate highs).

#### False Positive Guards

- Not this bug when: a commission checkpoint is pushed in `addValidator` at the exact add timestamp (fallback scalar never consulted for a past interval).
- Not this bug when: user deduction and validator accrual use the same rounding direction and the difference is provably bounded dust (< 1 wei per segment).
- Safe if: removed reward tokens keep a dedicated `claimCommissionForRemovedToken` path, or removal forces full settlement first.
- Requires attacker control of: nothing for the freeze paths (admin action suffices); for #53037 collusion, the validator controls its own commission and a staker times claims — both permissionless.
- Impact requires unclaimed history: if all rewards are settled atomically at every rate change (no accrual windows), retroactivity has no surface.

### Vulnerability Description

#### Root Cause

1. **Missing initial checkpoint** (#53037): the code "relies on that variable being returned if the correct commission is not found" — `fallbackComm = $.validators[validatorId].commission;` — so pre-checkpoint intervals inherit today's rate.
2. **Asymmetric settlement**: `setValidatorCommission()` settles only the validator's perspective (`_settleCommissionForValidatorUpToNow`) while user rewards keep flowing through `getEffectiveCommissionRateAt()`, letting a later rate cut retroactively raise historical staker payouts (validator–staker collusion extracts treasury yield).
3. **Rounding direction mismatch** (#53072): "per-user commission uses ceiling division while validator commission accrues with floor division, so user deductions can exceed validator accrual; the excess isn't credited to anyone."
4. **Permissionless micro-settlement** (#51961): repeated `forceSettleValidatorCommission()` with low `timeDelta` keeps every segment's commission below one wei → rounds to zero → validator never accrues.
5. **Token-liveness gate on claims** (#50924): `_validateIsToken` reverts for removed tokens, freezing already-accrued commission with no alternative exit.

#### Attack Scenario / Path Variants

**Path A: Retroactive commission collusion (critical)**
Path key: `missing_commission_checkpoint | addValidator | getEffectiveCommissionRateAt | user over-reward`
Entry surface: `addValidator()` then `setValidatorCommission()`
Contracts touched: `ValidatorFacet -> PlumeRewardLogic -> RewardsFacet`
Boundary crossed: `validator-controlled commission applied to user-accrued past intervals`
1. Validator added with `maxAllowedValidatorCommission` set; only the scalar is stored (no checkpoint).
2. Staker stakes and deliberately does not claim; time passes.
3. Validator cuts commission to the minimum (validator side is settled up to now; user side is not).
4. Staker claims: `getEffectiveCommissionRateAt()` applies the new low rate to the entire historical interval — user receives far more than entitled; treasury/other stakers fund the difference.

**Path B: Rounding-direction theft/drift**
Path key: `rounding_direction_mismatch | forceSettleValidatorCommission | updateRewardPerTokenForValidator | commission loss/drift`
Entry surface: `forceSettleValidatorCommission()` (permissionless) / natural claims
1. Per-user deductions rounded up (ceil), validator accrual rounded down (floor) in each segment.
2. Aggregate over many segments: users underpaid, unclaimed-yield dust accumulates with no owner (#53072), or micro-deltas forced by an attacker round commission to zero permanently (#51961).

**Path C: Frozen commission on removed reward token**
Path key: `removed_token_gate | requestCommissionClaim | _validateIsToken | frozen commission`
Entry surface: `removeRewardToken()` (admin) + `requestCommissionClaim()` (validator)
1. Validator accrues commission in reward token T.
2. Admin removes T from `rewardTokens` (`isRewardToken(T) = false`).
3. `requestCommissionClaim(id, T)` reverts inside `_validateIsToken`.
4. Accrued commission permanently frozen; parallel family blocks staker claims too (#52165, #50425).

#### Vulnerable Pattern Examples

**Example 1: No checkpoint at validator creation** [Approx Vulnerability : CRITICAL]
```solidity
// ❌ VULNERABLE: #53037 — only the scalar is set; history starts empty
function addValidator(/* ... */) external onlyRole(OPERATOR_ROLE) {
    // ...
    $.validators[validatorId].commission = initialCommission; // ❌ no checkpoint pushed
}
// later, for the FIRST interval nothing is found, so:
fallbackComm = $.validators[validatorId].commission; // ❌ today's rate applied retroactively
```

**Example 2: Ceil for users, floor for validators** [Approx Vulnerability : HIGH]
```solidity
// ❌ VULNERABLE: #53072 — asymmetric rounding in PlumeRewardLogic
// validator accrual:
validatorCommission = grossRewardForValidatorThisSegment * commissionRate / 1e18; // floor ❌
// user deduction (elsewhere in the same settlement):
userDeduction = (userReward * commissionRate + 1e18 - 1) / 1e18;                 // ceil ❌
// => deductions > accruals; difference accrues to no one — systematic underpayment
```

**Example 3: Permissionless micro-settlement rounds commission to zero** [Approx Vulnerability : HIGH]
```solidity
// ❌ VULNERABLE: #51961 — anyone can settle at tiny timeDelta
function forceSettleValidatorCommission(uint16 validatorId) external { // no access control ❌
    PlumeRewardLogic._settleCommissionForValidatorUpToNow($, validatorId);
    // with elapsed ≈ 1s, grossRewardForValidatorThisSegment * rate / PRECISION == 0 (floor)
    // repeated forever => validator never accrues commission
}
```

### Impact Analysis

#### Technical Impact
- Retroactive rate application corrupts historical reward-per-token accounting (both directions)
- Unclaimable-yield residue accumulates with no recovery function (multiple "no function to recover" highs: #52847, #52439, #51992)
- Permanent freeze of accrued validator commission and, in sibling paths, staker rewards (#52165)

#### Business Impact
- Direct theft of unclaimed yield from honest stakers/validators; validator–staker collusion value extraction (#53037 impacts: "Permanent freezing of funds", "Theft of unclaimed yield")
- Protocol insolvency risk flagged in #53070 ("Theft of unclaimed yield", "Protocol insolvency")

#### Affected Scenarios
- Any validator whose commission ever changes after a no-checkpoint add window
- Reward tokens rotated out by governance while commissions are outstanding
- Slash-adjacent settlement (#51479, #53018, #53039: `validatorLastUpdateTimes` advanced past slash ts) — same checkpoint-discipline family

### Secure Implementation

**Fix 1: Checkpoint at every rate-affecting transition + single rounding direction + claim path for removed tokens**
```solidity
// ✅ SECURE: push a checkpoint the moment a validator exists; never consult a live
// scalar for a past interval; settle BOTH sides atomically on change.
function addValidator(uint16 id, uint256 rate) external onlyRole(OPERATOR_ROLE) {
    $.validators[id].commission = rate;
    $.commissionCheckpoints[id].push(Checkpoint(block.timestamp, rate)); // ✅ history starts at add
}
function getEffectiveCommissionRateAt(uint16 id, uint256 t) internal view returns (uint256) {
    // ✅ latest checkpoint with time <= t; REQUIRE existence — no scalar fallback for past intervals
    return _latestCheckpointAtOrBefore($.commissionCheckpoints[id], t); // reverts if none
}
function setValidatorCommission(uint16 id, uint256 newRate) external {
    PlumeRewardLogic._settleCommissionForValidatorUpToNow($, id); // settle validator side...
    RewardsFacetLib._settleAllUserRewardsUpToNow($, id);          // ✅ ...AND user side, same instant
    $.commissionCheckpoints[id].push(Checkpoint(block.timestamp, newRate));
}
// commission claim must not depend on token liveness:
function requestCommissionClaim(uint16 id, address token) external { // ✅ no _validateIsToken gate;
    // settle + payout whatever was accrued while token was active   // removed tokens stay claimable
}
```

### Detection Patterns

#### High-Signal Grep Seeds
```
getEffectiveCommissionRateAt
_settleCommissionForValidatorUpToNow
updateRewardPerTokenForValidator
requestCommissionClaim
forceSettleValidatorCommission
_validateIsToken
isRewardToken
setMaxAllowedValidatorCommission
validatorLastUpdateTimes
```

#### Code Patterns to Look For
```
- Scalar `commission` read as fallback when checkpoint lookup misses (retroactivity primitive)
- One-sided settlement on rate change (validator settled, users not, or vice versa)
- `+ PRECISION - 1) / PRECISION` in one settlement path and plain `/ PRECISION` in its counterpart
- Permissionless settle functions callable with attacker-chosen timestamps/deltas
- Token-liveness modifier (_validateIsToken / isRewardToken) guarding claim of ALREADY-accrued balances
```

#### Audit Checklist
- [ ] Does `addValidator` (and every commission-rate mutation) push a checkpoint at the exact effective timestamp?
- [ ] On any rate change, are BOTH validator and user perspectives settled atomically before the new rate applies?
- [ ] Do user deduction and validator accrual round in the same direction (or is the delta provably redistributed)?
- [ ] Can commission/rewards accrued in a since-removed reward token still be claimed via a dedicated path?
- [ ] Is `forceSettle*` rate-limited or access-controlled so micro-deltas cannot zero out accrual?

### Real-World Examples

#### Known Exploits
- None public at time of writing; findings from a paid attackathon (triaged by Immunefi).

#### Related CVEs/Reports
- Immunefi #53037 (CRITICAL, retroactive commission), #53070, #53072, #51961, #50924 — Plume Network Attackathon 2025
- Near-duplicate family members: #52424, #52500, #53061, #52955, #52667, #52931, #53025, #52104, #52711, #51946, #52944

### Prevention Guidelines

#### Development Best Practices
1. Treat every rate-bearing storage write as a checkpoint event; forbid scalar fallbacks for past timestamps.
2. Settle both sides of a split (deductor and accrual account) in the same transaction as any rate change.
3. Never gate exit/claim of accrued value on current registry liveness (token active, validator active).

#### Testing Requirements
- Unit: checkpoint lookup at t < first checkpoint, t == change block, t in slashed interval
- Fuzz: ceil-vs-floor divergence over random segment splits; assert bounded dust
- Integration: addValidator → stake → change commission → claim; removeRewardToken with outstanding commission

### Keywords for Search

`plume`, `validator commission`, `commission checkpoint`, `reward per token`, `retroactive rewards`, `getEffectiveCommissionRateAt`, `forceSettleValidatorCommission`, `requestCommissionClaim`, `ceil floor rounding`, `rounding direction mismatch`, `removed reward token`, `frozen commission`, `staking diamond`, `PlumeStakingStorage`, `PlumeRewardLogic`, `theft of unclaimed yield`, `validator collusion`, `checkpoint accounting`, `attackathon`, `immunefi`

### Related Vulnerabilities

- DB/unique/l1-misc/plume/plume-arctoken-batched-yield-distribution.md (same corpus: snapshot-less distribution family)
- DB/unique/l1-misc/stacks-signer-validation.md (checkpoint/nonce discipline on a different L1)
