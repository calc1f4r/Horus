---
# Core Classification
protocol: Iron Bank
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28099
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Iron%20Bank/README.md#3-interest-rate-model-update-impacts-the-old-time-period
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

Interest rate model update impacts the old time period

### Overview


This bug report is about a problem with the compound-protocol's TripleSlopeRateModel.sol function. When an admin changes the interest rate model parameters, the indexes are incorrectly recalculated in the upcoming accrueInterest() function call. This means that the new interest settings are applied to the previous period of time, which is not correct.

The recommended solution is to create a special service contract which will change the interest rate model parameters just after the accrueInterest() function is called for each asset. This will ensure that the correct interest settings are applied to the appropriate period of time.

### Original Finding Content

##### Description
After an admin changes the interest rate model parameters by using this function
https://github.com/ibdotxyz/compound-protocol/blob/8cd45803b48552e344e22be280c9e1c03ec8644a/contracts/TripleSlopeRateModel.sol#L100
indexes will be recalculated in the upcoming accrueInterest() function call. But this call applies new interest settings to the previous period of time which is not correct.
##### Recommendation
The interest rate model parameters should be changed just after calling the accrueInterest() function for each asset. It can be done by creating a special service contract.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Iron Bank |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Iron%20Bank/README.md#3-interest-rate-model-update-impacts-the-old-time-period
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

