---
# Core Classification
protocol: WeightedLiquidityPool
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52425
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/dexodus/weightedliquiditypool
source_link: https://www.halborn.com/audits/dexodus/weightedliquiditypool
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
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

Price Discrepancy Risk Between Chainlink Oracle and Uniswap

### Overview

See description below for full details.

### Original Finding Content

##### Description

The `rebalancePool` function and the `swapUsdcToEthExactOutput` logic rely on the Chainlink oracle for ETH/USD price data while executing swaps through the Uniswap router. Discrepancies between the Chainlink oracle price and the Uniswap price can arise due to market volatility, differences in data sources, or short-term pool manipulation. This discrepancy can result in:

1. Inefficient rebalancing that diverges from actual pool values.
2. Failed user transactions due to mismatches in expected and actual swap outcomes, requiring frequent adjustments of `swapSlippage`.
3. Vulnerability to price manipulation attacks, especially if Chainlink prices lag behind real-time market conditions.

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:M/A:M/D:N/Y:N/R:P/S:C (3.9)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:M/A:M/D:N/Y:N/R:P/S:C)

##### Recommendation

Consider using Uniswap's prices directly for rebalancing and swaps. Use a Volume-Weighted Average Price (VWAP) over a suitable time frame to mitigate the risk of price manipulation. This approach ensures price alignment with the swap router and provides more accurate and secure operations. Specific actions include:

1. **Integrate Uniswap Price Feeds**:
2. Fetch VWAP data using Uniswap's pool observations or by querying a reliable Uniswap price oracle.
3. Use this price as the basis for calculations in `rebalancePool` and `swapUsdcToEthExactOutput`.
4. **Implement Manipulation Safeguards**:
5. Use time-weighted average prices rather than spot prices to reduce susceptibility to flash loan or sandwich attacks.
6. **Adapt Slippage Management**:
7. Ensure `setswapSlippage` does not require frequent adjustments by aligning pricing mechanisms, reducing user transaction failures.

By aligning the pricing source with the swap mechanism (Uniswap), this approach ensures operational consistency, reduces risks of transaction failures, and mitigates pool manipulation threats.

##### Remediation

**RISK ACCEPTED:** The **Dexodus team** accepted the risk of this finding.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | WeightedLiquidityPool |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/dexodus/weightedliquiditypool
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/dexodus/weightedliquiditypool

### Keywords for Search

`vulnerability`

