---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41210
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Lido%20Oracle/README.md#1-potential-revert-when-available_eth-0
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

Potential Revert When `available_eth == 0`

### Overview

See description below for full details.

### Original Finding Content

##### Description
The issue is identified in the `_calculate_finalization_batches` method of the `Withdrawal` service. If `available_eth == 0`, the call to `calculate_finalization_batches` will revert due to internal checks. This can cause the entire function to fail, even though it could handle the zero available ETH case more gracefully.

The issue is classified as **Low** severity because it occurs in a specific edge case, where no ETH is available for finalization. However, addressing this would improve the robustness of the service, especially in low-ETH conditions.

##### Recommendation
We recommend adding a check for `available_eth == 0` before calling the `calculate_finalization_batches` function. If `available_eth` is zero, the function should return an empty list or handle this scenario in a way that prevents reverts.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Lido%20Oracle/README.md#1-potential-revert-when-available_eth-0
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

