---
# Core Classification
protocol: P2P.org
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52745
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/P2P.org/Staking%20Lending%20Proxy/README.md#3-missing-zero-address-checks-in-constructors
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
  - MixBytes
---

## Vulnerability Title

Missing Zero-Address Checks in Constructors

### Overview

See description below for full details.

### Original Finding Content

##### Description
This issue has been identified within constructors of `P2pEthenaProxyFactory` and `P2pEthenaProxy` contracts. 

There are no explicit checks for zero addresses for critical parameters (`_p2pTreasury`, `_stakedUSDeV2`, `_USDe`, `_factory`), potentially leading to non-functional contract deployments.

##### Recommendation
We recommend explicitly adding checks for zero addresses.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | P2P.org |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/P2P.org/Staking%20Lending%20Proxy/README.md#3-missing-zero-address-checks-in-constructors
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

