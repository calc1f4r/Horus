# access-control 3

> 74 nodes · cohesion 0.24

## Key Concepts

- **1. Public Mint + Public Burn on Token Contract (SafeMoon $8.9M)** (71 connections) — `DB/general/access-control/defihacklabs-access-control-2023-patterns.md`
- **2. Public Fee Transfer Function on DEX Pair (LeetSwap $630K)** (65 connections) — `DB/general/access-control/defihacklabs-access-control-2023-patterns.md`
- **3. Aggregator Arbitrary-Sender Swap (SwapX $1M)** (65 connections) — `DB/general/access-control/defihacklabs-access-control-2023-patterns.md`
- **Secure Implementations** (65 connections) — `DB/general/access-control/defihacklabs-access-control-2023-patterns.md`
- **4. Token Lock/Claim with Migration Vulnerability (SHIDO $230K)** (63 connections) — `DB/general/access-control/defihacklabs-access-control-2023-patterns.md`
- **5. Router/Bot Authorization Failures (Maestro $630K, UniBot $84K)** (63 connections) — `DB/general/access-control/defihacklabs-access-control-2023-patterns.md`
- **5. Flash Loan + Spot Price (CompounderFinance $27.2M, Gamma $6.3M, Allbridge $550K)** (55 connections) — `DB/oracle/price-manipulation/defihacklabs-oracle-manipulation-2023-patterns.md`
- **2. Concentrated Liquidity Bin Manipulation (Jimbo $8M)** (53 connections) — `DB/oracle/price-manipulation/defihacklabs-oracle-manipulation-2023-patterns.md`
- **3. Curve LP Token Price Manipulation (Zunami $2M)** (53 connections) — `DB/oracle/price-manipulation/defihacklabs-oracle-manipulation-2023-patterns.md`
- **Secure Implementations** (51 connections) — `DB/oracle/price-manipulation/defihacklabs-oracle-manipulation-2023-patterns.md`
- **1. Unvalidated callTo/callData in Swap/Route Structs [CRITICAL]** (49 connections) — `DB/general/arbitrary-call/defihacklabs-arbitrary-call-2024-2025.md`
- **1. Low-Cost Oracle Reporter Manipulation (BonqDAO $88M)** (49 connections) — `DB/oracle/price-manipulation/defihacklabs-oracle-manipulation-2023-patterns.md`
- **4. vToken Collateral Oracle Manipulation (0vix $2M)** (49 connections) — `DB/oracle/price-manipulation/defihacklabs-oracle-manipulation-2023-patterns.md`
- **6. Lending Protocol Oracle Manipulation (RodeoFinance $888K)** (49 connections) — `DB/oracle/price-manipulation/defihacklabs-oracle-manipulation-2023-patterns.md`
- **2. Unrestricted External Call Actions (OPERATION_CALL) [CRITICAL]** (47 connections) — `DB/general/arbitrary-call/defihacklabs-arbitrary-call-2024-2025.md`
- **4. Yul Integer Overflow Calldata Corruption [CRITICAL]** (47 connections) — `DB/general/arbitrary-call/defihacklabs-arbitrary-call-2024-2025.md`
- **5. Unverified Aggregator Proxy Forwarding [CRITICAL]** (47 connections) — `DB/general/arbitrary-call/defihacklabs-arbitrary-call-2024-2025.md`
- **Root Cause Analysis** (45 connections) — `DB/general/arbitrary-call/dex-aggregator-unvalidated-call-data.md`
- **3. Bridge Signer Validation Bypass [CRITICAL]** (43 connections) — `DB/general/arbitrary-call/defihacklabs-arbitrary-call-2024-2025.md`
- **Rug Pull & Malicious Contract Detection Patterns** (29 connections) — `DB/general/malicious/rug-pull-detection-patterns.md`
- **dex_pair** (26 connections) — `DB/general/access-control/defihacklabs-access-control-2023-patterns.md`
- **bridge_gateway** (22 connections) — `DB/general/access-control/defihacklabs-access-control-2023-patterns.md`
- **flash loan price manipulation** (18 connections) — `DB/oracle/price-manipulation/defihacklabs-flashloan-oracle-2022-patterns.md`
- **balancer_pool** (14 connections) — `DB/oracle/price-manipulation/defihacklabs-oracle-manipulation-2023-patterns.md`
- **curve_pool** (14 connections) — `DB/oracle/price-manipulation/defihacklabs-oracle-manipulation-2023-patterns.md`
- *... and 49 more nodes in this community*

## Relationships

- [access-control](access-control.md) (34 shared connections)
- [defi 5](defi_5.md) (16 shared connections)
- [oracle](oracle.md) (16 shared connections)
- [amm](amm.md) (11 shared connections)
- [general 2](general_2.md) (4 shared connections)
- [cosmos 7](cosmos_7.md) (1 shared connections)

## Source Files

- `DB/general/access-control/defihacklabs-access-control-2023-patterns.md`
- `DB/general/arbitrary-call/defihacklabs-arbitrary-call-2024-2025.md`
- `DB/general/arbitrary-call/dex-aggregator-unvalidated-call-data.md`
- `DB/general/malicious/rug-pull-detection-patterns.md`
- `DB/oracle/price-manipulation/defihacklabs-flashloan-oracle-2022-patterns.md`
- `DB/oracle/price-manipulation/defihacklabs-oracle-manipulation-2023-patterns.md`

## Audit Trail

- EXTRACTED: 228 (32%)
- INFERRED: 494 (68%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*