---
# Core Classification
protocol: Venus Multichain Support
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60188
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/venus-multichain-support/f163c791-6598-41b2-b626-b347ac0ee032/index.html
source_link: https://certificate.quantstamp.com/full/venus-multichain-support/f163c791-6598-41b2-b626-b347ac0ee032/index.html
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Shih-Hung Wang
  - Julio Aguilar
  - Ibrahim Abouzied
  - Cameron Biniamow
---

## Vulnerability Title

Chainlink Oracle Can Have Its Prices Overridden

### Overview


The Venus team has acknowledged a bug in the `ChainlinkOracle.sol` file. The `setDirectPrice()` function allows a user to manually set a price for an asset, but it is currently given priority over the price returned by a price feed, even if the feed is successful. This can lead to incorrect prices being used by the protocol. The recommendation is to check for price feed failures and whether the manually set price has become stale before using it.

### Original Finding Content

**Update**
Marked as "Acknowledged" by the Venus team. The Venus team provided the following explanation:

> The current behavior is the expected one. Direct prices are set via VIP (Venus Improvement Proposal), with the approval of the Venus Community. And it’s expected they have a higher priority than other sources, in any case

**File(s) affected:**`oracle/contracts/oracles/ChainlinkOracle.sol`

**Description:**`setDirectPrice()` allows a user with sufficient access control to manually set a price for any asset in the `prices[]` mapping. `_getPriceInternal()` will return the `prices[]` mapping if it is non-zero, preferring it over the price returned by `_getChainlinkPrice()`.

The comment specifies that the manually set price is "useful under extenuating conditions such as price feed failure". However, the price is currently used in preference of the price feed, even if it is successful. Additionally, the price never becomes stale. Even if the price is accurately set on initialization, it may not remain so and the protocol would continue operating under a false price.

**Recommendation:** Programmatically check for a price feed failure before returning the manual price. Check whether or not the manual price has become stale.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Venus Multichain Support |
| Report Date | N/A |
| Finders | Shih-Hung Wang, Julio Aguilar, Ibrahim Abouzied, Cameron Biniamow |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/venus-multichain-support/f163c791-6598-41b2-b626-b347ac0ee032/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/venus-multichain-support/f163c791-6598-41b2-b626-b347ac0ee032/index.html

### Keywords for Search

`vulnerability`

