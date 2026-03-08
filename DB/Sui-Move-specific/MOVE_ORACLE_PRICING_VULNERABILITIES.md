---
protocol: generic
chain: sui, aptos, movement
category: oracle_pricing
vulnerability_type: stale_price, oracle_update_skip, sltp_clipping, undervalued_collateral, boundary_check, faulty_constant, unauthorized_feed
attack_type: price_manipulation, fund_extraction, liquidation_exploit
affected_component: oracle, price_feed, tick_calculation, collateral_valuation, amm_pricing
primitives:
  - chainlink
  - pyth
  - oracle
  - price_feed
  - tick_index
  - sqrtprice
  - collateral
  - sltp
severity: high
impact: fund_loss, incorrect_pricing, liquidation_exploit
exploitability: 0.7
financial_impact: critical
tags:
  - move
  - sui
  - aptos
  - oracle
  - price_feed
  - stale_price
  - chainlink
  - pyth
  - tick
  - sqrtprice
  - amm
  - collateral
  - sltp
  - defi
  - manipulation
language: move
version: all
---

## References
| # | Source | Protocol | Auditor | Severity |
|---|--------|----------|---------|----------|
| [R1] | reports/ottersec_move_audits/markdown/aave_aptos_v3_audit_final.md | Aave Aptos V3 | OtterSec | HIGH |
| [R2] | reports/ottersec_move_audits/markdown/aftermath_perps_oracle_audit_final.md | Aftermath Perps | OtterSec | HIGH |
| [R3] | reports/ottersec_move_audits/markdown/bluefin_spot_audit_final.md | Bluefin Spot | OtterSec | CRITICAL |
| [R4] | reports/ottersec_move_audits/markdown/echelon_lpt_audit_final.md | Echelon LPT | OtterSec | HIGH |

## Move Oracle and Pricing Vulnerabilities

**Comprehensive patterns for stale oracle prices, update skipping, SLTP clipping bugs, undervalued collateral, price boundary errors, faulty constants, and unauthorized feed registration in Move-based DeFi protocols across Sui and Aptos chains.**

### Overview

Oracle and pricing vulnerabilities appeared in 4/29 OtterSec Move audit reports (14%), with 1 CRITICAL, 5 HIGH, and 2 MEDIUM findings. These issues affect the fundamental price accuracy that lending, perpetuals, and AMM protocols depend on. Move-specific manifestations include incorrect fixed-point arithmetic with Move's strong typing, tick calculation errors from faulty constants, and Sui-specific oracle observation patterns.

### Vulnerability Description

#### Root Cause Categories

1. **Stale price consumption** — No maximum timestamp age check on oracle data
2. **Oracle update skipping** — Update only on tick change, skipping same-tick observations
3. **SLTP position size clipping** — Signed-to-unsigned conversion creates impossibly large values
4. **Undervalued collateral** — Oracle mispricing of derived assets (staked LPTs)
5. **Price boundary errors** — Inclusive vs exclusive comparison at tick limits
6. **Faulty constant** — Hardcoded constant with wrong number of digits
7. **Unauthorized feed registration** — Missing capability verification on price feed setup

---

## Pattern 1: Missing Staleness Check on Oracle Price — move-oracle-001

**Frequency**: 1/29 reports (Aave Aptos V3 [R1])
**Severity consensus**: HIGH
**Validation**: Weak — single protocol, but universal pattern (well-documented in Solidity too)

### Attack Scenario
1. Oracle price feed stops updating (oracle downtime, network congestion)
2. Protocol continues using last known price for lending/liquidation decisions
3. Actual market price diverges significantly from stale oracle price
4. Attacker borrows at inflated collateral value, or avoids liquidation at deflated value
5. Protocol accumulates bad debt from stale prices

### Vulnerable Pattern Example

**Aave Aptos V3 — No Timestamp Check on Chainlink Data** [HIGH] [R1]
```move
// ❌ VULNERABLE: No staleness check on oracle price
public fun get_asset_price(oracle: &Oracle, asset: address): u256 {
    let (price, _decimals, timestamp) = chainlink::latest_round_data(
        oracle.feed_address
    );
    
    // ❌ Timestamp never checked against maximum age
    // Price could be hours or days old
    // Used directly in lending, liquidation, and borrowing calculations
    
    assert!(price > 0, E_INVALID_PRICE);
    (price as u256)
}
```

