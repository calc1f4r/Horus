# proxy 4

> 24 nodes · cohesion 0.86

## Key Concepts

- **callback_reentrancy** (220 connections) — `DB/amm/concentrated-liquidity/v4-hook-token-compatibility.md`
- **Critical Exploits ($10M+) [CRITICAL]** (43 connections) — `DB/general/reentrancy/defi-reentrancy-patterns.md`
- **Fix 2: ReentrancyGuard Modifier** (41 connections) — `DB/general/reentrancy/defi-reentrancy-patterns.md`
- **Fix 1: Checks-Effects-Interactions (CEI) Pattern** (39 connections) — `DB/general/reentrancy/defi-reentrancy-patterns.md`
- **Fix 3: Read-Only Reentrancy Protection (Balancer/Curve)** (39 connections) — `DB/general/reentrancy/defi-reentrancy-patterns.md`
- **Historical Exploits (2021) [CRITICAL]** (39 connections) — `DB/general/reentrancy/defi-reentrancy-patterns.md`
- **Lower-Severity Exploits (<$100K) [CRITICAL]** (39 connections) — `DB/general/reentrancy/defi-reentrancy-patterns.md`
- **Fix 4: Callback Whitelist / Validation** (37 connections) — `DB/general/reentrancy/defi-reentrancy-patterns.md`
- **High-Severity Exploits ($1M-$10M) [CRITICAL]** (35 connections) — `DB/general/reentrancy/defi-reentrancy-patterns.md`
- **Medium-Severity Exploits ($100K-$1M) [CRITICAL]** (35 connections) — `DB/general/reentrancy/defi-reentrancy-patterns.md`
- **callback_function** (28 connections) — `DB/general/flash-loan/flash-loan-attack-patterns.md`
- **batchHarvestMarketRewards** (26 connections) — `DB/general/reentrancy/defi-reentrancy-patterns.md`
- **external_calls** (18 connections) — `DB/general/reentrancy/defi-reentrancy-patterns.md`
- **Balancer_pool_state** (18 connections) — `DB/general/reentrancy/defi-reentrancy-patterns.md`
- **checkCurveReentrancy** (18 connections) — `DB/general/reentrancy/defi-reentrancy-patterns.md`
- **Curve_remove_liquidity** (18 connections) — `DB/general/reentrancy/defi-reentrancy-patterns.md`
- **ERC721_onReceived** (18 connections) — `DB/general/reentrancy/defi-reentrancy-patterns.md`
- **Compiler-Level Vulnerability Patterns** (13 connections) — `DB/unique/defihacklabs/compiler-level-vulnerabilities.md`
- **DB/general/reentrancy/defi-reentrancy-patterns.md** (9 connections) — `DB/general/reentrancy/defi-reentrancy-patterns.md`
- **check curve reentrancy** (4 connections) — `DB/general/reentrancy/defi-reentrancy-patterns.md`
- **vyper_compiler** (2 connections) — `DB/unique/defihacklabs/compiler-level-vulnerabilities.md`
- **fix callback whitelist validation** (2 connections) — `DB/general/reentrancy/defi-reentrancy-patterns.md`
- **vyper reentrancy lock bug** (2 connections) — `DB/unique/defihacklabs/compiler-level-vulnerabilities.md`
- **DB/unique/defihacklabs/compiler-level-vulnerabilities.md** (1 connections) — `DB/unique/defihacklabs/compiler-level-vulnerabilities.md`

## Relationships

- [defi 3](defi_3.md) (42 shared connections)
- [defi 2](defi_2.md) (25 shared connections)
- [bridge](bridge.md) (13 shared connections)
- [token](token.md) (11 shared connections)
- [proxy 2](proxy_2.md) (10 shared connections)
- [proxy 3](proxy_3.md) (8 shared connections)
- [defi](defi.md) (8 shared connections)
- [amm 2](amm_2.md) (7 shared connections)
- [cosmos 9](cosmos_9.md) (3 shared connections)
- [cosmos 7](cosmos_7.md) (1 shared connections)

## Source Files

- `DB/amm/concentrated-liquidity/v4-hook-token-compatibility.md`
- `DB/general/flash-loan/flash-loan-attack-patterns.md`
- `DB/general/reentrancy/defi-reentrancy-patterns.md`
- `DB/unique/defihacklabs/compiler-level-vulnerabilities.md`

## Audit Trail

- EXTRACTED: 160 (43%)
- INFERRED: 212 (57%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*