---
# Core Classification
protocol: Ronin
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45246
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-10-ronin
source_link: https://code4rena.com/reports/2024-10-ronin
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
finders_count: 0
finders:
---

## Vulnerability Title

[01] Use of Uniswap's `slot0` value in Quoter may lead to volatile estimates

### Overview

See description below for full details.

### Original Finding Content


The MixedRouteQuoterV1 contract uses Uniswap's `slot0` value to provide quotes for swap outcomes. While efficient, this approach may result in more volatile and potentially less accurate quotes compared to using time-weighted average prices (TWAP).

### Description

The contract retrieves the current price from the Uniswap pool's `slot0` storage, which represents the most recent price update. This method is fast and gas-efficient but can be subject to short-term price fluctuations and potential manipulation, especially in low liquidity situations. As a result, the quotes provided may not always reflect the most representative price for users looking to execute swaps.

[MixedRouteQuoterV1.sol#L62](https://github.com/ronin-chain/katana-v3-contracts/blob/03c80179e04f40d96f06c451ea494bb18f2a58fc/src/periphery/lens/MixedRouteQuoterV1.sol#L62)

```solidity
Contract: MixedRouteQuoterV1.sol
Line 62: (uint160 v3SqrtPriceX96After, int24 tickAfter,,,,,,) = pool.slot0();
```

### Impact

The use of `slot0` for quoting may lead to:
- More volatile quote results.
- Potential for less accurate estimates during periods of high volatility.
- Slightly increased susceptibility to short-term price manipulations.

However, as this is a quoter contract explicitly designed for off-chain use and quick estimates, the overall impact is low. Users are expected to understand that quotes are estimates and may change before trade execution.

### Recommended Mitigation

Consider implementing an optional TWAP-based quoting function for users who prefer more stable estimates.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Ronin |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2024-10-ronin
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2024-10-ronin

### Keywords for Search

`vulnerability`

