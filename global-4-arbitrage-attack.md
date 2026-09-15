---
# Core Classification
protocol: GMX
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27191
audit_firm: Guardian Audits
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Guardian Audits/2022-10-24-GMX.md
github_link: none

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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Guardian Audits
---

## Vulnerability Title

GLOBAL-4 | Arbitrage Attack

### Overview


This bug report is about the potential for economically viable price manipulation/arbitrage attacks in the spot prices from multiple exchanges. Documentation in README.md suggests that spot prices from multiple exchanges will be used to determine prices for execution, which can be exploited by attackers. To prevent this, the team suggested adopting a TWAP with multiple price readings to make such attacks economically unviable, or using failsafes such as open interest caps. Optionally, order book depth/liquidity for each exchange should be considered in the calculation to further limit the scope of manipulation attacks. The GMX team acknowledged the report.

### Original Finding Content

**Description**

Documentation in README.md suggests that spot prices from multiple exchanges will be used to determine prices for execution. Such a price collection scheme potentially allows for economically viable price manipulation/arbitrage attacks. Attackers may be able to manipulate prices to game orders into guaranteed profits, or cause mass liquidations.

**Recommendation**

Adopt a TWAP with multiple price readings to make such attacks economically unviable. Otherwise, be prepared to use failsafes such as open interest caps to limit these attacks. 
Optionally, order book depth/liquidity for each exchange should be considered in the calculation to further limit the scope of manipulation attacks.

**Resolution**

GMX Team: Acknowledged

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Guardian Audits |
| Protocol | GMX |
| Report Date | N/A |
| Finders | Guardian Audits |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Guardian Audits/2022-10-24-GMX.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

