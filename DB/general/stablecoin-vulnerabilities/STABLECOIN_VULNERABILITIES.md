---
# Core Classification (Required)
protocol: generic
chain: everychain
category: logic
vulnerability_type: stablecoin_pricing_assumptions

# Attack Vector Details (Required)
attack_type: logical_error
affected_component: pricing_logic

# Technical Primitives (Required)
primitives:
  - stablecoin_peg
  - depeg_tolerance
  - oracle_price_feed
  - decimal_normalization
  - collateral_valuation
  - mint_redeem

# Impact Classification (Required)
severity: low
impact: incorrect_pricing
exploitability: 0.45
financial_impact: medium

# Context Tags (Optional but recommended)
tags:
  - defi
  - stablecoin
  - depeg
  - pricing
  - minting
  - collateral
  - oracle

# Version Info (Optional)
language: solidity|rust
version: all

# Pattern Identity (Required)
root_cause_family: logic_error
pattern_key: logic_error | pricing_logic | stablecoin_pricing_assumptions

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: single_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - block.timestamp
  - collateral_valuation
  - decimal_normalization
  - depeg_tolerance
  - getPrice
  - mint
  - mint_redeem
  - msg.sender
  - oracle_price_feed
  - receive
  - safeTransferFrom
  - stableToUsd
  - stablecoin_peg
---

## References & Source Reports

> **For Agents**: If you need more detail about a pattern, read the full report from the referenced file path.

| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| USD stablecoins assumed at peg | [reports/stablecoin_findings/usd-stablecoins-are-incorrectly-assumed-to-always-be-at-peg.md](reports/stablecoin_findings/usd-stablecoins-are-incorrectly-assumed-to-always-be-at-peg.md) | HIGH | Cyfrin |
| Minter ignores depegs + decimal mismatch | [reports/stablecoin_findings/minter-doesnt-account-for-depegs-exchange-rates-and-decimal-precision-mismatch-b.md](reports/stablecoin_findings/minter-doesnt-account-for-depegs-exchange-rates-and-decimal-precision-mismatch-b.md) | HIGH | Cyfrin |
| Protocol assumes 1 stable = 1 USD | [reports/stablecoin_findings/m-03-protocol-assumes-1-stable-1-usd.md](reports/stablecoin_findings/m-03-protocol-assumes-1-stable-1-usd.md) | MEDIUM | Pashov Audit Group |
| USD1 priced as $1 instead of pegged asset | [reports/stablecoin_findings/m-2-usd1-is-priced-as-1-instead-of-being-pegged-to-usdt.md](reports/stablecoin_findings/m-2-usd1-is-priced-as-1-instead-of-being-pegged-to-usdt.md) | MEDIUM | Sherlock |
| Incorrect assumption of USDC/USDT value | [reports/stablecoin_findings/l-03-incorrect-assumption-of-usdc-and-usdt-value.md](reports/stablecoin_findings/l-03-incorrect-assumption-of-usdc-and-usdt-value.md) | LOW | Pashov Audit Group |
| Hardcoded stablecoin price (Rust) | [reports/stablecoin_findings/l-09-hardcoded-stablecoin-price.md](reports/stablecoin_findings/l-09-hardcoded-stablecoin-price.md) | LOW | Pashov Audit Group |
| Hardcoded 6-decimal stablecoin assumptions | [reports/stablecoin_findings/l-02-hardcoded-6-decimal-stablecoin-assumptions-brick-protocol-on-18-decimal-dep.md](reports/stablecoin_findings/l-02-hardcoded-6-decimal-stablecoin-assumptions-brick-protocol-on-18-decimal-dep.md) | LOW | Shieldify |
| USDC depeg not handled in slippage | [reports/stablecoin_findings/usdc-is-not-valued-correctly-in-case-of-a-depeg-which-causes-a-loss-of-funds.md](reports/stablecoin_findings/usdc-is-not-valued-correctly-in-case-of-a-depeg-which-causes-a-loss-of-funds.md) | LOW | Codehawks |
| Missing stablecoin tolerance checks for new oracles | [reports/stablecoin_findings/no-stablecoin-tolerance-check-for-added-oracles.md](reports/stablecoin_findings/no-stablecoin-tolerance-check-for-added-oracles.md) | LOW | Quantstamp |

## Vulnerability Title

Stablecoin Pricing Assumptions and Depeg Handling Failures

### Overview

