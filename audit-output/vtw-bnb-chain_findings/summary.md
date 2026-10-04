# bnb-chain Findings → DB Extraction Summary

**Date:** 2026-09-10 · **Operator:** vtw subagent · **Corpus:** `reports/bnb-chain_findings/` (7 reports) · **Index:** `audit-output/vtw-bnb-chain_findings/raw-index.json`

## What was done

Read all 7 source reports in full, extracted root-cause-distinct vulnerability patterns, and wrote 5 DB entries under `DB/bnb-chain/` following `TEMPLATE.md` (frontmatter + References + Quick View + boundary map + signals + FP guards + path variants + vulnerable/secure examples + detection patterns + keywords).

## Entries created

| # | File | Source report(s) | Severity | Core pattern |
|---|------|------------------|----------|--------------|
| 1 | `DB/bnb-chain/consensus/geth-inherited-bsc-audit-findings.md` | truesec geth audit 2017 | HIGH (cluster) | Insecure defaults & fragile implicit checks in geth inherited by bsc: CORS allow-all default (`newCorsHandler` empty `AllowedOrigins` → rs/cors allow-all, commit 5e29f4b), peer-controlled 16.8MB RLPx frame allocs, divide-by-zero `qosReduceConfidence`, negative-tx-value guarded only by RLP encoding in block processing, intPool memory abuse, weak PRNG seed fallback, ethash race |
| 2 | `DB/bnb-chain/tokens/stkbnb-redemption-accounting.md` | Halborn Persistence stkBNB 2022 (HAL-01..05) | MEDIUM | Claim pipeline guards wrong ledger (`address(this).balance` vs `_claimReserve`) → revert DoS; FeeVault→StakePool fee lock; admin `selfDestruct` with user funds; uint256→int256 unsafe casts; `.transfer` 2300-gas payout |
| 3 | `DB/bnb-chain/tokens/bnbx-staking-derivative.md` | Halborn Stader BnbX 2022 (HAL-01..04) | HIGH | Operator-inflatable pool total (`totalRedelegated` in `getTotalPooledBnb`) desyncs mint/burn conversions → `totalDeposited -= totalBnbToWithdraw` underflow freezes ALL exits; first-depositor 0-share mint via `? 1 : x` clamps; missing `_disableInitializers`; zero-address gaps |
| 4 | `DB/bnb-chain/defi/launchpool-deposit-validation.md` | PeckShield BSCStation 2021 (PVE-001..007) + PinkSale deflationary sibling | MEDIUM | ERC20-inherited staking LP with unhooked `_transfer` → `userInfo.amount` shadow-ledger desync → both transfer parties locked out of withdraw + stranded rewardDebt; reward-config mutators skip `_updatePool()` checkpoint; raw `transfer()` on non-compliant tokens; unbounded `unStakingFee` |
| 5 | `DB/bnb-chain/defi/pinksale-subscription-access.md` | PeckShield PinkSale 2022 (PVE-001..004) | MEDIUM | `updateCalculatedData(users[], amounts[])` = ungoverned bulk rewrite of post-commitment allocations (no event/timelock/bounds); `setCanFinalize` force-finalize; raw `IERC20.approve` breaks USDT-class tokens in `_lockLiquidity`/`addLiquidity`; deflationary currency book desync |

## Skipped

- **`consensus/parlia-fast-finality-considerations.md` — SKIPPED (no evidence).** Grep for `parlia|finality|Parlia` across `reports/bnb-chain_findings/` returned 0 hits. The corpus (2017-2022 launchpad/LSD audits + geth client audit) contains no Parlia/fast-finality content. Per task rule: create only if evidence exists.
- **BSCEX Launchpadx report** (Halborn 2021: missing address check, ignored return values — all LOW/INFO) had no root cause distinct from patterns already covered in entries 4 and 5; folded the zero-address/return-value classes into those entries rather than duplicating.

## Verification notes

- All 5 reference paths in the References tables point to files that exist under `reports/bnb-chain_findings/` (verified via directory listing).
- Severity/likelihood/impact figures and code snippets taken verbatim from source reports (line numbers preserved where cited: e.g. StakePool L781-793, StakeManager L265-288/L426-441, SubscriptionPool L3200-3208/L3552-3568).
- Frontmatter `chain: bsc`, `language: solidity|go` (go for the geth-inherited entry, solidity for the other four).
- Remediation status preserved from sources: stkbnb fixed @ d059bcc, bnbx fixed @ d56ab58 + 4e04e46, BSCStation fixed @ 1dd2057 (+7d905b7), PinkSale PVE-002 fixed (MD5 799c117f) / others confirmed.

## Not done (per instructions)

- `generate_manifests.py` NOT run (explicitly excluded from task scope).

## Low/Info residual + missed-report fold (2026-09-11)

- bscex launchpadx (3 rows) + launchpoolx (4 LOW) folded into defi/launchpool-deposit-validation; corpus now fully cited
