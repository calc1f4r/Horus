---
# Core Classification
protocol: Velodrome
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63621
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Velodrome/Pool%20Launcher/README.md#2-missing-pool-validation-lets-anyone-create-lockers-for-arbitrary-tokens
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

Missing Pool Validation Lets Anyone Create Lockers for Arbitrary Tokens

### Overview

See description below for full details.

### Original Finding Content

##### Description
`V2LockerFactory.lock()` accepts a raw `address _pool` parameter and never verifies that the address is an authentic Velodrome V2 pool produced by the authorised `v2Factory`. A user can therefore pass any ERC-20 contract (or even a non-ERC-20 contract) as `_pool` together with an arbitrary `_lp` amount. 

Although no vulnerabilities have been detected, validating user supplied addresses remains best practice and reduces the chance of hidden issues surfacing later.

##### Recommendation
We recommend validating that `_pool` is registered in the `v2Factory` during locker creation in `V2LockerFactory.lock()` function.

> **Client's Commentary**  
> Fixed in https://github.com/velodrome-finance/pool-launcher/commit/e151d0101573d8c7c56ccc9e03bb5277ab62a9b0

---


### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Velodrome |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Velodrome/Pool%20Launcher/README.md#2-missing-pool-validation-lets-anyone-create-lockers-for-arbitrary-tokens
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

