---
vulnerability_class: state_root_fork_choice_mismatch
title: "State-Root & Fork-Choice Integrity Gaps: buffered blocks skip validation, stale trie updates, side-chain hashes"
protocol: eth-l1-clients
category: Consensus / Blockchain Tree
vulnerability_type: validation_bypass
attack_type: state_root_skip|sidechain_hash_corruption|fork_choice_accounting_bug|chain_split
affected_component: blockchain_tree|fork_choice|state_providers|trie_updates
chain: ethereum
severity: critical
impact: chain_split|wrong_state_served|consensus_divergence
severity_range: "HIGH to CRITICAL"
source: Sigma Prime reth 2024 + Immunefi Ethereum Protocol Attackathon 2024-2025

primitives:
  - buffered_blocks_skip_state_root_validation
  - side_chain_hashes_invalid_for_state_provider
  - trieupdates_flush_reorders_operations
  - trie_updates_not_removed_for_all_chains_on_fork_choice_updated
  - shallow_copy_of_byte_slice_fork
  - engineapi_error_hash_mismatch

affected_components:
  - blockchain tree (block buffering, canonical chain commit)
  - fork-choice update handling (engine API)
  - trie update queues / state providers
  - historical block hash machinery

tags:
  - state_root
  - fork_choice
  - blockchain_tree
  - reth
  - erigon
  - engine_api
  - consensus
  - chain_split
  - sigp

total_reports_analyzed: 6

# Pattern Identity (Required)
root_cause_family: consensus_pipeline_validation_gap
pattern_key: state_root_fork_choice_gap | buffered_sidechain_trie_accounting | chain_split

# Interaction Scope
interaction_scope: consensus_pipeline

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - try_connect_buffered_blocks
  - state_root
  - canonical_chain
  - fork_choice_updated
  - TrieUpdates
  - flush()
  - side_chain
  - latest_valid_hash
  - BufferedBlocks
  - new_chain_fork
  - dataCopy
---

# State-Root & Fork-Choice Mismatch (buffered blocks, trie update accounting)

## Overview

The blockchain tree must guarantee: every committed block's state root was verified against
execution output, and fork-choice updates cleanly re-point canonical state. Sigma Prime's 2024 reth
audit surfaced the canonical cluster of violations here — RETH-01 (Critical), RETH-02 (Critical),
RETH-05 (High, **Open**), RETH-18 (Medium) — plus Attackathon-era reports in erigon showing the same
class elsewhere:

- **RETH-01 (Critical, Resolved): Invalid Side Chain Hashes For State Provider** — state served
  against wrong/side-chain hashes; consumers read state that never was canonical.
- **RETH-02 (Critical, Resolved): `TrieUpdates::flush()` Will Change Order Of Operations For Extended Updates** — persistence ordering bug corrupting trie state under load.
- **RETH-05 (High, Open at report time): State Roots May Not Be Checked For Buffered Blocks** —
  `try_connect_buffered_blocks()` allows buffered blocks to skip state-root validation when
  reconnecting to the tree. This is the single highest-signal pattern in this class.
- **RETH-18 (Medium): Trie Updates Not Removed For All Chains During Fork Choice Updated** — stale
  trie update sets survive fork-choice reorgs → wrong state roots after reorg.
- **erigon #37199 [Low]**: shallow copy of byte slice in precompile `dataCopy` → potential chain
  fork (mutable aliasing of consensus data).

**Root Cause Statement**: This vulnerability exists because the block-validation pipeline has
fast paths (buffered-block reconnect, side-chain state serving, deferred trie flushes) that skip or
reorder the state-root checks and cleanup that the canonical commit path enforces — so a block can
be committed/served with an unverified or stale state root, splitting the chain.

**Observed Frequency**: concentrated (reth 2024 audit) but structurally recurring in any client
with buffered/tree-based block pipelines (erigon variants found at Attackathon).
**Consensus Severity**: HIGH to CRITICAL

---

#### Agent Quick View

