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
solodit_id: 52524
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

Bounds validation required for safe array access

### Overview

See description below for full details.

### Original Finding Content

##### Description

The `findResolver(bytes, uint256)` function in the **UniversalResolver** contract lacks comprehensive bounds validation for the `offset` and `labelLength` parameters. These parameters are used to index and slice the `name` array, but there is no explicit check ensuring that both `offset` and `offset + labelLength + 1` remain within the array's bounds. This oversight can lead to out-of-bounds memory access, causing the function to revert unexpectedly when handling crafted or invalid inputs.

  

Code Location
-------------

The `findResolver` function lacks comprehensive bounds validation for the `offset` and `labelLength` parameters:

```
    function findResolver(bytes calldata name, uint256 offset) internal view returns (address, bytes32, uint256) {
        uint256 labelLength = uint256(uint8(name[offset]));
        if (labelLength == 0) {
            return (address(0), bytes32(0), offset);
        }
        uint256 nextLabel = offset + labelLength + 1;
        bytes32 labelHash;
        if (
            // 0x5b == '['
            // 0x5d == ']'
            labelLength == 66 && name[offset + 1] == 0x5b && name[nextLabel - 1] == 0x5d
        ) {
            // Encrypted label
            (labelHash,) = bytes(name[offset + 2:nextLabel - 1]).hexStringToBytes32(0, 64);
        } else {
            labelHash = keccak256(name[offset + 1:nextLabel]);
        }
        (address parentresolver, bytes32 parentnode, uint256 parentoffset) = findResolver(name, nextLabel);
        bytes32 node = keccak256(abi.encodePacked(parentnode, labelHash));
        address resolver = registry.resolver(node);
        if (resolver != address(0)) {
            return (resolver, node, offset);
        }
        return (parentresolver, node, parentoffset);
    }
```

##### BVSS

[AO:A/AC:L/AX:H/R:N/S:U/C:N/A:L/I:N/D:N/Y:N (0.8)](/bvss?q=AO:A/AC:L/AX:H/R:N/S:U/C:N/A:L/I:N/D:N/Y:N)

##### Recommendation

Add a validation step at the beginning of the `findResolver` function to ensure that `offset` is within the array's bounds and that the calculated range `offset + labelLength + 1` does not exceed the length of the `name` array.

##### Remediation

**SOLVED:** The **Beranames team** solved the issue in the specified commit id.

##### Remediation Hash

<https://github.com/Beranames/beranames-contracts-v2/pull/106/commits/af34c26c430ae3ba31f9ab87057378dd9deb4d1b>

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

