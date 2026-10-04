# VTW other-l1_findings — Triage Summary

Tracks triage of `raw-index.json` (~8,200 lines) into `DB/unique/l1-misc/` knowledge-base entries.

## Status: 9 entries written from this corpus

| # | Entry | Chain | Sources (verified under `reports/other-l1_findings/`) | Max sev |
|---|-------|-------|--------------------------------------------------------|---------|
| 1 | near-aurora-rainbow-bridge-light-client.md | NEAR/Aurora | (prior batch) | high |
| 2 | near-burrow-margin-accounting.md | NEAR | (prior batch) | high |
| 3 | aptos-move-fund-pending-transactions.md | Aptos | (prior batch) | high |
| 4 | aptos-move-prover-notes.md | Aptos | (prior batch) | — |
| 5 | **avalanche-node-validation.md** | Avalanche | Least Authority bridge audit 2023-07 (Issues A–D verified from ToC); ToB avalanchego 2025-08 (high/DoS, metadata-verified); OZ warp-messaging 2023-11 (index-verified, resolved) | high (ToB node DoS) |
| 6 | **polygon-bor-heimdall-validation.md** | Polygon | Least Authority bor/heimdall feature-milestones 2023-07 (Issue A + Suggestions 2/4/6 verified from ToC); bor-claude-rules consensus/contract-interaction files (index-verified) | high (family) |
| 7 | **zcash-librustzcash-tx-builder.md** | Zcash | Zellic librustzcash 2026-07 (all 5 findings §3.1–3.5 verified verbatim from contents: ZIP-233 burn drop, merkle_path_from_slice panic, empty-vs-absent transparent bundle txid divergence, Orchard-on-V4 version bypass, nu7 w/o zip-233 invalid V6); bucket also has ironwood/sapling/zakura Zellic + 3 ToB reviews | low×4+info (integrator impact) |
| 8 | **stacks-signer-validation.md** | Stacks | Coinfabrik stacks-signer 2025-04 (ToC-verified: 4 critical/4 high/6 medium, HI-01 Replay Attack on Vote); sibyl audit 2025-02 (index-verified) | critical |
| 9 | — | — | — | — |

## Chain buckets in raw index (audit-relevant)

- **avalanche**: 3 subnet-evm/graft audits (Least Authority ×2, OpenZeppelin ×1) + ToB avalanchego 2025 → covered by entry 5
- **polygon bor/heimdall**: feature-milestones audit + 7 bor-claude-rules internal files → covered by entry 6
- **zcash**: 8 findings — librustzcash, ironwood, sapling, zakura (Zellic), 3 ToB reviews, security-warnings doc → covered by entry 7 (largest non-EVM bucket; zcash chosen over cardano/fuel per 2+ findings rule)
- **stacks**: signer audit 2025-04 (critical bucket) + sibyl 2025-02 → covered by entry 8
- **cardano**: 1 finding only (cardano-ledger-security-md) — below 2+ threshold, skipped
- **fuel**: only irrelevant matches (fuelonblast, fuelet wallet, powertrade-fuel) — no core Fuel L1 findings, skipped
- **aptos**: 5 findings (2 hybrid/lean docs, prover PDFs ×2, VM security doc) → covered by entries 3–4 (prior batch)
- **near**: covered by entries 1–2 (prior batch)
- **dusk**: rusk-consensus audit 2024-09 (gas sev) — remaining candidate
- **cosmos-ish (milkyway, incrementfi, celer)**: app-level, not L1 core — out of l1-misc scope

## Remaining candidates (not yet written)

- dusk rusk-consensus (verify_new_block) — 1 finding
- ToB edera container-runtime review — not L1
- ToB near-one confidential-key-derivation — NEAR-adjacent, check overlap with entries 1–2

## Notes

- Source PDFs under `reports/other-l1_findings/` are word-per-line extractions; entries cite the strongest verified fragments (ToC/finding lists) and mark metadata-only basis explicitly in each References table.
- `generate_manifests.py` intentionally NOT run (per task instruction).

## Low/Info residual + missed-report fold (2026-09-11)

- MISSED-sec-tier recovered (extraction pipeline had skipped these): chromatic (4C/2H/2M/3L/5I), lybra v2 (2H/5M/6L/3I -> l1-staking), strike (6M/4L/7I), pirate-nation (2C/5H/4M/3L/9I), irrigation (2C/4M/1L/2I) -> l1-contracts/l1-staking
- executive summaries folded as aggregate rows: bracket-fi passage (6C/3M/6I stated, redacted), c3-pyteal (2H/3M/3L/10I stated), trust-wallet barz (severities unstated)
- Nethermind Low/Info: polygon-id nm0069 (2L), polygonid nm0113 (1M/8L), token-bridge nm0544b (1L), renzo nm0472 (4I+2BP) -> l1-contracts/l1-bridges/l1-access-control
- verified clean (0 findings): matterlabs-verifier x2, tenet-llsd, grandine-matterlabs
- remaining uncited: dead Immunefi pages, docs/security.md guides, .pdf binaries of cited .md twins
