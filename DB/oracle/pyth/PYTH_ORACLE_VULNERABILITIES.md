---
# Core Classification (Required)
protocol: generic
chain: everychain
category: oracle
vulnerability_type: pyth_oracle_integration

# Attack Vector Details (Required)
attack_type: data_manipulation|economic_exploit|logical_error
affected_component: price_feed|validation_logic|state_transition

# Oracle-Specific Fields
oracle_provider: pyth
oracle_attack_vector: staleness|manipulation|confidence|variance|exponent|arbitrage|entropy

# Technical Primitives (Required)
primitives:
  - confidence_interval
  - timestamp
  - max_age
  - price_feed
  - publish_time
  - exponent
  - getPriceUnsafe
  - getPriceNoOlderThan
  - updatePriceFeeds
  - pull_oracle
  - EMA_price

# Impact Classification (Required)
severity: critical
impact: incorrect_pricing|fund_loss|dos|manipulation|liquidation
exploitability: 0.75
financial_impact: high

# Context Tags
tags:
  - defi
  - lending
  - perpetuals
  - dex
  - external_dependency
  - time_dependent
  - pull_based_oracle

# Version Info
language: solidity|rust|move
version: all

# Pattern Identity (Required)
root_cause_family: missing_validation
pattern_key: missing_validation | price_feed | pyth_oracle_integration

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: multi_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - EMA_price
  - _entropyCallback
  - _getPythPrice
  - abs
  - assetExchangeRate
  - atomicSwapAndProvide
  - block.number
  - block.timestamp
  - borrow
  - burn
  - checkFreshness
  - checkInRange
  - commit
  - confidence_interval
  - createMarket
  - deposit
  - ensurePriceUpdate
  - execute
  - executeVault
  - executeWithOracle
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Staleness Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Mach Finance - Missing Staleness Check | `reports/pyth_findings/m-1-missing-staleness-check-in-pythoracle-can-lead-to-forced-liquidations-and-th.md` | MEDIUM | Sherlock |
| Astrolab - Using Stale Price | `reports/pyth_findings/m-07-using-stale-price-in-pyth-network.md` | MEDIUM | Pashov Audit Group |
| Oku Protocol - Incorrect Freshness Logic | `reports/pyth_findings/m-2-incorrect-freshness-logic-validation-in-pythoracle-breaking-the-entire-mecha.md` | MEDIUM | Sherlock |

### Confidence Interval Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Hedge Vault - Missing Confidence Check | `reports/pyth_findings/missing-pyth-oracle-confidence-interval-check.md` | LOW | OtterSec |
| Tsunami GMX - Dangerous Confidence Use | `reports/pyth_findings/dangerous-use-of-confidence-interval.md` | LOW | OtterSec |
| Reya Network - Confidence Not Validated | `reports/pyth_findings/m-03-confidence-interval-of-pyth-price-is-not-validated.md` | MEDIUM | Pashov Audit Group |

### Exponent Handling Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Radiant Riz - Exponent Unchecked | `reports/pyth_findings/pyth-feeds-exponent-unchecked.md` | LOW | OpenZeppelin |
| Euler Oracle - Positive Exponent | `reports/pyth_findings/the-pythoracle-wont-work-with-positive-expparameter.md` | LOW | Spearbit |
| Folks Finance - Unsafe Casting | `reports/pyth_findings/unsafe-casting-will-lead-to-break-of-pythnode-oracle.md` | LOW | Immunefi |

### Same-Transaction Price Manipulation
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Perpetual V3 - Two Prices Same TX | `reports/pyth_findings/h-1-two-pyth-prices-can-be-used-in-the-same-transaction-to-attack-the-lp-pools.md` | HIGH | Sherlock |
| FlatMoney - Different Prices Same TX | `reports/pyth_findings/m-8-oracle-can-return-different-prices-in-same-transaction.md` | MEDIUM | Sherlock |
| Nabla - Arbitrage Same Block | `reports/pyth_findings/m-10-arbitrage-opportunity-using-different-prices-in-the-same-block.md` | MEDIUM | Pashov Audit Group |

### Pull-Based Oracle Exploitation
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Prodigy - Empty Price Update | `reports/pyth_findings/price-manipulation-vulnerability-in-vault-execution-due-to-unchecked-pyth-oracle.md` | HIGH | Halborn |
| Perennial V2 - Out-of-Order Commits | `reports/pyth_findings/m-2-pythoracle-commit-function-doesnt-require-nor-stores-pyth-price-publish-time.md` | MEDIUM | Sherlock |

### Price Update Fee Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Prodigy - Excess ETH Not Refunded | `reports/pyth_findings/excess-eth-not-refunded-in-price-update-transactions.md` | MEDIUM | Halborn |

### Self-Liquidation Attacks
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Euler EVK - Self-Liquidation Profit | `reports/pyth_findings/self-liquidations-of-leveraged-positions-can-be-profitable.md` | HIGH | Spearbit |
| Apollon - Pull Oracle Self-Liquidation | `reports/pyth_findings/m-12-pull-based-oracle-may-allow-for-profitable-self-liquidations.md` | MEDIUM | Recon Audits |

### Pyth Entropy (VRF) Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Pyth Entropy - Seed Not Bound | `reports/pyth_findings/fortuna-entropy-seed-does-not-bind-provider-identity.md` | LOW | Trail of Bits |
| Megapot - Provider Change Attack | `reports/pyth_findings/m-06-changes-to-pyth-entropy-provider-used-by-scaledentropyprovider-allow-attack.md` | MEDIUM | Code4rena |

