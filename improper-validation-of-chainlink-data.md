---
# Core Classification
protocol: Advanced Blockchain
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17699
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/AdvancedBlockchainQ12022.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/AdvancedBlockchainQ12022.pdf
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Troy Sargent
  - Anish Naik
  - Nat Chin
---

## Vulnerability Title

Improper validation of Chainlink data

### Overview

See description below for full details.

### Original Finding Content

## Diﬃculty: Medium

## Type: Data Validation

## Target: 
v2-sdk-contracts/contracts/libraries/oracles/ChainlinkLib.sol

## Description
The `latestRoundData` function returns a signed integer that is coerced to an unsigned integer without checking that the value is positive. An overflow (e.g., `uint(-1)`) would result in drastic misrepresentation of the price and unexpected behavior.

In addition, `ChainlinkLib` does not ensure the completeness or recency of round data, so pricing data may not reflect recent changes. It is best practice to define a window in which data is considered sufficiently recent (e.g., within a minute of the last update) by comparing the block timestamp to `updatedAt`.

```solidity
(, int256 price, , , ) = _aggregator.latestRoundData();
return uint256(price);
```
*Figure 16.1: Part of the `getCurrentTokenPrice` function in ChainlinkLib.sol:113-114*

## Recommendations
**Short term:** Have `latestRoundData` and similar functions verify that values are non-negative before converting them to unsigned integers, and add an invariant—`require(updatedAt != 0 && answeredInRound == roundID)`—to ensure that the round has finished and that the pricing data is from the current round.

**Long term:** Define a minimum update threshold and add the following check:
```solidity
require((block.timestamp - updatedAt <= minThreshold) && (answeredInRound == roundID));
```

---

**Trail of Bits**  
**Advanced Blockchain Security Assessment**  
**PUBLIC**

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Advanced Blockchain |
| Report Date | N/A |
| Finders | Troy Sargent, Anish Naik, Nat Chin |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/AdvancedBlockchainQ12022.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/AdvancedBlockchainQ12022.pdf

### Keywords for Search

`vulnerability`

