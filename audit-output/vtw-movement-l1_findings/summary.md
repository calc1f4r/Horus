# VTW Movement L1 Findings — DB Entry Summary

**Date:** 2026-09-10
**Source index:** `audit-output/vtw-movement-l1_findings/raw-index.json` (99 indexed reports, 60 critical/high)
**Reports dir:** `reports/movement-l1_findings/` (all referenced files verified present)
**Output dir:** `DB/sui-move/movement-l1/` (new)

## Created entries (3)

| # | Entry | Severity | Cluster | Reports covered |
|---|-------|----------|---------|-----------------|
| 1 | `da-blob-unbounded-size-decompression-dos.md` | Critical | DA blob size/decompression unbounded → chain halt | 41489, 41334, 42143, 42233, 43114 (+43110 related) |
| 2 | `da-prevalidation-signature-bypass.md` | High (→Critical w/ 43307, 41531) | Conditional prevalidation / signature bypass on DA ingress | 41373, 41794, 41722, 43017, 43307 (+41531, 41714/15, 43323/24 related) |
| 3 | `grpc-no-timeout-fd-exhaustion.md` | Critical | gRPC services without TCP timeouts → FD exhaustion → sequencer crash | 43244, 43246, 43250, 43251 (+41368, 42102, 43177 related) |

All 14 primary report references verified to exist on disk (1 initial check-loop typo for 43251; the entry itself references the correct `...-finality-viewer.md` filename, which exists).

Each entry follows the DB template: frontmatter (protocol/chain/language, category, vulnerability_type, root_cause_family, pattern_key, attack_type, affected_component, primitives, code_keywords, severity, impact) + References + Agent Quick View + Contract/Boundary Map + Valid Bug Signals + False Positive Guards + Examples (code from reports) + Fix + Keywords.

## Remaining clusters (future work)

Prioritized by clarity × severity from the 60 crit/high index entries:

1. **Mempool sequence-number / duplicate-tx invariants** (~8 reports: 41437, 41466, 41878, 42011, 42762, 42896, 42903, 42991, 43222, 43136) — edge cases break `sequence_number` tracking, duplicate admission, seq-0 replay. High/critical.
2. **Sequencer/DA economics — sequencer wallet + TIA drain** (41531, 43241, 43253, 42513) — attacker forces sequencer/nodes to pay DA gas. Critical.
3. **DA light-node batch/range validation gaps** (43315, 43322, 43323, 43324, 43330, 43177, 43110) — unbounded height, missing batch validation, malicious override of priority. Critical/high.
4. **Consensus/execution ordering — chain split & divergence** (41012, 41987, 42298, 42749, 43333, 42941) — out-of-order Celestia block execution, oversized blocks split chain, replay via blob verification, typelayout depth divergence. Critical.
5. **Transaction tampering / ID & priority manipulation** (41714, 41715, 42395, 43229) — partially covered by entry 2 (related list); standalone entry optional.
6. **Blocking-in-async / deadlock / panic liveness bugs** (41255, 42936, 42934, 42837) — thread pool exhaustion, concurrent lock deadlock in TransactionPipe, keyless signature panic. Critical/medium.
7. **Gas pool / refunds / stuck funds** (42930, 42513) — users unable to raise gas, storage refund loss. High.
8. **Passthrough-mode DA correctness** (41686, 41722*, 43241) — streams txs instead of blocks; partial overlap with entries 2. High.

(* = already cited as related in a created entry.)

## Notes

- Severity mix in source: 30 critical / 30 high of 99 indexed (rest insight/medium).
- `generate_manifests.py` intentionally NOT run per task instructions.
- Language field set to `move` per instructions even though findings are largely in Rust infra components (protocol: movement, chain: movement) — consistent with sibling DB conventions seen in `DB/eth-l1-clients/`.
