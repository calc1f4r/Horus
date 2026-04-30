# amm

> 116 nodes · cohesion 0.23

## Key Concepts

- **9. Asymmetric Base/Quote Treatment in Virtual Bonding Curve** (87 connections) — `DB/general/bonding-curve/BONDING_CURVE_MISC_VULNERABILITIES.md`
- **Secure Pattern 3: sqrtPrice-Based Tick Derivation** (81 connections) — `DB/amm/concentrated-liquidity/price-oracle-manipulation.md`
- **8. Collateral Depeg Cascading to Bonding Curve** (81 connections) — `DB/general/bonding-curve/BONDING_CURVE_MISC_VULNERABILITIES.md`
- **7. Unsafe Downcast Breaks Supply Invariant** (77 connections) — `DB/general/bonding-curve/BONDING_CURVE_MISC_VULNERABILITIES.md`
- **Secure Pattern 2: Per-Position Liquidity Accounting** (73 connections) — `DB/amm/concentrated-liquidity/liquidity-management-vulnerabilities.md`
- **2. Stale TWAP Oracle Due to Unpoked Metapool** (73 connections) — `DB/general/bonding-curve/BONDING_CURVE_MISC_VULNERABILITIES.md`
- **Secure Pattern 2: Dual Price Validation** (71 connections) — `DB/amm/concentrated-liquidity/price-oracle-manipulation.md`
- **3. Flash Loan Protection Bypass via Self-Liquidation** (71 connections) — `DB/general/bonding-curve/BONDING_CURVE_MISC_VULNERABILITIES.md`
- **4. Rebalance Rate Limiting Missing — Vault Drainage** (71 connections) — `DB/general/bonding-curve/BONDING_CURVE_MISC_VULNERABILITIES.md`
- **5. Wash Trading to Steal Keeper/Spot Trading Rewards** (71 connections) — `DB/general/bonding-curve/BONDING_CURVE_MISC_VULNERABILITIES.md`
- **6. Batch Operation Fails Atomically on Single Asset** (71 connections) — `DB/general/bonding-curve/BONDING_CURVE_MISC_VULNERABILITIES.md`
- **3. ERC-1155 `onERC1155Received` Reentrancy During NFT Mint** (71 connections) — `DB/general/reentrancy/defihacklabs-callback-reentrancy-2022-patterns.md`
- **4. Native ETH/AVAX `receive()` Reentrancy — exitMarket/State Bypass** (71 connections) — `DB/general/reentrancy/defihacklabs-callback-reentrancy-2022-patterns.md`
- **Move Event Emission, Configuration & Upgrade Safety Vulnerabilities** (71 connections) — `DB/Sui-Move-specific/MOVE_EVENT_CONFIGURATION_VULNERABILITIES.md`
- **Secure Pattern 1: TWAP Oracle with Proper Configuration** (69 connections) — `DB/amm/concentrated-liquidity/price-oracle-manipulation.md`
- **10. Protocol Fees Stuck After Graduation** (69 connections) — `DB/general/bonding-curve/BONDING_CURVE_MISC_VULNERABILITIES.md`
- **11. Token Supply Not Correctly Burned on Graduation** (69 connections) — `DB/general/bonding-curve/BONDING_CURVE_MISC_VULNERABILITIES.md`
- **12. Graduation Stuck Due to Third-Party Contract Interference** (69 connections) — `DB/general/bonding-curve/BONDING_CURVE_MISC_VULNERABILITIES.md`
- **Pattern 1: Missing Events for Critical State Changes — move-evtcfg-001** (69 connections) — `DB/Sui-Move-specific/MOVE_EVENT_CONFIGURATION_VULNERABILITIES.md`
- **1. Oracle Price Denomination Mismatch (USD vs DAI)** (67 connections) — `DB/general/bonding-curve/BONDING_CURVE_MISC_VULNERABILITIES.md`
- **1. ERC-677 `onTokenTransfer` Reentrancy During Liquidation** (67 connections) — `DB/general/reentrancy/defihacklabs-callback-reentrancy-2022-patterns.md`
- **2. Flash Loan Callback Reentrancy — Deposit-in-Callback** (67 connections) — `DB/general/reentrancy/defihacklabs-callback-reentrancy-2022-patterns.md`
- **Pattern 10: Two-Step Ownership Transfer Missing — move-evtcfg-010** (65 connections) — `DB/Sui-Move-specific/MOVE_EVENT_CONFIGURATION_VULNERABILITIES.md`
- **Pattern 11: Reentrancy via External Module Callback — move-evtcfg-011** (61 connections) — `DB/Sui-Move-specific/MOVE_EVENT_CONFIGURATION_VULNERABILITIES.md`
- **Pattern 12: Hardcoded Batch Parameters in Event Emission — move-evtcfg-012** (61 connections) — `DB/Sui-Move-specific/MOVE_EVENT_CONFIGURATION_VULNERABILITIES.md`
- *... and 91 more nodes in this community*

## Relationships

- No strong cross-community connections detected

## Source Files

- `DB/Sui-Move-specific/MOVE_EVENT_CONFIGURATION_VULNERABILITIES.md`
- `DB/amm/concentrated-liquidity/fee-collection-distribution.md`
- `DB/amm/concentrated-liquidity/liquidity-management-vulnerabilities.md`
- `DB/amm/concentrated-liquidity/price-oracle-manipulation.md`
- `DB/general/access-control/defihacklabs-access-control-2024-2025.md`
- `DB/general/bonding-curve/BONDING_CURVE_MISC_VULNERABILITIES.md`
- `DB/general/flash-loan/FLASH_LOAN_VULNERABILITIES.md`
- `DB/general/reentrancy/defihacklabs-callback-reentrancy-2022-patterns.md`
- `DB/unique/amm/constantproduct/SPARTAN_DIVIDEND_GAMING.md`
- `DB/unique/amm/constantproduct/TRADERJOE_FEE_DEBT_THEFT.md`

## Audit Trail

- EXTRACTED: 656 (38%)
- INFERRED: 1064 (62%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*