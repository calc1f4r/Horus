---
# Core Classification
protocol: vechain-stargate
chain: vechain
category: state_accounting
vulnerability_type: reward_overclaim_after_exit

# Pattern Identity
root_cause_family: boundary_condition_error
pattern_key: strict_inequality_claim_window | claimable-delegation-periods | delegation-exit-claimed-through-end | vtho-reward-drain

# Interaction Scope
interaction_scope: multi_contract
involved_contracts:
  - Stargate.sol (_claimableDelegationPeriods / claimRewards)
  - ProtocolStaker (validator period source, delegatorsEffectiveStake checkpoints)
path_keys:
  - strict_inequality_claim_window | claimRewards-after-exit | Stargate->ProtocolStaker
  - strict_inequality_claim_window | claimableDelegationPeriods-fallback-branch | Stargate-internal

# Attack Vector Details
attack_type: logical_error
affected_component: delegation reward claim-window computation

# Technical Primitives
primitives:
  - period_range_arithmetic
  - lastClaimedPeriod_cursor
  - endPeriod_sentinel (type(uint32).max)
  - effective_stake_checkpoints
  - strict_vs_inclusive_boundary

# Grep / Hunt-Card Seeds
code_keywords:
  - _claimableDelegationPeriods
  - claimableDelegationPeriods
  - claimRewards
  - lastClaimedPeriod
  - endPeriod
  - requestDelegationExit
  - completedPeriods
  - currentValidatorPeriod
  - delegatorsEffectiveStake
  - _claimableRewardsForPeriod

# Impact Classification
severity: high
impact: theft_of_unclaimed_yield
financial_impact: high

# Context Tags
tags:
  - defi
  - staking
  - delegation
  - rewards
  - off_by_one
  - l1

# Version Info
language: solidity
version: hayabusa-stargate-release
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [HIGH-1] | reports/vechain-l1_findings/59563-sc-high-exited-delegators-can-claim-rewards-indefinitely-after-exit.md | HIGH | immunefi (@dray) | #59563 |
| [HIGH-2] | reports/vechain-l1_findings/59358-sc-high-off-by-one-error-in-reward-claim-logic-allows-delegators-to-steal-vtho-for-periods-aft.md | HIGH | immunefi | #59358 |
| [HIGH-3] | reports/vechain-l1_findings/59733-sc-high-post-exit-delegations-can-drain-future-rewards.md | HIGH | immunefi | #59733 |
| [HIGH-4] | reports/vechain-l1_findings/60150-sc-high-off-by-one-in-claim-window-lets-exited-delegations-harvest-post-exit-rewards.md | HIGH | immunefi | #60150 |
| [HIGH-5] | reports/vechain-l1_findings/60019-sc-high-off-by-one-in-stargate-sol-claimabledelegationperiods-lets-exited-nfts-siphon-validato.md | HIGH | immunefi | #60019 |

## Exited Delegators Drain Future VTHO Rewards via Off-By-One Claim Window

**Strict `endPeriod > nextClaimablePeriod` guard fails after claiming through end period → fallback branch returns post-exit periods → indefinite VTHO drain from active delegators**

### Overview

`Stargate._claimableDelegationPeriods` bounds the claim window for an EXITED delegation with a strict inequality. Once a delegator has claimed through `endPeriod`, the guard never triggers again and the fallback branch returns `(endPeriod + 1, completedPeriods)` — periods entirely after exit — paying the exited delegator a share of every future period's rewards indefinitely.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because the exit branch uses `endPeriod > nextClaimablePeriod` (strict) instead of `>=`/terminal clamping, and no terminal status flag stops `lastClaimedPeriod` from advancing past `endPeriod`, so after the first post-exit claim the fallback branch treats the exited delegation as perpetually active."
- Pattern key: `strict_inequality_claim_window | claimable-delegation-periods | delegation-exit-claimed-through-end | vtho-reward-drain`
- Interaction scope: `multi_contract` (Stargate reward accounting ↔ ProtocolStaker validator periods)
- Primary affected component(s): `_claimableDelegationPeriods`, `claimRewards`
- Contracts / modules involved: `Stargate.sol`, `ProtocolStaker`
- Path keys: `strict_inequality_claim_window | claimRewards-after-exit | Stargate->ProtocolStaker`
- High-signal code keywords: `_claimableDelegationPeriods`, `claimableDelegationPeriods`, `claimRewards`, `lastClaimedPeriod`, `endPeriod`, `requestDelegationExit`, `completedPeriods`, `delegatorsEffectiveStake`
- Typical sink / impact: `theft of unclaimed yield from active delegators`
- Validation strength: `strong` (Hardhat PoC proves post-exit claims pay out)

#### Contract / Boundary Map

