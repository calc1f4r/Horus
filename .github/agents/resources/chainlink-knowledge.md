# Chainlink Oracle - Quick Knowledge Reference

> **Purpose**: Fast lookup reference for the `chainlink-reasoning-agent`. Contains condensed reasoning prompts, checklists, and vulnerability signatures.

---

## Core Validation Requirements

| Check | Required | Attack If Missing |
|-------|----------|-------------------|
| `answer > 0` | ✓ | Invalid/zero price used |
| `updatedAt > 0` | ✓ | Incomplete round used |
| `block.timestamp - updatedAt < threshold` | ✓ | Stale price exploitation |
| `minAnswer < answer < maxAnswer` | ✓ | Circuit breaker bypass |
| Sequencer uptime (L2) | ✓ (L2 only) | Post-downtime exploitation |

---

## Vulnerability Quick Checklist

### ⚠️ Category 1: Staleness Vulnerabilities

**One-liner**: Protocol uses outdated prices that don't reflect current market conditions.

**Quick Checks:**
- [ ] Is `updatedAt` validated from latestRoundData()?
- [ ] Is threshold per-token or hardcoded single value?
- [ ] Does threshold match feed's actual heartbeat?
- [ ] Is startedAt > 0 checked?

**Exploit Signature:**
```solidity
(, int256 price, , , ) = feed.latestRoundData();  // ❌ updatedAt ignored!
```

**Common Heartbeats:**
| Feed | Mainnet | L2 |
|------|---------|-----|
| ETH/USD | 1 hour | 1 hour |
| BTC/USD | 1 hour | 1 hour |
| Altcoins | 24 hours | 24 hours |

**Reasoning Prompt:**
> "If the price is 23 hours old and market dropped 50%, what happens?"

---

### ⚠️ Category 2: L2 Sequencer Vulnerabilities

**One-liner**: L2 prices appear fresh but are stale due to sequencer downtime.

**Quick Checks:**
- [ ] Is this deployed on Arbitrum/Optimism/Base?
- [ ] Is sequencerUptimeFeed used?
- [ ] Is GRACE_PERIOD enforced after sequencer restart?
- [ ] Is startedAt from sequencer feed checked?

**Exploit Signature:**
```solidity
// ❌ No sequencer check on L2
function getPrice() external view returns (uint256) {
    (, int256 price, , uint256 updatedAt, ) = feed.latestRoundData();
    require(block.timestamp - updatedAt < HEARTBEAT);  // Passes but stale!
    return uint256(price);
}
```

**Grace Period Requirement:**
- Minimum: 1 hour after sequencer restart
- Sequencer answer: 0 = up, 1 = down

**Reasoning Prompt:**
> "If sequencer was down for 2 hours during a price crash, who gets liquidated unfairly?"

---

### ⚠️ Category 3: Circuit Breaker / Min-Max Price

**One-liner**: During extreme crashes, Chainlink returns minAnswer instead of actual price.

**Quick Checks:**
- [ ] Does protocol check answer against minAnswer/maxAnswer?
- [ ] Is the comparison `> minAnswer`, not `>= minAnswer`?
- [ ] What happens if price equals boundary value?

**Exploit Signature:**
```solidity
// ❌ No circuit breaker check
require(price > 0);  // Passes when price = minAnswer!
```

**Real-World Impact:**
- Venus Protocol: $100M+ loss during LUNA crash
- minAnswer returned $0.10 when LUNA was $0.001

**Reasoning Prompt:**
> "If LUNA crashes to $0.001 but Chainlink returns $0.10, what can I borrow against it?"

---

### ⚠️ Category 4: Deprecated API Usage

**One-liner**: Using deprecated functions that lack validation data.

**Quick Checks:**
- [ ] Is `latestAnswer()` used? (deprecated)
- [ ] Is only `answeredInRound` relied upon? (being deprecated)
- [ ] Are all 5 return values from latestRoundData() validated?

**Exploit Signature:**
```solidity
int256 price = feed.latestAnswer();  // ❌ Deprecated, no validation possible
```

**Reasoning Prompt:**
> "Without updatedAt, how do I know this price isn't from yesterday?"

---

### ⚠️ Category 5: Access Denial / Revert Handling

**One-liner**: If Chainlink reverts, protocol becomes completely unusable.

**Quick Checks:**
- [ ] Is latestRoundData() wrapped in try/catch?
- [ ] Is there a fallback oracle?
- [ ] Can users still withdraw during oracle failure?

**Exploit Signature:**
```solidity
// ❌ Unprotected call - can DOS entire protocol
(, int256 price, , , ) = feed.latestRoundData();
```

**Secure Pattern:**
```solidity
try feed.latestRoundData() returns (...) {
    // Use price
} catch {
    // Fallback to secondary oracle
}
```

**Reasoning Prompt:**
> "If Chainlink blocks access, can users still withdraw their funds?"

---

### ⚠️ Category 6: Decimal Handling

**One-liner**: Wrong decimal assumptions cause catastrophic mispricing.