This vulnerability exists because missing validation or hardcoded pricing assumptions in stablecoin valuation, mint/redeem, or collateral logic allow depegged assets or mismatched decimals to be treated as $1, leading to incorrect pricing, unfair minting/redemptions, and potential fund loss.



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of logic_error"
- Pattern key: `logic_error | pricing_logic | stablecoin_pricing_assumptions`
- Interaction scope: `single_contract`
- Primary affected component(s): `pricing_logic`
- High-signal code keywords: `block.timestamp`, `collateral_valuation`, `decimal_normalization`, `depeg_tolerance`, `getPrice`, `mint`, `mint_redeem`, `msg.sender`
- Typical sink / impact: `incorrect_pricing`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `N/A`
- Trust boundary crossed: `internal`
- Shared state or sync assumption: `state consistency across operations`

#### Valid Bug Signals

- Signal 1: State variable updated after external interaction instead of before (CEI violation)
- Signal 2: Withdrawal path produces different accounting than deposit path for same principal
- Signal 3: Reward accrual continues during paused/emergency state
- Signal 4: Edge case in state machine transition allows invalid state

#### False Positive Guards

- Not this bug when: Standard security patterns (access control, reentrancy guards, input validation) are in place
- Safe if: Protocol behavior matches documented specification
- Requires attacker control of: specific conditions per pattern

### Vulnerability Description

#### Root Cause

- Stablecoins are treated as permanently pegged to $1 (or to another stablecoin) without real-time price validation.
- Hardcoded prices or static exchange rates are used where a live oracle or tolerance bounds are required.
- Decimal precision mismatches between stablecoins and synthetic tokens are ignored or assumed.
- Oracle integration omits stablecoin-specific tolerance checks when adding or updating feeds.

#### Attack Scenario

1. A stablecoin depegs below $1 (or above $1) due to market stress.
2. The protocol still values the stablecoin at $1 (or at the wrong reference asset) in pricing, minting, or collateral calculations.
3. An attacker deposits depegged stablecoins or triggers mint/redeem flows to receive inflated value.
4. The protocol accrues bad debt or users are over/under-compensated, draining liquidity or causing insolvency.

#### Vulnerable Pattern Examples

**Example 1: Stablecoins assumed at $1 in collateral valuation** [Approx Vulnerability : HIGH]
> Reference: [reports/stablecoin_findings/usd-stablecoins-are-incorrectly-assumed-to-always-be-at-peg.md](reports/stablecoin_findings/usd-stablecoins-are-incorrectly-assumed-to-always-be-at-peg.md)
```solidity
// ❌ VULNERABLE: Treats USDs/USDC as always $1
if (_token0 == address(USDs) || _token1 == address(USDs)) {
    _usds += _underlying0 * 10 ** (18 - ERC20(_token0).decimals());
    _usds += _underlying1 * 10 ** (18 - ERC20(_token1).decimals());
}
```

**Example 2: Minting ignores depegs and decimal mismatches** [Approx Vulnerability : HIGH]
> Reference: [reports/stablecoin_findings/minter-doesnt-account-for-depegs-exchange-rates-and-decimal-precision-mismatch-b.md](reports/stablecoin_findings/minter-doesnt-account-for-depegs-exchange-rates-and-decimal-precision-mismatch-b.md)
```solidity
// ❌ VULNERABLE: Mints 1:1 without checking decimals or depeg risk
function mint(address to, uint256 amount) external onlyWhitelisted(msg.sender) onlyWhitelisted(to) nonReentrant {
    baseAsset.safeTransferFrom(msg.sender, address(this), amount);
    hilBTCToken.mint(to, amount);
}
```

**Example 3: 1 stable = 1 USD assumption in constructor** [Approx Vulnerability : MEDIUM]
> Reference: [reports/stablecoin_findings/m-03-protocol-assumes-1-stable-1-usd.md](reports/stablecoin_findings/m-03-protocol-assumes-1-stable-1-usd.md)
```solidity
// ❌ VULNERABLE: Hardcodes USDC/USDT to $1
numeratorUsdc = 1 * 10 ** (IERC20Metadata(IOFT(_stargateUsdc).token()).decimals() - 1);
numeratorUsdt = 1 * 10 ** (IERC20Metadata(IOFT(_stargateUsdt).token()).decimals() - 1);
```

**Example 4: Pegged-to-asset stable priced as $1** [Approx Vulnerability : MEDIUM]
> Reference: [reports/stablecoin_findings/m-2-usd1-is-priced-as-1-instead-of-being-pegged-to-usdt.md](reports/stablecoin_findings/m-2-usd1-is-priced-as-1-instead-of-being-pegged-to-usdt.md)
```solidity
// ❌ VULNERABLE: Uses USDT price feed but treats USD1 as $1
price = oracle.getLatestPrice(priceQuoteToken);
_checkPrice(priceQuoteToken, price);
```

