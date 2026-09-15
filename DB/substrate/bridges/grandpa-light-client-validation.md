---
# Core Classification
protocol: composable
chain: polkadot
category: bridge
vulnerability_type: consensus_validation_bypass
root_cause_family: incomplete_result_validation

# Pattern Identity
pattern_key: partial-result-check | GRANDPA justification verification | commit with duplicates/equivocations | invalid finality accepted

# Interaction Scope
interaction_scope: single_contract
involved_contracts:
  - pallet-grandpa-light-client (justification.rs)
  - prover (prover/src/lib.rs)
path_keys:
  - partial-result-check | validate_commit | is_valid() only, counters ignored | invalid justification accepted
  - partial-result-check | VoterSet::new | duplicate voters in validator set | total_weight manipulation
  - partial-result-check | prover loop | unbounded unknown_headers | prover DoS (infinite loop / OOM)

# Attack Vector Details
attack_type: data_validation_bypass
affected_component: GRANDPA justification/finality verification

# Technical Primitives
primitives:
  - grandpa_justification
  - precommit
  - VoterSet
  - total_weight
  - num_duplicated_precommits
  - num_invalid_voters
  - num_equivocations
  - validate_commit
  - ancestry_rule
  - unknown_headers

# Grep / Hunt-Card Seeds
code_keywords:
  - validate_commit
  - is_valid
  - num_duplicated_precommits
  - num_invalid_voters
  - num_equivocations
  - VoterSet::new
  - total_weight
  - unknown_headers

severity: medium
impact: invalid_finality_accepted
language: rust
tags:
  - substrate
  - bridge
  - grandpa
  - light_client
  - finality
  - dos
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [gpc1] | reports/substrate-l1_findings/composable-halborn-grandpa-lc.md | MEDIUM | Halborn | HAL-01 `validate_commit` result only checked via `is_valid()`, ignoring `num_duplicated_precommits`/`num_invalid_voters`/`num_equivocations` (`justification.rs:57,77,74`) — SOLVED in commit `bd400dd` |
| [gpc2] | reports/substrate-l1_findings/composable-halborn-grandpa-lc.md | MEDIUM | Halborn | HAL-02 `VoterSet::new` accepts duplicate voters → `total_weight` manipulation — SOLVED |
| [gpc3] | reports/substrate-l1_findings/composable-halborn-grandpa-lc.md | MEDIUM | Halborn | HAL-03 prover DoS — infinite loop / OOM via unbounded `unknown_headers` (`prover/src/lib.rs:121-141`) — SOLVED |
| [x4] | reports/substrate-l1_findings/composable-audits-halborn-audit20221003-pallet-grandpa-light-client-bridge-pdf.md | MEDIUM | Halborn | (HAL-01) GRANDPA JUSTIFICATION - MISSING COMMIT VALIDATION |
| [x5] | reports/substrate-l1_findings/composable-audits-halborn-audit20221003-pallet-grandpa-light-client-bridge-pdf.md | MEDIUM | Halborn | (HAL-02) GRANDPA JUSTIFICATION - MISSING VOTERS VALIDATION |
| [x6] | reports/substrate-l1_findings/composable-audits-halborn-audit20221003-pallet-grandpa-light-client-bridge-pdf.md | MEDIUM | Halborn | (HAL-03) GRANDPA PROVER - DENIAL OF SERVICE |
| [x7] | reports/substrate-l1_findings/audit-reports-snowbridge-2024-05-24-audit-report-snowbridge-v1-1-pdf.md | CRITICAL | auditor | Attackers can drain relayer funds and hence DoS the bridge by spamming create_agent transactions |
| [x8] | reports/substrate-l1_findings/audit-reports-snowbridge-2024-05-24-audit-report-snowbridge-v1-1-pdf.md | CRITICAL | auditor | Attackers can drain sovereign funds and hence DoS the bridge by spamming registerToken transactions |
| [x9] | reports/substrate-l1_findings/audit-reports-snowbridge-2024-05-24-audit-report-snowbridge-v1-1-pdf.md | HIGH | auditor | Partial update may temporarily stall the bridge |

## Partial Commit-Validation Result Lets Invalid GRANDPA Justifications Pass a Light Client

**A GRANDPA light client checks only the boolean `is_valid()` of `validate_commit` while ignoring the duplicated-precommit / invalid-voter / equivocation counters, so malformed justifications are accepted as valid finality** - representative of bridge light clients that consume a rich validation result but assert only part of it.

### Overview