### Secure Implementation
```move
// ✅ SECURE: Enforce maximum price age
const MAX_PRICE_AGE_SECONDS: u64 = 3600; // 1 hour

public fun get_asset_price(oracle: &Oracle, asset: address, clock: &Clock): u256 {
    let (price, _decimals, timestamp) = chainlink::latest_round_data(
        oracle.feed_address
    );
    
    assert!(price > 0, E_INVALID_PRICE);
    
    // ✅ Staleness check
    let now = clock::timestamp_ms(clock) / 1000;
    assert!(now - timestamp <= MAX_PRICE_AGE_SECONDS, E_STALE_PRICE);
    
    (price as u256)
}
```

---

## Pattern 2: Oracle Update Skipped on Same Tick — move-oracle-002

**Frequency**: 1/29 reports (Bluefin Spot [R3])
**Severity consensus**: HIGH
**Validation**: Weak — single protocol, but affects all CLOB/AMM with TWAP

### Attack Scenario
1. AMM/CLOB maintains on-chain oracle observations (TWAP)
2. Oracle update triggered only when tick index changes
3. Multiple swaps at same tick index → no oracle updates between them
4. On-chain TWAP becomes stale during active trading at a single tick
5. Downstream protocols using the TWAP get incorrect price data

### Vulnerable Pattern Example

**Bluefin Spot — Oracle Only Updates on Tick Change** [HIGH] [R3]
```move
// ❌ VULNERABLE: Update skipped when tick doesn't change
public fun swap(pool: &mut Pool, amount: u64, is_buy: bool, clock: &Clock) {
    let old_tick = pool.current_tick;
    
    // Execute swap logic, compute new tick
    let (new_tick, amount_out) = compute_swap(pool, amount, is_buy);
    
    if (new_tick != old_tick) {
        // Only updates oracle when tick actually changes
        update_oracle_observation(pool, clock, new_tick);
    };
    // ❌ If tick stays same after swap (e.g., small swap within tick range),
    // oracle observation NOT updated
    // TWAP becomes stale for same-tick trading periods
    
    pool.current_tick = new_tick;
}
```

### Secure Implementation
```move
// ✅ SECURE: Update oracle on every swap regardless of tick change
public fun swap(pool: &mut Pool, amount: u64, is_buy: bool, clock: &Clock) {
    let old_tick = pool.current_tick;
    let (new_tick, amount_out) = compute_swap(pool, amount, is_buy);
    
    // ✅ Always update oracle observation — even same tick
    update_oracle_observation(pool, clock, new_tick);
    
    pool.current_tick = new_tick;
}
```

---

## Pattern 3: SLTP Size Clipping via Signed/Unsigned Conversion — move-oracle-003

**Frequency**: 1/29 reports (Aftermath Perps [R2])
**Severity consensus**: HIGH
**Validation**: Weak — single protocol, but affects any perps with SLTP

### Attack Scenario
1. User has a negative (short) base position: e.g., -1000 units
2. SLTP (Stop-Loss/Take-Profit) order needs to know position size for clipping
3. Negative position value cast to u64 → becomes very large positive number (2^64 - 1000)
4. SLTP order size not clipped because "position size" appears huge
5. SLTP order executes at oversized amount → liquidation risk or protocol loss

### Vulnerable Pattern Example

**Aftermath Perps — Negative to Large u64 Conversion** [HIGH] [R2]
```move
// ❌ VULNERABLE: Negative base position becomes huge u64
public fun clip_sltp_size(
    position: &Position,
    sltp_size: u64,
): u64 {
    // position.base_amount is i64 (signed)
    // ❌ Casting negative i64 to u64 gives very large positive value
    let position_size = (position.base_amount as u64);  // ❌ -1000 → 18446744073709550616
    
    // Clipping check: sltp_size should be ≤ position_size
    if (sltp_size > position_size) {
        position_size
    } else {
        sltp_size
        // ❌ sltp_size is always <= huge u64, so NEVER clipped
        // SLTP order can exceed actual position size
    }
}
```