**Example 5: Hardcoded stablecoin price in Rust** [Approx Vulnerability : LOW]
> Reference: [reports/stablecoin_findings/l-09-hardcoded-stablecoin-price.md](reports/stablecoin_findings/l-09-hardcoded-stablecoin-price.md)
```rust
// ❌ VULNERABLE: Assumes stablecoin price is always 1 USD
if mint == constants::DEPOSIT_MINT1 || mint == constants::DEPOSIT_MINT2 {
    return Ok(100000);
}
```

**Example 6: Hardcoded 6-decimal assumptions** [Approx Vulnerability : LOW]
> Reference: [reports/stablecoin_findings/l-02-hardcoded-6-decimal-stablecoin-assumptions-brick-protocol-on-18-decimal-dep.md](reports/stablecoin_findings/l-02-hardcoded-6-decimal-stablecoin-assumptions-brick-protocol-on-18-decimal-dep.md)
```solidity
// ❌ VULNERABLE: Assumes stablecoin decimals are always 6
uint256 public constant MAX_LOAN_AMOUNT = 1_000_000 * 10**6;
uint256 public constant MIN_SELLBACK_AMOUNT = 1 * 10**6;
```

**Example 7: Depeg handling mismatch in slippage calculations** [Approx Vulnerability : LOW]
> Reference: [reports/stablecoin_findings/usdc-is-not-valued-correctly-in-case-of-a-depeg-which-causes-a-loss-of-funds.md](reports/stablecoin_findings/usdc-is-not-valued-correctly-in-case-of-a-depeg-which-causes-a-loss-of-funds.md)
```solidity
// ❌ VULNERABLE: Uses Chainlink USDC price directly for slippage
ChainlinkResponse memory chainlinkResponse = _getChainlinkResponse(_feed);
return (chainlinkResponse.answer, chainlinkResponse.decimals);
```

### Impact Analysis

#### Technical Impact
- Incorrect pricing of collateral and mint/redeem operations during depeg events.
- Arbitrage paths created by treating depegged stables as $1.
- Protocol state drift due to rounding and decimal mismatches.

#### Business Impact
- User over-minting or over-redemption, draining protocol liquidity.
- Undercollateralization and insolvency risk during stablecoin volatility.
- Loss of trust in stablecoin-backed products.

#### Affected Scenarios
- **Common pattern (4/9 reports):** Hardcoded $1 valuation or “1 stable = 1 USD” assumptions.
- **Common pattern (5/9 reports):** Depeg handling omitted in mint/redeem or collateral logic.
- **Recurring variant (3/9 reports):** Decimal precision mismatches between stablecoins and synthetic tokens.

### Secure Implementation

**Fix 1: Oracle-based stablecoin valuation with depeg tolerance**
```solidity
// ✅ SECURE: Use price feed with a tight peg tolerance and staleness checks
function stableToUsd(address stable, uint256 amount) internal view returns (uint256) {
    (uint256 price, uint8 decimals, uint256 updatedAt) = oracle.getPrice(stable);
    require(block.timestamp - updatedAt <= MAX_STALENESS, "stale price");
    require(_withinPeg(price, decimals, PEG_TOLERANCE_BPS), "depeg");
    return amount * price / 10 ** decimals;
}
```

**Fix 2: Normalize decimals and enforce asset pairing**
```solidity
// ✅ SECURE: Require matching decimals or normalize explicitly
function mint(address to, uint256 amount) external {
    uint8 baseDecimals = IERC20Metadata(baseAsset).decimals();
    uint8 synthDecimals = IERC20Metadata(synthAsset).decimals();
    require(baseDecimals == synthDecimals, "decimals mismatch");
    baseAsset.safeTransferFrom(msg.sender, address(this), amount);
    synthAsset.mint(to, amount);
}
```

### Detection Patterns

#### Code Patterns to Look For
- Stablecoin prices hardcoded to $1 (e.g., `return Ok(100000)` or `1 * 10**decimals`).
- Comments or logic assuming “stablecoins never depeg” without oracle validation.
- Decimal constants like `10**6` or `10**18` used without reading token decimals.
- Oracle update functions missing stablecoin tolerance checks.

#### Audit Checklist
- [ ] Verify all stablecoin valuations use an oracle or validated peg tolerance.
- [ ] Confirm mint/redeem logic handles depeg events and reverts when out of bounds.
- [ ] Ensure decimal normalization is based on `IERC20Metadata.decimals()`.
- [ ] Validate stablecoin-specific checks are applied on oracle updates and additions.

