---
# Core Classification
protocol: Benqi Ignite
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44271
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md
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
finders_count: 2
finders:
  - Immeas
  - Giovanni Di Siena
---

## Vulnerability Title

Incorrect assumption that Chainlink price feeds will always have the same decimals

### Overview

See description below for full details.

### Original Finding Content

**Description:** There are several instances [[1](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L227), [2](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L299), [3](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L381)] in `Ignite` where the decimal precision of Chainlink price feeds are assumed to be equal. Currently, this does not cause any issues as both `AVAX`, `QI`, and all other `USD` feeds return prices with `8` decimal precision, but this should be handled explicitly as `ETH` feeds return prices with `18` decimal precision as explained [here](https://ethereum.stackexchange.com/questions/92508/do-all-chainlink-feeds-return-prices-with-8-decimals-of-precision).

**Recommended Mitigation:** Consider explicit handling of Chainlink price feed decimals.

**BENQI:** Acknowledged, USD feeds always have eight decimals.

**Cyfrin:** Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Benqi Ignite |
| Report Date | N/A |
| Finders | Immeas, Giovanni Di Siena |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