### Secure Implementation
```move
// ✅ SECURE: Use absolute value for position size comparison
public fun clip_sltp_size(
    position: &Position,
    sltp_size: u64,
): u64 {
    // ✅ Use absolute value of position
    let position_size = if (position.base_amount >= 0) {
        (position.base_amount as u64)
    } else {
        ((-position.base_amount) as u64)  // ✅ Correct absolute value
    };
    
    if (sltp_size > position_size) {
        position_size
    } else {
        sltp_size
    }
}
```

---

## Pattern 4: Undervalued Collateral from Oracle Mispricing — move-oracle-004

**Frequency**: 1/29 reports (Echelon LPT [R4])
**Severity consensus**: HIGH
**Validation**: Weak — single protocol, but common in LPT-based lending

### Attack Scenario
1. Protocol accepts staked LP tokens (LPTs) as collateral
2. Oracle prices LPTs at face value, not considering underlying LP composition
3. LPT price diverges from underlying LP token value
4. Borrower deposits overvalued LPTs, borrows undervalued assets
5. Borrower profits from price discrepancy at protocol's expense

### Vulnerable Pattern Example

**Echelon LPT — Staked LPT Oracle Mispricing** [HIGH] [R4]
```move
// ❌ VULNERABLE: Simple price lookup doesn't account for LPT mechanics
public fun get_collateral_value(
    oracle: &Oracle,
    collateral_type: TypeInfo,
    amount: u64,
): u64 {
    let price = get_asset_price(oracle, collateral_type);
    
    // ❌ For staked LPTs, price may not reflect:
    // 1. Pending reward claims that affect true value
    // 2. Slashing events that reduce backing
    // 3. Exit queue delays that affect liquidity
    // 4. LP impermanent loss since last oracle update
    
    amount * price / PRECISION
}
```

### Secure Implementation
```move
// ✅ SECURE: Calculate LPT value from underlying components
public fun get_lpt_collateral_value(
    oracle: &Oracle,
    lpt_pool: &LPTPool,
    amount: u64,
): u64 {
    // ✅ Get underlying token amounts per LPT share
    let (underlying_a, underlying_b) = get_lpt_underlying(lpt_pool, amount);
    
    // ✅ Price each underlying separately
    let value_a = underlying_a * get_asset_price(oracle, lpt_pool.token_a) / PRECISION;
    let value_b = underlying_b * get_asset_price(oracle, lpt_pool.token_b) / PRECISION;
    
    // ✅ Apply haircut for exit delays and IL risk
    let raw_value = value_a + value_b;
    raw_value * LPT_HAIRCUT_BPS / 10000
}
```

---

## Pattern 5: Incorrect Price Boundary Checks — move-oracle-005

**Frequency**: 1/29 reports (Bluefin Spot [R3])
**Severity consensus**: HIGH
**Validation**: Weak — single protocol, but affects any tick-based AMM

### Vulnerable Pattern Example

**Bluefin Spot — Inclusive vs Exclusive Tick Boundaries** [HIGH] [R3]
```move
// ❌ VULNERABLE: >= and <= allow price to equal boundary
public fun validate_tick(tick: i32) {
    // ❌ Should be strict inequality: > MIN_TICK and < MAX_TICK
    assert!(tick >= MIN_TICK && tick <= MAX_TICK, E_TICK_OUT_OF_RANGE);
    // When tick == MIN_TICK or tick == MAX_TICK:
    // sqrt_price pushed to exact boundary → undefined behavior in AMM math
    // tick_to_sqrt_price(MIN_TICK) = 0, breaking ratio calculations
}
```

### Secure Implementation
```move
// ✅ SECURE: Strict inequalities at boundaries
public fun validate_tick(tick: i32) {
    assert!(tick > MIN_TICK && tick < MAX_TICK, E_TICK_OUT_OF_RANGE);
}
```

---

## Pattern 6: Faulty Constant Definition — move-oracle-006

**Frequency**: 1/29 reports (Bluefin Spot [R3])
**Severity consensus**: CRITICAL
**Validation**: Weak — single protocol, but CRITICAL impact

### Vulnerable Pattern Example

