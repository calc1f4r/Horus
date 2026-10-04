# VTW Plume L1 Findings — DB Distillation Summary

**Date:** 2026-09-10
**Source corpus:** `reports/plume-l1_findings/` (351 files; Immunefi Plume Network Attackathon, Jul–Aug 2025)
**Raw index:** `audit-output/vtw-plume-l1_findings/raw-index.json` (11 critical, 130 high, 38 medium, 113 low, 59 insight)
**Output:** `DB/unique/l1-misc/plume/` (2 entries) — `generate_manifests.py` intentionally NOT run per instructions.

## Cluster → Entry Mapping

| # | Cluster (by severity & frequency) | Source sev / count | Entry file |
|---|---|---|---|
| 1 | Validator commission checkpoint/settlement accounting failures (missing add-time checkpoint → retroactive rate application; ceil-vs-floor rounding; permissionless micro-settlement; commission frozen on removed reward tokens) | CRITICAL ×1 + HIGH ×~50 (largest high cluster) | `plume-validator-commission-checkpoint-accounting.md` |
| 2 | ArcToken batched yield distribution without snapshots (live balances + mutable holders set across batches → double-dip/omission; division-remainder lock) | HIGH ×~30 (second-largest cluster) | `plume-arctoken-batched-yield-distribution.md` |

## Key Patterns Captured

- **Cluster 1 (commission accounting):** the critical (#53037) comes from `addValidator()` setting only the `commission` scalar with no checkpoint, so `getEffectiveCommissionRateAt()` falls back to the *current* rate for past intervals — a validator that later cuts its rate retroactively raises historical staker payouts (validator–staker collusion). Siblings: one-sided settlement on `setValidatorCommission`/`setMaxAllowedValidatorCommission` (#53070), ceil-for-users/floor-for-validators rounding drift (#53072, #53061), permissionless `forceSettleValidatorCommission()` at tiny timeDelta zeroing accrual (#51961), and `_validateIsToken` on `requestCommissionClaim()` freezing commission on removed reward tokens (#50924 + ≥7 near-duplicates).
- **Cluster 2 (batched yield):** `distributeYieldWithLimit` walks a mutable EnumerableSet of holders reading live `balanceOf` and recomputing `effectiveTotalSupply` per batch, with no epoch snapshot, no claim-once tracking, and no remainder sweep. Verified loss model from #49710: max loss ≈ (batches − 1) × attacker balance × yield-per-token; #52371 adds swap-and-pop index omission + tail re-append double-pay; #52798 shows per-batch remainders permanently locked (unbatched sibling handles them correctly).
- **Notable clusters intentionally left out (documented for future passes):** ArcToken factory upgrade-control chaos (DEFAULT_ADMIN_ROLE/UPGRADER_ROLE self-grant, ~12 highs incl. #50784, #50822, #52649); jackpot/streak eligibility stale-read family (~10 highs, e.g. #50796, #52601); unrestricted `stakeOnBehalf` gas-griefing family (~6 highs, e.g. #50433, #52573); DEX-aggregator partial-fill residuals (4 criticals: #49854, #49863, #52923, #52980, #53011, #53022 class).

## Verification Notes

- All 12 reference paths in the two entries verified to exist in `reports/plume-l1_findings/` (directory holds exactly 351 files, matching the index).
- Primary sources read with code excerpts and PoC steps: #53037, #53070, #53072, #51961, #50924 (entry 1); #49710, #52371, #51558, #52798 (entry 2).
- Note: the task brief suggested "RWA tokenization compliance/access" and "oracle/price feed" as candidate clusters; the actual index shows the high-severity mass concentrated in staking-commission accounting and batched-yield distribution (the RWA-relevant surfaces), so the top-2 clusters by severity × frequency were distilled instead. Oracle content is limited to a single callback-timing finding (#51218); upgrade-access control is large but was ranked third.
- Both entries follow TEMPLATE.md: full frontmatter (protocol `plume`, chain `plume`, root_cause_family, pattern_key + path_keys, interaction_scope, involved_contracts, primitives, grep-able code_keywords, severity/impact), References table with verified paths, Agent Quick View, Contract/Boundary Map, Valid Bug Signals, FP Guards, Path A/B/C variants, 3 vulnerable examples, 1 secure fix, detection/grep seeds, audit checklist, real-world report IDs, 20+ keywords.
- Language field: `solidity` on both entries (Plume is an EVM L1 for RWA tokenization; all findings target `plume/src` and `arc/src` Solidity).
- `generate_manifests.py` NOT run, per instructions.

## Residual fold (2026-09-11)
- 51352 Immunefi CRITICAL (1inch partial-swap unspent-amount loss) folded into plume/rwa-token-deposit; remaining uncited file verified dead page
