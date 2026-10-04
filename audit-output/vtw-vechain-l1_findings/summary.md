# VTW VeChain L1 Findings — DB Distillation Summary

**Date:** 2026-09-10
**Source corpus:** `reports/vechain-l1_findings/` (124 files; Immunefi VeChain Hayabusa Upgrade Attackathon + VeChain/Stargate Hayabusa audit competition)
**Raw index:** `audit-output/vtw-vechain-l1_findings/raw-index.json` (1 critical, 69 high, 8 medium, 33 insight, 13 low)
**Output:** `DB/unique/l1-misc/vechain/` (5 entries) — `generate_manifests.py` intentionally NOT run per instructions.

## Cluster → Entry Mapping

| # | Cluster (by severity & frequency) | Source sev / count | Entry file |
|---|---|---|---|
| 1 | Same-period delegation + validator exit → `SubPendingVet` underflow, permanent freeze (native thor staker) | CRITICAL ×1 | `vechain-same-period-delegation-frozen-on-validator-exit.md` |
| 2 | Post-exit reward over-claim / off-by-one in `_claimableDelegationPeriods` (Stargate.sol) | HIGH ×~20 | `vechain-post-exit-delegation-reward-drain-off-by-one.md` |
| 3 | Double effective-stake decrement across exit + unstake flows (Stargate.sol) — largest high-sev cluster | HIGH ×~30 | `vechain-double-effective-stake-decrement-unstake-freeze.md` |
| 4 | First reward period lost when delegating to PENDING validators (`lastClaimedPeriod` init off-by-one) | HIGH ×2 | `vechain-pending-validator-first-period-reward-loss.md` |
| 5 | Native builtin gas undercharge post-HAYABUSA fork (`native_isEndorsed` uncharged SLOADs; metering family) | INSIGHT ×5+ (shutdown-class impact) | `vechain-native-builtin-gas-undercharge-post-fork.md` |

## Key Patterns Captured

- **Lifecycle-race accounting (cluster 1):** branch predicates (`Delegation.Started()`) computed from exit-frozen counters while shared aggregates (`aggregation.Pending`) are independently reset by housekeeping → orphaned pending entries → underflow freeze. Hardfork-class fix.
- **Boundary-condition reward math (clusters 2 & 4):** one reward cursor (`lastClaimedPeriod`) mishandles both ends of the delegation lifecycle — strict `endPeriod > next` inequality lets exited NFTs farm future periods indefinitely; `+1` initialization at delegate-time skips the first active period for pending validators.
- **Duplicate state mutation (cluster 3):** `_updatePeriodEffectiveStake(..., false)` reachable from both `requestDelegationExit` and the `unstake` EXITED/PENDING branch without a once-guard → panic 0x11 → permanent unstake freeze. Largest cluster (~30 near-duplicate highs).
- **Fork-drifting gas schedules (cluster 5):** hardcoded entry-point `UseGas` lumps vs post-fork callee storage reads (`GetValidation` inside `TransitionPeriodBalanceCheck`) → ≥16.7% undercharge per endorsement check; per-block frequency during PoA→PoS transition.

## Verification Notes

- All 5 entries reference report files verified to exist in `reports/vechain-l1_findings/`; primary reports (55632, 59563, 60311, 59657, 56454) were read in full/near-full, including code excerpts and PoCs.
- One index filename was truncated (`59802-…delegato.md`); actual file `…delegators.md` located via directory listing and used in the references table.
- All entries follow TEMPLATE.md: full frontmatter (protocol/chain/category/root_cause_family/pattern_key/interaction_scope/path_keys/primitives/code_keywords/severity/impact), References table, Agent Quick View, Contract/Boundary Map, Valid Bug Signals, FP Guards, 3 vulnerable examples, 2 fixes, detection/grep seeds, checklist, real-world reports, 15+ keywords.
- Language field: entries 2–4 `solidity` (Stargate.sol); entries 1 & 5 are Go (thor native builtins) with explicit inline note, since VeChain L1 builtin logic is Go but reachable via the EVM-dialect extension ABI.

## Residual Corpus (not distilled here)

~40 remaining highs are near-duplicates of clusters 2–3 (listed as variant report IDs inside the entries' Related sections). Remaining insights/mediums/low cover: RPC null-body crash, P2P header-validation DoS, finality 2/3 threshold strictness, DPoS threshold switch undercount, renewallist bloat, totalSupply semantics, uint64 `checkStake` overflow (medium #55957), housekeeping goroutine panic, inactive-validator scheduling bypass.

## Residual fold (2026-09-11)
- 3 live Immunefi reports folded (57136 BC-Low txpool priority cache, 56345 BC-Insight finality freeze -> node-consensus-endpoints; 56256 BC-Insight redundant sload -> contracts-staking); corpus now fully cited
