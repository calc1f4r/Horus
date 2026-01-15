Note : Hey Agent please ignore this file, if the protocol does not use Chainlink oracles.
---
# Core Classification (Required)
protocol: generic
chain: everychain
category: oracle
vulnerability_type: chainlink_oracle_integration

# Attack Vector Details (Required)
attack_type: data_manipulation|economic_exploit|logical_error|dos
affected_component: price_feed|validation_logic|state_transition

# Oracle-Specific Fields
oracle_provider: chainlink
oracle_attack_vector: staleness|manipulation|circuit_breaker|l2_sequencer|decimal_handling|access_denial|front_running|phase_id

# Technical Primitives (Required)
primitives:
  - latestRoundData
  - staleness_check
  - heartbeat
  - minAnswer
  - maxAnswer
  - sequencer_uptime_feed
  - try_catch
  - roundId
  - phaseId
  - answeredInRound
  - decimals
  - AggregatorV3Interface
  - priceFeed
  - updatedAt
  - startedAt

# Impact Classification (Required)
severity: critical|high|medium|low
impact: incorrect_pricing|fund_loss|dos|manipulation|liquidation
exploitability: 0.80
financial_impact: high

# Context Tags
tags:
  - defi
  - lending
  - perpetuals
  - dex
  - external_dependency
  - push_based_oracle
  - l2_networks

# Version Info
language: solidity
version: all
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Staleness Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Chainlink latestRoundData stale results | `reports/chainlink_findings/chainlinks-latestrounddata-might-return-stale-or-incorrect-results.md` | MEDIUM | Multiple |
| Missing staleness check | `reports/chainlink_findings/lack-of-chainlinks-stale-price-checks.md` | MEDIUM | Multiple |
| No price staleness check | `reports/chainlink_findings/no-check-for-staleness-of-price-in-oracle.md` | MEDIUM | Multiple |
| Fixed heartbeat too stale | `reports/chainlink_findings/m-03-fixed-hearbeat-used-for-price-validation-is-too-stale-for-some-tokens.md` | MEDIUM | Sherlock |

### L2 Sequencer Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Missing Arbitrum sequencer check | `reports/chainlink_findings/missing-checks-for-whether-arbitrum-sequencer-is-active.md` | MEDIUM | Zokyo |
| No L2 sequencer uptime check | `reports/chainlink_findings/m-12-no-check-if-arbitrumoptimism-l2-sequencer-is-down-in-chainlink-feeds-priceo.md` | MEDIUM | Multiple |
| Missing sequencer check in calculateArbAmount | `reports/chainlink_findings/m-02-missing-check-for-active-l2-sequencer-in-calculatearbamount.md` | MEDIUM | Sherlock |

### Circuit Breaker / Min-Max Price Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Aggregator hits minAnswer | `reports/chainlink_findings/chainlink-aggregators-return-the-incorrect-price-if-it-drops-below-minanswer.md` | LOW-MEDIUM | Codehawks |
| Off-by-one in minMax check | `reports/chainlink_findings/m-06-off-by-one-bug-prevents-the-_compareminmax-from-detecting-chainlink-aggrega.md` | MEDIUM | Code4rena |
| Missing circuit breaker | `reports/chainlink_findings/m-09-missing-circuit-breaker-checks-in-ethpercvx-for-chainlinks-price-feed.md` | MEDIUM | Multiple |

### Deprecated API Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Usage of deprecated API | `reports/chainlink_findings/04-usage-of-deprecated-chainlink-api.md` | LOW | Code4rena |
| Deprecated latestAnswer | `reports/chainlink_findings/use-of-deprecated-chainlinks-latestanswer-function.md` | LOW | Multiple |

### Access Denial / Revert Handling
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Unhandled Chainlink revert | `reports/chainlink_findings/01-unhandled-chainlink-revert-can-lock-price-oracle-access.md` | LOW | Code4rena |
| Missing try/catch | `reports/chainlink_findings/03-vaultgetusdvalue-should-be-wrapped-in-a-try-catch.md` | LOW | Multiple |

### Decimal Handling Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Incorrect decimal handling | `reports/chainlink_findings/h-01-incorrect-handling-of-pricefeeddecimals.md` | HIGH | Code4rena |
| Decimal assumption | `reports/chainlink_findings/chainlink-decimals-assumption.md` | LOW-MEDIUM | Multiple |

