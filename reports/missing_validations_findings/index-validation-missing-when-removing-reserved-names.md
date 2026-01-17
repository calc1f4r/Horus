---
# Core Classification
protocol: Name Service (BNS) Contracts v2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52530
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/beranames/name-service-bns-contracts-v2
source_link: https://www.halborn.com/audits/beranames/name-service-bns-contracts-v2
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

Index validation missing when removing reserved names

### Overview

See description below for full details.

### Original Finding Content

##### Description

The `removeReservedName` function in the **ReservedRegistry** contract does not validate whether the provided index is within the valid range (e.g.: less than `_reservedNamesCount`). If an invalid index is supplied, the function will revert, as the access to an out-of-bounds index will trigger a failure in the operation. However, without explicit index validation, the function may not provide a clear error message to the caller, and the revert behavior might lead to a poor user experience.

  

Code Location
-------------

The `removeReservedName` function does not validate whether the provided index is within the valid range:

```
function removeReservedName(uint256 index_) public onlyOwner {
  bytes32 labelHash_ = _reservedNamesList[index_];
  delete _reservedNames[labelHash_];
  _reservedNamesList[index_] = _reservedNamesList[_reservedNamesCount - 1];
  _reservedNamesCount--;
}
```

##### BVSS

[AO:A/AC:L/AX:L/R:N/S:U/C:N/A:N/I:N/D:N/Y:N (0.0)](/bvss?q=AO:A/AC:L/AX:L/R:N/S:U/C:N/A:N/I:N/D:N/Y:N)

##### Recommendation

It is recommended to explicitly validate the index to ensure that it is within the valid range before performing the removal operation. This will provide a clear error message and improve the clarity of contract interactions.

##### Remediation

**SOLVED:** The **Beranames team** solved the issue in the specified commit id.

##### Remediation Hash

<https://github.com/Beranames/beranames-contracts-v2/pull/94/commits/36ffb4f701bc7b2dc313bcc646c901a2aec95e57>

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Name Service (BNS) Contracts v2 |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/beranames/name-service-bns-contracts-v2
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/beranames/name-service-bns-contracts-v2

### Keywords for Search

`vulnerability`