### Real-World Examples

- **The Standard Smart Vault** — stablecoins assumed at peg — [reports/stablecoin_findings/usd-stablecoins-are-incorrectly-assumed-to-always-be-at-peg.md](reports/stablecoin_findings/usd-stablecoins-are-incorrectly-assumed-to-always-be-at-peg.md)
- **Syntetika** — depeg and decimal mismatch in minting — [reports/stablecoin_findings/minter-doesnt-account-for-depegs-exchange-rates-and-decimal-precision-mismatch-b.md](reports/stablecoin_findings/minter-doesnt-account-for-depegs-exchange-rates-and-decimal-precision-mismatch-b.md)
- **LayerZeroZROClaim** — 1 stable = 1 USD assumption — [reports/stablecoin_findings/m-03-protocol-assumes-1-stable-1-usd.md](reports/stablecoin_findings/m-03-protocol-assumes-1-stable-1-usd.md)
- **Unitas Protocol** — pegged-to-asset stable priced as $1 — [reports/stablecoin_findings/m-2-usd1-is-priced-as-1-instead-of-being-pegged-to-usdt.md](reports/stablecoin_findings/m-2-usd1-is-priced-as-1-instead-of-being-pegged-to-usdt.md)
- **SuperSale** — USDC/USDT treated as $1 — [reports/stablecoin_findings/l-03-incorrect-assumption-of-usdc-and-usdt-value.md](reports/stablecoin_findings/l-03-incorrect-assumption-of-usdc-and-usdt-value.md)
- **Pump** — hardcoded stable price in Rust — [reports/stablecoin_findings/l-09-hardcoded-stablecoin-price.md](reports/stablecoin_findings/l-09-hardcoded-stablecoin-price.md)
- **SteadeFi** — depeg handling mismatch in slippage — [reports/stablecoin_findings/usdc-is-not-valued-correctly-in-case-of-a-depeg-which-causes-a-loss-of-funds.md](reports/stablecoin_findings/usdc-is-not-valued-correctly-in-case-of-a-depeg-which-causes-a-loss-of-funds.md)
- **StakeStone Tokenized Vault** — missing stable tolerance on oracle updates — [reports/stablecoin_findings/no-stablecoin-tolerance-check-for-added-oracles.md](reports/stablecoin_findings/no-stablecoin-tolerance-check-for-added-oracles.md)

### Prevention Guidelines

#### Development Best Practices
1. Use oracle feeds for stablecoins with explicit peg tolerance bounds.
2. Normalize decimals dynamically using token metadata.
3. Pause or revert mint/redeem when depeg thresholds are breached.

#### Testing Requirements
- Unit tests for: depeg scenarios ($0.95, $0.80, $1.05) and oracle staleness.
- Integration tests for: mint/redeem flows with mixed decimals (6/8/18).
- Fuzzing targets: price feeds, decimal conversions, and slippage limits.

### Keywords for Search

`stablecoin`, `depeg`, `hardcoded_price`, `1_stable_1_usd`, `decimal_mismatch`, `mint_redeem`, `collateral_valuation`, `oracle_tolerance`, `peg_validation`, `slippage_miscalculation`, `usdc`, `usdt`

### Related Vulnerabilities

- [DB/general/missing-validations](DB/general/missing-validations)
- [DB/general/rounding-precision-loss](DB/general/rounding-precision-loss)
- [DB/general/slippage-protection](DB/general/slippage-protection)
### Detection Patterns

#### Code Patterns to Look For
```
- See vulnerable pattern examples above for specific code smells
- Check for missing validation on critical state-changing operations
- Look for assumptions about external component behavior
```

#### Audit Checklist
- [ ] Verify all state-changing functions have appropriate access controls
- [ ] Check for CEI pattern compliance on external calls
- [ ] Validate arithmetic operations for overflow/underflow/precision loss
- [ ] Confirm oracle data freshness and sanity checks

### Keywords for Search

> These keywords enhance vector search retrieval:

`block.timestamp`, `collateral`, `collateral_valuation`, `decimal_normalization`, `defi`, `depeg`, `depeg_tolerance`, `getPrice`, `logic`, `mint`, `mint_redeem`, `minting`, `msg.sender`, `oracle`, `oracle_price_feed`, `pricing`, `receive`, `safeTransferFrom`, `stableToUsd`, `stablecoin`, `stablecoin_peg`, `stablecoin_pricing_assumptions`
