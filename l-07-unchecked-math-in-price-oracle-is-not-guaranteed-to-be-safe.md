---
# Core Classification
protocol: Fungify
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31830
audit_firm: ZachObront
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-11-01-fungify.md
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
  - Zach Obront
---

## Vulnerability Title

[L-07] Unchecked math in price oracle is not guaranteed to be safe

### Overview

See description below for full details.

### Original Finding Content

In the Chainlink Price Oracle, we expect the price of the asset to be returned in 8 decimals. We then perform the following calculation to transfer it into `36 - asset decimals` decimals:
```solidity
unchecked { price = uint(rate) * 10**(28 - decimals[asset]); }
```
While this multiplication is likely to be safe in most practical cases, it is not guaranteed to be safe.

- `rate` is returned as an `int256`, which could be as high as `type(int256).max = 57896044618658097711785492504343953926634992332820282019728792003956564819967`
- this value is equal to the max `uint256` / 2, which will overflow when any decimal adjustment is applied to it

Practically, we can calculate the maximum safe value for `rate` as:
- `type(uint256).max / 10**28 = 11579208923731619542357098500868790785326998466564`
- any value greater than this can overflow when multiplying by decimals
- since `rate` is always returned in 8 decimals, this represents a value of approximately `11579208923731619542357098500868790785326998466564 / 10**8 = 115792089237316195423570985008687907853269 ~= 10**41`

In this situation, the price will overflow and result in the token being undervalued by the oracle.

**Recommendation**

While it is unlikely that a token will return a value this high, it would be safer to remove the unchecked block to be sure.

**Review**

Fixed as recommended in [7e0ee60622ddcbf384657da480ef9c851f2adc11](https://github.com/fungify-dao/taki-contracts/pull/9/commits/7e0ee60622ddcbf384657da480ef9c851f2adc11).

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ZachObront |
| Protocol | Fungify |
| Report Date | N/A |
| Finders | Zach Obront |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-11-01-fungify.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

