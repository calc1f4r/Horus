---
# Core Classification
protocol: XPress
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 56821
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/XPress/Liquidity%20Vault/README.md#5-missing-price-factor-in-claimed-shares-calculation
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

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

Missing Price Factor in Claimed Shares Calculation

### Overview


This report discusses a bug in the `_claimOrder` function of the `ProxyLOB` contract. When a certain condition is met, the code does not correctly calculate the value of claimed shares, resulting in a higher-than-accurate reserves value. This bug is considered critical because it affects the reported balances of the protocol. To fix this, the suggested solution is to use a different calculation method.

### Original Finding Content

##### Description
This issue has been identified within the `_claimOrder` function of the `ProxyLOB` contract. 

When `isAsk = false`, the current code subtracts `(totalClaimedShares + passiveFee) * scalingFactorTokenY` from the reserves without multiplying `totalClaimedShares` by `price`. Consequently, the actual value of the claimed shares is not correctly accounted for, resulting in a higher-than-accurate reserves value.

The issue is classified as **critical** severity because it leads to a miscalculation of the claimed token’s worth, which inflates the protocol’s reported balances.

##### Recommendation
We recommend using `(totalClaimedShares * price + passiveFee) * scalingFactorTokenY` for the subtraction. This ensures the claimed amount is converted into its proper value before being removed from the reserves.


***

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | XPress |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/XPress/Liquidity%20Vault/README.md#5-missing-price-factor-in-claimed-shares-calculation
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

