# general 6

> 32 nodes · cohesion 1.06

## Key Concepts

- **Move Oracle and Pricing Vulnerabilities [HIGH]** (99 connections) — `DB/Sui-Move-specific/MOVE_ORACLE_PRICING_VULNERABILITIES.md`
- **Pattern 1: Missing Staleness Check on Oracle Price — move-oracle-001** (87 connections) — `DB/Sui-Move-specific/MOVE_ORACLE_PRICING_VULNERABILITIES.md`
- **Pattern 10: Undervalued Collateral from Naive LPT Pricing — move-oracle-010 [HIGH]** (75 connections) — `DB/Sui-Move-specific/MOVE_ORACLE_PRICING_VULNERABILITIES.md`
- **Pattern 9: Oracle Not Updated When Tick Unchanged but Price Changes — move-oracle-009 [HIGH]** (69 connections) — `DB/Sui-Move-specific/MOVE_ORACLE_PRICING_VULNERABILITIES.md`
- **Pattern 7: Unauthorized Price Feed Registration — move-oracle-007** (67 connections) — `DB/Sui-Move-specific/MOVE_ORACLE_PRICING_VULNERABILITIES.md`
- **Pattern 8: Fixed-Point Arithmetic Sign Bit Confusion — move-oracle-008** (67 connections) — `DB/Sui-Move-specific/MOVE_ORACLE_PRICING_VULNERABILITIES.md`
- **Pattern 4: Undervalued Collateral from Oracle Mispricing — move-oracle-004** (65 connections) — `DB/Sui-Move-specific/MOVE_ORACLE_PRICING_VULNERABILITIES.md`
- **Pattern 5: Incorrect Price Boundary Checks — move-oracle-005** (65 connections) — `DB/Sui-Move-specific/MOVE_ORACLE_PRICING_VULNERABILITIES.md`
- **Pattern 6: Faulty Constant Definition — move-oracle-006** (65 connections) — `DB/Sui-Move-specific/MOVE_ORACLE_PRICING_VULNERABILITIES.md`
- **Pattern 11: Duplicate Source ID Corrupting Price Aggregation — move-oracle-011 [HIGH]** (63 connections) — `DB/Sui-Move-specific/MOVE_ORACLE_PRICING_VULNERABILITIES.md`
- **Pattern 12: Custom Price Exceeding Oracle Price Cap — move-oracle-012 [HIGH]** (63 connections) — `DB/Sui-Move-specific/MOVE_ORACLE_PRICING_VULNERABILITIES.md`
- **Pattern 2: Oracle Update Skipped on Same Tick — move-oracle-002** (63 connections) — `DB/Sui-Move-specific/MOVE_ORACLE_PRICING_VULNERABILITIES.md`
- **Pattern 3: SLTP Size Clipping via Signed/Unsigned Conversion — move-oracle-003** (63 connections) — `DB/Sui-Move-specific/MOVE_ORACLE_PRICING_VULNERABILITIES.md`
- **oracle** (52 connections) — `DB/general/bonding-curve/BONDING_CURVE_MISC_VULNERABILITIES.md`
- **Pattern 13: Confidence-Before-Timestamp Ordering Error — move-oracle-013 [HIGH]** (51 connections) — `DB/Sui-Move-specific/MOVE_ORACLE_PRICING_VULNERABILITIES.md`
- **collateral_valuation** (44 connections) — `DB/general/reentrancy/defihacklabs-readonly-reentrancy-patterns.md`
- **amm_pricing** (28 connections) — `DB/Sui-Move-specific/MOVE_ORACLE_PRICING_VULNERABILITIES.md`
- **tick_calculation** (28 connections) — `DB/Sui-Move-specific/MOVE_ORACLE_PRICING_VULNERABILITIES.md`
- **liquidation_exploit** (28 connections) — `DB/Sui-Move-specific/MOVE_ORACLE_PRICING_VULNERABILITIES.md`
- **reports/ottersec_move_audits/markdown/echelon_lpt_audit_final.md** (28 connections) — `DB/Sui-Move-specific/MOVE_ORACLE_PRICING_VULNERABILITIES.md`
- **get_collateral_value** (26 connections) — `DB/Sui-Move-specific/MOVE_ORACLE_PRICING_VULNERABILITIES.md`
- **get_lpt_collateral_value** (26 connections) — `DB/Sui-Move-specific/MOVE_ORACLE_PRICING_VULNERABILITIES.md`
- **get_validated_price** (26 connections) — `DB/Sui-Move-specific/MOVE_ORACLE_PRICING_VULNERABILITIES.md`
- **least_significant_bit** (26 connections) — `DB/Sui-Move-specific/MOVE_ORACLE_PRICING_VULNERABILITIES.md`
- **register_price_feed** (26 connections) — `DB/Sui-Move-specific/MOVE_ORACLE_PRICING_VULNERABILITIES.md`
- *... and 7 more nodes in this community*

## Relationships

- [general](general.md) (60 shared connections)
- [amm](amm.md) (20 shared connections)
- [access-control](access-control.md) (20 shared connections)
- [defi 9](defi_9.md) (18 shared connections)
- [oracle 3](oracle_3.md) (14 shared connections)
- [proxy 2](proxy_2.md) (2 shared connections)

## Source Files

- `DB/Sui-Move-specific/MOVE_ORACLE_PRICING_VULNERABILITIES.md`
- `DB/general/bonding-curve/BONDING_CURVE_MISC_VULNERABILITIES.md`
- `DB/general/reentrancy/defihacklabs-readonly-reentrancy-patterns.md`

## Audit Trail

- EXTRACTED: 216 (32%)
- INFERRED: 458 (68%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*