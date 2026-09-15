---
# Core Classification
protocol: Salty.IO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29614
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-10-saltyio-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-10-saltyio-securityreview.pdf
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
finders_count: 2
finders:
  - Damilola Edwards
  - Richie Humphrey
---

## Vulnerability Title

Any user can add liquidity to any pool and bypass the token whitelist

### Overview


This report describes a bug in a function called "addLiquidity" that allows anyone to create trading pairs and provide liquidity for any type of token, including malicious ones. This could potentially lead to attacks that could result in the loss of funds for users. Additionally, there is a lack of checks in place to prevent users from blacklisted regions from accessing this function. The report recommends implementing token whitelist and user authorization checks in the short term and reviewing critical operations in the codebase for proper access control in the long term.

### Original Finding Content

## Diﬃculty: Low

## Type: Data Validation

### Description
The absence of token whitelist checks within the `addLiquidity` function allows any user to create trading pairs, including pairs with malicious tokens, and to provide liquidity for arbitrary token pairs. This vulnerability may expose the protocol to potential reentrancy attacks, thereby resulting in the potential loss of funds for users who provide liquidity for the pool. Furthermore, the lack of authorization checks on this function allows users from blacklisted regions to directly call `addLiquidity` on a pool, bypassing the AccessManager access control and associated geolocation check.

```solidity
// Add liquidity for the specified trading pair (must be whitelisted)
function addLiquidity(
    IERC20 tokenA,
    IERC20 tokenB,
    uint256 maxAmountA,
    uint256 maxAmountB,
    uint256 minLiquidityReceived,
    uint256 deadline
) public nonReentrant ensureNotExpired(deadline) returns (uint256 addedAmountA, uint256 addedAmountB, uint256 addedLiquidity) {
    require(
        exchangeConfig.initialDistribution().bootstrapBallot().startExchangeApproved(),
        "The exchange is not yet live"
    );
    require(address(tokenA) != address(tokenB), "Cannot add liquidity for duplicate tokens");
}
```
*Figure 5.1: The addLiquidity function for the Liquidity contract (src/pools/Pools.sol#L149-L177)*

### Exploit Scenario
Alice creates a trading pair using a malicious token. The malicious token pair allows attackers to perform reentrancy attacks and to steal funds from Alice, who provides liquidity in the associated pool.

### Recommendations
- **Short term:** Add the appropriate token whitelist and user authorization checks to the `addLiquidity` function.
- **Long term:** Review critical operations in the codebase and ensure that proper access control mechanisms are put in place.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Salty.IO |
| Report Date | N/A |
| Finders | Damilola Edwards, Richie Humphrey |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2023-10-saltyio-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2023-10-saltyio-securityreview.pdf

### Keywords for Search

`vulnerability`

