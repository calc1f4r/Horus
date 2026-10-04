---
# Core Classification
protocol: vechain
chain: vechain
category: gas_metering
vulnerability_type: native_builtin_gas_undercharge

# Pattern Identity
root_cause_family: unmetered_native_operation
pattern_key: missing_sload_charge | native-builtin-gas-metering | post-fork-extra-storage-reads | economic-depletion

# Interaction Scope
interaction_scope: multi_contract
involved_contracts:
  - builtin/authority_native.go (native_isEndorsed)
  - builtin/staker/transition.go (TransitionPeriodBalanceCheck)
  - builtin/staker validation service (GetValidation SLOADs)
path_keys:
  - missing_sload_charge | native_isEndorsed-post-HAYABUSA | authority->staker
  - missing_sload_charge | TransitionPeriodBalanceCheck-GetValidation | staker-internal

# Attack Vector Details
attack_type: resource_mispricing
affected_component: native builtin gas accounting during PoA→PoS transition

# Technical Primitives
primitives:
  - env.UseGas explicit charging
  - thor.SloadGas / thor.GetBalanceGas constants
  - fork-conditional code paths (pre/post HAYABUSA)
  - native_isEndorsed
  - endorsement balance check

# Grep / Hunt-Card Seeds
code_keywords:
  - native_isEndorsed
  - UseGas
  - SloadGas
  - GetBalanceGas
  - TransitionPeriodBalanceCheck
  - GetValidation
  - KeyProposerEndorsement
  - QueuedVET
  - gascharger
  - authority_native

# Impact Classification
severity: medium
impact: economic_depletion_of_network
financial_impact: medium

# Context Tags
tags:
  - l1
  - gas-metering
  - native-builtin
  - pos-transition
  - eip-parallel (cf. EVM gas schedule bugs)
  - consensus-adjacent

# Version Info
language: go   # thor native builtin (Go); callable from Solidity via builtin extension ABI
version: release/hayabusa (post-HAYABUSA fork paths)
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [INS-1] | reports/vechain-l1_findings/56454-bc-insight-gas-undercharging-threatens-hayabusa-network-upgrade.md | INSIGHT (network-shutdown impact class) | immunefi (@Angry_Mustache_Man) | #56454 |
| [INS-2] | reports/vechain-l1_findings/56629-bc-insight-there-is-an-issue-in-mapping-gas-undercharge-and-is-enables-30-extra-node-work-per.md | INSIGHT | immunefi | #56629 |
| [INS-3] | reports/vechain-l1_findings/56187-bc-insight-brittle-hardcoded-gas-metering-model.md | INSIGHT | immunefi | #56187 |
| [INS-4] | reports/vechain-l1_findings/56513-bc-insight-during-the-call-to-native-issuance-there-s-a-missing-gas-charge-before-call-to-calc.md | INSIGHT | immunefi | #56513 |
| [INS-5] | reports/vechain-l1_findings/55711-sc-insight-redundant-gas-charge-in-native-addvalidation-function-leads-to-unnecessary-gas-cost.md | INSIGHT | immunefi | #55711 |

## Native Builtin Gas Undercharge After HAYABUSA Fork (native_isEndorsed et al.)

**Post-fork code path in `TransitionPeriodBalanceCheck` performs extra uncharged SLOADs (`GetValidation`) — `native_isEndorsed` charges 1000 gas for ≥1200 gas of work (~16.7% undercharge), repeated on every endorsement check**

### Overview

VeChain's native builtins charge gas via explicit `env.UseGas(...)` calls with hardcoded constants. In `native_isEndorsed`, the pre-HAYABUSAA balance-check pricing (1000 gas: 3×SloadGas + GetBalanceGas) is carried past the fork, but `TransitionPeriodBalanceCheck` now also calls `GetValidation` (≥1 extra SLOAD ≥200 gas) on the post-fork path. Every call undercharges ≥200 gas; every block validation during the PoA→PoS transition invokes this check, economically draining the protocol's gas model.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because gas charges are hardcoded per code path rather than per operation actually executed: the post-HAYABUSA branch of `TransitionPeriodBalanceCheck` reads validation storage (`GetValidation` SLOADs) that `native_isEndorsed` never charges for."
- Pattern key: `missing_sload_charge | native-builtin-gas-metering | post-fork-extra-storage-reads | economic-depletion`
- Interaction scope: `multi_contract` (authority native builtin → staker transition/balance checker)
- Primary affected component(s): `native_isEndorsed` gas schedule; `TransitionPeriodBalanceCheck` post-fork branch
- Contracts / modules involved: `builtin/authority_native.go`, `builtin/staker/transition.go`, staker validation service
- Path keys: `missing_sload_charge | native_isEndorsed-post-HAYABUSA | authority->staker`
- High-signal code keywords: `native_isEndorsed`, `UseGas`, `SloadGas`, `GetBalanceGas`, `TransitionPeriodBalanceCheck`, `GetValidation`, `gascharger`
- Typical sink / impact: `systematic gas underpricing → economic depletion / spam cheapening → potential network shutdown class`
- Validation strength: `strong` (static source-check PoC + measured GetValidation gas consumption test provided)

