---
# Core Classification
protocol: Vaultka
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37036
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-11-09-Vaultka.md
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
finders_count: 1
finders:
  - Zokyo
---

## Vulnerability Title

Chainlink’s latestRoundData May Return Stale Or Incorrect Result

### Overview


This bug report is about a problem with Chainlink's latestRoundData feature, which is used to retrieve price data. The report states that there is not enough protection against outdated prices, which can lead to inaccurate data and potentially lost funds. The recommended solution is to add checks to ensure that the prices returned are correct.

### Original Finding Content

**Severity** - Medium

**Status** - Acknowledged

**Description**

Chainlink's latestRoundData is used inside getLatestData at L373 to retrieve price feed data, however there is insufficient protection against price staleness.
Return arguments are necessary to determine the validity of the returned price, as it is possible for an outdated price to be received. See here for reasons why a price feed might stop updating.
The return value updatedAt contains the timestamp at which the received price was last updated, and can be used to ensure that the price is not outdated. See more information about latestRoundID in the Chainlink docs. Inaccurate price data can lead to functions not working as expected and/or lost funds.


**Recommendation**:

Introduce sufficient checks to ensure correct prices returned.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Vaultka |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-11-09-Vaultka.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

