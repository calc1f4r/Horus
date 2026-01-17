---
# Core Classification
protocol: HUB v1
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51890
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/concrete/hub-v1
source_link: https://www.halborn.com/audits/concrete/hub-v1
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
  - Halborn
---

## Vulnerability Title

Missing Validation for Consistent chainId and eid

### Overview

See description below for full details.

### Original Finding Content

##### Description

In the `RegistryManager` contract, the function `addEndpointIdToChainId` is not enforcing validation to check if `chainId_` and `eid_` (Endpoint ID) are equal, which is implied as a requirement by other contract logic. This can cause issues, especially in the context of the function `_getRemoteChainEid` in `RemoteChainHandler`. If a mismatch or incorrect mapping occurs, it could lead to returning invalid or duplicate addresses for different chain IDs through the `_getRemoteChainEidAddress` function.

Specifically, if the same `eid_` is assigned to multiple chain IDs or if the `REMOTE_ENDPOINT_TO_ADDRESS` mapping isn't properly verified before setting values, the protocol could retrieve wrong data, potentially affecting the functionality across different chains.

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:H/A:N/D:N/Y:N/R:F/S:C (2.3)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:H/A:N/D:N/Y:N/R:F/S:C)

##### Recommendation

To prevent invalid mappings and ensure that each chain ID corresponds to its own endpoint ID, you should:

* Add a check in `addEndpointIdToChainId` to ensure that `chainId_` and `eid_` are equal, or at least enforce a validation logic that guarantees no duplicate endpoint IDs are assigned to multiple chains.
* Before setting or updating the endpoint or chain mappings, ensure that `REMOTE_ENDPOINT_TO_ADDRESS` or `REMOTE_CHAIN_TO_REGISTRY` are properly validated to avoid un-synced or duplicate mappings.

##### Remediation

**RISK ACCEPTED**: The **Concrete team** accepted the risk of this finding. Names that could cause confusion were changed. There is a 1-to-n relationship between chainId and eid. Usually, there will be only one eid per chainId, but the distinction is made in case we want to have more than one deployment per chain. So we will only have one active eid per chain.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | HUB v1 |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/concrete/hub-v1
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/concrete/hub-v1

### Keywords for Search

`vulnerability`