**Bluefin Spot — MAX_U64 Missing a Digit** [CRITICAL] [R3]
```move
// ❌ VULNERABLE: Constant has wrong number of digits
const MAX_U64: u64 = 184467440737095516;  // ❌ 15 significant chars
// Correct value: 18446744073709551615     // Should be 16 significant chars

// Used in least_significant_bit() for tick calculations
public fun least_significant_bit(x: u64): u8 {
    if (x >= MAX_U64) {
        // ❌ Highest bit NEVER detected because MAX_U64 is too small
        // lsb(2^63) returns wrong value
        return 63;
    };
    // ... rest of bit scan logic
    // Result: incorrect tick-to-price conversions for half the tick space
}
```

### Secure Implementation
```move
// ✅ SECURE: Correct constant
const MAX_U64: u64 = 18446744073709551615;  // ✅ 2^64 - 1

// Or use built-in constant
const MAX_U64: u64 = 0xFFFFFFFFFFFFFFFF;
```

---

## Pattern 7: Unauthorized Price Feed Registration — move-oracle-007

**Frequency**: 1/29 reports (Aftermath Perps [R2])
**Severity consensus**: HIGH
**Validation**: Weak — single protocol

### Vulnerable Pattern Example

**Aftermath Perps — Missing Authority Check on Feed Registration** [HIGH] [R2]
```move
// ❌ VULNERABLE: No specific authority verification
public fun register_price_feed(
    oracle: &mut OracleConfig,
    authority_cap: &AuthorityCap<PACKAGE>,  // ❌ Missing ASSISTANT type param check
    feed_id: vector<u8>,
    decimals: u8,
) {
    // ❌ Any AuthorityCap<PACKAGE, *> accepted
    // Should require AuthorityCap<PACKAGE, ASSISTANT> specifically
    // Attacker with AuthorityCap<PACKAGE, USER> can register fake feeds
    
    table::add(&mut oracle.feeds, feed_id, FeedConfig { decimals });
}
```

### Secure Implementation
```move
// ✅ SECURE: Require specific authority type
public fun register_price_feed(
    oracle: &mut OracleConfig,
    authority_cap: &AuthorityCap<PACKAGE, ASSISTANT>,  // ✅ Specific type
    feed_id: vector<u8>,
    decimals: u8,
) {
    table::add(&mut oracle.feeds, feed_id, FeedConfig { decimals });
}
```

---

## Pattern 8: Fixed-Point Arithmetic Sign Bit Confusion — move-oracle-008

**Frequency**: 1/29 reports (Aftermath Perps [R2])
**Severity consensus**: MEDIUM
**Validation**: Weak — single protocol

### Vulnerable Pattern Example

**Aftermath Perps — Sign Bit Conflated with Overflow** [MEDIUM] [R2]
```move
// ❌ VULNERABLE: from_u256balance conflates sign bit with overflow
public fun from_u256balance(x: u256): IFixed {
    // ❌ If highest bit is set, function treats it as overflow
    // But in signed fixed-point, highest bit indicates negative value
    if (x & SIGN_BIT_MASK != 0) {
        abort E_OVERFLOW  // ❌ Legitimate negative results incorrectly rejected
    };
    IFixed { value: x }
}
```

### Secure Implementation
```move
// ✅ SECURE: Separate sign handling from overflow detection
public fun from_u256balance(x: u256, is_negative: bool): IFixed {
    // ✅ Use magnitude + sign flag instead of sign bit
    assert!(x <= MAX_MAGNITUDE, E_OVERFLOW);
    IFixed { value: x, negative: is_negative }
}
```

---

## Pattern 9: Oracle Not Updated When Tick Unchanged but Price Changes — move-oracle-009

**Severity**: MEDIUM  
**ID**: move-oracle-009  
**References**: Bluefin Spot (OS-BFS-ADV-02)

### Attack Scenario
An AMM only updates its on-chain oracle observation when the tick index changes. However, the sqrt price can change significantly within the same tick (especially in concentrated liquidity pools). This means the oracle reports a stale price despite actual trading activity, allowing arbitrageurs to exploit the lag. Any downstream protocol reading this TWAP gets a manipulable, outdated value.

