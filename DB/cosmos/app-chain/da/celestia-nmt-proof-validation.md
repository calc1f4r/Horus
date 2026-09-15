---
protocol: celestia
chain: celestia
category: da
vulnerability_type: nmt_inclusion_proof_validation

# Pattern Identity
root_cause_family: logic_error
pattern_key: logic_error | nmt_namespace_proof | nmt_inclusion_proof_validation

# Interaction Scope
interaction_scope: library
involved_contracts:
  - NMT library (HashNode / verifyLeafHashes / VerifyInclusion / VerifyNamespace)
  - celestia-app share serving
  - Light client data availability sampling
path_keys:
  - missing_ordering_check | HashNode | namespace ordering unverified | invalid tree accepted
  - ignore_max_ns_bug | precomputedMaxNs | maxNs mis-computed | wrong namespace range proof
  - empty_proof_panic | verifyLeafHashes | VerifyInclusion on empty | panic DoS

# Attack Vector Details
attack_type: logical_error|dos
affected_component: da_inclusion_proofs|data_availability

# Technical Primitives
primitives:
  - namespaced_merkle_tree
  - namespace_range_proof
  - inclusion_proof_verification
  - min_ns_max_ns_computation
  - ignore_max_namespace_option

# Grep / Hunt-Card Seeds
code_keywords:
  - HashNode
  - verifyLeafHashes
  - VerifyInclusion
  - VerifyNamespace
  - ignoreMaxNS
  - precomputedMaxNs
  - maxNs
  - minNs
  - NamespaceId
  - nmt

# Impact Classification
severity: high
impact: invalid_data_inclusion_accepted|dos|da_proof_forgery
exploitability: 0.4
financial_impact: high

# Context Tags
tags:
  - celestia
  - cosmos
  - appchain
  - da
  - nmt
  - merkle
  - inclusion-proof
  - data-availability

language: go
version: celestiaorg/nmt (Q1 2023 audit, issues 148-linked; library)

---

## References & Source Reports

> **For Agents**: If you need detailed information, read the referenced report file.

