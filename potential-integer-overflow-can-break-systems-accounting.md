---
# Core Classification
protocol: Volatility Technologies Ltd
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61653
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/volatility-technologies-ltd/e23eb3db-8b11-4dcf-840f-dd4d3a56c6e3/index.html
source_link: https://certificate.quantstamp.com/full/volatility-technologies-ltd/e23eb3db-8b11-4dcf-840f-dd4d3a56c6e3/index.html
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
  - Julio Aguilar
  - Mustafa Hasan
  - Jeffrey Kam
---

## Vulnerability Title

Potential Integer Overflow Can Break System's Accounting

### Overview

See description below for full details.

### Original Finding Content

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation:

> The protocol makes assumptions regarding which tokens can be used as collateral, and what level of precision will be provided by the price feed. Under these assumptions, overflow is not possible. In particular, we will only use stablecoins where the decimals and theoretical supply bounds ensure that overflow cannot occur. The price feed will be configured per asset to ensure that enough precision is given, but that size of the price values cannot lead to overflow. These assumptions and constraints will be made clear in the public documentation.

**File(s) affected:**`PriceFeed.sol`, `MultiLot.sol`

**Description:** There are various locations where integer overflow can occur in the codebase, which can lead to inaccurate rewards accounting and unintentional reverts. In particular, we have the following snippet from `_resolveLot()`:

```
if (startPriceTokenA == 0 || d2 > d1) {
    lot.totalClaimPoolB = (2 * (size - feeAmountPerSide)).toUint128();
    winningToken = lot.tokenB;
}
// If token B is invalid or if token A had a greater increase in price...
else if (startPriceTokenB == 0 || d1 > d2) {
    lot.totalClaimPoolA = (2 * (size - feeAmountPerSide)).toUint128();
    winningToken = lot.tokenA;
}
// Otherwise, in the case of a tie...
else {
    uint128 claim = (size - feeAmountPerSide).toUint128();
    lot.totalClaimPoolA = claim;
    lot.totalClaimPoolB = claim;
}
```

It is possible for `(2 * (size - feeAmountPerSide))` to be greater than `2^128`. In which case, casting it back to the `uint128` will lead to an inaccurate accounting of how much the users can claim. This happens when `size` is on the order of `2^128`. However, this is unlikely to happen because `size` equals how many collateral tokens are in the lot, and per discussion with the team, these tokens will likely be stablecoins.

Furthermore, it is also possible for the following snippet in `_resolveLot()` to revert:

```
if (!priceFeed.isInvalid(lot.tokenA)) {
    startPriceTokenA = priceFeed.getHistoricalPrice(lot.tokenA, lot.startTimestamp);
    resolvePriceTokenA = priceFeed.getHistoricalPrice(lot.tokenA, endTimestamp);
}
if (!priceFeed.isInvalid(lot.tokenB)) {
    startPriceTokenB = priceFeed.getHistoricalPrice(lot.tokenB, lot.startTimestamp);
    resolvePriceTokenB = priceFeed.getHistoricalPrice(lot.tokenB, endTimestamp);
}
uint256 d1 = resolvePriceTokenA * startPriceTokenB; 
uint256 d2 = resolvePriceTokenB * startPriceTokenA;
```

Since `priceFeed.getHistoricalPrice()` returns a type of `uint256`, it is possible to overflow in the calculation of `d1` and `d2`, causing unintentional reverts. The likelihood of this happening depends on the results of the price feed and how the Relative Finance team chooses to represent the price in the price feed backend.

**Recommendation:** While unlikely to occur, we would still recommend the team clearly state these assumptions in the documentation so end-users are aware of these system constraints.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Volatility Technologies Ltd |
| Report Date | N/A |
| Finders | Julio Aguilar, Mustafa Hasan, Jeffrey Kam |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/volatility-technologies-ltd/e23eb3db-8b11-4dcf-840f-dd4d3a56c6e3/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/volatility-technologies-ltd/e23eb3db-8b11-4dcf-840f-dd4d3a56c6e3/index.html

### Keywords for Search

`vulnerability`