- Entry surface(s): `claimRewards(tokenId)` (public, permissionless), `claimableDelegationPeriods(tokenId)` (view, reveals window)
- Contract hop(s): `Stargate.claimRewards -> _claimableDelegationPeriods (bad window) -> _claimableRewardsForPeriod × N -> delegatorsEffectiveStake[validator] (stale stake) -> VTHO transfer`
- Trust boundary crossed: reward distribution trusting delegation-lifecycle state that no longer matches effective-stake checkpoints
- Shared state or sync assumption: `delegatorsEffectiveStake` history must reflect only *active* delegations; exit without unstake/redelegate never subtracts it

#### Valid Bug Signals

- Signal 1: delegation status EXITED (`endPeriod != type(uint32).max && endPeriod < currentValidatorPeriod`) while `claimableRewards(tokenId)` still grows period over period
- Signal 2: second `claimRewards` after claiming through `endPeriod` succeeds and returns periods `> endPeriod`
- Signal 3: validator keeps producing blocks (`completedPeriods` advances) — each period mints a fresh claimable slice for the exited NFT

#### False Positive Guards

- Not this bug when: the delegator fully unstakes or re-delegates after exit — `_updatePeriodEffectiveStake(..., false)` then removes the stale stake and future claims compute to zero
- Not this bug when: `MAX_CLAIMABLE_PERIODS` caps a single claim's range — the cap limits burst size, not the ability to keep claiming forever
- Safe if: window computation returns `min(nextClaimablePeriod, endPeriod)` terminal for EXITED delegations, or claim path reverts once `lastClaimedPeriod >= endPeriod`
- Requires attacker control of: only their own NFT + exit timing; no governance/oracle access needed

### Vulnerability Description

#### Root Cause

The claim-window function tries three branches. For an exited delegation whose cursor is still behind `endPeriod`, the second branch correctly returns `[next, endPeriod]` and sets `lastClaimedPeriod = endPeriod`. On the *next* call `nextClaimablePeriod = endPeriod + 1`, so `endPeriod > nextClaimablePeriod` is false; the third branch sees `nextClaimablePeriod < currentValidatorPeriod` (validator still active) and returns `(endPeriod + 1, completedPeriods)`. Because exiting never decremented `delegatorsEffectiveStake`, `_claimableRewardsForPeriod` still credits the ghost stake for each future period.

#### Attack Scenario / Path Variants

**Path A: Infinite post-exit farm (primary)**
Path key: `strict_inequality_claim_window | claimRewards-after-exit | Stargate->ProtocolStaker`
1. Attacker stakes VET → NFT, delegates to an active validator.
2. `requestDelegationExit(tokenId)` once accumulated; wait for exit period to complete (status EXITED).
3. Call `claimRewards` — returns through `endPeriod`, sets `lastClaimedPeriod = endPeriod`.
4. Every later `claimRewards` (validator keeps producing) pays `(endPeriod+1 … completedPeriods)` — drain forever while keeping stake idle.

**Path B: View oracle / silent over-claim**
Path key: `strict_inequality_claim_window | claimableDelegationPeriods-fallback-branch | Stargate-internal`
1. Same setup; `claimableDelegationPeriods` itself returns first > `endPeriod` — the bug is visible on-chain before any claim.
2. Combined with skipping intermediate claims, an attacker time-spaces claims to always stay within `MAX_CLAIMABLE_PERIODS` per call.

#### Vulnerable Pattern Examples

**Example 1: The vulnerable window computation (Stargate.sol ~L880–927)** [Approx Vulnerability : HIGH]
```solidity
// ❌ VULNERABLE: strict '>' lets the window escape past endPeriod forever
uint32 nextClaimablePeriod = $.lastClaimedPeriod[_tokenId] + 1;
if (nextClaimablePeriod < startPeriod) {
    nextClaimablePeriod = startPeriod;
}

if (
    endPeriod != type(uint32).max &&
    endPeriod < currentValidatorPeriod &&
    endPeriod > nextClaimablePeriod          // <-- strict: fails once cursor == endPeriod
) {
    return (nextClaimablePeriod, endPeriod);
}

if (nextClaimablePeriod < currentValidatorPeriod) {
    return (nextClaimablePeriod, completedPeriods); // <-- pays post-exit periods
}
```

**Example 2: Cursor advances past the terminal boundary**
```solidity
// ❌ VULNERABLE: no terminal check — lastClaimedPeriod may exceed endPeriod
// inside claimRewards after computing the window:
$.lastClaimedPeriod[_tokenId] = lastClaimablePeriod; // == completedPeriods, past endPeriod
// nothing prevents lastClaimedPeriod from sailing past endPeriod for EXITED NFTs
```

**Example 3: Exit never subtracts effective stake**
```solidity
// ❌ VULNERABLE: ghost stake persists after exit
// _updatePeriodEffectiveStake(..., false) runs ONLY on unstake/redelegate:
function _claimableRewardsForPeriod(...) internal view returns (uint256) {
    uint256 eff = $.delegatorsEffectiveStake[_validator][period]; // still contains exited NFT
    return eff * rewardPerPeriod / totalEffective; // exited NFT keeps earning
}
```