Halborn's 2022 audit of Composable's `pallet-grandpa-light-client-bridge` found all three findings at Medium severity (all SOLVED in commit `bd400dd`): HAL-01 discards most of the commit-validation result, HAL-02 lets duplicate validators inflate/deflate the voter set weight, and HAL-03 lets prover input drive an unbounded loop into OOM.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because `validate_commit` returns a structured result whose anomaly counters signal rejection, but the caller only inspects `is_valid()`, so justifications containing duplicated precommits, invalid voters, or equivocations are treated as valid finality."
- Pattern key: `partial-result-check | GRANDPA justification verification | commit with duplicates/equivocations | invalid finality accepted`
- Interaction scope: `single_contract`
- Primary affected component(s): `justification verification (validate_commit / check_commit_validation_result), VoterSet construction, prover header pipeline`
- Contracts / modules involved: `pallet-grandpa-light-client justification.rs, prover/src/lib.rs`
- Path keys: `is_valid() only, counters ignored`, `duplicate voters in validator set`, `unbounded unknown_headers`
- High-signal code keywords: `validate_commit, is_valid, num_duplicated_precommits, num_invalid_voters, num_equivocations, VoterSet, total_weight, unknown_headers`
- Typical sink / impact: `invalid finality accepted → bogus header finalization on the bridging chain / prover DoS`
- Validation strength: `strong` (auditor-confirmed, fixed in commit `bd400dd`)

#### Contract / Boundary Map

- Entry surface(s): justification submission extrinsic / runtime API ingesting GRANDPA justifications; off-chain prover fed with headers
- Contract hop(s): `justification ingestion -> validate_commit -> is_valid() assertion -> header finalized`
- Trust boundary crossed: `bridge/relay boundary — external GRANDPA consensus data entering the parachain runtime`
- Shared state or sync assumption: `the light client's view of the source chain's finalized headers must exactly match the source chain's actual finality`

#### Valid Bug Signals

- Signal 1: A call to `validate_commit(...)` whose result is consumed only via `is_valid()` while `num_duplicated_precommits`, `num_invalid_voters`, `num_equivocations` are never read (`justification.rs:57,77,74`).
- Signal 2: `VoterSet::new(voters)` builds a set without deduplicating voter keys, so `total_weight` is attacker-influenced ([gpc2]).
- Signal 3: A prover loop iterating `unknown_headers` with no bound on count or total size (`prover/src/lib.rs:121-141`).

#### False Positive Guards

- Not this bug when: the caller checks every field of the validation result (treats any non-zero counter as invalid), or uses an upstream `finality-grandpa` helper that already enforces it.
- Safe if: the voter set is constructed from an authority-set root already committed on-chain and deduplicated by construction.
- Requires attacker control of: submitted justification bytes (HAL-01/02) or prover input headers (HAL-03).
- Note: all three issues were SOLVED in commit `bd400dd` — check the deployed revision before reporting.

### Vulnerability Description

#### Root Cause

`validate_commit` in finality-grandpa returns a `CommitValidationResult` whose `is_valid()` is a coarse boolean; the individual counters exist precisely because duplicated precommits, precommits from invalid voters, and equivocations must each invalidate the commit even when the raw weight threshold is met. The pallet asserted only the boolean ([gpc1]). Separately, `VoterSet::new` did not reject duplicate voters, letting set weight be miscounted ([gpc2]), and the prover processed `unknown_headers` without bounds ([gpc3]).

#### Attack Scenario / Path Variants

**Path A: Equivocating/duplicated justification accepted as finality**
Path key: `partial-result-check | validate_commit | is_valid() only, counters ignored | invalid justification accepted`
Entry surface: justification submission
Contracts touched: `justification.rs -> validate_commit -> is_valid()`
Boundary crossed: relay-to-parachain finality data
1. Attacker (or faulty relayer) crafts a justification whose precommit weight passes the threshold only because a precommit is counted twice or a non-voter's precommit is included.
2. `validate_commit` returns a result with non-zero `num_duplicated_precommits` / `num_invalid_voters` / `num_equivocations` — but `is_valid()` alone is checked at `justification.rs:57,77,74`.
3. The light client finalizes a header the source chain never finalized; downstream bridge transfers execute against bogus finality.

**Path B: Duplicate voters manipulate total_weight**
Path key: `partial-result-check | VoterSet::new | duplicate voters in validator set | total_weight manipulation`
1. Attacker influences the voter-set input to `VoterSet::new` (e.g., via authority-set update message).
2. Duplicate entries make `total_weight` over- or under-counted, shifting the >2/3 threshold.
3. Justifications that should fail (or that were crafted to pass) clear the manipulated threshold.

**Path C: Prover DoS via unbounded unknown_headers**
Path key: `partial-result-check | prover loop | unbounded unknown_headers | prover DoS (infinite loop / OOM)`
Entry surface: prover input (`prover/src/lib.rs:121-141`)
1. Attacker feeds the prover a header stream with a large or cyclic `unknown_headers` set.
2. The prover loops without a termination bound — infinite loop or memory exhaustion.
3. Bridge proof production halts (liveness attack on the bridge service).

#### Vulnerable Pattern Examples

