---
# Core Classification
protocol: AgoraStableSwap_2025-06-05
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63864
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/AgoraStableSwap-security-review_2025-06-05.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[L-14] Using fixed pair prices allows arbitrage

### Overview

See description below for full details.

### Original Finding Content


Pair prices are fixed and adjusted with linear interest in the case of interest-bearing assets. As AUSD is meant to be pegged to USD, the price of the pair might not necessarily represent the actual value of the asset. While stablecoins tend to be valued at 1 USD, market fluctuations can lead to temporary deviations from this value. Additionally, interest-bearing assets such as USTB and USYC might have discrete price changes ([e.g. once per day](https://usyc.docs.hashnote.com/overview/token-price#price-reporting)), while their price in the pair is adjusted linearly. Also, the protocol might not be able to reflect the changes in the interest rate of the asset in real time, as they require a manual update of the pair price.

Given that there is no slippage in the swap and there is no limit on the amount of tokens that can be swapped, users can potentially arbitrage the price difference between the pair and the actual market price of the asset, withdrawing all the liquidity of the overvalued asset and leaving the pool with a single token, causing a loss of funds for the protocol and potentially degrading the value of the stablecoin.

As the arbitration strategy is only profitable when the price divergence is greater than the swap fee, increasing the swap fee can mitigate the risk of arbitrage attacks. However, this has some drawbacks as 1) This will only reduce the chance of arbitrage attacks, but not eliminate them, and 2) It will deter users from using the protocol, as they will have to pay a higher fee for the swap.

Recommendations:
Use external price oracles to determine the actual market price of the assets in the pair.





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | AgoraStableSwap_2025-06-05 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/AgoraStableSwap-security-review_2025-06-05.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

