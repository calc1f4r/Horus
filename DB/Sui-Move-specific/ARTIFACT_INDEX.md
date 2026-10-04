# Sui/Move Findings — Artifact Index

This document indexes all downloaded audit report artifacts referenced by the
69 Sui/Move vulnerability findings in `reports/sui_move_findings/`.

## Downloaded Artifacts Summary

| # | Filename | Source | Type | Referenced By |
|---|----------|--------|------|---------------|
| 1 | `certificate.quantstamp.com-full-report-2.html` | Quantstamp — Dipcoin Perpetual | HTML | missing-on-chain-zk-proof-verification, denial-of-service-in-several-functions-due-to-object-limits |
| 2 | `github.com-AftermathFinance-aftermath-core-.html` | AftermathFinance GitHub Repo | HTML | missing-owner-check, incorrect-price-calculation, risk-of-arithmetic-overflow, missing-invariant-checks, price-manipulation |
| 3 | `certificate.quantstamp.com-full-report-4.html` | Quantstamp — Dipcoin Vault | HTML | denial-of-service-in-several-functions-due-to-object-limits |
| 4 | `github.com-Bucket-Protocol-v1-periphery-2f6.html` | Bucket Protocol v1 Periphery GitHub | HTML | users-unable-to-claim-surplus, precision-loss-in-redistribution, improper-stake-update, improper-tank-value-update, improper-conversion |
| 5 | `github.com-MystenLabs-deepbookv3-77d3d535.html` | MystenLabs DeepBook V3 GitHub | HTML | bigvector-size-overflow, incorrect-base-quantity-calculation, improper-order-quantity-calculation, volume-overflow-risk, trade-proof-bypass, denial-of-service-due-to-excessive-gas-consumption |
| 6 | `sherlock-contest-857.html` | Sherlock Contest #857 — ZetaChain | HTML | h-2, m-1, m-5, m-6, m-11, m-12, m-24, m-25 (all ZetaChain findings) |
| 7 | `github.com-Bucket-Protocol-v1-periphery-2f6.html` (dup) | Bucket Protocol GitHub | HTML | (same as #4) |
| 8 | `certificate.quantstamp.com-full-report-3.html` | Quantstamp — Bucket Protocol V2 | HTML | security-level-constraint-can-be-circumvented |
| 9 | `github.com-AftermathFinance-aftermath-core-.html` (dup) | Aftermath Finance GitHub | HTML | (same as #2) |
| 10 | `github.com-MystenLabs-deepbookv3-77d3d535.html` (dup) | MystenLabs DeepBook V3 GitHub | HTML | (same as #5) |
| 11 | `github.com-volo-sui-volo-liquid-staking-2f4.html` | Volo Liquid Staking GitHub | HTML | restake-sui, include-pending-in-unstake, round-up-shares |
| 12 | `github.com-MystenLabs-sui-3c59aa0b.html` | MystenLabs Sui Core GitHub | HTML | bypass-id-leak-verifier, dynamic-field-hash-collision, modules-digest-collision, blocking-user-funds-in-kiosk, potential-overflow-in-threshold, rpc-node-crashes, arbitrary-update-of-last-epoch-mixed, incorrect-value-in-record-name, absence-of-checks-for-max-ttl, mixing-over-limit-suifrens, rounding-errors-result-in-lost-accrued-rewards |
| 13 | `github.com-axelarnetwork-axelar-cgp-sui-3c5.html` | Axelar CGP Sui GitHub | HTML | utilization-of-incorrect-flow-tracking, incorrect-function-call |
| 14 | `consensys.io-diligence-audits-2023-07-solfl.html` | ConsenSys Diligence — Solflare Sui Snap | HTML | All 7 wallet/snap findings |
| P1 | `1-certificate.quantstamp.com-full-report-2.pdf` | Quantstamp Dipcoin Perpetual PDF | PDF | same as #1 |
| P2 | `8-certificate.quantstamp.com-full-report-3.pdf` | Quantstamp Bucket V2 PDF | PDF | same as #8 |

## Auditor Coverage

| Auditor | Reports | Protocols Covered |
|---------|---------|-------------------|
| OtterSec | 54 | Cetus, BlueFin, Aftermath, Bucket, DeepBook, Turbos, Volo, Lombard, Security Token, Mysten Labs Sui Core, Sui Bridge, Axelar |
| Sherlock (ZetaChain contest) | 8 | ZetaChain Sui Integration |
| ConsenSys Diligence | 7 | Solflare Sui Snap |
| Quantstamp | 3 | Dipcoin Perpetual, Dipcoin Vault, Bucket Protocol V2 |

## Protocol Coverage

| Protocol | # Findings | Severity Range | DB Entry |
|----------|-----------|----------------|----------|
| Mysten Labs Sui Core | 12 | MEDIUM–HIGH | Object Model, Arithmetic |
| BlueFin | 6 | MEDIUM–HIGH | Arithmetic, Access Control, DeFi Logic |
| DeepBook V3 | 5 | MEDIUM–HIGH | Arithmetic, Access Control, DeFi Logic |
| Bucket Protocol | 6 | MEDIUM–HIGH | DeFi Logic, Access Control |
| Aftermath Finance | 5 | MEDIUM–HIGH | Access Control, DeFi Logic, Arithmetic |
| Cetus CLMM | 4 | MEDIUM–HIGH | Arithmetic, Access Control |
| ZetaChain | 8 | MEDIUM–HIGH | Cross-Chain Bridge |
| Solflare Sui Snap | 7 | MEDIUM–HIGH | Wallet/Snap Security |
| Volo Liquid Staking | 3 | MEDIUM–HIGH | DeFi Logic |
| Sui Bridge | 3 | MEDIUM–HIGH | Object Model, Cross-Chain |
| Axelar CGP Sui | 2 | MEDIUM–HIGH | DeFi Logic, Cross-Chain |
| Turbos Finance | 2 | MEDIUM | DeFi Logic, Access Control |
| Dipcoin | 3 | MEDIUM–HIGH | Access Control, Object Model |
| Lombard | 1 | MEDIUM | Access Control |
| Security Token | 3 | MEDIUM–HIGH | Arithmetic, Access Control |
| Bluefin Spot | 1 | MEDIUM | DeFi Logic |

## Artifact Location

All artifacts are stored in:
```
reports/sui_move_findings/artifacts/
```

Additional manifest files:
- `download_manifest.json` — Complete URL-to-file mapping with success/failure status
- `candidate_links.csv` — All candidate audit report URLs extracted from findings
- `summary.txt` — Download session summary
