# VTW Stacks L1 Findings — DB Distillation Summary

**Date:** 2026-09-10
**Source corpus:** `reports/stacks-l1_findings/` (48 files; Immunefi Stacks Attackathon I (sbtc `immunefi_attackaton_0.9`, Dec 2024–Jan 2025) + Stacks Attackathon II (sbtc `immunefi_attackaton_1.0`, Mar 2025))
**Raw index:** `audit-output/vtw-stacks-l1_findings/raw-index.json` (37 indexed findings: 2 critical, 13 high, 9 medium, 5 low, 8 insight)
**Output:** `DB/unique/l1-misc/stacks/` (2 new entries; `stacks-signer-validation.md` already existed at `DB/unique/l1-misc/` — pattern not recreated) — `generate_manifests.py` intentionally NOT run per instructions.

## Cluster → Entry Mapping

| # | Cluster (by severity & frequency) | Source sev / count | Entry file |
|---|---|---|---|
| 1 | sBTC signer-set liveness sabotage via wsts signing-round manipulation (nonce-withhold stall, malformed-packet round abort, DKG OOB crash, deposit/withdrawal burst halts) | HIGH ×8 of 13 highs (largest cluster) | `sbtc-signer-liveness-wsts-round-sabotage.md` |
| 2 | Coordinator drains multi-sign wallet via unvalidated transaction construction (depositless BTC tx fee bypass, unchecked STX fee, duplicate contract calls, unannounced sweep) | CRITICAL ×1 + HIGH ×3 (all 4 direct fund-loss theft reports) | `sbtc-coordinator-unvalidated-transaction-drain.md` |

## Key Patterns Captured

- **Cluster 1 (liveness):** every report shares one root cause — the wsts threshold-signing pipeline trusts peer messages. Verified signals: nonce gathering accepts the first threshold responses "without checking the integrity of the nonces vector" (#38516); the nonce-providing set is hard-wired as the sig-share dependency so one withholder times out every round (#38053, with `cargo test` PoC); `wsts::process_message` turns a single peer's `gather_sig_shares` error into a round-wide `SignError` abort (#38477); `DkgPrivateShares` with empty share bytes OOB-crashes receivers after a signature-only check (#37814); unbounded public inputs wedge the network without any signer role — 500+ withdrawal calls in one Stacks tx cause request-decider FK violations (#40692, verified signer log) and a single BTC tx with 1,000+ dust deposits eats GBs of memory and crash-loops restarts (#42747). Siblings documented: #37811 (SignatureShareRequest length), #38111 (axum 2MB body limit vs block events), #42752 (libp2p DoS).
- **Cluster 2 (coordinator theft):** the corpus's direct-loss-of-funds reports all reduce to "signers validate deposits, not the transaction envelope". #38458 (critical): `to_input_rows` iterates `reports.deposits` for fee checks, so a depositless BTC tx bypasses *all* fee validation — "the attacker can cooperate with BTC miners to steal all BTC". #38392: no fee bound on coordinator-set STX contract-call fees. #38398: no duplicate-execution check → repeated fee bleed. #37479: coordinator executes signed sweeps without notifying peers → deposits swept with no sBTC minted, funds permanently locked (hardfork-class impact).
- **Distinct from the pre-existing `stacks-signer-validation.md`** (Coinfabrik Rust audit: vote replay / ack status confusion): both new entries cover the Immunefi attackathon corpus — wsts round design and coordinator transaction authorship — no overlap with the vote-nonce/ack-status pattern.
- **Left out (future passes):** clarity/smart-contract-layer findings are nearly absent from this corpus — it is almost entirely the Rust signer (`sbtc`); medium/insight buckets (9 medium, 8 insight) unminuted. The task brief's suggested "clarity contract asset handling / pox stacking" clusters do not exist as high-sev mass in this index; PoX is untouched by all 15 high+critical findings, which all target the sBTC signer.

## Verification Notes

- All 10 reference paths in the two entries verified to exist in `reports/stacks-l1_findings/` (directory holds 48 files; index lists 37 findings).
- Primary sources read with code excerpts (`validation.rs::to_input_rows`, `transaction_signer.rs::handle_stacks_transaction_sign_request`, `wsts::fire.rs`, `handle_wsts_message`) and PoCs/logs: #38458, #38392, #38398, #37479, #38053, #38477, #38516, #37814, #40692, #42747.
- Both entries follow TEMPLATE.md: full frontmatter (chain `stacks`, language `rust`, protocol `sbtc`), References table with verified paths, Agent Quick View, Contract/Boundary Map, Valid Bug Signals, FP Guards, Path A–D variants, 3 vulnerable Rust examples, 1 secure fix, grep seeds, audit checklist, report IDs, 25+ keywords.
- Cross-links: the two new entries reference each other and the pre-existing `DB/unique/l1-misc/stacks-signer-validation.md` (which in turn cites the other-l1 Coinfabrik bucket).
- `generate_manifests.py` NOT run, per instructions.
