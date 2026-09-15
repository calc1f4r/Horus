# Flare FAssets L1 Findings — DB Entry Summary

**Date:** 2026-09-10 · **Source corpus:** `reports/flare-l1_findings/` (120 files, Immunefi Audit Comp | Flare | FAssets, mainnet OR audit, May 2025; 17 high / 19 medium / 32 low / 39 insight) · **Index:** `audit-output/vtw-flare-l1_findings/raw-index.json`

## Entries written (3) — `DB/unique/l1-misc/flare/`

| # | File | Cluster | Sev (source) | Source reports |
|---|------|---------|--------------|----------------|
| 1 | `fassets-collateral-pool-unverified-reward-claim.md` | Attestation/agent collateral management | HIGH (#45893) | [45893] verified read |
| 2 | `fassets-minting-payment-default-forged-attestation.md` | Attestation proof verification (minting default fraud) | HIGH (#45904) | [45904] verified read |
| 3 | `fassets-execute-minting-executor-fee-hijack.md` | Minting execution race (executor fee theft/DoS) | MEDIUM (#45447) | [45447] verified read |

## Cluster takeaways

- **Agent collateral management (#45893):** `CollateralPool.claimAirdropDistribution/claimDelegationRewards` credit an agent-supplied external `.claim()` return value into `totalCollateral` with no balance-delta or token check. PoC drains the entire pool via early `exit()`. Family: `missing_validation` on external return values feeding shared accounting.
- **Attestation criteria bypass (#45904):** `mintingPaymentDefault`'s source-address guard (`checkSourceAddresses`/`sourceAddressesRoot`) degenerately passes for non-handshake reservations (zero root) with a proof over the impossible source `bytes32(0)` — FDC confirms "no payment from 0x00..0". Agent forces a default despite valid payment, keeps underlying + fee. Family: `flawed_boolean_validation` / sentinel-value confusion in cross-chain attestation verification. Mitigation: add `crt.sourceAddressesRoot != bytes32(0)` to the checked branch.
- **Minting execution race (#45447):** executor fee pushed via `Transfers.transferNAT` with hardcoded 100k gas stipend; contract executors revert permanently, and agents (allowed callers via permission disjunction) front-run executors so the "unclaimed" fee lands in the agent's own collateral pool via `distributeCollateralReservationFee`. Family: `hardcoded_gas_allowance` + fee-fallback conflict of interest. Fix direction: pull-based executor fees.

## Cross-cluster compound risk

The three entries chain: gas-griefed executors (#45447) leave paid-but-unproven mintings open longer, which is exactly the window a malicious agent needs to submit forged non-payment proofs (#45904); extracted value accrues to agent collateral pools whose accounting can be independently inflated (#45893). All three require a malicious/compromised Agent — a single trusted-role compromise yields layered theft paths.

## Process notes

- All References tables point at verified-read files in `reports/flare-l1_findings/` with Immunefi source links.
- Each entry: TEMPLATE.md frontmatter (chain `flare`, language `solidity`), Agent Quick View, Contract/Boundary Map, Valid Bug Signals, FP guards, 3 real code examples drawn from the source reports, 1 secure fix, detection/grep seeds, 15+ keywords.
- `generate_manifests.py` intentionally NOT run (per task instruction).