### Impact Analysis

#### Technical Impact
- Reward pool drained by ghost delegations; per-period `delegatorsEffectiveStake` history corrupted
- Active delegators' shares diluted every period an attacker farms
- On-chain view (`claimableDelegationPeriods`) leaks the malformed window (detection signal)

#### Business Impact
- Direct, unbounded VTHO theft from honest stakers until patched

#### Affected Scenarios
- Any validator that remains active after a delegator exits — the default case
- Compounds with first-period loss (#59657 family) to distort rewards on both ends of a delegation's life

### Secure Implementation

**Fix 1: Terminal clamp on the claim window**
```solidity
// ✅ SECURE: exited delegations can never claim past endPeriod
uint32 nextClaimablePeriod = $.lastClaimedPeriod[_tokenId] + 1;
if (nextClaimablePeriod < startPeriod) nextClaimablePeriod = startPeriod;

if (endPeriod != type(uint32).max && endPeriod < currentValidatorPeriod) {
    if (nextClaimablePeriod > endPeriod) return (0, 0);         // fully claimed
    return (nextClaimablePeriod, endPeriod);                     // inclusive terminal
}
if (nextClaimablePeriod < currentValidatorPeriod) {
    return (nextClaimablePeriod, completedPeriods);
}
return (0, 0);
```

**Fix 2: Terminal flag + stake sweep at exit**
```solidity
// ✅ SECURE: hard-stop cursor and remove ghost stake when exit completes
if ($.lastClaimedPeriod[_tokenId] >= endPeriod && delegation.status == DelegationStatus.EXITED) {
    revert AlreadyFullyClaimed();
}
// and in the exit-completion hook (not only unstake/redelegate):
_updatePeriodEffectiveStake(_validator, _tokenId, endPeriod + 1, false);
```

### Detection Patterns

#### Contract / Call Graph Signals
```
- Range/window computations guarding a terminal boundary with strict inequality
- Reward cursor (lastClaimedPeriod) lacking a max(endPeriod) clamp
- Effective-stake checkpoints decremented on withdraw paths but not on lifecycle-exit paths
```

#### High-Signal Grep Seeds
```
- _claimableDelegationPeriods
- claimableDelegationPeriods
- lastClaimedPeriod
- endPeriod
- requestDelegationExit
- completedPeriods
- delegatorsEffectiveStake
- MAX_CLAIMABLE_PERIODS
```

#### Code Patterns to Look For
```
- Pattern 1: `end > next` style guards instead of `next > end ⇒ stop` terminal checks
- Pattern 2: sentinel default (`type(uint32).max`) mixed into range logic without exhaustive branch coverage
- Pattern 3: claim functions that trust stake history which exit paths never decrement
```

#### Audit Checklist
- [ ] Enumerate branch behavior for `nextClaimablePeriod == endPeriod`, `== endPeriod + 1`, `> endPeriod`
- [ ] Property test: total claimed by NFT ≤ rewards for periods `[startPeriod, min(endPeriod, now)]`
- [ ] Verify effective-stake checkpoint teardown on EVERY lifecycle terminal state

### Real-World Examples

#### Known Exploits
- **VeChain Stargate (hayabusa audit comp)** — exited NFTs farmed future-period VTHO — Nov 2025 — contest finding, no live exploit
  - Link: https://reports.immunefi.com/vechain-or-stargate-hayabusa (reports #59563, #59358, #59733, #60150, #60019)
  - Root cause: strict `endPeriod > nextClaimablePeriod` guard + never-removed ghost effective stake

#### Related CVEs/Reports
- Sister variants: #59361, #59665, #59709, #59863, #60069, #60081, #60102, #60154, #60169, #60192, #60265, #60310, #60400, #60431, #60516, #59316 (ghost-stake infinite drain)

### Prevention Guidelines

#### Development Best Practices
1. Use inclusive terminal boundaries and explicit "fully claimed" returns in window math
2. Treat lifecycle-exit completion as a state-mutation event (sweep stakes), not a passive flag

#### Testing Requirements
- Unit: claim sequence `exit → claim → claim` must yield zero on second call
- Fuzz: for random period advances, invariant `claimableRewards(EXITED) == 0` once cursor ≥ endPeriod

### Keywords for Search

`vechain`, `stargate`, `VTHO`, `delegation`, `rewards`, `claim window`, `off-by-one`, `endPeriod`, `lastClaimedPeriod`, `exited delegator`, `ghost stake`, `effective stake`, `strict inequality`, `yield theft`, `unclaimed rewards`, `claimRewards`, `validator period`, `infinite claim`, `reward drain`, `staking NFT`

### Related Vulnerabilities

- vechain-same-period-delegation-frozen-on-validator-exit.md (same exit window, fund-freeze sink)
- vechain-double-effective-stake-decrement-unstake-freeze.md (stake-side accounting on exit)
- vechain-pending-validator-first-period-reward-loss.md (delegation start boundary, mirror image)