**Example 1: Only the boolean is checked (from [gpc1])** [Approx Vulnerability : MEDIUM]
```rust
// ❌ VULNERABLE: justification.rs:57,77,74 — rich result collapsed to is_valid()
let validation = validate_commit(&commit, &block, &voters, &mut ancestry_chain);
if !validation.is_valid() {   // counters below are never consulted
    return Err(Error::InvalidJustification);
}
// MISSING: reject when validation.num_duplicated_precommits() > 0
//           || validation.num_invalid_voters() > 0
//           || validation.num_equivocations() > 0
Ok(())
```

**Example 2: VoterSet built without dedup (from [gpc2])** [Approx Vulnerability : MEDIUM]
```rust
// ❌ VULNERABLE: duplicate voters accepted into the set
let voters: Vec<(AuthorityId, u64)> = raw_authorities.into_iter().collect(); // may contain dupes
let voter_set = VoterSet::new(voters); // total_weight double-counts duplicated keys
// => 2/3 supermajority arithmetic is wrong; crafted commits pass or valid ones fail
```

**Example 3: Unbounded prover loop (from [gpc3])** [Approx Vulnerability : MEDIUM]
```rust
// ❌ VULNERABLE: prover/src/lib.rs:121-141 — no cap on unknown_headers
while let Some(header) = next_unknown_header(&mut stream) {
    unknown_headers.push(decode_full(&header)?); // attacker controls count and size
    // no max-headers / max-bytes bound -> infinite loop or OOM
}
```

### Impact Analysis

#### Technical Impact

- Invalid finality accepted on the bridging chain — the light client's core invariant breaks; any bridge decision (token mint/release) built on finalized headers becomes attacker-influenceable.
- Weight-threshold manipulation via duplicated voters shifts consensus accounting ([gpc2]).
- Prover liveness killed by resource exhaustion ([gpc3]).

#### Business Impact

- A GRANDPA light client that accepts bad justifications undermines every cross-chain message relying on it; for Composable's bridge this was a block-the-launch class of defect (all fixed pre-deploy, commit `bd400dd`).

#### Affected Scenarios

- Any pallet embedding `finality-grandpa`'s `validate_commit` or reimplementing commit checks.
- Bridges whose relayer/prover accepts externally sourced header lists.
- Authority-set updates ingested from messages rather than on-chain state.

### Secure Implementation

**Fix 1: Assert the full validation result, not just is_valid()**
```rust
// ✅ SECURE: every anomaly counter must be zero (per Halborn fix)
let validation = validate_commit(&commit, &block, &voters, &mut ancestry_chain)?;
ensure!(
    validation.is_valid()
        && validation.num_duplicated_precommits() == 0
        && validation.num_invalid_voters() == 0
        && validation.num_equivocations() == 0,
    Error::InvalidJustification
);
```

**Fix 2: Deduplicated voter set + bounded prover input**
```rust
// ✅ SECURE: reject duplicate authorities and cap prover work
let mut seen = HashSet::new();
let voters = raw_authorities.into_iter().filter(|(id, _)| seen.insert(id.clone())).collect();
let voter_set = VoterSet::new(voters).ok_or(Error::DuplicateVoter)?;

ensure!(unknown_headers.len() <= MAX_UNKNOWN_HEADERS, Error::TooManyHeaders);
ensure!(total_bytes <= MAX_PROOF_BYTES, Error::ProofTooLarge);
```

### Detection Patterns

#### High-Signal Grep Seeds
```
- validate_commit
- is_valid
- num_duplicated_precommits
- num_invalid_voters
- num_equivocations
- VoterSet::new
- total_weight
- unknown_headers
```

#### Code Patterns to Look For
```
- Pattern 1: `if !result.is_valid()` immediately after validate_commit with counters unread
- Pattern 2: VoterSet::new over an un-deduplicated iterator of (AuthorityId, weight)
- Pattern 3: loops draining attacker-sized header/proof vectors with no length/byte cap
```

#### Audit Checklist
- [ ] Are all CommitValidationResult counters checked (or a helper that does)?
- [ ] Can the voter set contain duplicate keys at construction?
- [ ] Does the prover/relayer bound the number and total size of unknown headers?
- [ ] Is the deployed revision at/after fix commit `bd400dd`?

### Keywords for Search

`GRANDPA light client`, `validate_commit`, `is_valid`, `commit validation`, `equivocation`, `duplicated precommits`, `invalid voters`, `VoterSet`, `total weight`, `justification verification`, `finality bypass`, `bridge light client`, `prover DoS`, `unknown headers`, `finality-grandpa`, `Composable bridge`, `Halborn`

### Related Vulnerabilities

- DB/substrate/bridges/snowbridge-bridge-accounting.md (BeefyClient validation flaws)
- DB/substrate/crypto/sr25519-signature-verification.md (consensus-crypto edge cases)
