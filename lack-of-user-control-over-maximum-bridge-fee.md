---
# Core Classification
protocol: EYWA
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41154
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/EYWA/CLP/README.md#4-lack-of-user-control-over-maximum-bridge-fee
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

protocol_categories:
  - dexes

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Lack of user control over maximum bridge fee

### Overview


The `PortalV2.unlock()` function in the Eywa-CLP project charges users a fee specified in the Whitelist contract. This fee can be increased by the admin up to 100%, which can affect transactions already in progress. Currently, users are not able to set a maximum fee, which can lead to unexpected fees being charged. To address this issue, it is recommended to either allow users to set a maximum fee before sending a transaction, or implement a mechanism to update the fee with a notice period to alert users of any changes. 

### Original Finding Content

##### Description

- https://github.com/eywa-protocol/eywa-clp/blob/d68ba027ff19e927d64de123b2b02f15a43f8214/contracts/PortalV2.sol#L89
- https://github.com/eywa-protocol/eywa-clp/blob/d68ba027ff19e927d64de123b2b02f15a43f8214/contracts/Whitelist.sol#L90

The `PortalV2.unlock()` function charges the user a fee specified in the Whitelist contract, which can be increased by the admin up to 100%, affecting transactions already in progress based on lower fees. Currently, the user cannot set a threshold for the maximum fee, which can lead to situations where a user initiates a bridge transaction expecting a nominal fee, but the admin - without ill intent - increases the fee, resulting in the user receiving less money than anticipated.

##### Recommendation

There are various ways to address this issue. One option is to empower users to set a maximum fee before sending a transaction. Another option is to implement a mechanism to update the bridge fee with a notice period, such as one day, to alert users of the change.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | EYWA |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/EYWA/CLP/README.md#4-lack-of-user-control-over-maximum-bridge-fee
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

