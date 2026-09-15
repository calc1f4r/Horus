---
# Core Classification
protocol: Radiant Riz Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35192
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/radiant-riz-audit
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
  - OpenZeppelin
---

## Vulnerability Title

OracleRouter Not Utilizing Pyth Confidence Interval

### Overview

See description below for full details.

### Original Finding Content

The OracleRouter [reads data from Pyth](https://github.com/radiant-capital/riz/blob/65ca7bb55550d30388e2b2277fefe5686ab7e4e8/src/OracleRouter.sol#L166) without incorporating the [confidence interval](https://github.com/radiant-capital/riz/blob/65ca7bb55550d30388e2b2277fefe5686ab7e4e8/src/interfaces/PythStructs.sol#L16-L17) returned by Pyth.


In some cases, this confidence interval may be useful, to set bounds on the value of assets in the system for purposes of collateralization or liquidation, or when markets are subject to high fluctuation of prices.


Consider utilizing the Pyth returned confidence interval, or alternatively explaining why it is not needed within the documentation.


***Update:** Acknowledged, not resolved. The Radiant team stated:*



> *Chainlink has no such functionality and we treat each oracle provider equally (i.e., the oracle can provide the latest prices). Also, we have doubts if we need to utilize this function in the `OracleRouter`.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Radiant Riz Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/radiant-riz-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