- Root cause statement: "This vulnerability exists because of consensus_pipeline_validation_gap (buffered blocks skip state root / trie update accounting)"
- Pattern key: `state_root_fork_choice_gap | buffered_sidechain_trie_accounting | chain_split`
- Interaction scope: `consensus_pipeline`
- Primary affected component(s): `blockchain_tree`, `fork_choice`
- High-signal code keywords: `try_connect_buffered_blocks`, `TrieUpdates`, `flush`, `fork_choice_updated`
- Typical sink / impact: `chain_split` / `wrong_state_served`
- Validation strength: `high` (Sigma Prime audit with code excerpts)

#### Contract / Boundary Map

- Entry surface(s): engine API `forkchoiceUpdated`/`newPayload`, block import, reorg paths
- Contract hop(s): `new block -> buffer -> execute -> state root check? -> tree insert -> canonical commit / side chain`
- Trust boundary crossed: `consensus-layer payload proposer (semi-trusted) + network blocks`
- Shared state or sync assumption: `canonical state root == executed state root for every committed block`

#### Valid Bug Signals

- Signal 1: Any code path that inserts/commits a block without comparing `block.state_root` to the executed root (search every `insert`/`connect` in the tree)
- Signal 2: Buffered-block reconnect path reusing earlier validation results without re-checking
- Signal 3: Trie-update queue keyed by block but not invalidated/removed on reorg (`fork_choice_updated` handler)
- Signal 4: Persistence flush ordering not transactional w.r.t. trie node ordering
- Signal 5: Shared/aliased byte slices between consensus objects (Go: `append` aliasing; shallow copies)

#### False Positive Guards

- Not this bug when: the buffered path re-executes or carries forward a cryptographically-bound validation receipt for the same block hash
- Safe if: single commit function verifies root immediately before DB write inside one transaction
- Requires attacker control of: block/payload content reaching the node (network or malicious CL proposer — CL is semi-trusted, engine API is JWT-guarded but forks target content)
- Liveness-only bugs (node stalls but serves no wrong state) are a different class — see txpool entry

## Real Reports

### 1. Sigma Prime reth 2024 — RETH-05 (High, Open): State Roots May Not Be Checked For Buffered Blocks

Report: `reports/eth-l1-clients_findings/reth-sigp-2024.md` (finding text ~line 451:
`try_connect_buffered_blocks()` at `blockchain_tree` ~L828 allows buffered blocks to skip state
root validation when connecting a new block `BlockNumHash`).

### 2. Sigma Prime reth 2024 — RETH-01 (Critical, Resolved): Invalid Side Chain Hashes For State Provider

Same report (findings table ~line 178).

### 3. Sigma Prime reth 2024 — RETH-02 (Critical, Resolved): TrieUpdates::flush() Order-Of-Operations; RETH-18 (Medium): Trie Updates Not Removed For All Chains During Fork Choice Updated; RETH-09/RETH-10 (High): EngineAPI invalid-hash errors / latest_valid_hash not finding canonical hashes

Same report.

### 4. Immunefi #37199 [BC-Low] — Potential chain fork due to shallow copy of byte slice (erigon)

Report: `reports/eth-l1-clients_findings/37199-bc-low-potential-chain-fork-due-to-shallow-copy-of-byte-slice.md`
NOTE: filename in the reports directory ends `-byte-slice.md` — verified present.
Precompile `dataCopy` returns an aliasing copy; later mutation corrupts consensus data → fork.

## Vulnerable Code Pattern (generic)

```rust
// VULNERABLE: buffered reconnect path skips state root verification (RETH-05 pattern)
fn try_connect_buffered_blocks(&mut self, new_block: BlockNumHash) {
    if let Some(buffered) = self.buffered.take(&new_block.parent) {
        // parent was validated once, reconnect children WITHOUT re-checking roots
        self.insert_validated(buffered);        // assumes validity by association
    }
}
```

```go
// VULNERABLE: aliasing copy of consensus bytes (#37199 pattern)
func dataCopy(evm *EVM, data []byte) []byte {
    return data[:len(data):len(data)]  // still shares backing array if resliced upstream
}
```

## Detection & Hunt Strategy

1. Map every entry point that marks a block "validated" (import, buffer-connect, side-chain
   insert) and assert each performs (or provably inherits, same-hash) a state-root comparison.
2. Instrument reorg/fork-choice tests: force N-block deep reorgs and diff trie-update set
   membership before/after `fork_choice_updated` (RETH-18 pattern).
