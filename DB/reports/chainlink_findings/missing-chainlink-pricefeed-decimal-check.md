---
# Core Classification
protocol: Swaap Finance Safeguard Pool
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60518
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/swaap-finance-safeguard-pool/d304d4d7-05aa-42bd-92ba-7fd7f5e701ac/index.html
source_link: https://certificate.quantstamp.com/full/swaap-finance-safeguard-pool/d304d4d7-05aa-42bd-92ba-7fd7f5e701ac/index.html
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
finders_count: 4
finders:
  - Danny Aksenov
  - Julio Aguliar
  - Rabib Islam
  - Ruben Koch
---

## Vulnerability Title

Missing Chainlink Pricefeed Decimal Check

### Overview

See description below for full details.

### Original Finding Content

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation:

> We chose to keep it as it is because it adds significant gas cost for an event that is unlikely to happen

**File(s) affected:**`ChainlinkUtils.sol`

**Description:** Currently, the scaling factors for the two assets of the oracle prices are calculated once based on the return value of `oracle.decimals()` in the constructor of the `SafeguardPool`, however, technically, the decimals could be subject to change. Therefore, it is a good best practice to check that the decimals meet the expectations when fetching prices from a Chainlink oracle.

**Recommendation:** Make `oracleDecimals` a global variable. In `getLatestPrice()`, check `oracle.decimals() == oracleDecimals`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Swaap Finance Safeguard Pool |
| Report Date | N/A |
| Finders | Danny Aksenov, Julio Aguliar, Rabib Islam, Ruben Koch |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/swaap-finance-safeguard-pool/d304d4d7-05aa-42bd-92ba-7fd7f5e701ac/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/swaap-finance-safeguard-pool/d304d4d7-05aa-42bd-92ba-7fd7f5e701ac/index.html

### Keywords for Search

`vulnerability`

