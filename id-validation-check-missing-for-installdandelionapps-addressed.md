---
# Core Classification
protocol: Dandelion Organizations
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13889
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2019/12/dandelion-organizations/
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

protocol_categories:
  - dexes
  - cdp
  - services
  - launchpad
  - rwa

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Alexander Wade

---

## Vulnerability Title

ID validation check missing for installDandelionApps ✓ Addressed

### Overview

See description below for full details.

### Original Finding Content

#### Resolution



This was addressed in [commit 8d1ecb1bc892d6ea1d34c7234e35de031db2bebd](https://github.com/1Hive/dandelion-org/pull/31/commits/8d1ecb1bc892d6ea1d34c7234e35de031db2bebd) by removing the `_id` parameter from `newTokenAndBaseInstance` and `newBaseInstance`, and adding a validation check to `installDandelionApps`.


#### Description


`DandelionOrg` allows users to kickstart an Aragon organization by using a dao template. There are two primary functions to instantiate an org: `newTokenAndBaseInstance`, and `installDandelionApps`. Both functions accept a parameter, `string _id`, meant to represent an ENS subdomain that will be assigned to the new org during the instantiation process. The two functions are called independently, but depend on each other.


In `newTokenAndBaseInstance`, a sanity check is performed on the `_id` parameter, which ensures the `_id` length is nonzero:


**code/dandelion-org/contracts/DandelionOrg.sol:L155**



```
\_validateId(\_id);

```
Note that the value of `_id` is otherwise unused in `newTokenAndBaseInstance`.


In `installDandelionApps`, this check is missing. The check is only important in this function, since it is in `installDandelionApps` that the ENS subdomain registration is actually performed.


#### Recommendation


Use `_validateId` in `installDandelionApps` rather than `newTokenAndBaseInstance`. Since the `_id` parameter is otherwise unused in `newTokenAndBaseInstance`, it can be removed.


Alternatively, the value of the submitted `_id` could be cached between calls and validated in `newTokenAndBaseInstance`, similarly to `newToken`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Dandelion Organizations |
| Report Date | N/A |
| Finders | Alexander Wade
 |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2019/12/dandelion-organizations/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