### External Links
- [Pyth Network Documentation](https://docs.pyth.network/)
- [Pyth SDK Solidity](https://github.com/pyth-network/pyth-sdk-solidity)
- [Solodit Vulnerability Database](https://solodit.cyfrin.io/)

---

# Pyth Oracle Integration Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for Pyth Oracle Security Audits**


---

## Table of Contents

1. [Staleness Vulnerabilities](#1-staleness-vulnerabilities)
2. [Confidence Interval Vulnerabilities](#2-confidence-interval-vulnerabilities)
3. [Exponent Handling Vulnerabilities](#3-exponent-handling-vulnerabilities)
4. [Same-Transaction Price Manipulation](#4-same-transaction-price-manipulation)
5. [Pull-Based Oracle Exploitation](#5-pull-based-oracle-exploitation)
6. [Price Update Fee Vulnerabilities](#6-price-update-fee-vulnerabilities)
7. [Self-Liquidation Attacks](#7-self-liquidation-attacks)
8. [Timestamp Validation Vulnerabilities](#8-timestamp-validation-vulnerabilities)
9. [Pyth Entropy (VRF) Vulnerabilities](#9-pyth-entropy-vrf-vulnerabilities)
10. [Integration & Configuration Vulnerabilities](#10-integration--configuration-vulnerabilities)

---

## 1. Staleness Vulnerabilities

### Overview

Pyth Network is a pull-based oracle where consumers must provide signed price updates. Unlike push-based oracles (Chainlink), prices are NOT automatically updated on-chain. This creates critical staleness risks when protocols fail to validate price freshness.

> **📚 Source Reports for Deep Dive:**
> - `reports/pyth_findings/m-1-missing-staleness-check-in-pythoracle-can-lead-to-forced-liquidations-and-th.md` (Mach Finance - Sherlock)
> - `reports/pyth_findings/m-07-using-stale-price-in-pyth-network.md` (Astrolab - Pashov)
> - `reports/pyth_findings/m-2-incorrect-freshness-logic-validation-in-pythoracle-breaking-the-entire-mecha.md` (Oku - Sherlock)



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of missing_validation"
- Pattern key: `missing_validation | price_feed | pyth_oracle_integration`
- Interaction scope: `multi_contract`
- Primary affected component(s): `price_feed|validation_logic|state_transition`
- High-signal code keywords: `EMA_price`, `_entropyCallback`, `_getPythPrice`, `abs`, `assetExchangeRate`, `atomicSwapAndProvide`, `block.number`, `block.timestamp`
- Typical sink / impact: `incorrect_pricing|fund_loss|dos|manipulation|liquidation`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `DEX.function -> LPPool.function -> LendingProtocol.function`
- Trust boundary crossed: `callback / external call`
- Shared state or sync assumption: `state consistency across operations`

#### Valid Bug Signals

- Signal 1: Critical input parameter not validated against expected range or format
- Signal 2: Oracle data consumed without staleness check or sanity bounds
- Signal 3: User-supplied address or calldata forwarded without validation
- Signal 4: Missing check allows operation under invalid or stale state

#### False Positive Guards

- Not this bug when: Validation exists but is in an upstream function caller
- Safe if: Parameter range is inherently bounded by the type or protocol invariant
- Requires attacker control of: specific conditions per pattern

### Vulnerability Description

#### Root Cause

Protocols use `getPriceUnsafe()` or fail to enforce proper staleness checks with `getPriceNoOlderThan()`. The Pyth oracle returns the most recently stored price regardless of how old it is.

#### Attack Scenario

1. Price feed hasn't been updated for an extended period
2. Significant price movement occurs in the real market
3. Attacker uses stale on-chain price to execute trades, liquidations, or borrowing at favorable rates
4. Protocol suffers financial loss due to mispriced operations

### Vulnerable Pattern Examples

**Example 1: Using getPriceUnsafe Without Staleness Check** [MEDIUM]
> 📖 Reference: `reports/pyth_findings/m-1-missing-staleness-check-in-pythoracle-can-lead-to-forced-liquidations-and-th.md`
```solidity
// ❌ VULNERABLE: No staleness validation at all
function getPrice(bytes32 priceId) public view returns (int64) {
    PythStructs.Price memory price = pyth.getPriceUnsafe(priceId);
    return price.price;
}
```

**Example 2: Meaningless publishTime > 0 Check** [MEDIUM]
> 📖 Reference: Pattern observed in multiple audits
```solidity
// ❌ VULNERABLE: publishTime > 0 is NOT a staleness check
function getPrice(bytes32 priceId) public view returns (int64) {
    PythStructs.Price memory price = pyth.getPriceUnsafe(priceId);
    require(price.publishTime > 0, "invalid price");  // This is meaningless!
    return price.price;
}
```

**Example 3: Infinite Tolerance with type(uint64).max** [MEDIUM]
> 📖 Reference: Pattern observed in multiple audits
```solidity
// ❌ VULNERABLE: Effectively disables staleness bounds
function getPrice(bytes32 priceId) public view returns (int64) {
    PythStructs.Price memory price = pyth.getPriceNoOlderThan(priceId, type(uint64).max);
    return price.price;
}
```

**Example 4: Incorrect Freshness Logic (Inverted Condition)** [MEDIUM]
> 📖 Reference: `reports/pyth_findings/m-2-incorrect-freshness-logic-validation-in-pythoracle-breaking-the-entire-mecha.md`
```solidity
// ❌ VULNERABLE: Logic is inverted - always considers prices stale
function checkInRange(bytes32 priceId, uint256 noOlderThan) public view {
    PythStructs.Price memory price = pyth.getPriceUnsafe(priceId);
    // WRONG: This condition is backwards!
    require(price.publishTime < block.timestamp - noOlderThan, "Stale Price");
}
// Should be: require(price.publishTime >= block.timestamp - noOlderThan, "Stale Price");
```

**Example 5: No Staleness Check in View Function** [LOW]
> 📖 Reference: `reports/pyth_findings/m-07-using-stale-price-in-pyth-network.md`
```solidity
// ❌ VULNERABLE: Exchange rate calculation with potentially stale price
function assetExchangeRate(uint8 inputId) public view returns (uint256) {
    if (inputPythIds[inputId] == assetPythId)
        return weiPerShare;
    PythStructs.Price memory inputPrice = pyth.getPriceUnsafe(inputPythIds[inputId]);
    PythStructs.Price memory assetPrice = pyth.getPriceUnsafe(assetPythId);
    // No publishTime validation - prices could be arbitrarily old
    return calculateRate(inputPrice, assetPrice);
}
```

### Impact Analysis

#### Technical Impact
- Incorrect price inputs for swaps, lending, liquidation logic
- Protocol operates on outdated market data
- State corruption in pricing and risk modules

#### Business Impact
- Direct financial loss via mispriced trades
- Forced unfair liquidations of healthy positions
- Loss of user trust and protocol reputation
- Potential protocol insolvency

#### Affected Scenarios
- Lending protocols: Incorrect collateral valuation
- Perpetual DEXes: Wrong funding rate calculations
- AMMs: Arbitrage opportunities against stale prices
- Liquidation systems: Unfair or blocked liquidations

### Secure Implementation

**Fix 1: Use getPriceNoOlderThan with Reasonable Max Age**
```solidity
// ✅ SECURE: Enforces maximum staleness
function getSafePrice(bytes32 priceId) public view returns (int64) {
    uint256 maxAge = 60; // 60 seconds max staleness
    PythStructs.Price memory price = pyth.getPriceNoOlderThan(priceId, maxAge);
    return price.price;
}
```

**Fix 2: Manual Staleness Check with getPriceUnsafe**
```solidity
// ✅ SECURE: Manual staleness validation
function getSafePrice(bytes32 priceId, uint256 maxAge) public view returns (int64) {
    PythStructs.Price memory price = pyth.getPriceUnsafe(priceId);
    require(
        price.publishTime >= block.timestamp - maxAge,
        "Price is stale"
    );
    return price.price;
}
```

**Fix 3: Update Before Read Pattern**
```solidity
// ✅ SECURE: Force fresh price update before reading
function getSafePriceWithUpdate(
    bytes32 priceId,
    bytes[] calldata priceUpdateData
) public payable returns (int64) {
    uint256 fee = pyth.getUpdateFee(priceUpdateData);
    pyth.updatePriceFeeds{value: fee}(priceUpdateData);
    
    PythStructs.Price memory price = pyth.getPrice(priceId);
    return price.price;
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- getPriceUnsafe() without publishTime validation
- getPriceNoOlderThan(..., type(uint64).max)
- getPriceNoOlderThan(..., VERY_LARGE_NUMBER)
- publishTime > 0 as the only validation
- Missing staleness check in price-dependent functions
- Inverted staleness conditions (< instead of >=)
```

#### Audit Checklist
- [ ] Verify all getPriceUnsafe calls have manual staleness checks
- [ ] Check getPriceNoOlderThan maxAge parameter is reasonable (< 5 minutes)
- [ ] Ensure staleness thresholds are appropriate for asset volatility
- [ ] Verify fallback oracle exists for stale price scenarios
- [ ] Check that staleness check logic is not inverted

### Real-World Examples

#### Known Exploits & Findings
- **Mach Finance** - Missing staleness check led to forced liquidations risk
- **Astrolab** - getPriceUnsafe used without publishTime verification
- **Oku Protocol** - Inverted staleness logic broke entire order system
- **Multiple DeFi Protocols** - Stale prices enabled arbitrage attacks

---

## 2. Confidence Interval Vulnerabilities

### Overview

Pyth prices include a confidence interval (`conf`) representing price uncertainty. High confidence means uncertain/unreliable price data. Ignoring this field can lead to accepting manipulated or unreliable prices.

> **📚 Source Reports for Deep Dive:**
> - `reports/pyth_findings/m-03-confidence-interval-of-pyth-price-is-not-validated.md` (Velar - Pashov)
> - `reports/pyth_findings/dangerous-price-spread-for-users.md` (LoopFi - Pashov)

### Vulnerability Description

#### Root Cause

Protocols ignore the `price.conf` field or use arbitrary constant thresholds instead of ratio-based validation. The confidence interval should be checked relative to the price magnitude.

#### Attack Scenario

1. Market experiences high volatility or low liquidity
2. Pyth reports price with wide confidence interval
3. Protocol accepts price without checking confidence
4. Attacker exploits the uncertain price for favorable trades

### Vulnerable Pattern Examples

**Example 1: Completely Ignoring Confidence Interval** [LOW]
> 📖 Reference: `reports/pyth_findings/m-03-confidence-interval-of-pyth-price-is-not-validated.md`
```solidity
// ❌ VULNERABLE: No confidence check at all
function getPrice(bytes32 priceId) public view returns (int64) {
    PythStructs.Price memory price = pyth.getPrice(priceId);
    return price.price;  // price.conf completely ignored!
}
```

**Example 2: Arbitrary Constant Threshold** [LOW]
```solidity
// ❌ VULNERABLE: Fixed constant doesn't scale with price
function getPrice(bytes32 priceId) public view returns (int64) {
    PythStructs.Price memory price = pyth.getPrice(priceId);
    require(price.conf < 1000000, "confidence too high");  // Arbitrary!
    return price.price;
}
```

**Example 3: Dangerous Price Band Calculation** [LOW]
```solidity
// ❌ VULNERABLE: Wide confidence causes large price spreads
function getPrimaryPrice(address _token, bool _maximise) public view returns (uint256) {
    PythStructs.Price memory priceStruct = pyth.getPrice(priceFeedId);
    uint256 price;
    if (_maximise) {
        price = uint256(priceStruct.price) + uint256(priceStruct.conf);
    } else {
        price = uint256(priceStruct.price) - uint256(priceStruct.conf);
    }
    return price;
}
// User can lose conf * 2 * position_size even with no price movement!
```

### Impact Analysis

#### Technical Impact
- Acceptance of unreliable price data
- Price spreads that cause deterministic losses
- Cascading errors in downstream pricing modules

#### Business Impact
- Unnecessary losses for users in volatile markets
- Potential for price manipulation during uncertainty
- Reduced protocol reliability

### Secure Implementation

**Fix 1: Ratio-Based Confidence Check**
```solidity
// ✅ SECURE: Confidence as percentage of price
function getSafePrice(
    bytes32 priceId,
    uint64 maxAge,
    uint64 maxConfBps  // e.g., 100 = 1%
) public view returns (int64) {
    PythStructs.Price memory price = pyth.getPriceNoOlderThan(priceId, maxAge);
    
    // Check confidence is within acceptable percentage of price
    require(
        uint64(price.conf) * 10_000 <= uint64(abs(price.price)) * maxConfBps,
        "Confidence interval too wide"
    );
    
    return price.price;
}

function abs(int64 x) internal pure returns (int64) {
    return x < 0 ? -x : x;
}
```

**Fix 2: Reject High-Uncertainty Prices**
```solidity
// ✅ SECURE: Maximum confidence ratio check
function validateAndGetPrice(bytes32 priceId) public view returns (int64, uint64) {
    PythStructs.Price memory price = pyth.getPrice(priceId);
    
    uint256 priceAbs = price.price >= 0 ? uint256(int256(price.price)) : uint256(-int256(price.price));
    uint256 confRatio = (uint256(price.conf) * 10000) / priceAbs;
    
    require(confRatio <= 200, "Price confidence > 2%"); // Max 2% uncertainty
    
    return (price.price, price.conf);
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- price.conf never accessed or checked
- Confidence compared to arbitrary constants
- Price ± conf used without maximum spread limits
- Missing confidence validation in critical functions
```

#### Audit Checklist
- [ ] Verify confidence interval is checked on all price reads
- [ ] Ensure confidence thresholds are ratio-based, not absolute
- [ ] Check that high-confidence scenarios trigger fallback behavior
- [ ] Verify spread calculations don't cause excessive user losses

---

## 3. Exponent Handling Vulnerabilities

### Overview

Pyth prices include an `expo` (exponent) field for decimal normalization. The actual price is `price * 10^expo`. Incorrect handling of this field leads to severely mispriced assets.

> **📚 Source Reports for Deep Dive:**
> - `reports/pyth_findings/pyth-feeds-exponent-unchecked.md` (Thala - OpenZeppelin)
> - `reports/pyth_findings/the-pythoracle-wont-work-with-positive-expparameter.md` (Perennial - Spearbit)
> - `reports/pyth_findings/unsafe-casting-will-lead-to-break-of-pythnode-oracle.md` (Synthetix - Immunefi)

### Vulnerability Description

#### Root Cause

Protocols use raw `price.price` without applying the exponent scaling, or fail to handle edge cases where exponent values are outside expected ranges.

#### Attack Scenario

1. Protocol reads Pyth price without applying exponent
2. Price is interpreted with wrong decimal precision
3. Assets are valued at 10^n times their actual value
4. Massive arbitrage or liquidation opportunities arise

### Vulnerable Pattern Examples

**Example 1: Ignoring Exponent Completely** [CRITICAL]
```solidity
// ❌ VULNERABLE: Raw price without exponent scaling
function getRawPrice(bytes32 priceId) public view returns (int64) {
    PythStructs.Price memory price = pyth.getPrice(priceId);
    return price.price;  // WRONG! Missing * 10^expo scaling
}
```

**Example 2: Hardcoded Exponent Assumption** [HIGH]
```solidity
// ❌ VULNERABLE: Assumes exponent is always -8
function getPrice(bytes32 priceId) public view returns (uint256) {
    PythStructs.Price memory price = pyth.getPrice(priceId);
    return uint256(uint64(price.price)) * 1e10;  // Assumes expo = -8, target = 18 decimals
}
```

**Example 3: Unsafe Casting with Negative Factor** [HIGH]
```solidity
// ❌ VULNERABLE: Factor can be negative, causing SafeCast revert
function process(bytes memory parameters) internal view returns (uint256) {
    PythStructs.Price memory pythData = pyth.getPriceUnsafe(priceFeedId);
    
    int256 factor = 18 + pythData.expo;  // Can be negative if expo < -18
    uint256 price = factor > 0
        ? pythData.price.toUint256() * (10 ** factor.toUint256())  // Reverts if factor < 0!
        : pythData.price.toUint256() / (10 ** factor.toUint256());
    
    return price;
}
```

**Example 4: Unchecked Exponent Range** [MEDIUM]
```solidity
// ❌ VULNERABLE: No validation of exponent bounds
function _getPythPrice() internal view returns (uint256) {
    PythStructs.Price memory priceData = pyth.getPrice(feedId);
    // If abs(expo) > 18, subtraction underflows or causes issues
    return uint256(int256(priceData.price)) * 10 ** (18 - uint32(-priceData.expo));
}
```

**Example 5: Not Handling Positive Exponents** [MEDIUM]
```solidity
// ❌ VULNERABLE: Only handles negative exponents
function normalizePrice(bytes32 priceId) public view returns (uint256) {
    PythStructs.Price memory price = pyth.getPrice(priceId);
    require(price.expo < 0, "Unexpected positive exponent");
    return uint256(uint64(price.price)) * 10 ** uint32(-price.expo);
}
// Pyth CAN return positive exponents in future - this will revert
```

### Impact Analysis

#### Technical Impact
- Prices off by orders of magnitude
- Complete breakdown of protocol pricing logic
- Potential for division by zero or overflow

#### Business Impact
- Catastrophic mispricing of assets
- Protocol insolvency risk
- Total loss of user funds possible

### Secure Implementation

**Fix 1: Proper Exponent Normalization to 18 Decimals**
```solidity
// ✅ SECURE: Handles both positive and negative exponents
function getNormalizedPrice(bytes32 priceId, uint64 maxAge) public view returns (uint256) {
    PythStructs.Price memory price = pyth.getPriceNoOlderThan(priceId, maxAge);
    
    require(price.price > 0, "Invalid price");
    
    uint256 priceValue = uint256(uint64(price.price));
    
    if (price.expo >= 0) {
        return priceValue * 10 ** (18 + uint32(price.expo));
    } else {
        int32 absExpo = -price.expo;
        if (absExpo <= 18) {
            return priceValue * 10 ** (18 - uint32(absExpo));
        } else {
            return priceValue / 10 ** (uint32(absExpo) - 18);
        }
    }
}
```

**Fix 2: With Exponent Range Validation**
```solidity
// ✅ SECURE: Validates exponent is in acceptable range
function getValidatedPrice(bytes32 priceId) public view returns (uint256) {
    PythStructs.Price memory price = pyth.getPrice(priceId);
    
    require(price.expo >= -18 && price.expo <= 18, "Exponent out of range");
    require(price.price > 0, "Invalid price");
    
    int256 scaledPrice = int256(price.price);
    int256 targetDecimals = 18;
    int256 adjustedExpo = targetDecimals + int256(price.expo);
    
    if (adjustedExpo >= 0) {
        scaledPrice *= int256(10 ** uint256(adjustedExpo));
    } else {
        scaledPrice /= int256(10 ** uint256(-adjustedExpo));
    }
    
    return uint256(scaledPrice);
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- price.expo never accessed
- Hardcoded decimal assumptions (e.g., always multiply by 1e10)
- Negative exponent casting without bounds check
- Missing handling for positive exponent values
- Unsafe int32 to uint32 casting of expo
```

#### Audit Checklist
- [ ] Verify exponent is applied in all price calculations
- [ ] Check for proper handling of both positive and negative exponents
- [ ] Ensure exponent range is validated (typically -18 to +18)
- [ ] Verify no unsafe casting operations on expo field

---

## 4. Same-Transaction Price Manipulation

### Overview

Pyth's pull-based model allows multiple price updates within a single transaction. An attacker can submit different prices to enter and exit positions at favorable rates, creating risk-free arbitrage.

> **📚 Source Reports for Deep Dive:**
> - `reports/pyth_findings/m-8-oracle-can-return-different-prices-in-same-transaction.md` (FlatMoney - Sherlock)
> - `reports/pyth_findings/m-10-arbitrage-opportunity-using-different-prices-in-the-same-block.md` (Nabla - Pashov)
> - `reports/pyth_findings/lp-deposits-and-withdrawals-can-be-arbitraged.md` (Perpetual V3 - OtterSec)

### Vulnerability Description

#### Root Cause

The protocol doesn't enforce that the same price is used throughout a transaction, or allows users to update prices between operations. Unlike push oracles, Pyth prices can be updated by anyone at any time.

#### Attack Scenario

1. Attacker collects two valid Pyth price signatures at different timestamps
2. In a single transaction: update to price1 → deposit/open position → update to price2 → withdraw/close position
3. Profit = position_size * (price2 - price1) - fees
4. Attack is risk-free and can be amplified with flash loans

### Vulnerable Pattern Examples

**Example 1: No Price Consistency Enforcement** [CRITICAL]
```solidity
// ❌ VULNERABLE: Price can change between deposit and withdraw
contract LPPool {
    function deposit(uint256 amount, bytes[] calldata priceData) external payable {
        pyth.updatePriceFeeds{value: msg.value}(priceData);
        uint256 price = getOraclePrice();
        uint256 shares = (amount * 1e18) / price;
        _mint(msg.sender, shares);
    }
    
    function withdraw(uint256 shares, bytes[] calldata priceData) external payable {
        pyth.updatePriceFeeds{value: msg.value}(priceData);
        uint256 price = getOraclePrice();  // Can be different price!
        uint256 amount = (shares * price) / 1e18;
        _burn(msg.sender, shares);
        token.transfer(msg.sender, amount);
    }
}
```

**Example 2: Arbitrageable Swap Function** [HIGH]
```solidity
// ❌ VULNERABLE: Swap without price update, followed by swap with update
contract DEX {
    function swapExactTokensForTokens(
        uint256 amountIn,
        bytes[] calldata priceData
    ) external payable {
        if (priceData.length > 0) {
            pyth.updatePriceFeeds{value: msg.value}(priceData);
        }
        uint256 price = getPrice();  // Uses current stored price
        // Execute swap...
    }
    
    // Attacker: swap without update (old price) → swap with update (new price) → profit
}
```

**Example 3: LP Deposit/Withdraw Attack Vector** [HIGH]
```solidity
// ❌ VULNERABLE: Share price based on updatable oracle
contract OracleMaker {
    function deposit(uint256 amount) external {
        uint256 price = _getPrice();  // Oracle can be updated before this
        uint256 vaultValue = _getVaultValueSafe(vault, price);
        uint256 shares = (amount * totalSupply()) / vaultValue;
        _mint(msg.sender, shares);
    }
    
    function withdraw(uint256 shares) external {
        uint256 price = _getPrice();  // Different price possible!
        uint256 vaultValue = _getVaultValueSafe(vault, price);
        uint256 amount = vaultValue * shares / totalSupply();
        _burn(msg.sender, shares);
        // Transfer amount...
    }
}
```

### Impact Analysis

#### Technical Impact
- Protocol's oracle can return different prices in same transaction
- LP pools vulnerable to deposit/withdraw arbitrage
- Order execution can be sandwiched

#### Business Impact
- Direct extraction of value from LPs
- Protocol loses funds to arbitrageurs
- Honest users receive worse execution

#### Affected Scenarios
- LP deposits and withdrawals
- Perpetual position opening/closing
- Lending collateral operations
- Any paired operations using oracle prices

### Secure Implementation

**Fix 1: Store Price Per Block**
```solidity
// ✅ SECURE: Same price used throughout block
contract SecurePriceCache {
    struct CachedPrice {
        uint256 price;
        uint256 blockNumber;
    }
    mapping(bytes32 => CachedPrice) public priceCache;
    
    function getConsistentPrice(bytes32 priceId) public returns (uint256) {
        if (priceCache[priceId].blockNumber == block.number) {
            return priceCache[priceId].price;
        }
        
        PythStructs.Price memory price = pyth.getPrice(priceId);
        uint256 normalizedPrice = normalizePrice(price);
        
        priceCache[priceId] = CachedPrice({
            price: normalizedPrice,
            blockNumber: block.number
        });
        
        return normalizedPrice;
    }
}
```

**Fix 2: Atomic Operation with Single Price Fetch**
```solidity
// ✅ SECURE: Single price fetch for paired operations
function atomicSwapAndProvide(
    bytes[] calldata priceData,
    uint256 swapAmount,
    uint256 lpAmount
) external payable {
    // Update and fetch price ONCE
    pyth.updatePriceFeeds{value: msg.value}(priceData);
    uint256 price = getPrice();
    
    // Use same price for all operations
    _executeSwap(swapAmount, price);
    _provideLiquidity(lpAmount, price);
}
```

**Fix 3: Require Trusted Relayers for LP Operations**
```solidity
// ✅ SECURE: Only trusted keepers can execute LP operations
contract TrustedLPPool {
    mapping(address => bool) public trustedRelayers;
    
    modifier onlyTrustedRelayer() {
        require(trustedRelayers[msg.sender], "Not trusted");
        _;
    }
    
    function deposit(uint256 amount) external onlyTrustedRelayer {
        // Only keepers who don't profit from manipulation can deposit
    }
    
    function withdraw(uint256 shares) external onlyTrustedRelayer {
        // Only keepers who don't profit from manipulation can withdraw
    }
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- updatePriceFeeds() callable before each operation
- No block-based price caching
- Paired operations (deposit/withdraw, open/close) use separate price fetches
- No whitelist/restrictions on who can trigger operations
- Price updates not atomically bundled with state changes
```

#### Audit Checklist
- [ ] Check if same price is used for paired operations
- [ ] Verify presence of block-based price caching
- [ ] Assess if flash loans can amplify the attack
- [ ] Check for trusted relayer restrictions on sensitive operations
- [ ] Ensure operations can't be sandwiched within same transaction

### Real-World Examples

#### Known Exploits & Findings
- **Perpetual Protocol V3** - LP pools attackable with two prices in same tx
- **FlatMoney** - Oracle could return different prices in same transaction
- **Nabla** - Arbitrage using different prices in same block

---

## 5. Pull-Based Oracle Exploitation

### Overview

Unlike push-based oracles (Chainlink) where keepers update prices, Pyth requires users to submit price updates. This creates unique attack vectors where users can strategically withhold or submit favorable prices.

> **📚 Source Reports for Deep Dive:**
> - `reports/pyth_findings/price-manipulation-vulnerability-in-vault-execution-due-to-unchecked-pyth-oracle.md` (Pear Protocol - Halborn)
> - `reports/pyth_findings/m-2-pythoracle-commit-function-doesnt-require-nor-stores-pyth-price-publish-time.md` (Perennial - Sherlock)
> - `reports/pyth_findings/attacker-can-bypass-price-update-with-empty-priceupdatedata.md` (Cega - Pashov)

### Vulnerability Description

#### Root Cause

Anyone can call `updatePriceFeeds()` with any valid (signed) price that's newer than the current on-chain price. Attackers can strategically choose which prices to submit.

#### Attack Scenario

1. Attacker monitors off-chain Pyth prices for favorable historical values
2. Attacker finds a valid signed price that benefits their position
3. Attacker submits this price and executes their operation atomically
4. Protocol uses the attacker-chosen price

### Vulnerable Pattern Examples

**Example 1: User-Controlled Price Updates** [HIGH]
```solidity
// ❌ VULNERABLE: User chooses when to update and which price to use
function executeVault(bytes[] calldata priceUpdateData) external payable {
    uint256 fee = pyth.getUpdateFee(priceUpdateData);
    pyth.updatePriceFeeds{value: fee}(priceUpdateData);
    
    int256 price = getPrice();
    // Vault execution uses user-submitted price
    settleVault(price);
}
```

**Example 2: Empty Price Update Allowed** [HIGH]
```solidity
// ❌ VULNERABLE: Empty priceUpdateData skips price update
function execute(bytes[] calldata priceUpdateData) external payable {
    updatePrice(priceUpdateData);  // Does nothing if array is empty!
    int256 oraclePriceAtExpiry = getPrice();  // Uses stale price
    // Execute with potentially old price...
}

function updatePrice(bytes[] calldata _priceUpdateData) public payable {
    uint256 fee = pyth.getUpdateFee(_priceUpdateData);
    pyth.updatePriceFeeds{value: fee}(_priceUpdateData);  // No-op if empty!
}
```

**Example 3: Out-of-Order Price Commits** [MEDIUM]
```solidity
// ❌ VULNERABLE: Commit doesn't enforce publishTime ordering
function commit(uint256 oracleVersion, bytes calldata updateData) external payable {
    // Missing: if (pythPrice.publishTime <= _lastCommittedPublishTime) revert();
    PythStructs.Price memory pythPrice = _validateAndGetPrice(oracleVersion, updateData);
    prices[oracleVersion] = pythPrice.price;
    // Attacker can commit older price after newer one!
}
```

### Impact Analysis

#### Technical Impact
- User controls which price is used for their operations
- Historical prices can be weaponized
- Protocol's price assumptions are violated

#### Business Impact
- Risk-free exploitation of price selection
- Unfair liquidations using cherry-picked prices
- Value extraction from honest users

### Secure Implementation

**Fix 1: Require Non-Empty Price Update**
```solidity
// ✅ SECURE: Ensure price is actually updated
modifier ensurePriceUpdate(bytes[] calldata priceUpdateData) {
    require(priceUpdateData.length > 0, "Price update required");
    _;
}

function execute(bytes[] calldata priceUpdateData) external payable ensurePriceUpdate(priceUpdateData) {
    uint256 fee = pyth.getUpdateFee(priceUpdateData);
    pyth.updatePriceFeeds{value: fee}(priceUpdateData);
    
    // Now price is guaranteed to be updated
    int256 price = getPrice();
    settleVault(price);
}
```

**Fix 2: Enforce Publish Time Ordering**
```solidity
// ✅ SECURE: Only accept prices newer than last committed
uint256 private lastCommittedPublishTime;

function commit(bytes calldata updateData) external payable {
    pyth.updatePriceFeeds{value: msg.value}(abi.encode(updateData));
    PythStructs.Price memory price = pyth.getPrice(feedId);
    
    require(
        price.publishTime > lastCommittedPublishTime,
        "Price must be newer than last commit"
    );
    
    lastCommittedPublishTime = price.publishTime;
    storedPrice = price.price;
}
```

**Fix 3: Trusted Keeper Pattern**
```solidity
// ✅ SECURE: Only authorized keepers can update prices
contract TrustedPriceUpdater {
    mapping(address => bool) public keepers;
    
    modifier onlyKeeper() {
        require(keepers[msg.sender], "Not keeper");
        _;
    }
    
    function updateAndExecute(
        bytes[] calldata priceUpdateData
    ) external payable onlyKeeper {
        pyth.updatePriceFeeds{value: msg.value}(priceUpdateData);
        // Execute operation...
    }
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- User-provided priceUpdateData without validation
- Empty priceUpdateData array handling
- No publishTime ordering enforcement
- updatePriceFeeds() callable by untrusted parties
- Price used in same transaction as user-triggered update
```

#### Audit Checklist
- [ ] Verify price updates cannot be skipped with empty array
- [ ] Check for publishTime ordering enforcement
- [ ] Assess if user-chosen prices can benefit them
- [ ] Verify critical operations use keeper-updated prices
- [ ] Check for time-based restrictions on user-submitted updates

---

## 6. Price Update Fee Vulnerabilities

### Overview

Pyth requires a fee (in native token) to update prices. Mishandling of this fee can lead to stuck funds, DoS conditions, or loss of user ETH.

> **📚 Source Reports for Deep Dive:**
> - `reports/pyth_findings/excess-eth-not-refunded-in-price-update-transactions.md` (Pear Protocol - Halborn)
> - `reports/pyth_findings/pyth-oracle-update-fee-is-lost-when-price-does-not-need-updating.md` (Cega - Pashov)

### Vulnerability Description

#### Root Cause

Protocols don't properly calculate the required fee, don't refund excess ETH, or don't provide adequate fee handling in payable functions.

### Vulnerable Pattern Examples

**Example 1: No Excess Fee Refund** [MEDIUM]
```solidity
// ❌ VULNERABLE: Excess ETH not refunded to user
function updatePrice(bytes[] calldata _priceUpdateData) public payable {
    uint256 fee = pyth.getUpdateFee(_priceUpdateData);
    pyth.updatePriceFeeds{value: fee}(_priceUpdateData);
    // msg.value - fee is stuck in contract!
}
```

**Example 2: Missing Payable Keyword** [HIGH]
```solidity
// ❌ VULNERABLE: Function can't receive ETH for oracle fees
function executeWithOracle(bytes[] calldata priceData) external {  // Missing payable!
    // This will fail because no ETH can be sent
    uint256 fee = pyth.getUpdateFee(priceData);
    pyth.updatePriceFeeds{value: fee}(priceData);  // Will revert!
}
```

**Example 3: Hardcoded Fee Assumption** [MEDIUM]
```solidity
// ❌ VULNERABLE: Assumes fee is always a fixed amount
function updatePrice(bytes[] calldata priceData) public payable {
    require(msg.value >= 0.001 ether, "Insufficient fee");
    pyth.updatePriceFeeds{value: 0.001 ether}(priceData);  // Fee may have changed!
}
```

### Secure Implementation

**Fix 1: Calculate Fee and Refund Excess**
```solidity
// ✅ SECURE: Proper fee handling with refund
function updatePrice(bytes[] calldata _priceUpdateData) public payable {
    uint256 fee = pyth.getUpdateFee(_priceUpdateData);
    require(msg.value >= fee, "Insufficient fee");
    
    pyth.updatePriceFeeds{value: fee}(_priceUpdateData);
    
    // Refund excess
    uint256 excess = msg.value - fee;
    if (excess > 0) {
        (bool success, ) = msg.sender.call{value: excess}("");
        require(success, "Refund failed");
    }
}
```

**Fix 2: Use getUpdateFee Dynamically**
```solidity
// ✅ SECURE: Dynamic fee calculation
function executeWithOracle(bytes[] calldata priceData) external payable {
    uint256 requiredFee = pyth.getUpdateFee(priceData);
    require(msg.value >= requiredFee, "Fee too low");
    
    pyth.updatePriceFeeds{value: requiredFee}(priceData);
    
    // Return excess to caller
    if (msg.value > requiredFee) {
        payable(msg.sender).transfer(msg.value - requiredFee);
    }
    
    // Continue with operation...
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- updatePriceFeeds() called without calculating fee first
- Missing refund of excess msg.value
- Functions calling oracle but not marked payable
- Hardcoded fee values instead of dynamic calculation
- No fee validation before oracle call
```

#### Audit Checklist
- [ ] Verify fee is calculated with getUpdateFee()
- [ ] Check excess ETH is refunded to sender
- [ ] Ensure all oracle-calling functions are payable
- [ ] Verify fee amount is validated before operations

---

## 7. Self-Liquidation Attacks

### Overview

Pull-based oracles enable attackers to open positions and liquidate themselves in the same transaction by sandwiching price updates, extracting value from the protocol.

> **📚 Source Reports for Deep Dive:**
> - `reports/pyth_findings/self-liquidations-of-leveraged-positions-can-be-profitable.md` (Euler - Spearbit)

### Vulnerability Description

#### Root Cause

The ability to update prices on-demand allows attackers to create positions at one price and immediately liquidate at another, profiting from the price difference minus fees.

#### Attack Scenario

1. Find collateral/debt pair with significant historical price volatility
2. Flash loan collateral, open max leverage position at current price
3. Update oracle to a historical price where position is liquidatable
4. Self-liquidate, repay flash loan, pocket the profit

### Vulnerable Pattern Examples

**Example 1: No Protection Against Same-Tx Liquidation** [HIGH]
```solidity
// ❌ VULNERABLE: Position can be opened and liquidated in same tx
contract LendingProtocol {
    function borrow(uint256 amount, bytes[] calldata priceData) external payable {
        updateOraclePrice(priceData);
        // Create position...
    }
    
    function liquidate(address user, bytes[] calldata priceData) external payable {
        updateOraclePrice(priceData);  // Attacker updates to liquidatable price
        // Liquidate position...
    }
    
    // Attacker can call borrow() then liquidate() with different prices!
}
```

### Profitability Calculation

```
Profit = maxBorrowAssets - maxRepayAssets - fees

Where:
- maxBorrowAssets = LTV_borrow * collateralBalance * collateralPrice_0 / debtPrice
- maxRepayAssets = collateralBalance * discountFactor * collateralPrice_1 / debtPrice

Profitable when:
LTV_borrow > discountFactor * (1 - priceDrop)
```

### Secure Implementation

**Fix 1: Time Lock Between Operations**
```solidity
// ✅ SECURE: Minimum time between position open and liquidation
mapping(address => uint256) public positionOpenTime;

function borrow(uint256 amount) external {
    // ... create position
    positionOpenTime[msg.sender] = block.timestamp;
}

function liquidate(address user) external {
    require(
        block.timestamp >= positionOpenTime[user] + MIN_POSITION_AGE,
        "Position too young"
    );
    // ... liquidate
}
```

**Fix 2: Block-Based Price Lock**
```solidity
// ✅ SECURE: Same price must be used within a block
mapping(bytes32 => mapping(uint256 => uint256)) public blockPriceCache;

function getBlockLockedPrice(bytes32 feedId) internal returns (uint256) {
    if (blockPriceCache[feedId][block.number] == 0) {
        blockPriceCache[feedId][block.number] = getCurrentOraclePrice(feedId);
    }
    return blockPriceCache[feedId][block.number];
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- Open and close operations in same transaction possible
- No time lock between position creation and liquidation
- User-controllable price updates before liquidations
- No block-based price consistency enforcement
```

#### Audit Checklist
- [ ] Check for minimum position age before liquidation
- [ ] Verify price consistency within transactions/blocks
- [ ] Assess profitability of self-liquidation attack
- [ ] Check if flash loans can amplify the attack

---

## 8. Timestamp Validation Vulnerabilities

### Overview

Proper validation of Pyth's `publishTime` is crucial. Incorrect comparisons or missing validations can allow manipulation or break functionality.

> **📚 Source Reports for Deep Dive:**
> - `reports/pyth_findings/m-2-pythoracle-commit-function-doesnt-require-nor-stores-pyth-price-publish-time.md` (Perennial - Sherlock)
> - `reports/pyth_findings/m-2-incorrect-freshness-logic-validation-in-pythoracle-breaking-the-entire-mecha.md` (Oku - Sherlock)

### Vulnerable Pattern Examples

**Example 1: Wrong Timestamp Comparison Operator** [HIGH]
```solidity
// ❌ VULNERABLE: Uses < instead of >=, logic is inverted
function checkFreshness(bytes32 priceId, uint256 noOlderThan) public view {
    PythStructs.Price memory price = pyth.getPriceUnsafe(priceId);
    require(price.publishTime < block.timestamp - noOlderThan, "Stale");
    // Should be: price.publishTime >= block.timestamp - noOlderThan
}
```

**Example 2: No Publish Time Stored** [MEDIUM]
```solidity
// ❌ VULNERABLE: Only stores price, not publishTime
function commit(bytes calldata updateData) external payable {
    pyth.updatePriceFeeds{value: msg.value}(abi.encode(updateData));
    PythStructs.Price memory price = pyth.getPrice(feedId);
    storedPrice = price.price;
    // Missing: storedPublishTime = price.publishTime;
    // Cannot verify ordering for future commits!
}
```

**Example 3: Future Timestamp Allowed** [MEDIUM]
```solidity
// ❌ VULNERABLE: No check for future timestamps
function validatePrice(bytes32 priceId) public view returns (int64) {
    PythStructs.Price memory price = pyth.getPrice(priceId);
    require(price.publishTime > 0, "Invalid");
    // Missing: require(price.publishTime <= block.timestamp, "Future timestamp");
    return price.price;
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Complete timestamp validation
function getValidatedPrice(bytes32 priceId, uint256 maxAge) public view returns (int64) {
    PythStructs.Price memory price = pyth.getPriceUnsafe(priceId);
    
    // Check price is not from the future
    require(price.publishTime <= block.timestamp, "Future timestamp");
    
    // Check price is not too old
    require(
        price.publishTime >= block.timestamp - maxAge,
        "Price too stale"
    );
    
    return price.price;
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- Inverted comparison operators (< instead of >=)
- Missing future timestamp check
- publishTime not stored for ordering verification
- No sanity checks on timestamp values
```

---

## 9. Pyth Entropy (VRF) Vulnerabilities

### Overview

Pyth Entropy provides verifiable randomness. Vulnerabilities include sequence number collisions, callback manipulation, and entropy seed binding issues.

> **📚 Source Reports for Deep Dive:**
> - `reports/pyth_findings/fortuna-entropy-seed-does-not-bind-provider-identity.md` (Pyth Network - Trail of Bits)
> - `reports/pyth_findings/m-06-changes-to-pyth-entropy-provider-used-by-scaledentropyprovider-allow-attack.md` (Megapot - Code4rena)

### Vulnerable Pattern Examples

**Example 1: Sequence Number Not Bound to Provider** [HIGH]
```solidity
// ❌ VULNERABLE: Same sequence can exist for different providers
mapping(uint64 => PendingRequest) private pending;

function requestRandomness() external payable returns (uint64 sequence) {
    sequence = entropy.requestV2{value: msg.value}(entropyProvider, gasLimit);
    pending[sequence].callback = msg.sender;
    // If provider changes, attacker can collide sequence numbers!
}
```

**Example 2: Callback Can Be Made to Revert** [MEDIUM]
```solidity
// ❌ VULNERABLE: Malicious callback prevents clearing pending state
function _entropyCallback(uint64 sequence, bytes32 randomNumber) internal {
    PendingRequest storage request = pending[sequence];
    (bool success, ) = request.callback.call(
        abi.encodeWithSelector(request.selector, randomNumber)
    );
    // If callback reverts, pending[sequence] is never cleared
    // Attacker can exploit this for sequence collisions
    delete pending[sequence];
}
```

**Example 3: Entropy Seed Not Bound to Provider Address** [MEDIUM]
```rust
// ❌ VULNERABLE: Seed derivation doesn't include provider address
pub fn from_config(
    secret: &str,
    chain_id: &ChainId,
    random: &[u8; 32],
    chain_length: u64,
) -> Result<Self> {
    let mut input: Vec<u8> = vec![];
    input.extend_from_slice(&hex::decode(secret)?);
    input.extend_from_slice(&chain_id.as_bytes());
    input.extend_from_slice(random);
    // Missing: input.extend_from_slice(&provider_address);
    let secret: [u8; 32] = Keccak256::digest(input).into();
    Ok(Self::new(secret, chain_length.try_into()?))
}
```

### Secure Implementation

**Fix 1: Bind Requests to Provider Address**
```solidity
// ✅ SECURE: Include provider in request tracking
mapping(address => mapping(uint64 => PendingRequest)) private pending;

function requestRandomness() external payable returns (uint64 sequence) {
    sequence = entropy.requestV2{value: msg.value}(entropyProvider, gasLimit);
    pending[entropyProvider][sequence].callback = msg.sender;
}
```

**Fix 2: Handle Callback Failures Gracefully**
```solidity
// ✅ SECURE: Clear state even if callback fails
function _entropyCallback(uint64 sequence, bytes32 randomNumber) internal {
    PendingRequest memory request = pending[sequence];
    delete pending[sequence];  // Clear BEFORE callback
    
    try ICallback(request.callback).onRandomness(randomNumber) {
        // Success
    } catch {
        // Log failure but don't revert
        emit CallbackFailed(sequence, request.callback);
    }
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- Sequence numbers not bound to provider address
- Callback can revert and block state cleanup
- Entropy seed derivation missing unique identifiers
- No validation of entropy provider changes
```

---

## 10. Integration & Configuration Vulnerabilities

### Overview

Misconfiguration of Pyth integration parameters, hardcoded addresses, and improper setup can cause protocol failures.

> **📚 Source Reports for Deep Dive:**
> - `reports/pyth_findings/pyth-price-feed-doesnt-use-latest-hermes-api-endpoint.md` (Cega - Pashov)
> - `reports/pyth_findings/using-deprecated-hermes-api-endpoints.md` (Truflation - Pashov)

### Vulnerable Pattern Examples

**Example 1: Hardcoded Pyth Network URL** [LOW]
```solidity
// ❌ VULNERABLE: Cannot change endpoint if it moves
string constant PYTH_URL = "https://hermes.pyth.network";
// If endpoint changes, contract is bricked
```

**Example 2: Deprecated API Endpoint Usage** [MEDIUM]
```javascript
// ❌ VULNERABLE: Using deprecated Hermes API endpoint
const pythUrl = "https://hermes.pyth.network/api/latest_price_feeds";
// This endpoint may be deprecated and stop working
```

**Example 3: Price Feed Mismatch with Token** [HIGH]
```solidity
// ❌ VULNERABLE: No validation that feed matches token
function createMarket(
    address baseToken,
    bytes32 priceFeedId  // User can provide wrong feed!
) external {
    markets[baseToken] = Market({
        token: baseToken,
        feed: priceFeedId  // Could be ETH feed for BTC token!
    });
}
```

**Example 4: Unconfigurable Staleness Threshold** [MEDIUM]
```solidity
// ❌ VULNERABLE: Hardcoded staleness may be wrong for some assets
uint256 constant MAX_PRICE_AGE = 3600;  // 1 hour - too long for volatile assets!

function getPrice(bytes32 feedId) public view returns (int64) {
    return pyth.getPriceNoOlderThan(feedId, MAX_PRICE_AGE).price;
}
```

### Secure Implementation

**Fix 1: Configurable Parameters**
```solidity
// ✅ SECURE: Admin-configurable parameters
contract SecurePythOracle {
    address public pythAddress;
    mapping(bytes32 => uint256) public feedMaxAge;
    
    function setPythAddress(address _pyth) external onlyOwner {
        pythAddress = _pyth;
    }
    
    function setFeedMaxAge(bytes32 feedId, uint256 maxAge) external onlyOwner {
        require(maxAge > 0 && maxAge <= 3600, "Invalid max age");
        feedMaxAge[feedId] = maxAge;
    }
}
```

**Fix 2: Validate Feed-Token Mapping**
```solidity
// ✅ SECURE: Verify feed is appropriate for token
function createMarket(
    address baseToken,
    bytes32 priceFeedId,
    string calldata expectedSymbol
) external onlyOwner {
    // Verify the feed exists and matches expected symbol
    PythStructs.Price memory price = pyth.getPrice(priceFeedId);
    require(price.price > 0, "Invalid feed");
    
    // Additional off-chain verification of feed<->token mapping recommended
    emit MarketCreated(baseToken, priceFeedId, expectedSymbol);
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- Hardcoded Pyth contract addresses
- Hardcoded API endpoints
- No validation of feed-to-token mapping
- Unconfigurable staleness thresholds
- Missing admin functions for parameter updates
```

---

## Prevention Guidelines

### Development Best Practices

1. **Always validate staleness** - Use `getPriceNoOlderThan()` with appropriate max age
2. **Check confidence intervals** - Reject prices with confidence > 1-2% of price
3. **Apply exponent scaling** - Never use raw `price.price` without `10^expo` scaling
4. **Enforce price consistency** - Cache prices per block for paired operations
5. **Validate price updates** - Don't accept empty `priceUpdateData` arrays
6. **Refund excess fees** - Always return unused ETH to users
7. **Use configurable parameters** - Don't hardcode addresses or thresholds
8. **Implement fallback oracles** - Have backup price sources for stale data

### Testing Requirements

#### Unit Tests
- Staleness rejection at boundary conditions
- Confidence interval threshold enforcement
- Exponent normalization for various expo values
- Fee calculation and refund logic

#### Integration Tests
- Same-transaction price manipulation attempts
- Self-liquidation attack scenarios
- Price update with empty data handling
- Oracle failover to backup

#### Fuzzing Targets
- Exponent values (-18 to +18 range)
- Confidence interval edge cases
- Timestamp manipulation attempts
- Fee overpayment scenarios

---

## Keywords for Search

`pyth`, `oracle`, `stale_price`, `staleness`, `confidence_interval`, `variance`, `max_age`, `publish_time`, `price_feed`, `expo`, `exponent`, `normalization`, `incorrect_pricing`, `oracle_integrity`, `getPriceUnsafe`, `getPriceNoOlderThan`, `updatePriceFeeds`, `pull_oracle`, `push_oracle`, `price_manipulation`, `same_transaction`, `arbitrage`, `liquidation`, `self_liquidation`, `flash_loan`, `sandwich_attack`, `entropy`, `VRF`, `randomness`, `sequence_number`, `fee_refund`, `EMA_price`, `price_confidence`, `oracle_adapter`, `price_cache`, `block_price`

---

## Related Vulnerabilities

- [Chainlink Oracle Vulnerabilities](../chainlink/CHAINLINK_VULNERABILITIES.md)
- [TWAP Oracle Manipulation](../twap/TWAP_VULNERABILITIES.md)
- [Flash Loan Attacks](../../economic/FLASH_LOAN_ATTACKS.md)
- [Liquidation Vulnerabilities](../../logic/LIQUIDATION_VULNERABILITIES.md)

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

`EMA_price`, `_entropyCallback`, `_getPythPrice`, `abs`, `assetExchangeRate`, `atomicSwapAndProvide`, `block.number`, `block.timestamp`, `borrow`, `burn`, `checkFreshness`, `checkInRange`, `commit`, `confidence_interval`, `createMarket`, `defi`, `deposit`, `dex`, `ensurePriceUpdate`, `execute`, `executeVault`, `executeWithOracle`, `exponent`, `external_dependency`, `getPriceNoOlderThan`, `getPriceUnsafe`, `lending`, `max_age`, `oracle`, `perpetuals`, `price_feed`, `publish_time`, `pull_based_oracle`, `pull_oracle`, `pyth_oracle_integration`, `time_dependent`, `timestamp`, `updatePriceFeeds`