### Phase/Round ID Issues
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| PhaseId change DOS | `reports/chainlink_findings/m-10-funding-settlement-will-be-dosd-for-a-time-after-the-phaseid-change-of-an-u.md` | MEDIUM | Sherlock |
| Binary search roundId issue | `reports/chainlink_findings/m-1-chainlinkaggregator-binary-search-for-roundid-does-not-work-correctly-and-or.md` | MEDIUM | Sherlock |

### External Links
- [Chainlink Data Feeds Documentation](https://docs.chain.link/data-feeds)
- [Chainlink L2 Sequencer Uptime Feeds](https://docs.chain.link/data-feeds/l2-sequencer-feeds)
- [Chainlink Best Practices](https://docs.chain.link/data-feeds#best-practices)
- [Solodit Vulnerability Database](https://solodit.cyfrin.io/)

---

# Chainlink Oracle Integration Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for Chainlink Oracle Security Audits**

---

## Table of Contents

1. [Staleness Vulnerabilities](#1-staleness-vulnerabilities)
2. [L2 Sequencer Uptime Vulnerabilities](#2-l2-sequencer-uptime-vulnerabilities)
3. [Circuit Breaker / Min-Max Price Vulnerabilities](#3-circuit-breaker--min-max-price-vulnerabilities)
4. [Deprecated API Usage](#4-deprecated-api-usage)
5. [Access Denial / Revert Handling](#5-access-denial--revert-handling)
6. [Decimal/Precision Handling](#6-decimalprecision-handling)
7. [Phase ID / Round ID Handling](#7-phase-id--round-id-handling)
8. [Price Manipulation / Front-Running](#8-price-manipulation--front-running)
9. [Heartbeat Configuration Issues](#9-heartbeat-configuration-issues)

---

## 1. Staleness Vulnerabilities

### Overview

Chainlink price feeds update prices based on deviation thresholds and heartbeat intervals. When protocols fail to validate price freshness using `updatedAt` from `latestRoundData()`, they risk using stale prices that don't reflect current market conditions.

> **📚 Source Reports for Deep Dive:**
> - `reports/chainlink_findings/chainlinks-latestrounddata-might-return-stale-or-incorrect-results.md`
> - `reports/chainlink_findings/lack-of-chainlinks-stale-price-checks.md`
> - `reports/chainlink_findings/m-03-fixed-hearbeat-used-for-price-validation-is-too-stale-for-some-tokens.md`

### Vulnerability Description

#### Root Cause

Protocols call `latestRoundData()` but ignore the `updatedAt` return value, or use hardcoded heartbeat thresholds that don't match the actual feed's update frequency. Different Chainlink feeds have different heartbeat intervals (1h, 24h, etc.).

#### Attack Scenario

1. Market volatility causes significant price movement
2. Chainlink feed hasn't updated within heartbeat interval (but within threshold)
3. Protocol uses stale price for liquidations, lending, or trading
4. Attacker exploits price discrepancy for profit

### Vulnerable Pattern Examples

**Example 1: No Staleness Check at All** [MEDIUM]
> 📖 Reference: `reports/chainlink_findings/lack-of-chainlinks-stale-price-checks.md`
```solidity
// ❌ VULNERABLE: No validation of updatedAt timestamp
function getPrice(address token) external view returns (uint256) {
    (, int256 price, , , ) = priceFeed.latestRoundData();
    require(price > 0, "Invalid price");
    return uint256(price);
}
```

**Example 2: Incomplete Validation** [MEDIUM]
> 📖 Reference: `reports/chainlink_findings/chainlinks-latestrounddata-might-return-stale-or-incorrect-results.md`
```solidity
// ❌ VULNERABLE: Missing updatedAt and startedAt checks
function getLatestPrice() public view returns (int256) {
    (uint80 roundId, int256 answer, , , uint80 answeredInRound) = 
        priceFeed.latestRoundData();
    require(answeredInRound >= roundId, "Stale price");
    require(answer > 0, "Invalid price");
    return answer;
    // Missing: updatedAt validation!
}
```

**Example 3: Fixed Heartbeat for All Tokens** [MEDIUM]
> 📖 Reference: `reports/chainlink_findings/m-03-fixed-hearbeat-used-for-price-validation-is-too-stale-for-some-tokens.md`
```solidity
// ❌ VULNERABLE: Same threshold for all feeds (24 hours)
uint256 constant HEARTBEAT = 86400; // 24 hours

function getPrice(AggregatorV3Interface feed) external view returns (uint256) {
    (, int256 price, , uint256 updatedAt, ) = feed.latestRoundData();
    require(block.timestamp - updatedAt < HEARTBEAT, "Stale price");
    // Problem: Some feeds have 1-hour heartbeat, 24h is too permissive!
    return uint256(price);
}
```

**Example 4: Zero Staleness Tolerance** [LOW]
> 📖 Reference: Pattern observed in multiple audits
```solidity
// ❌ VULNERABLE: Price considered stale even when fresh
function getPrice(AggregatorV3Interface feed) external view returns (uint256) {
    (, int256 price, , uint256 updatedAt, ) = feed.latestRoundData();
    require(block.timestamp == updatedAt, "Stale price"); // Too strict!
    return uint256(price);
}
```

### Impact Analysis

#### Technical Impact
- Incorrect price inputs for financial calculations
- Protocol operates on outdated market data
- Incorrect liquidation triggers

#### Business Impact
- Direct financial loss via arbitrage
- Unfair liquidations of healthy positions
- User fund loss due to mispriced operations
- Protocol insolvency risk (e.g., Venus/LUNA crash)

#### Affected Scenarios
- **Lending Protocols**: Incorrect collateral valuation
- **Perpetual DEXes**: Wrong funding rate calculations
- **AMMs**: Arbitrage opportunities
- **Liquidation Systems**: Unfair liquidations

### Secure Implementation

**Fix 1: Complete latestRoundData Validation**
```solidity
// ✅ SECURE: Full validation of all return values
function getLatestPrice() public view returns (int256) {
    (
        uint80 roundId,
        int256 answer,
        uint256 startedAt,
        uint256 updatedAt,
        uint80 answeredInRound
    ) = priceFeed.latestRoundData();
    
    require(answer > 0, "Chainlink: Invalid price");
    require(updatedAt > 0, "Chainlink: Round not complete");
    require(answeredInRound >= roundId, "Chainlink: Stale price round");
    require(
        block.timestamp - updatedAt <= STALENESS_THRESHOLD,
        "Chainlink: Stale price"
    );
    
    return answer;
}
```

**Fix 2: Token-Specific Heartbeat Configuration**
```solidity
// ✅ SECURE: Different heartbeats per token
mapping(address => uint256) public heartbeatThresholds;

function getPrice(address token) external view returns (uint256) {
    AggregatorV3Interface feed = priceFeeds[token];
    uint256 heartbeat = heartbeatThresholds[token];
    require(heartbeat > 0, "Heartbeat not configured");
    
    (, int256 price, , uint256 updatedAt, ) = feed.latestRoundData();
    require(block.timestamp - updatedAt <= heartbeat, "Stale price");
    return uint256(price);
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- latestRoundData() with ignored updatedAt
- latestRoundData() with ignored startedAt
- Hardcoded staleness threshold for all tokens
- Missing answeredInRound >= roundId check
- Staleness threshold significantly larger than feed heartbeat
```

#### Audit Checklist
- [ ] Verify updatedAt is checked against reasonable threshold
- [ ] Check startedAt > 0 validation exists
- [ ] Verify answeredInRound >= roundId check
- [ ] Confirm heartbeat thresholds match Chainlink feed configuration
- [ ] Check for different thresholds per token/feed

---

## 2. L2 Sequencer Uptime Vulnerabilities

### Overview

On L2 networks (Arbitrum, Optimism, Base), the sequencer can go offline. During downtime, oracle prices may become stale while appearing valid. Chainlink provides sequencer uptime feeds to detect this scenario.

> **📚 Source Reports for Deep Dive:**
> - `reports/chainlink_findings/missing-checks-for-whether-arbitrum-sequencer-is-active.md`
> - `reports/chainlink_findings/m-12-no-check-if-arbitrumoptimism-l2-sequencer-is-down-in-chainlink-feeds-priceo.md`
> - `reports/chainlink_findings/m-4-no-check-if-arbitrum-l2-sequencer-is-down-in-chainlink-feeds.md`

### Vulnerability Description

#### Root Cause

When the L2 sequencer is down, transactions are queued but not processed. Oracle prices stop updating but `latestRoundData()` still returns the last known price without any indication of staleness beyond the timestamp.

#### Attack Scenario

1. L2 sequencer goes down
2. Significant price movement occurs on L1
3. Sequencer comes back online, users submit transactions
4. Protocol uses stale L2 prices before oracles update
5. Attacker exploits stale prices for liquidations or trades

### Vulnerable Pattern Examples

**Example 1: No Sequencer Check** [MEDIUM]
> 📖 Reference: `reports/chainlink_findings/missing-checks-for-whether-arbitrum-sequencer-is-active.md`
```solidity
// ❌ VULNERABLE: No sequencer uptime validation for L2
function getPrice(AggregatorV3Interface feed) external view returns (uint256) {
    (, int256 price, , uint256 updatedAt, ) = feed.latestRoundData();
    require(block.timestamp - updatedAt < HEARTBEAT, "Stale price");
    return uint256(price);
    // Missing sequencer uptime check!
}
```

**Example 2: Missing Grace Period** [MEDIUM]
> 📖 Reference: `reports/chainlink_findings/insufficient-checks-to-confirm-the-correct-status-of-the-sequenceruptimefeed.md`
```solidity
// ❌ VULNERABLE: No grace period after sequencer restart
function getPrice() external view returns (uint256) {
    (, int256 sequencerAnswer, , , ) = sequencerUptimeFeed.latestRoundData();
    require(sequencerAnswer == 0, "Sequencer down");
    // Missing grace period! Prices may still be stale after restart
    
    (, int256 price, , , ) = priceFeed.latestRoundData();
    return uint256(price);
}
```

### Impact Analysis

#### Technical Impact
- Stale prices used during/after sequencer downtime
- Incorrect liquidation calculations
- Protocol state corruption

#### Business Impact
- Mass unfair liquidations when sequencer comes back
- Significant user fund loss
- Protocol reputation damage
- Dutch auctions executing at wrong prices

#### Affected Scenarios
- All DeFi protocols on Arbitrum, Optimism, Base
- Especially critical for lending protocols with liquidations
- Time-sensitive operations like auctions

### Secure Implementation

**Fix 1: Complete Sequencer Uptime Check with Grace Period**
```solidity
// ✅ SECURE: Full sequencer validation with grace period
AggregatorV3Interface internal sequencerUptimeFeed;
uint256 private constant GRACE_PERIOD_TIME = 3600; // 1 hour

function getLatestPrice(AggregatorV3Interface priceFeed) public view returns (int256) {
    // Check sequencer status
    (, int256 answer, uint256 startedAt, , ) = sequencerUptimeFeed.latestRoundData();
    
    // Answer == 0: Sequencer is up
    // Answer == 1: Sequencer is down
    bool isSequencerUp = answer == 0;
    require(isSequencerUp, "Sequencer is down");
    
    // Ensure grace period has passed since sequencer came back up
    uint256 timeSinceUp = block.timestamp - startedAt;
    require(timeSinceUp > GRACE_PERIOD_TIME, "Grace period not over");
    
    // Now safe to get price
    (, int256 price, , uint256 updatedAt, ) = priceFeed.latestRoundData();
    require(block.timestamp - updatedAt < STALENESS_THRESHOLD, "Stale price");
    
    return price;
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- L2 deployment without sequencerUptimeFeed integration
- Sequencer check without grace period
- Missing sequencer check in any price-fetching function
- Hardcoded L1-only oracle logic deployed to L2
```

#### Audit Checklist
- [ ] Check if protocol deploys to L2 (Arbitrum, Optimism, Base)
- [ ] Verify sequencer uptime feed is integrated
- [ ] Confirm grace period is enforced after sequencer restart
- [ ] Check all price-fetching paths include sequencer validation

---

## 3. Circuit Breaker / Min-Max Price Vulnerabilities

### Overview

Chainlink aggregators have built-in circuit breakers with `minAnswer` and `maxAnswer` values. During extreme price movements (like LUNA crash), the reported price may hit these bounds instead of reflecting actual market price.

> **📚 Source Reports for Deep Dive:**
> - `reports/chainlink_findings/chainlink-aggregators-return-the-incorrect-price-if-it-drops-below-minanswer.md`
> - `reports/chainlink_findings/m-06-off-by-one-bug-prevents-the-_compareminmax-from-detecting-chainlink-aggrega.md`
> - `reports/chainlink_findings/m-09-missing-circuit-breaker-checks-in-ethpercvx-for-chainlinks-price-feed.md`

### Vulnerability Description

#### Root Cause

When an asset's actual price drops below `minAnswer` or rises above `maxAnswer`, Chainlink returns the boundary value instead of the real price. Protocols that don't check for these boundary conditions will operate with incorrect prices.

#### Attack Scenario

1. Asset price crashes (e.g., LUNA went from $80 to $0.001)
2. Chainlink returns `minAnswer` (e.g., $0.10) instead of actual price
3. Protocol values collateral at minAnswer (100x actual value)
4. Attacker borrows assets using overvalued collateral
5. Attacker defaults, protocol suffers massive bad debt

### Vulnerable Pattern Examples

**Example 1: No Min/Max Check** [MEDIUM]
> 📖 Reference: `reports/chainlink_findings/chainlink-aggregators-return-the-incorrect-price-if-it-drops-below-minanswer.md`
```solidity
// ❌ VULNERABLE: No circuit breaker check
function getPrice() external view returns (uint256) {
    (, int256 price, , , ) = priceFeed.latestRoundData();
    require(price > 0, "Invalid price");
    return uint256(price);
    // Missing minAnswer/maxAnswer validation!
}
```

**Example 2: Off-by-One in Boundary Check** [MEDIUM]
> 📖 Reference: `reports/chainlink_findings/m-06-off-by-one-bug-prevents-the-_compareminmax-from-detecting-chainlink-aggrega.md`
```solidity
// ❌ VULNERABLE: Off-by-one allows boundary prices through
function _compareMinMax(
    IAggregator _tokenAggregator,
    int192 _answer
) internal view {
    int192 maxAnswer = _tokenAggregator.maxAnswer();
    int192 minAnswer = _tokenAggregator.minAnswer();

    // Bug: Should be >= and <= to catch boundary values!
    if (_answer > maxAnswer || _answer < minAnswer) {
        revert OracleIsDead();
    }
}
```

### Impact Analysis

#### Technical Impact
- Incorrect price during extreme market conditions
- Collateral massively overvalued during crashes
- Protocol cannot detect actual market price

#### Business Impact
- Massive bad debt accumulation (Venus/LUNA: $100M+ loss)
- Protocol insolvency
- Complete loss of user funds in worst cases

#### Real-World Examples
- **Venus Protocol**: Lost $100M+ during LUNA crash due to minAnswer returning $0.10 when LUNA was worth $0.001
- **Blizz Finance**: Similar loss on Avalanche

### Secure Implementation

**Fix 1: Direct Min/Max Boundary Check**
```solidity
// ✅ SECURE: Check if price equals boundary values
function getPrice(AggregatorV3Interface feed) external view returns (uint256) {
    (, int256 price, , uint256 updatedAt, ) = feed.latestRoundData();
    
    // Get aggregator bounds
    int192 minAnswer = IAggregator(address(feed)).minAnswer();
    int192 maxAnswer = IAggregator(address(feed)).maxAnswer();
    
    // Revert if at boundary (circuit breaker triggered)
    require(
        int192(price) > minAnswer && int192(price) < maxAnswer,
        "Price at circuit breaker boundary"
    );
    
    return uint256(price);
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- latestRoundData() without minAnswer/maxAnswer check
- Boundary check using > and < instead of >= and <=
- Missing IAggregator interface for accessing bounds
- Only checking price > 0 without upper/lower bounds
```

#### Audit Checklist
- [ ] Verify minAnswer/maxAnswer bounds are checked
- [ ] Check boundary comparison uses >= and <= (not > and <)
- [ ] Confirm fallback behavior when circuit breaker triggers
- [ ] Review handling of extreme market conditions

---

## 4. Deprecated API Usage

### Overview

Chainlink has deprecated certain API methods like `latestAnswer()` in favor of `latestRoundData()`. Using deprecated APIs may return stale data and lacks the additional validation parameters needed for secure oracle integration.

> **📚 Source Reports for Deep Dive:**
> - `reports/chainlink_findings/04-usage-of-deprecated-chainlink-api.md`
> - `reports/chainlink_findings/use-of-deprecated-chainlinks-latestanswer-function.md`
> - `reports/chainlink_findings/m-02-chainlink-pricer-is-using-a-deprecated-api.md`

### Vulnerability Description

#### Root Cause

`latestAnswer()` only returns the price without timestamps or round information, making it impossible to validate staleness or round completeness.

### Vulnerable Pattern Examples

**Example 1: Using latestAnswer** [LOW]
> 📖 Reference: `reports/chainlink_findings/04-usage-of-deprecated-chainlink-api.md`
```solidity
// ❌ VULNERABLE: Using deprecated API
function getPrice() external view returns (int256) {
    return priceFeed.latestAnswer(); // Deprecated!
}
```

**Example 2: Using answeredInRound (Being Deprecated)** [LOW]
> 📖 Reference: `reports/chainlink_findings/m-09-pendlelporacle_fetchandvalidate-uses-chainlinks-deprecated-answeredinround.md`
```solidity
// ❌ VULNERABLE: answeredInRound is being deprecated
function getPrice() external view returns (int256) {
    (uint80 roundId, int256 answer, , , uint80 answeredInRound) = 
        priceFeed.latestRoundData();
    require(answeredInRound >= roundId, "Stale"); // May not work in future
    return answer;
}
```

### Secure Implementation

**Fix 1: Use latestRoundData with Full Validation**
```solidity
// ✅ SECURE: Use modern API with proper validation
function getPrice() external view returns (int256) {
    (
        uint80 roundId,
        int256 answer,
        uint256 startedAt,
        uint256 updatedAt,
        uint80 answeredInRound
    ) = priceFeed.latestRoundData();
    
    require(answer > 0, "Invalid price");
    require(startedAt > 0, "Round not started");
    require(updatedAt > 0, "Round not complete");
    require(block.timestamp - updatedAt <= STALENESS_THRESHOLD, "Stale price");
    
    return answer;
}
```

---

## 5. Access Denial / Revert Handling

### Overview

Chainlink's multisigs can block access to price feeds. If protocols don't handle potential reverts gracefully, a blocked feed can cause complete denial of service.

> **📚 Source Reports for Deep Dive:**
> - `reports/chainlink_findings/01-unhandled-chainlink-revert-can-lock-price-oracle-access.md`
> - `reports/chainlink_findings/03-vaultgetusdvalue-should-be-wrapped-in-a-try-catch.md`
> - `reports/chainlink_findings/m-18-protocols-usability-becomes-very-limited-when-access-to-chainlink-oracle-da.md`

### Vulnerability Description

#### Root Cause

Direct calls to `latestRoundData()` without try/catch. If Chainlink blocks access, the call reverts and the entire transaction fails.

### Vulnerable Pattern Examples

**Example 1: Unprotected Direct Call** [LOW]
> 📖 Reference: `reports/chainlink_findings/01-unhandled-chainlink-revert-can-lock-price-oracle-access.md`
```solidity
// ❌ VULNERABLE: Unhandled revert can DOS entire protocol
function getPrice() public view returns (uint256) {
    (, int256 answer, , , ) = priceFeed.latestRoundData();
    return uint256(answer);
}
```

### Secure Implementation

**Fix 1: Try/Catch with Fallback**
```solidity
// ✅ SECURE: Graceful handling with fallback oracle
function getPrice() public view returns (uint256) {
    try priceFeed.latestRoundData() returns (
        uint80 roundId,
        int256 answer,
        uint256 startedAt,
        uint256 updatedAt,
        uint80 answeredInRound
    ) {
        // Validate and return
        if (answer > 0 && block.timestamp - updatedAt < STALENESS_THRESHOLD) {
            return uint256(answer);
        }
    } catch {
        // Chainlink call failed, use fallback
    }
    
    // Fallback to secondary oracle
    return fallbackOracle.getPrice();
}
```

---

## 6. Decimal/Precision Handling

### Overview

Chainlink price feeds return prices with different decimal precisions (typically 8 or 18 decimals). Assuming a fixed decimal count or miscalculating conversions leads to severely incorrect prices.

> **📚 Source Reports for Deep Dive:**
> - `reports/chainlink_findings/h-01-incorrect-handling-of-pricefeeddecimals.md`
> - `reports/chainlink_findings/chainlink-decimals-assumption.md`
> - `reports/chainlink_findings/assuming-chainlink-price-feed-decimals-can-lead-to-unintended-errors.md`

### Vulnerability Description

#### Root Cause

Hardcoded assumption that all Chainlink feeds use 8 decimals. USD-denominated feeds use 8 decimals, but ETH-denominated feeds use 18 decimals.

### Vulnerable Pattern Examples

**Example 1: Hardcoded Decimal Assumption** [HIGH]
> 📖 Reference: `reports/chainlink_findings/h-01-incorrect-handling-of-pricefeeddecimals.md`
```solidity
// ❌ VULNERABLE: Assumes all feeds have 8 decimals
function getPrice() external view returns (uint256) {
    (, int256 price, , , ) = priceFeed.latestRoundData();
    return uint256(price) * 1e10; // Assumes 8 decimals to scale to 18
    // WRONG if feed has 18 decimals!
}
```

**Example 2: Incorrect Scaling Math** [HIGH]
> 📖 Reference: Pattern observed in multiple audits
```solidity
// ❌ VULNERABLE: Wrong decimal scaling
function getPrice(AggregatorV3Interface feed) external view returns (uint256) {
    uint8 decimals = feed.decimals();
    (, int256 price, , , ) = feed.latestRoundData();
    // Bug: Should be (18 - decimals), not (decimals - 18)
    return uint256(price) * 10 ** (decimals - 18);
}
```

### Secure Implementation

**Fix 1: Dynamic Decimal Handling**
```solidity
// ✅ SECURE: Properly scale based on actual feed decimals
function getPrice(AggregatorV3Interface feed) external view returns (uint256) {
    uint8 feedDecimals = feed.decimals();
    (, int256 price, , , ) = feed.latestRoundData();
    
    if (feedDecimals < 18) {
        return uint256(price) * 10 ** (18 - feedDecimals);
    } else if (feedDecimals > 18) {
        return uint256(price) / 10 ** (feedDecimals - 18);
    }
    return uint256(price);
}
```

---

## 7. Phase ID / Round ID Handling

### Overview

Chainlink roundIds are composed of phaseId (16 bits) + aggregatorRoundId (64 bits). When the phase changes (aggregator upgrade), the roundId jumps by 2^64, which can break protocols that assume sequential roundIds.

> **📚 Source Reports for Deep Dive:**
> - `reports/chainlink_findings/m-10-funding-settlement-will-be-dosd-for-a-time-after-the-phaseid-change-of-an-u.md`
> - `reports/chainlink_findings/m-1-chainlinkaggregator-binary-search-for-roundid-does-not-work-correctly-and-or.md`
> - `reports/chainlink_findings/m-dos-in-libchainlinkoracle-when-not-considering-phaseid.md`

### Vulnerability Description

#### Root Cause

Protocols that query historical rounds using `roundId - 1` will fail after a phase change because that round doesn't exist in the new phase.

### Vulnerable Pattern Examples

**Example 1: Sequential Round Assumption** [MEDIUM]
> 📖 Reference: `reports/chainlink_findings/m-10-funding-settlement-will-be-dosd-for-a-time-after-the-phaseid-change-of-an-u.md`
```solidity
// ❌ VULNERABLE: Assumes rounds are sequential
function getHistoricalPrice(uint80 currentRound) external view returns (int256) {
    (, int256 prevPrice, , , ) = priceFeed.getRoundData(currentRound - 1);
    // REVERTS after phase change! Round doesn't exist
    return prevPrice;
}
```

### Secure Implementation

**Fix 1: Handle Phase Changes with Try/Catch**
```solidity
// ✅ SECURE: Handle phase transitions gracefully
function getHistoricalPrice(uint80 currentRound) external view returns (int256) {
    try priceFeed.getRoundData(currentRound - 1) returns (
        uint80, int256 price, uint256, uint256, uint80
    ) {
        return price;
    } catch {
        // Phase changed, try with lower phaseId
        uint16 currentPhase = uint16(currentRound >> 64);
        uint64 roundInPhase = uint64(currentRound);
        
        if (currentPhase > 0 && roundInPhase == 1) {
            // Get last round from previous phase
            uint80 prevPhaseRound = uint80((uint256(currentPhase - 1) << 64));
            // Additional logic to find valid round
        }
        revert("Historical price unavailable");
    }
}
```

---

## 8. Price Manipulation / Front-Running

### Overview

Since Chainlink updates are on-chain transactions, attackers can monitor the mempool and front-run oracle updates to profit from price changes.

> **📚 Source Reports for Deep Dive:**
> - `reports/chainlink_findings/20-oracle-price-updates-could-be-front-run-to-game-the-system.md`
> - `reports/chainlink_findings/oracle-update-front-running-allows-extraction-of-value-from-vaults.md`

### Vulnerability Description

#### Root Cause

Predictable oracle updates allow MEV bots to sandwich transactions or front-run price changes for profit.

### Impact Analysis

- MEV extraction from protocol users
- Gradual value leakage over time
- Unfair advantages for sophisticated actors

### Detection Patterns

#### Audit Checklist
- [ ] Review if protocol operations can be sandwiched around oracle updates
- [ ] Check for commit-reveal patterns to prevent front-running
- [ ] Verify slippage protection is sufficient

---

## 9. Heartbeat Configuration Issues

### Overview

Different Chainlink feeds have different heartbeat intervals. Using a single hardcoded threshold for all feeds can be too permissive for some and too strict for others.

> **📚 Source Reports for Deep Dive:**
> - `reports/chainlink_findings/m-03-fixed-hearbeat-used-for-price-validation-is-too-stale-for-some-tokens.md`
> - `reports/chainlink_findings/l-09-lack-of-heartbeat-configurability-makes-oracles-brittle-to-chainlink-change.md`
> - `reports/chainlink_findings/wrong-oracle-timeout-value-is-used-for-oraclegetassetprice.md`

### Common Heartbeat Intervals

| Asset Type | Typical Heartbeat |
|------------|-------------------|
| ETH/USD | 1 hour |
| BTC/USD | 1 hour |
| Stablecoins | 24 hours |
| Exotic pairs | 24 hours |
| L2 feeds | Variable |

### Secure Implementation

**Fix 1: Per-Feed Heartbeat Configuration**
```solidity
// ✅ SECURE: Configurable heartbeat per feed
mapping(address => uint256) public feedHeartbeats;

function setFeedHeartbeat(address feed, uint256 heartbeat) external onlyOwner {
    require(heartbeat > 0, "Invalid heartbeat");
    feedHeartbeats[feed] = heartbeat;
}

function getPrice(address feed) external view returns (uint256) {
    uint256 heartbeat = feedHeartbeats[feed];
    require(heartbeat > 0, "Feed not configured");
    
    (, int256 price, , uint256 updatedAt, ) = 
        AggregatorV3Interface(feed).latestRoundData();
    require(block.timestamp - updatedAt <= heartbeat, "Stale price");
    return uint256(price);
}
```

---

## Prevention Guidelines

### Development Best Practices

1. **Always validate ALL return values from latestRoundData()**
2. **Use token-specific heartbeat thresholds**
3. **Implement sequencer uptime checks for L2 deployments**
4. **Check minAnswer/maxAnswer circuit breaker bounds**
5. **Use try/catch for oracle calls with fallback oracles**
6. **Never assume fixed decimals - always check feed.decimals()**
7. **Handle phase ID transitions for historical queries**

### Testing Requirements

- Unit tests for stale price scenarios
- Integration tests for L2 sequencer downtime
- Fuzz tests for decimal handling
- Tests for circuit breaker boundary conditions

---

## Keywords for Search

`chainlink`, `oracle`, `latestRoundData`, `staleness`, `stale price`, `heartbeat`, `updatedAt`, `startedAt`, `roundId`, `answeredInRound`, `phaseId`, `sequencer`, `l2 sequencer`, `arbitrum`, `optimism`, `base`, `circuit breaker`, `minAnswer`, `maxAnswer`, `price feed`, `decimals`, `latestAnswer`, `deprecated`, `try catch`, `fallback oracle`, `AggregatorV3Interface`, `front-running`, `oracle manipulation`, `liquidation`, `LUNA crash`, `Venus protocol`, `price bounds`, `grace period`, `uptime feed`

---

## Related Vulnerabilities

- [Pyth Oracle Vulnerabilities](../pyth/PYTH_ORACLE_VULNERABILITIES.md)
- [Chainlink VRF Vulnerabilities](./CHAINLINK_VRF_VULNERABILITIES.md)
- [Chainlink CCIP Vulnerabilities](./CHAINLINK_CCIP_VULNERABILITIES.md)
- [Chainlink Automation Vulnerabilities](./CHAINLINK_AUTOMATION_VULNERABILITIES.md)