### Vulnerable Pattern Example
```move
// ❌ VULNERABLE: Oracle updated only on tick change
public fun swap(pool: &mut Pool, amount_in: u64, zero_for_one: bool) {
    let old_tick = pool.current_tick;
    // ... execute swap, compute new sqrt_price and new_tick ...
    let new_tick = compute_new_tick(pool.sqrt_price);
    
    if (new_tick != old_tick) {
        // ❌ Only updates when tick crosses — misses intra-tick price movement
        update_oracle_observation(pool, new_tick);
    };
    pool.current_tick = new_tick;
}
```

### Secure Implementation
```move
// ✅ SECURE: Update oracle on every price change, not just tick change
public fun swap(pool: &mut Pool, amount_in: u64, zero_for_one: bool) {
    // ... execute swap ...
    let new_tick = compute_new_tick(pool.sqrt_price);
    // ✅ Always update observation with current sqrt_price
    update_oracle_observation(pool, new_tick, pool.sqrt_price);
    pool.current_tick = new_tick;
}
```

---

## Pattern 10: Undervalued Collateral from Naive LPT Pricing — move-oracle-010

**Severity**: HIGH  
**ID**: move-oracle-010  
**References**: Echelon LPT (OS-ELP-ADV-00)

### Attack Scenario
A lending protocol accepts LP tokens as collateral but prices them using total reserves divided by total supply. An attacker can manipulate the pool's spot reserves (via swap/flashloan) immediately before a collateral assessment, artifically deflating or inflating the LP token price. This enables borrowing against overvalued collateral or triggering unfair liquidations on undervalued positions.

### Vulnerable Pattern Example
```move
// ❌ VULNERABLE: LP token priced using spot reserves
public fun get_lpt_price(pool: &Pool, oracle: &PriceOracle): u64 {
    let total_supply = pool.lp_supply;
    let reserve_a = balance::value(&pool.reserve_a);
    let reserve_b = balance::value(&pool.reserve_b);
    // ❌ Spot reserves are manipulable via flash loan
    let price_a = oracle::get_price(oracle, pool.token_a);
    let price_b = oracle::get_price(oracle, pool.token_b);
    (reserve_a * price_a + reserve_b * price_b) / total_supply
}
```

### Secure Implementation
```move
// ✅ SECURE: Use fair LP pricing (Alpha Homora / Chainlink method)
public fun get_lpt_price(pool: &Pool, oracle: &PriceOracle): u64 {
    let total_supply = pool.lp_supply;
    let price_a = oracle::get_price(oracle, pool.token_a);
    let price_b = oracle::get_price(oracle, pool.token_b);
    // ✅ Fair reserves computed from invariant, not spot
    let fair_reserve_a = math::sqrt((pool.k * price_b) / price_a);
    let fair_reserve_b = math::sqrt((pool.k * price_a) / price_b);
    (fair_reserve_a * price_a + fair_reserve_b * price_b) / total_supply
}
```

---

## Pattern 11: Duplicate Source ID Corrupting Price Aggregation — move-oracle-011

**Severity**: MEDIUM  
**ID**: move-oracle-011  
**References**: Thala Oracle (OS-TOP-ADV-00)

### Attack Scenario
A price aggregation oracle accepts multiple price sources but doesn't validate source ID uniqueness. A malicious or misconfigured source registers the same ID twice, so its price is double-counted in the median/average calculation. This skews the aggregated price, enabling profitable trades against protocols that consume it.

### Vulnerable Pattern Example
```move
// ❌ VULNERABLE: No duplicate source ID check
public fun register_source(oracle: &mut PriceOracle, source_id: u64, source_addr: address) {
    // ❌ Same source_id can be registered multiple times
    vector::push_back(&mut oracle.sources, SourceInfo { id: source_id, addr: source_addr });
}

public fun aggregate_price(oracle: &PriceOracle): u64 {
    let prices = vector::empty<u64>();
    let i = 0;
    while (i < vector::length(&oracle.sources)) {
        // ❌ Duplicate source contributes price twice to median
        let source = vector::borrow(&oracle.sources, i);
        vector::push_back(&mut prices, get_source_price(source));
        i = i + 1;
    };
    compute_median(&prices)
}
```

