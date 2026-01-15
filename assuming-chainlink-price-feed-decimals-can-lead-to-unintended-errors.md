---
# Core Classification
protocol: Evo Soulboundtoken
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 56886
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-02-cyfrin-evo-soulboundtoken-v2.0.md
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
  - Dacian
  - Giovanni Di Siena
---

## Vulnerability Title

Assuming Chainlink price feed decimals can lead to unintended errors

### Overview

See description below for full details.

### Original Finding Content

**Description:** In general, Chainlink x/USD price feeds use 8 decimal precision however this is not universally true for example [AMPL/USD](https://etherscan.io/address/0xe20CA8D7546932360e37E9D72c1a47334af57706#readContract#F3) uses 18 decimal precision.

Instead of [assuming Chainlink oracle price precision](https://medium.com/contractlevel/chainlink-oracle-defi-attacks-93b6cb6541bf#87fc), the precision variable could be declared `immutable` and initialized in the constructor via [`AggregatorV3Interface::decimals`](https://docs.chain.link/data-feeds/api-reference#decimals).

In practice though the price oracle is hard-coded in `script/HelperConfig.s.sol` and does use 8 decimals for on Optimism, so the current configuration will work fine.

**Evo:**
Fixed in commit [f594ae0](https://github.com/contractlevel/sbt/commit/f594ae004d4afc80f19e17c0f61d50caa00a4811).

**Cyfrin:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Evo Soulboundtoken |
| Report Date | N/A |
| Finders | Dacian, Giovanni Di Siena |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-02-cyfrin-evo-soulboundtoken-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

