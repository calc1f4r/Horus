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
solodit_id: 49214
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Ozean%20Finance/README.md#2-usdc-depeg-risk-in-usdx-bridge
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
  - MixBytes
---

## Vulnerability Title

USDC Depeg Risk in USDX Bridge

### Overview


This bug report discusses an issue with the `bridge` function in the `USDXBridge` contract. This issue involves a risk of instant arbitrage when the value of USDC or other assets changes. This could cause the value of USDX to decrease and affect its stability. The recommendation is to add a `pause` function to the bridge, which would allow the operation to be temporarily stopped and mitigate the risk of arbitrage and market depreciation.

### Original Finding Content

##### Description
The following issue has been identified within the `bridge` function of the `USDXBridge` contract. Specifically, this involves a potential instant arbitrage risk in cases where USDC or other assets lose their peg. In such cases, the market price of USDX may depreciate because the bridge will provide an instantaneous arbitrage opportunity. This represents a risk that can impact the overall stability of the USDX token.

##### Recommendation
We recommend implementing a `pause` function capability in the bridge functionality, allowing the operation to be temporarily halted. This could assist in risk mitigation by providing control over potential arbitrage exploitation and reducing potential market depreciation impacts.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Ozean Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Ozean%20Finance/README.md#2-usdc-depeg-risk-in-usdx-bridge
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

