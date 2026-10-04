---
# Core Classification
protocol: Canto
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25379
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-09-canto
source_link: https://code4rena.com/reports/2022-09-canto
github_link: https://github.com/code-423n4/2022-09-canto-findings/issues/73

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - yield
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[H-01] Hardcoded USD pegs can be broken

### Overview


A bug report has been filed concerning the hardcoding of prices for USDC and USDT, which are the underlying tokens of cUSDC and cUSDT. This practice is discouraged due to the risk of either stablecoin de-pegging, which can cause major losses for lending protocols. An example of this is the UST debacle, where the price of USDT dropped to $0.95 before recovering.

Furthermore, the philosopher George Santayana's quote “Those who cannot remember the past are condemned to repeat it” is applicable to this situation. Therefore, it is important to take the necessary steps to mitigate this risk.

The recommended mitigation steps include the use of trusted and established oracle providers such as Chainlink, Band Protocol, or Flux. The USDC/NOTE or USDT/NOTE price feed may be used, but NOTE has its own volatility concerns.

### Original Finding Content


The prices of USDC and USDT, which (I assume) are the underlying tokens of `cUSDC` and `cUSDT`, have been hardcoded to parity. Such practices are highly discouraged because while the likelihood of either stablecoin de-pegging is low, it is not zero.

Because of the UST debacle, the [price of USDT dropped to `$0.95`](https://www.cnbc.com/2022/05/12/tether-usdt-stablecoin-drops-below-1-peg.html) before making a recovery.

### Impact

Here is an example of how [a lending protocol on Fantom was affected by such a depeg event because they hardcoded the value](\[https://cryptoslate.com/scream-protocol-losses-millions-to-stablecoin-depeg/]\(https://cryptoslate.com/scream-protocol-losses-millions-to-stablecoin-depeg/\)).

To quote philosopher George Santayana, *“Those who cannot remember the past are condemned to repeat it.”*

### Recommended Mitigation Steps

Consider using a price feed by trusted and established oracle providers like Chainlink, Band Protocol or Flux. The USDC/NOTE or USDT/NOTE price feed may be used as well, but NOTE has its own volatility concerns.


***

 


### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Canto |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-09-canto
- **GitHub**: https://github.com/code-423n4/2022-09-canto-findings/issues/73
- **Contest**: https://code4rena.com/reports/2022-09-canto

### Keywords for Search

`vulnerability`

