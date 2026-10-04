
## Completion pass (substrate-l1)

- created: 7
  - DB/substrate/pallets/unbounded-iteration-dos.md
  - DB/substrate/pallets/rounding-issuance-math.md
  - DB/substrate/pallets/lending-liquidation.md
  - DB/substrate/pallets/vault-deposit-accounting.md
  - DB/substrate/pallets/token-balance-accounting.md
  - DB/substrate/pallets/error-handling-state-consistency.md
  - DB/substrate/pallets/missing-validation.md
- updated: 11
  - DB/substrate/pallets/xcm-instruction-validation.md
  - DB/substrate/pallets/crowdloan-refund-manipulation.md
  - DB/substrate/pallets/staking-unlock-relock-double-spend.md
  - DB/substrate/pallets/governance-origin-confusion.md
  - DB/substrate/oracle/ema-oracle-manipulation.md
  - DB/substrate/amm/omnipool-liquidity-math.md
  - DB/substrate/bridges/grandpa-light-client-validation.md
  - DB/substrate/crypto/sr25519-signature-verification.md
  - DB/substrate/lifecycle/runtime-upgrade-storage-migration.md
  - DB/substrate/pallets/origin-authorization-bypass.md
  - DB/substrate/lifecycle/runtime-upgrade-storage-migration.md
- leftover findings not bucketed: 43 (kept in buckets.json)

## Completion pass (substrate-l1)

- created: 1
  - DB/substrate/pallets/fee-handling.md
- updated: 18
  - DB/substrate/pallets/xcm-instruction-validation.md
  - DB/substrate/pallets/crowdloan-refund-manipulation.md
  - DB/substrate/pallets/staking-unlock-relock-double-spend.md
  - DB/substrate/pallets/governance-origin-confusion.md
  - DB/substrate/oracle/ema-oracle-manipulation.md
  - DB/substrate/amm/omnipool-liquidity-math.md
  - DB/substrate/bridges/grandpa-light-client-validation.md
  - DB/substrate/crypto/sr25519-signature-verification.md
  - DB/substrate/lifecycle/runtime-upgrade-storage-migration.md
  - DB/substrate/pallets/unbounded-iteration-dos.md
  - DB/substrate/pallets/rounding-issuance-math.md
  - DB/substrate/pallets/origin-authorization-bypass.md
  - DB/substrate/pallets/lending-liquidation.md
  - DB/substrate/pallets/vault-deposit-accounting.md
  - DB/substrate/pallets/token-balance-accounting.md
  - DB/substrate/lifecycle/runtime-upgrade-storage-migration.md
  - DB/substrate/pallets/error-handling-state-consistency.md
  - DB/substrate/pallets/missing-validation.md
- leftover findings not bucketed: 61 (kept in buckets.json)

## Low/Info residual + missed-report fold (2026-09-11)

- acala-trailofbits + publications-reviews-acalanetwork (dupe): 11 ToB findings folded (Docker config, sudo, transfer-max fee burn, CSRF dapp, etc.) into pallets/missing-validation, fee-handling, unbounded-iteration-dos
- alephbft-tob + publications-reviews-alephbft (dupe): 9 ToB findings folded (async error handling LOW, rollback/hooks/channel errors, blocking I/O)
- MISSED-sec-tier recovered: picasso-cosmos (4H/3M/4L), mantis escrow bridge CodeZen (7H/5M/10L), ottersec solana-ibc-avs (3C/2H/1L), solana-restaking-v2 draft (3C/3H/1M/2L), solana-bridge draft (3C/3H/1M/2L) -> vault-deposit-accounting, staking-unlock-relock, rounding-issuance-math, error-handling, missing-validation
- skipped: thorchain-bifrost-utxo (Zellic, 0 findings), 51 .pdf binaries whose .md twins are cited (8 twins also uncited: mantis/picasso/ottersec x2/solana-bridge/acala/alephbft — all now folded)
