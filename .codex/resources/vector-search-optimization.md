# Vector Search Optimization Guide

Database entries must be optimized for semantic search by LLMs and embedding models.

## Semantic Richness Principles

### 1. Use Domain-Specific Terminology

BAD: "Function doesn't check if price is old"

GOOD: "Protocols integrating Pyth Network's pull-based oracle fail to validate price freshness using publishTime field, allowing stale price data to persist during market volatility and be used in critical DeFi operations like liquidation calculations and collateral valuation"

### 2. Include Synonyms and Related Concepts

For every core term, add 3-5 synonyms. Example for "staleness check":
- price freshness validation
- timestamp verification
- publish time validation
- age threshold enforcement
- temporal bounds checking

### 3. Embed Attack Context

Don't just describe the bug — describe the full exploitation sequence:

```markdown
1. Market experiences 10% price movement
2. On-chain price hasn't been updated (no one paid update fee)
3. Attacker calls liquidation with stale price valuing collateral 10% lower
4. Healthy positions get unfairly liquidated
5. Attacker profits from liquidation bonus
```

### 4. Use Concrete Protocol References

Reference real protocols with audit firm and year:

> "In Mach Finance (Sherlock, 2024), missing staleness validation in `PythOracle.getPrice()` allowed liquidators to use 2-hour-old prices during volatile conditions."

## Keyword Strategy

Build comprehensive lists per entry:

| Category | Examples |
|----------|---------|
| **Primary terms** | Core vulnerability terminology |
| **API/function names** | `latestRoundData`, `getPriceUnsafe`, `convertToShares` |
| **Attack vector names** | `stale_price_attack`, `inflation_attack`, `sandwich` |
| **Impact descriptions** | `unfair_liquidation`, `fund_loss`, `DoS` |
| **Code pattern descriptors** | `missing_validation`, `inverted_condition` |
| **Protocol examples** | Real protocol names from sources |

Minimum 10 keywords per entry.

## Severity Documentation

When multiple sources disagree on severity:

**Rule**: Use the **LOWEST** rating unless strong justification exists for upgrade.

```markdown
**Severity**: MEDIUM (consensus)
- MEDIUM: Sherlock (Mach Finance), Pashov (Astrolab)
- LOW: Internal team assessment
```

Document frequency: "Unfair Liquidations (3/12 reports)" — distinguish common impacts from rare edge cases.
