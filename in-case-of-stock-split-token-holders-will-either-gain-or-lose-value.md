---
# Core Classification
protocol: DittoETH
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27447
audit_firm: Codehawks
contest_link: https://www.codehawks.com/contests/clm871gl00001mp081mzjdlwc
source_link: none
github_link: https://github.com/Cyfrin/2023-09-ditto

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

protocol_categories:
  - liquid_staking

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - ptsanev
---

## Vulnerability Title

In case of stock split, token holders will either gain or lose value

### Overview

See description below for full details.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-09-ditto/blob/22b189fffa00101a94b3c717bdd84e87f1f259c5/contracts/tokens/Asset.sol#L1-L31">https://github.com/Cyfrin/2023-09-ditto/blob/22b189fffa00101a94b3c717bdd84e87f1f259c5/contracts/tokens/Asset.sol#L1-L31</a>


## Summary
The protocol intends to virtualize assets outside of just tokens and pegged stablecoins, such as real estate and stocks.
Stock split and reverse split may cause the token accounting to be inaccurate.

## Vulnerability Details
Stock split and reverse split are very common in the stock market. There are many examples.
For instance, in a 2-for-1 stock split, a shareholder receives an additional share for each share held.
In the event of a stock split, the asset token representing the given stock will have wrong accounting when minting, since the split will remain unaccounted for.

## Impact
Token value can be lost or gained unfairly.

## Tools Used
Manual Review

## Recommendations
Due to the nature of the issue and the unpredictability of the way the protocol might choose to handle complex assets like stocks, there is no 1 mitigation for this issue. There could be some kind of custom oracle to watch out for such stock events and rebase the virtual values accordingly.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | DittoETH |
| Report Date | N/A |
| Finders | ptsanev |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-09-ditto
- **Contest**: https://www.codehawks.com/contests/clm871gl00001mp081mzjdlwc

### Keywords for Search

`vulnerability`

