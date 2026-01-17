---
# Core Classification
protocol: Ozean Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49219
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Ozean%20Finance/README.md#4-absence-of-a-usdx-to-stablecoin-exchange-mechanism
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

Absence of a USDX to Stablecoin Exchange Mechanism

### Overview

See description below for full details.

### Original Finding Content

##### Description
In the `USDXBridge` contract, it has been identified that there's no explicit mechanism for users to exchange their `USDX` tokens back to a deposited stablecoin. This constraint poses potential limitations to users, particularly those who do not want to complete the KYC process, which is the currently mandated pathway to perform such an exchange in case of a lack of liquidity of USDX on the market.

This issue is classified as Low severity because while it doesn’t pose a direct security risk, it can potentially impact the user experience and limit the operability of the contract by not providing an accessible pathway for USDX to stablecoin conversion.

##### Recommendation
We recommend adding this information to the documentation that the users might need to complete the KYC process to exchange USDX tokens.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Ozean Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Ozean%20Finance/README.md#4-absence-of-a-usdx-to-stablecoin-exchange-mechanism
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

