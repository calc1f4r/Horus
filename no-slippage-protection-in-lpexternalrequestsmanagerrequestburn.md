---
# Core Classification
protocol: Resolv
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43603
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Resolv/Treasury/README.md#1-no-slippage-protection-in-lpexternalrequestsmanagerrequestburn
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

No slippage protection in `LPExternalRequestsManager.requestBurn()`

### Overview


The bug report discusses an issue with the `requestBurn()` function in the LPExternalRequestsManager contract. This function allows users to burn RLP tokens, but there is no protection against slippage for providers. This means that when the `completeBurns()` function is called, the amount of tokens transferred is not based on any on-chain oracle and may result in providers receiving fewer tokens than expected. The recommendation is to add `minAmountOut` and `deadline` parameters to the workflow to address this issue.

### Original Finding Content

##### Description

* https://github.com/resolv-im/resolv-contracts/blob/2e24f0e76525a663e222530a88bdd968e5e818eb/contracts/LPExternalRequestsManager.sol#L215-L218

`LPExternalRequestsManager.requestBurn()` allows users to burn RLP tokens, but providers do not have any slippage protection &mdash; the amounts of tokens to transfer in `LPExternalRequestsManager.completeBurns()` are not related to any on-chain oracle and are susceptible to slippage: request providers may receive fewer tokens than they expected.

##### Recommendation
We recommend adding the `minAmountOut` and `deadline` parameters to the workflow.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Resolv |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Resolv/Treasury/README.md#1-no-slippage-protection-in-lpexternalrequestsmanagerrequestburn
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