3. Fuzz buffered-block arrival orders (out-of-order parents, duplicate hashes) with deliberately
   wrong state roots; the tree must reject, never commit.
4. Go clients: audit `[]byte` copies crossing consensus boundaries (`copy()` vs slice), run with
   `-race` under reorg load.
5. Cross-check engine-API error hashes (`latestValidHash` on invalid payloads) against the
   execution-apis spec (RETH-09/10 pattern).

## References

- `reports/eth-l1-clients_findings/reth-sigp-2024.md` (RETH-01, RETH-02, RETH-05, RETH-09, RETH-10, RETH-18)
- `reports/eth-l1-clients_findings/37199-bc-low-potential-chain-fork-due-to-shallow-copy-of-byte-slice.md`
- `reports/eth-l1-clients_findings/audit-reports-anoma-2023-03-28-audit-report-namada-ethereum-bridge-v1-0-pdf.md`- `reports/eth-l1-clients_findings/chainsafe-gossamer-sigp.md`- `reports/eth-l1-clients_findings/chainsafe-gossamer-sigp.md`- `reports/eth-l1-clients_findings/chainsafe-gossamer-sigp.md`- `reports/eth-l1-clients_findings/chainsafe-gossamer-sigp.md`- `reports/eth-l1-clients_findings/chainsafe-gossamer-sigp.md`- `reports/eth-l1-clients_findings/ef-pectra-sigp.md`- `reports/eth-l1-clients_findings/public-audits-reports-berachain-sigma-prime-berachain-reth-geth-security-assessment-report-v2-0-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-berachain-sigma-prime-berachain-reth-geth-security-assessment-report-v2-0-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-berachain-sigma-prime-berachain-reth-geth-security-assessment-report-v2-0-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-chainsafe-forest-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-chainsafe-forest-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-chainsafe-forest-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-chainsafe-forest-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-chainsafe-gossamer-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-chainsafe-gossamer-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-chainsafe-gossamer-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-chainsafe-gossamer-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-chainsafe-gossamer-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-commitboost-sigma-prime-commit-boost-client-security-assessment-report-v2-0-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-ethereum-foundation-pectra-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-filecoin-filecoin-lotus-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-filecoin-filecoin-lotus-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-filecoin-filecoin-lotus-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-filecoin-filecoin-lotus-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-obol-sigma-prime-obol-network-charon-security-assessment-report-v2-1-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-obol-sigma-prime-obol-network-charon-security-assessment-report-v2-1-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-reth-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-reth-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-reth-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-reth-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-reth-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-risc-zero-sigma-prime-risc-zero-the-signal-ethereum-security-assessment-report-v2-0-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-risc-zero-sigma-prime-risc-zero-the-signal-ethereum-security-assessment-report-v2-0-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-rise-sigma-prime-rise-core-node-security-assessment-report-v2-0-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-rise-sigma-prime-rise-core-node-security-assessment-report-v2-0-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-rise-sigma-prime-rise-core-node-security-assessment-report-v2-0-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-rise-sigma-prime-rise-core-node-security-assessment-report-v2-0-pdf.md`- `reports/eth-l1-clients_findings/publications-audit-reports-peckshield-audit-report-bscstationstartpools-v1-0-pdf.md`- `reports/eth-l1-clients_findings/publications-reviews-2023-04-prysm-securityreview-pdf.md`- `reports/eth-l1-clients_findings/publications-reviews-2023-08-scrolll2geth-securityreview-pdf.md`- `reports/eth-l1-clients_findings/publications-reviews-dfinityconsensus-pdf.md`- `reports/eth-l1-clients_findings/publications-spectral-modelers-zellic-audit-report-pdf.md`
- execution-apis engine_api spec (forkChoiceUpdated/newPayload validation flow)
- Immunefi/audit `37286` [SC-Insight] (execution-specs, INFO): Elimination of security checks in ForkCreator class — `reports/eth-l1-clients_findings/37286-sc-insight-elimination-of-security-checks-in-forkcreator-class.md` (Immunefi (warden))
- Immunefi/audit `37568` [BC-Insight] (lodestar, INFO): Missing specification logic — `reports/eth-l1-clients_findings/37568-bc-insight-missing-specification-logic.md` (Immunefi (Pig46940))
