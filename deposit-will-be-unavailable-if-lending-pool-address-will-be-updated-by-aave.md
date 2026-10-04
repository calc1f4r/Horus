---
# Core Classification
protocol: Yearn Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28492
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Yearn%20Finance/Generic%20Lender%20Aave/README.md#1-deposit-will-be-unavailable-if-lending-pool-address-will-be-updated-by-aave
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

Deposit will be unavailable if lending pool address will be updated by AAVE

### Overview


A bug has been identified in the Grandthrax/yearnV2-generic-lender-strat repository. The `deposit` function at line 132 assumes recent approval of token transfer, but the `safeApprove()` is only called once during contract initialization at line 49. This means that if the lending pool address is changed by AAVE, the `deposit()` will not be available until the contract is replaced.

The recommendation is to call `safeApprove()` on demand before calling `deposit()` on the lending pool. This will ensure that the `deposit()` function is available regardless of any changes to the lending pool address.

### Original Finding Content

##### Description
At line https://github.com/Grandthrax/yearnV2-generic-lender-strat/blob/55b4d3b03845b7b71b24b50baa30823b3e42ebcf/contracts/GenericLender/GenericAave.sol#L132 the `deposit` function assumes recent approval of token transfer. However, the  `safeApprove()` is called once during contract initialization(https://github.com/Grandthrax/yearnV2-generic-lender-strat/blob/55b4d3b03845b7b71b24b50baa30823b3e42ebcf/contracts/GenericLender/GenericAave.sol#L49) and possible changes of lending pool address is not tracked properly. If lending pool address is updated by AAVE, the `deposit()` will be unavailable/reverted until contract replacement.

##### Recommendation
Call `safeApprove()` on demand before calling `deposit()` on lending pool.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Yearn Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Yearn%20Finance/Generic%20Lender%20Aave/README.md#1-deposit-will-be-unavailable-if-lending-pool-address-will-be-updated-by-aave
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