### Secure Implementation
```move
// ✅ SECURE: Enforce source ID uniqueness
public fun register_source(oracle: &mut PriceOracle, source_id: u64, source_addr: address) {
    let i = 0;
    while (i < vector::length(&oracle.sources)) {
        assert!(vector::borrow(&oracle.sources, i).id != source_id, E_DUPLICATE_SOURCE);
        i = i + 1;
    };
    vector::push_back(&mut oracle.sources, SourceInfo { id: source_id, addr: source_addr });
}
```

---

## Pattern 12: Custom Price Exceeding Oracle Price Cap — move-oracle-012

**Severity**: MEDIUM  
**ID**: move-oracle-012  
**References**: Aave Aptos V3 (OS-AAV-ADV-04)

### Attack Scenario
An oracle allows admin-set custom prices for assets that don't have external price feeds. However, there's no upper bound on the custom price. An admin (or compromised admin key) sets an extreme price, and borrowers use the overvalued collateral to drain the protocol's lending reserves.

### Vulnerable Pattern Example
```move
// ❌ VULNERABLE: No cap on custom price
public fun set_custom_price(admin: &signer, asset: address, price: u64) {
    assert!(signer::address_of(admin) == @admin, E_UNAUTHORIZED);
    let state = borrow_global_mut<OracleState>(@oracle);
    // ❌ Admin can set price to u64::MAX
    table::upsert(&mut state.custom_prices, asset, price);
}
```

### Secure Implementation
```move
// ✅ SECURE: Cap custom price relative to recent oracle range
public fun set_custom_price(admin: &signer, asset: address, price: u64) {
    assert!(signer::address_of(admin) == @admin, E_UNAUTHORIZED);
    let state = borrow_global_mut<OracleState>(@oracle);
    let max_price = state.price_cap; // e.g., 10x last known oracle price
    assert!(price > 0 && price <= max_price, E_PRICE_OUT_OF_RANGE);
    table::upsert(&mut state.custom_prices, asset, price);
}
```

---

## Pattern 13: Confidence-Before-Timestamp Ordering Error — move-oracle-013

**Severity**: LOW  
**ID**: move-oracle-013  
**References**: Aftermath Perps (OS-AMP-ADV-03)

### Attack Scenario
When consuming Pyth oracle data, the protocol checks confidence interval (price ± conf) before checking the timestamp freshness. If the price data is stale, the confidence check may pass on outdated data, leading to transactions processing at a price that no longer reflects market conditions. The correct order is: check freshness first, then validate confidence.

### Vulnerable Pattern Example
```move
// ❌ VULNERABLE: Confidence checked before staleness
public fun get_validated_price(pyth_price: &Price): u64 {
    let price = pyth::get_price(pyth_price);
    let conf = pyth::get_conf(pyth_price);
    // ❌ Checking confidence on potentially stale data
    assert!(conf * 100 / price < MAX_CONF_PERCENTAGE, E_TOO_WIDE);
    
    let timestamp = pyth::get_timestamp(pyth_price);
    assert!(clock::timestamp_ms(clock) / 1000 - timestamp < MAX_AGE, E_STALE);
    price
}
```

### Secure Implementation
```move
// ✅ SECURE: Staleness check first, then confidence
public fun get_validated_price(pyth_price: &Price, clock: &Clock): u64 {
    let timestamp = pyth::get_timestamp(pyth_price);
    // ✅ Freshness first — reject before any other checks
    assert!(clock::timestamp_ms(clock) / 1000 - timestamp < MAX_AGE, E_STALE);
    
    let price = pyth::get_price(pyth_price);
    let conf = pyth::get_conf(pyth_price);
    assert!(conf * 100 / price < MAX_CONF_PERCENTAGE, E_TOO_WIDE);
    price
}
```

---

### Impact Analysis

#### Technical Impact
- Stale prices enabling bad debt accumulation (1/29 reports)
- Incorrect TWAP for downstream consumers (1/29 reports)
- SLTP orders exceeding position size → liquidations (1/29 reports)
- Undervalued collateral enabling profitable borrowing (1/29 reports)
- AMM pricing errors from faulty constant affecting half the tick space (1/29 reports) — CRITICAL
- Unauthorized price feed registration → price manipulation (1/29 reports)