### NMT Library Audit
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Check of the namespace ordering missing in HashNode (Implementation, Severity 3 High, RESOLVED) | `reports/cosmos-l1-nodes_findings/audits-celestia-2023-03-30-celestia-namespaced-merkle-tree-library-audit-pdf.md` | HIGH | Informal Systems |
| IgnoreMaxNS leads to false computing maxNs (Implementation, Severity 2 Medium, RESOLVED; nmt#148) | `reports/cosmos-l1-nodes_findings/audits-celestia-2023-03-30-celestia-namespaced-merkle-tree-library-audit-pdf.md` | MEDIUM | Informal Systems |
| verifyLeafHashes will panic if called from VerifyInclusion over an empty proof (Implementation, Severity 2 Medium, RESOLVED) | `reports/cosmos-l1-nodes_findings/audits-celestia-2023-03-30-celestia-namespaced-merkle-tree-library-audit-pdf.md` | MEDIUM | Informal Systems |
| Additional medium findings (helpers, docs) — all RESOLVED | `reports/cosmos-l1-nodes_findings/audits-celestia-2023-03-30-celestia-namespaced-merkle-tree-library-audit-pdf.md` | MEDIUM | Informal Systems |
| [k1] | reports/cosmos-l1-nodes_findings/audit-reports-astroport-2024-05-22-audit-report-astroport-hub-neutron-migration-v1-0-pdf.md | CRITICAL | Oak Security | Attackers can manipulate the proposal outcome by transferring voting powers |
| [k2] | reports/cosmos-l1-nodes_findings/audit-reports-avail-2026-01-15-audit-report-avail-cosmos-and-backend-changes-v1-0-pdf.md | CRITICAL | Oak Security | Non-deterministic time check causes consensus failures |
| [k3] | reports/cosmos-l1-nodes_findings/audit-reports-avail-2026-01-15-audit-report-avail-cosmos-and-backend-changes-v1-0-pdf.md | HIGH | Oak Security | Unbounded pending settlements are processed during the PreBlocker , which can cause consensus delays |
| [k4] | reports/cosmos-l1-nodes_findings/audit-reports-avail-2026-01-15-audit-report-avail-cosmos-and-backend-changes-v1-0-pdf.md | HIGH | Oak Security | External RPC dependencies in consensus logic allow validators to be stalled |
| [k5] | reports/cosmos-l1-nodes_findings/audit-reports-avail-2026-01-15-audit-report-avail-cosmos-and-backend-changes-v1-0-pdf.md | HIGH | Oak Security | Fetching vote extension events without timeouts can stall consensus |
| [k6] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2025-03-25-audit-report-neutron-independent-chain-v1-0-pdf.md | HIGH | Oak Security | Validators with significant voting power could censor others to prevent them from receiving rewards |
| [k7] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2026-04-09-audit-report-neutron-auction-and-undelegations-contract-chain-upgrade-phase-2-report-2-pdf.md | CRITICAL | Oak Security | Misconfigured governance module permissions causing consensus-halting panic on deposit burn |
| [k8] | reports/cosmos-l1-nodes_findings/audit-reports-sei-2023-05-15-audit-report-sei-cosmos-v1-0-pdf.md | CRITICAL | Oak Security | Non-deterministic iteration in BuildDependencyDag may break consensus |
| [k9] | reports/cosmos-l1-nodes_findings/audit-reports-stride-2022-09-26-audit-report-stride-v1-0-pdf.md | CRITICAL | Oak Security | Non-deterministic iterations can cause consensus failures |
| [k10] | reports/cosmos-l1-nodes_findings/audits-evmos-informal-evmos-report-2021q4-pdf.md | HIGH | Informal Systems | Delegating 10ˆ6 * 2ˆ63 - x for a small x halts consensus |
| [k11] | reports/cosmos-l1-nodes_findings/ibc-go-docs-audits-08-wasm-halborn-audit-report-pdf.md | MEDIUM | Halborn | CONSENSUS STATE IS NOT SET IN THE WASM LIGHTCLIENT |
| [k12] | reports/cosmos-l1-nodes_findings/publications-babylon-genesis-chain-zellic-audit-report-pdf.md | CRITICAL | Zellic | Panic triggered by incorrect logic in finality module's EndBlock |
| [k13] | reports/cosmos-l1-nodes_findings/publications-babylon-genesis-chain-zellic-audit-report-pdf.md | CRITICAL | Zellic | Slashed finality provider retaining voting power |
| [k14] | reports/cosmos-l1-nodes_findings/publications-babylon-genesis-chain-zellic-audit-report-pdf.md | CRITICAL | Zellic | Slashed finality provider restoring voting power through pending delegations |
| [k15] | reports/cosmos-l1-nodes_findings/publications-ibc-eureka-zellic-audit-report-pdf.md | CRITICAL | Zellic | Untrusted input is used as trusted consensus state |
| [k16] | reports/cosmos-l1-nodes_findings/publicreports-cosmos-audits-a41-supernova-cosmos-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | NON-DETERMINISTIC ITERATIONS CAN CAUSE CONSENSUS FAILURES |
| [k17] | reports/cosmos-l1-nodes_findings/v4-chain-audits-informal-systems-audit-report-phase-iii-pdf.md | HIGH | Informal Systems | Consensus changes does not make v4 live |
| [k35] | reports/cosmos-l1-nodes_findings/audits-injective-informal-report-injective-audit-202106-pdf.md | HIGH | Informal Systems | Injective Protocol Audit IF-INJECTIVE-11 Price feed does not validate prices, may crash consensus #331 Status: resolved (as of June 15, 2021) |
| [z36] | reports/cosmos-l1-nodes_findings/audit-reports-sei-2023-05-15-audit-report-sei-tendermint-v1-0-pdf.md | HIGH | Oak Security | Saving an invalid LastResultsHash and AppHash when performing a hard rollback |
| [q37] | reports/cosmos-l1-nodes_findings/audit-reports-dymension-2024-08-13-audit-report-dymension-point-1d-stream-6-rollapp-white-box-pentest-v1-1-pdf.md | INFO | Oak Security | Tendermint RPC API exposes private IP address |
| [q38] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2026-04-09-audit-report-neutron-auction-and-undelegations-contract-chain-upgrade-phase-2-report-1-pdf.md | LOW | Oak Security | tick_undelegation_amount is applied per validator  contradicting its README description as a total cap |

### Related Celestia Audits
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Celestia rsmt2d library audit | `reports/cosmos-l1-nodes_findings/audits-celestia-2023-09-13-audit-report-celestia-rsmt2d-library-pdf.md` | multi | Informal Systems |
| Celestia Informal systems audit (app) | `reports/cosmos-l1-nodes_findings/celestia-app-docs-audit-informal-systems-pdf.md` | multi | Informal Systems |
| Authored blobs audit | `reports/cosmos-l1-nodes_findings/celestia-app-docs-audit-informal-systems-authored-blobs-pdf.md` | multi | Informal Systems |
| QGB relayer security ADR | `reports/cosmos-l1-nodes_findings/celestia-app-docs-architecture-adr-004-qgb-relayer-security-md.md` | DESIGN | Celestia |

---

## Celestia NMT Inclusion-Proof Validation Vulnerabilities [HIGH]

### Overview

Celestia's Namespaced Merkle Tree (NMT) is the cryptographic core of its data-availability proofs: leaves are namespaced, and internal nodes commit to `[minNs, maxNs]` ranges so light clients can verify "all data for namespace N" with short range proofs. Informal Systems' Q1-2023 audit of the library found a High (missing namespace-ordering check in `HashNode`), plus mediums where `ignoreMaxNS` mis-computes `maxNs` and `verifyLeafHashes` panics on empty proofs from `VerifyInclusion`. All were RESOLVED upstream — the pattern remains a hunt card for NMT forks and for any namespaced-commitment scheme (e.g., rollup DA bridges, QGB-style attestations) that reimplements range proofs.

#### Agent Quick View

- Root cause statement: "Correct namespace proofs require internal node hashes to commit to correctly ordered and correctly bounded [minNs,maxNs] ranges; implementations that skip ordering checks at hash time, special-case the max namespace, or panic on degenerate proofs let attackers forge inclusion/absence proofs or crash verifiers."
- Pattern key: `logic_error | nmt_namespace_proof | nmt_inclusion_proof_validation`
- Interaction scope: `library`
- Primary affected component(s): `nmt HashNode/verifyLeafHashes/VerifyInclusion, share/row proof verification in celestia-app`
- High-signal code keywords: `HashNode`, `verifyLeafHashes`, `VerifyInclusion`, `ignoreMaxNS`, `precomputedMaxNs`, `maxNs`, `minNs`
- Typical sink / impact: `acceptance of a proof for data NOT in namespace N (DA forgery) / verifier panic (DoS of light clients, bridges)`
- Validation strength: `strong (dedicated formal-methods audit; all issues resolved + linked upstream)`

#### Component / Boundary Map

- Entry surface(s): `VerifyNamespace(namespacedProof)`, `VerifyInclusion(proof)` — proof bytes come from untrusted block data/servicers
- Component hop(s): `da header (row/col roots) → nmt proof check → application trusts namespace data` — the library is the last verifier
- Trust boundary crossed: `untrusted serving node → light client / bridge verification`
- Shared state or sync assumption: `tree roots in DA header are canonical; range proof soundness depends on min/max propagation invariants at every internal node`

#### Valid Bug Signals

- Signal 1: Internal-node hashing does not verify child namespace ordering (left.maxNs ≤ right.minNs) before computing parent range — invalid trees hash to valid-looking roots
- Signal 2: `ignoreMaxNS`/`precomputedMaxNs` special case can be triggered by crafted leaf data so `maxNs` is set to the precomputed value when a smaller true max applies (concrete numeric case in audit: leaves {7..8},{9..10} with precomputedMaxNs=10)
- Signal 3: `VerifyInclusion`/`verifyLeafHashes` panics (index access, hash of empty set) instead of returning error on empty/degenerate proofs — verifier crash on attacker input
- Signal 4: Absence proofs (prove namespace N has no data) not covered by tests around the max-namespace boundary

#### False Positive Guards

- Not this bug when: upstream celestiaorg/nmt post-fix (v0.x after audit resolutions, nmt#148 fixed) is used unmodified
- Safe if: ordering assertions run inside HashNode and proof verification returns errors (never panics) on all degenerate inputs
- Requires attacker control of: block data placement (block producer/servicer) or crafted proofs to light clients

### Vulnerable Pattern Examples

**Example 1: Missing ordering check when hashing nodes** [HIGH, RESOLVED]
> 📖 Reference: `reports/cosmos-l1-nodes_findings/audits-celestia-2023-03-30-celestia-namespaced-merkle-tree-library-audit-pdf.md`
"Check of the namespace ordering missing in HashNode — Implementation, Severity 3 High, RESOLVED." Without the check, a malformed tree (children out of namespace order) still produces roots a verifier accepts, undermining range-proof soundness.

**Example 2: IgnoreMaxNS computes wrong maxNs** [MEDIUM, RESOLVED — nmt#148]
> 📖 Reference: same report. Concrete case: `precomputedMaxNs = 10, ignoreMaxNS = true, left{7,8}, right{9,10}` → HashNode sets `maxNs = 10 (precomputed)` though `rightMinNs (9) < precomputedMaxNs` means the correct bound is `rightMinNs`; "This issue can lead to setting maxNs to n.precomputedMaxNs even if it could be set to a namespace ID that is smaller."

**Example 3: Panic on empty proof** [MEDIUM, RESOLVED]
> 📖 Reference: same report — "The function verifyLeafHashes will panic if called from VerifyInclusion function over an empty proof" → untrusted input crashes the verifier (light client / bridge DoS).

### Secure Implementation

```go
// ✅ SECURE: ordering-asserting node hashing + panic-free verification
func (n *NodeHasher) HashNode(left, right *Node) []byte {
    if left.MaxNs().Compare(right.MinNs()) > 0 {   // HIGH fix: enforce ordering
        panicMarkOrError(errNamespaceOrdering)      // error, not silent accept
    }
    minNs, maxNs := left.MinNs(), left.MaxNs()
    if right.MaxNs().Compare(maxNs) > 0 { maxNs = right.MaxNs() }
    if n.ignoreMaxNS && maxNs.Equals(n.precomputedMaxNs) {
        maxNs = computeTrueMax(left, right)         // MEDIUM fix: never trust precomputed
    }
    return hashRange(minNs, maxNs, left.Hash(), right.Hash())
}

func (n *Nmt) VerifyInclusion(proof *Proof, namespace, dataHash) error {
    if len(proof.LeafHashes) == 0 { return ErrEmptyProof }  // MEDIUM fix: no panic path
    return n.verifyLeafHashes(proof, namespace, dataHash)
}
```

### Impact Analysis

- **Frequency**: 1 dedicated library audit (16 findings incl. 1 High, 5 Medium); companion rsmt2d/app audits
- **Severity Distribution**: HIGH: 1, MEDIUM: 5, LOW/INFO: rest — ALL RESOLVED
- **Affected Protocols**: celestiaorg/nmt consumers: celestia-app, celestia-core, light clients, QGB/bridges, rollup DA verifiers; any NMT fork
- **Validation Strength**: Strong (Informal Systems; upstream issue tracker linkage)

**Cross-references**: `validation/input-validation-vulnerabilities.md` (degenerate-input panics), `bridge/cross-chain-bridge-vulnerabilities.md` (DA bridges), `consensus/consensus-finality-vulnerabilities.md`.
