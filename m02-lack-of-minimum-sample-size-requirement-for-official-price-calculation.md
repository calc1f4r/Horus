---
# Core Classification
protocol: Compound Open Oracle Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11555
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/compound-open-oracle-audit/
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

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[M02] Lack of minimum sample size requirement for official price calculation

### Overview


Compound's Open Oracle is responsible for calculating the official price of an asset. It takes price data from trusted sources, calculates a median price using the DelFiPrice contract's medianPrice function, and supplies the median price as the asset's official price. However, this process does not consider the sample size of the prices when calculating the median price, leaving the oracle vulnerable to a price manipulation attack when the sample size is low. To reduce this risk, Compound should consider implementing a minimum sample size requirement or returning the sample size together with the oracle's official price, to make users aware of the potential risks when the sample size is too low.

### Original Finding Content

To obtain the official price for an asset, Compound’s Open Oracle takes all reported price data from trusted sources, calculates a median price using the [`medianPrice` function](https://github.com/compound-finance/open-oracle/blob/e7a928334e5e454a88eec38e4ee1be5ee3b13f08/contracts/DelFiPrice.sol#L86) of the `DelFiPrice` contract, and finally supplies this median price as the asset’s price.


However, this process does not take into account the sample size of the prices when calculating the median price of an asset, which may render the oracle vunerable to a price manipulation attack when the sample size is low (see **[N09] Considerations on rogue sources** note for a more detailed description).


Consider either implementing a minimum sample size requirement or returning the sample size together with the oracle’s official price, so as to raise awareness on the potential risks when the sample size is dangerously low.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Compound Open Oracle Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/compound-open-oracle-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