**Quick Checks:**
- [ ] Is feed.decimals() queried or hardcoded assumption?
- [ ] Is scaling math correct: `10**(18 - decimals)`?
- [ ] Are both USD (8) and ETH (18) denominated feeds handled?

**Exploit Signature:**
```solidity
// ❌ Assumes 8 decimals for all feeds
return uint256(price) * 1e10;  // Wrong for 18-decimal feeds!
```

**Feed Decimals:**
| Denomination | Decimals |
|--------------|----------|
| USD pairs (ETH/USD) | 8 |
| ETH pairs (TOKEN/ETH) | 18 |

**Reasoning Prompt:**
> "If I use 1e10 multiplier on an 18-decimal feed, what's the price error?"

---

### ⚠️ Category 7: Phase ID / Round ID Issues

**One-liner**: Round ID math breaks after Chainlink aggregator upgrade.

**Quick Checks:**
- [ ] Does protocol query historical rounds with `roundId - 1`?
- [ ] Is phase change (roundId jump by 2^64) handled?
- [ ] Is there try/catch for getRoundData on historical rounds?

**Exploit Signature:**
```solidity
// ❌ Will revert after phase change
(, int256 prevPrice, , , ) = feed.getRoundData(currentRound - 1);
```

**Round ID Structure:**
```
roundId = (phaseId << 64) | aggregatorRoundId
```
After phase change, roundId jumps by 2^64, so `roundId - 1` doesn't exist.

**Reasoning Prompt:**
> "After Chainlink upgrades the aggregator, will my historical price queries still work?"

---

### ⚠️ Category 8: Front-Running Oracle Updates

**One-liner**: Attackers see oracle updates in mempool and trade before they're applied.

**Quick Checks:**
- [ ] Can operations be sandwiched around oracle updates?
- [ ] Is there commit-reveal pattern for sensitive operations?
- [ ] Is slippage protection sufficient?

**Reasoning Prompt:**
> "If I see a 5% price increase in the mempool, what can I front-run?"

---

### ⚠️ Category 9: Heartbeat Configuration

**One-liner**: Single threshold for all tokens is too loose for some, too strict for others.

**Quick Checks:**
- [ ] Are per-token heartbeat thresholds configured?
- [ ] Does 24h threshold apply to 1h heartbeat feeds?
- [ ] Is there a way to update thresholds per feed?

**Exploit Signature:**
```solidity
uint256 constant HEARTBEAT = 86400;  // ❌ Same for all tokens!
```

**Reasoning Prompt:**
> "If ETH/USD hasn't updated in 2 hours but passes 24h check, what trades are exploitable?"

---

## Complete Validation Template

```solidity
// ✅ SECURE: Complete Chainlink validation
function getPrice(AggregatorV3Interface feed) public view returns (uint256) {
    // 1. L2 Sequencer Check (if on L2)
    if (isL2) {
        (, int256 answer, uint256 startedAt, , ) = sequencerUptimeFeed.latestRoundData();
        require(answer == 0, "Sequencer down");
        require(block.timestamp - startedAt > GRACE_PERIOD, "Grace period");
    }
    
    // 2. Get price with all return values
    (
        uint80 roundId,
        int256 price,
        uint256 startedAt,
        uint256 updatedAt,
        uint80 answeredInRound
    ) = feed.latestRoundData();
    
    // 3. Basic validation
    require(price > 0, "Invalid price");
    require(startedAt > 0, "Round not started");
    require(updatedAt > 0, "Round not complete");
    
    // 4. Staleness check (per-token threshold)
    require(block.timestamp - updatedAt <= heartbeatThreshold[feed], "Stale");
    
    // 5. Circuit breaker check
    int192 minAnswer = IAggregator(address(feed)).minAnswer();
    int192 maxAnswer = IAggregator(address(feed)).maxAnswer();
    require(int192(price) > minAnswer && int192(price) < maxAnswer, "Circuit breaker");
    
    // 6. Decimal scaling
    uint8 decimals = feed.decimals();
    return uint256(price) * 10**(18 - decimals);
}
```

---

## Keywords for Code Search

```bash
# Staleness patterns
rg -n "latestRoundData|updatedAt|staleness|heartbeat"

# L2 sequencer patterns
rg -n "sequencerUptimeFeed|GRACE_PERIOD|isSequencerUp"

# Circuit breaker patterns
rg -n "minAnswer|maxAnswer|circuit"

# Decimal patterns
rg -n "decimals\(\)|1e8|1e10|1e18"

# Deprecated patterns
rg -n "latestAnswer\(\)|answeredInRound"

# Try/catch patterns
rg -n "try.*latestRoundData|catch"
```

---

## References

- Full Database: [CHAINLINK_PRICE_FEED_VULNERABILITIES.md](../../DB/oracle/chainlink/CHAINLINK_PRICE_FEED_VULNERABILITIES.md)
- Main Agent: [chainlink-reasoning-agent.md](../chainlink-reasoning-agent.md)
- Chainlink Docs: [docs.chain.link](https://docs.chain.link)