#### Business Impact
- Protocol insolvency from stale-price lending (Aave Aptos V3)
- Incorrect liquidations from SLTP bugs (Aftermath Perps)
- AMM mispricing affecting all trades (Bluefin Spot)
- Lending protocol losses from LPT mispricing (Echelon LPT)

#### Affected Scenarios
- Lending protocols consuming price feeds (Aave, Echelon)
- Perpetual DEXes with SLTP orders (Aftermath Perps)
- AMMs with on-chain TWAP oracles (Bluefin Spot)
- Any protocol with LPT/derived asset collateral
- Protocols with admin-registered price feeds

### Detection Patterns

#### Code Patterns to Look For
```
- Pattern 1: `latest_round_data()` without timestamp age check
- Pattern 2: `if (new_tick != old_tick) { update_oracle(...) }` — same-tick skip
- Pattern 3: `(signed_value as u64)` for position size — signed-to-unsigned cast
- Pattern 4: `get_price(collateral_type)` for LP/staked tokens without decomposition
- Pattern 5: `tick >= MIN_TICK` instead of `tick > MIN_TICK` at boundaries
- Pattern 6: Large numeric constants — count digits manually
- Pattern 7: `AuthorityCap<PACKAGE>` without second type parameter
- Pattern 8: Sign bit check conflated with overflow in fixed-point math
- Pattern 9: Oracle observation skipped when `new_tick == old_tick`
- Pattern 10: `reserve_a * price_a / total_supply` for LP pricing (spot manipulation)
- Pattern 11: `vector::push_back(&sources, ...)` without duplicate ID check
- Pattern 12: `table::upsert(&custom_prices, asset, price)` without upper bound
- Pattern 13: Confidence check before timestamp freshness check on Pyth data
```

#### Audit Checklist
- [ ] All oracle price reads include maximum age validation
- [ ] TWAP/oracle observations updated on every price-changing event (not just tick change)
- [ ] Signed-to-unsigned conversions use absolute value correctly
- [ ] LP token / derived asset pricing uses underlying composition, not face value
- [ ] Tick boundary checks use strict inequality (> and <, not >= and <=)
- [ ] All large numeric constants verified digit-by-digit
- [ ] Price feed registration requires specific capability type
- [ ] Fixed-point sign handling separated from overflow detection
- [ ] Oracle updates on every swap, not gated by tick change
- [ ] LP pricing uses fair reserves (invariant-based), not spot reserves
- [ ] Oracle source IDs validated for uniqueness at registration
- [ ] Custom/admin prices have upper bounds relative to oracle range
- [ ] Pyth price validation: staleness → confidence → price (correct order)

### Keywords for Search

> `oracle`, `price feed`, `stale price`, `staleness check`, `chainlink`, `pyth`, `latest_round_data`, `timestamp`, `TWAP`, `oracle observation`, `tick index`, `sqrtprice`, `SLTP`, `stop loss`, `take profit`, `position size`, `signed unsigned`, `collateral value`, `LPT`, `undervalued`, `tick boundary`, `MIN_TICK`, `MAX_TICK`, `MAX_U64`, `faulty constant`, `price feed registration`, `AuthorityCap`, `fixed point`, `sign bit`, `move oracle`, `sui oracle`, `aptos oracle`, `intra-tick`, `same tick skip`, `LP pricing`, `fair reserves`, `spot reserves`, `flash loan`, `source ID`, `duplicate source`, `median`, `aggregation`, `custom price`, `price cap`, `confidence`, `pyth confidence`, `stale then confidence`

### Related Vulnerabilities

- [MOVE_ARITHMETIC_PRECISION_VULNERABILITIES.md](MOVE_ARITHMETIC_PRECISION_VULNERABILITIES.md) — Fixed-point arithmetic errors
- [MOVE_DEFI_PROTOCOL_LOGIC_VULNERABILITIES.md](MOVE_DEFI_PROTOCOL_LOGIC_VULNERABILITIES.md) — Liquidation and solvency bugs
- [SUI_MOVE_DEFI_LOGIC_VULNERABILITIES.md](SUI_MOVE_DEFI_LOGIC_VULNERABILITIES.md) — Solodit-sourced pricing patterns
