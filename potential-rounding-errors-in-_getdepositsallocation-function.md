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
solodit_id: 41244
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#22-potential-rounding-errors-in-_getdepositsallocation-function
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

Potential Rounding Errors in `_getDepositsAllocation` Function

### Overview

See description below for full details.

### Original Finding Content

##### Description
The issue is identified within the [\_getDepositsAllocation](https://github.com/lidofinance/core/blob/fafa232a7b3522fdee5600c345b5186b4bcb7ada/contracts/0.8.9/StakingRouter.sol#L1424) function of the contract `StakingRouter`. The current implementation could lead to rounding errors when calculating the allocation of deposits among staking modules. Specifically, the sum of capacities minus the sum of allocations may be less than the total deposits to allocate (`_depositsToAllocate`), which could result in some staking modules not receiving their full allocation of validators. This could cause inefficiencies or under-utilization of available validators.

##### Recommendation
We recommend accumulating any remaining "dust" (i.e., small amounts resulting from rounding errors) and assigning it to one of the staking modules. This will ensure that the total number of validators allocated matches the expected amount, maximizing the use of available validators.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#22-potential-rounding-errors-in-_getdepositsallocation-function
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