#### Contract / Boundary Map

- Entry surface(s): `native_isEndorsed(nodeMaster)` — VM builtin extension callable from clauses; executed by every validator during endorsement checks
- Contract hop(s): `authority_native.native_isEndorsed -> Authority.Get (2 SLOADs, charged) -> Params.Get (1 SLOAD, charged) -> Staker.TransitionPeriodBalanceCheck -> GetBalance (charged) -> [post-HAYABUSA] GetValidation (UNCHARGED SLOADs)`
- Trust boundary crossed: gas schedule boundary between authority builtin and staker service internals — callee's cost invisible to caller's metering
- Shared state or sync assumption: hardcoded `UseGas` sums must cover worst-case operations on every fork side of each branch

#### Valid Bug Signals

- Signal 1: a `UseGas`-metered native function whose callee takes a fork-conditional branch adding storage reads (diff pre/post fork paths)
- Signal 2: measured op gas (via gascharger test) exceeds the static `UseGas` total charged at the entry point (here ≥1200 actual vs 1000 charged)
- Signal 3: the entry point runs per-block / per-endorsement during the transition — undercharge multiplies at consensus frequency

#### False Positive Guards

- Not this bug when: the extra reads occur only pre-fork and the charge matches the pre-fork path (mirror image)
- Not this bug when: callee operations are pure/in-memory (no SLOADs) — flat charge may legitimately cover them
- Safe if: metering is per-operation inside the callee (each `Get` charges its own SloadGas) rather than a hardcoded lump at the entry
- Impact framing: "undercharge" findings are usually low/insight severity; here the impact class claimed (repeated per-block exploitation → economic depletion → shutdown risk) plus transition-wide frequency elevates attention

### Vulnerability Description

#### Root Cause

`native_isEndorsed` charges a fixed 1000 gas: `SloadGas*2` (Authority.Get) + `SloadGas` (Params.Get) + `GetBalanceGas` (balance check). After the HAYABUSA fork, `TransitionPeriodBalanceCheck` — when the endorser balance is below the endorsement threshold — additionally loads the validator's `Validation` record (storage reads) to check `QueuedVET`. Those reads are on the post-fork path but absent from the charge list: actual cost ≥1200 gas, ≥16.7% undercharge per call.

#### Attack Scenario / Path Variants

**Path A: Per-block undercharge during transition**
Path key: `missing_sload_charge | native_isEndorsed-post-HAYABUSA | authority->staker`
1. Post-fork, endorser balance < endorsement param (common during migration).
2. Every `native_isEndorsed` call enters the `GetValidation` branch (uncharged SLOADs).
3. Every block validation during PoA→PoS calls it → aggregate uncharged work scales with block rate.

