# amm 2

> 80 nodes · cohesion 0.35

## Key Concepts

- **9. Asymmetric Base/Quote Treatment in Virtual Bonding Curve** (105 connections) — `DB/general/bonding-curve/BONDING_CURVE_MISC_VULNERABILITIES.md`
- **8. Collateral Depeg Cascading to Bonding Curve** (99 connections) — `DB/general/bonding-curve/BONDING_CURVE_MISC_VULNERABILITIES.md`
- **7. Unsafe Downcast Breaks Supply Invariant** (95 connections) — `DB/general/bonding-curve/BONDING_CURVE_MISC_VULNERABILITIES.md`
- **Secure Pattern 4: Protected Initialization** (87 connections) — `DB/amm/concentrated-liquidity/liquidity-management-vulnerabilities.md`
- **Secure Pattern 2: Dual Price Validation** (87 connections) — `DB/amm/concentrated-liquidity/price-oracle-manipulation.md`
- **Secure Pattern 3: sqrtPrice-Based Tick Derivation** (87 connections) — `DB/amm/concentrated-liquidity/price-oracle-manipulation.md`
- **Secure Pattern 4: Initialized Observation Check** (87 connections) — `DB/amm/concentrated-liquidity/price-oracle-manipulation.md`
- **10. Protocol Fees Stuck After Graduation** (87 connections) — `DB/general/bonding-curve/BONDING_CURVE_MISC_VULNERABILITIES.md`
- **11. Token Supply Not Correctly Burned on Graduation** (87 connections) — `DB/general/bonding-curve/BONDING_CURVE_MISC_VULNERABILITIES.md`
- **12. Graduation Stuck Due to Third-Party Contract Interference** (87 connections) — `DB/general/bonding-curve/BONDING_CURVE_MISC_VULNERABILITIES.md`
- **Secure Pattern 3: Fee-Adjusted LP Minting** (85 connections) — `DB/amm/concentrated-liquidity/liquidity-management-vulnerabilities.md`
- **Secure Pattern 1: TWAP Oracle with Proper Configuration** (85 connections) — `DB/amm/concentrated-liquidity/price-oracle-manipulation.md`
- **Secure Pattern 2: Per-Position Liquidity Accounting** (83 connections) — `DB/amm/concentrated-liquidity/liquidity-management-vulnerabilities.md`
- **Secure Pattern 1: Atomic Liquidity Verification** (81 connections) — `DB/amm/concentrated-liquidity/liquidity-management-vulnerabilities.md`
- **2. Stale TWAP Oracle Due to Unpoked Metapool** (81 connections) — `DB/general/bonding-curve/BONDING_CURVE_MISC_VULNERABILITIES.md`
- **3. Flash Loan Protection Bypass via Self-Liquidation** (79 connections) — `DB/general/bonding-curve/BONDING_CURVE_MISC_VULNERABILITIES.md`
- **4. Rebalance Rate Limiting Missing — Vault Drainage** (79 connections) — `DB/general/bonding-curve/BONDING_CURVE_MISC_VULNERABILITIES.md`
- **5. Wash Trading to Steal Keeper/Spot Trading Rewards** (79 connections) — `DB/general/bonding-curve/BONDING_CURVE_MISC_VULNERABILITIES.md`
- **6. Batch Operation Fails Atomically on Single Asset** (79 connections) — `DB/general/bonding-curve/BONDING_CURVE_MISC_VULNERABILITIES.md`
- **1. Oracle Price Denomination Mismatch (USD vs DAI) [CRITICAL]** (75 connections) — `DB/general/bonding-curve/BONDING_CURVE_MISC_VULNERABILITIES.md`
- **Vulnerability Title** (71 connections) — `DB/general/flash-loan/FLASH_LOAN_VULNERABILITIES.md`
- **1. ERC-677 `onTokenTransfer` Reentrancy During Liquidation [CRITICAL]** (57 connections) — `DB/general/reentrancy/defihacklabs-callback-reentrancy-2022-patterns.md`
- **2. Flash Loan Callback Reentrancy — Deposit-in-Callback [CRITICAL]** (53 connections) — `DB/general/reentrancy/defihacklabs-callback-reentrancy-2022-patterns.md`
- **3. ERC-1155 `onERC1155Received` Reentrancy During NFT Mint [CRITICAL]** (53 connections) — `DB/general/reentrancy/defihacklabs-callback-reentrancy-2022-patterns.md`
- **4. Native ETH/AVAX `receive()` Reentrancy — exitMarket/State Bypass [CRITICAL]** (51 connections) — `DB/general/reentrancy/defihacklabs-callback-reentrancy-2022-patterns.md`
- *... and 55 more nodes in this community*

## Relationships

- [defi](defi.md) (52 shared connections)
- [defi 6](defi_6.md) (32 shared connections)
- [protocol-specific 2](protocol-specific_2.md) (28 shared connections)
- [access-control 2](access-control_2.md) (18 shared connections)
- [defi 2](defi_2.md) (18 shared connections)
- [general 6](general_6.md) (18 shared connections)
- [general](general.md) (14 shared connections)
- [proxy 4](proxy_4.md) (7 shared connections)
- [defi 3](defi_3.md) (4 shared connections)
- [oracle](oracle.md) (3 shared connections)
- [oracle 2](oracle_2.md) (1 shared connections)

## Source Files

- `DB/amm/concentrated-liquidity/liquidity-management-vulnerabilities.md`
- `DB/amm/concentrated-liquidity/price-oracle-manipulation.md`
- `DB/general/bonding-curve/BONDING_CURVE_MISC_VULNERABILITIES.md`
- `DB/general/flash-loan/FLASH_LOAN_VULNERABILITIES.md`
- `DB/general/reentrancy/defihacklabs-callback-reentrancy-2022-patterns.md`

## Audit Trail

- EXTRACTED: 369 (29%)
- INFERRED: 924 (71%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*