**Path B: Deliberate cheap-call spam**
Path key: `missing_sload_charge | TransitionPeriodBalanceCheck-GetValidation | staker-internal`
1. Attacker contracts call the builtin directly at 1000 gas for ≥1200 gas of node work.
2. Repeat at high frequency: each call extracts ≥200 gas of uncompensated computation/storage access (CPU/IO DoS economics, cf. the "underpriced supply queries" finding #55925).

#### Vulnerable Pattern Examples

**Example 1: Fixed charges missing the post-fork reads (authority_native.go L105-137)** [Approx Vulnerability : MEDIUM]
```go
// ❌ VULNERABLE: charges pre-fork cost model on a post-fork path
{"native_isEndorsed", func(env *xenv.Environment) []any {
    var nodeMaster common.Address
    env.ParseArgs(&nodeMaster)

    env.UseGas(thor.SloadGas * 2)                 // Authority.Get
    listed, endorsor, _, _, err := Authority.Native(env.State()).Get(thor.Address(nodeMaster))
    ...
    env.UseGas(thor.SloadGas)                     // Params.Get
    endorsement, err := Params.Native(env.State()).Get(thor.KeyProposerEndorsement)
    ...
    env.UseGas(thor.GetBalanceGas)                // balance check ONLY
    isEndorsed, err := Staker.Native(env.State()).TransitionPeriodBalanceCheck(...)(...)
    // ⚠ no charge for GetValidation SLOADs executed post-HAYABUSA inside the checker
    return []any{isEndorsed}
}},
```

**Example 2: The uncharged branch (transition.go L72-98)** [Approx Vulnerability : MEDIUM]
```go
// ❌ VULNERABLE: post-fork branch adds storage reads the caller never pays for
func (s *Staker) TransitionPeriodBalanceCheck(fc *thor.ForkConfig, currentBlock uint32, endorsement *big.Int) authority.BalanceChecker {
    return func(validator, endorser thor.Address) (bool, error) {
        balance, err := s.state.GetBalance(endorser)
        ...
        if balance.Cmp(endorsement) >= 0 { return true, nil }
        if currentBlock < fc.HAYABUSA { return false, nil } // pre-fork: cheap path only
        validation, err := s.validationService.GetValidation(validator) // ⚠ SLOADs, uncharged
        ...
        queuedVET := big.NewInt(0).SetUint64(validation.QueuedVET)
        return queuedVET.Cmp(endorsement) >= 0, nil
    }
}
```

**Example 3: Same disease in other builtins (family evidence)**
```go
// ❌ VULNERABLE: sibling findings — native_issuance calls calculaterewards storage
// work before any charge (#56513); mapping SSTORE-reset undercharge adds ~30% node
// work per call (#56629); hardcoded per-path UseGas model is brittle across forks (#56187).
// Pattern: entry-point lump charges + fork-evolving callee work = drift.
```

### Impact Analysis

#### Technical Impact
- ≥200 gas (≥16.7%) undercharge per endorsed check post-fork
- Aggregate uncompensated node work scales with block validation frequency during transition
- Economic incentive to spam the builtin below true cost (CPU/IO amplification)

#### Business Impact
- Economic depletion of the fee model; spam cheapening; in the extreme, the reported impact class is inability to confirm transactions (network shutdown)

#### Affected Scenarios
- PoA→PoS transition window where every block runs endorsement checks
- Any future fork that widens callee work while entry-point charges stay hardcoded

### Secure Implementation

**Fix 1: Charge gas at the point of consumption**
```go
// ✅ SECURE: meter each storage read where it happens
if currentBlock >= fc.HAYABUSA {
    env.UseGas(thor.SloadGas * 2) // cover GetValidation's reads
}
validation, err := s.validationService.GetValidation(validator)
```

**Fix 2: Worst-case charge at entry**
```go
// ✅ SECURE: charge the maximum any branch can incur (pre-fork paths may overpay —
// acceptable and refundable), or restructure so the checker receives a metered env
env.UseGas(thor.SloadGas * 2 + thor.SloadGas + thor.GetBalanceGas + thor.SloadGas*2)
```

### Detection Patterns

#### Contract / Call Graph Signals
```
- Native/prehended builtins with lump-sum UseGas at entry calling services that branch on fork height
- Gas constants hardcoded adjacent to code that gains storage operations in later forks
- Diff-based review: for each `if block < FORK` guard, diff ops on both sides vs the charge set
```

#### High-Signal Grep Seeds
```
- native_isEndorsed
- UseGas(
- TransitionPeriodBalanceCheck
- fc.HAYABUSA
- GetValidation
- SloadGas
- gascharger
```

#### Code Patterns to Look For
```
- Pattern 1: `env.UseGas(<const>)` totals not derived from the callee's actual op count
- Pattern 2: fork-conditional early returns that skip *both* the work and its charge while the charged path adds work
- Pattern 3: gascharger tests measuring per-op consumption vs entry-point charges (the PoC approach)
```

#### Audit Checklist
- [ ] For every native builtin, enumerate post-fork branches and their storage ops; verify charge coverage
- [ ] Write gas-measurement tests (gascharger) per branch, not just happy path
- [ ] Check per-block-frequency entry points first (endorsement, issuance, header validation)

### Real-World Examples

#### Known Exploits
- **VeChain thor hayabusa** — native_isEndorsed undercharge ≥200 gas/call post-fork — Oct 2025 — contest finding (insight severity, shutdown-class impact)
  - Link: https://reports.immunefi.com/vechain-hayabusa-upgrade-or-attackathon (report #56454)
  - Root cause: hardcoded entry-point charges vs fork-expanded callee work

#### Related CVEs/Reports
- #56513 (native_issuance missing charge before calculaterewards), #56629 (mapping SSTORE undercharge ~30% extra work), #56187 (brittle hardcoded metering model), #55711 (inverse: redundant overcharge in addValidation), #55925 (underpriced totalSupply queries → cheap CPU DoS)

### Prevention Guidelines

#### Development Best Practices
1. Meter gas at the operation site, not at the entry point lump
2. Treat every fork guard as a gas-schedule review trigger

#### Testing Requirements
- Unit: gas-charged == gas-consumed per branch (gascharger instrumentation)
- CI: fork-matrix tests asserting charge coverage on both sides of every fork conditional

### Keywords for Search

`vechain`, `thor`, `hayabusa`, `native builtin`, `gas metering`, `undercharge`, `UseGas`, `SloadGas`, `native_isEndorsed`, `TransitionPeriodBalanceCheck`, `GetValidation`, `endorsement`, `PoA to PoS`, `fork conditional`, `economic depletion`, `spam`, `gas schedule`, `hardcoded gas`, `CPU DoS`, `network shutdown`, `consensus transition`

### Related Vulnerabilities

- vechain-same-period-delegation-frozen-on-validator-exit.md (same staker module, state-accounting sink)
- vechain-double-effective-stake-decrement-unstake-freeze.md (staking lifecycle accounting)
