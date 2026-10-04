---
# Core Classification
protocol: RipIt_2025-04-25
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62552
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/RipIt-security-review_2025-04-25.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-08] Inconsistent logic in `initiateBurn()` and `initiateBurnBatch()` functions

### Overview


There is a bug in the `initiateBurnBatch` function of the Packet contract. This function does not have the same logic as the `initiateBurn` function, causing inconsistent behavior when burning packets in batches. This means that packets intended for instant opening may not be handled correctly when burned in a batch. To fix this, the `initiateBurnBatch` function should include the same logic as the `initiateBurn` function for handling `BurnType.INSTANT_OPEN_PACKET` or prohibit the usage of this burn type in `initiateBurnBatch`.

### Original Finding Content


_Resolved_

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

The `initiateBurnBatch` function in the Packet contract exhibits inconsistent logic compared to the `initiateBurn` function. 

In `initiateBurn`, if the `burnType` is `BurnType.INSTANT_OPEN_PACKET`, the function calls `instantOpenPacket` to handle the burn operation.

```solidity
        if (params.burnType == BurnType.INSTANT_OPEN_PACKET) {
            randomAllocationPool.instantOpenPacket(params.packetId, _packetTypeIds[params.packetId], msg.sender);
        }
```

However, the `initiateBurnBatch` function lacks similar logic to process `BurnType.INSTANT_OPEN_PACKET`, which means that batch burning does not trigger the same behavior as individual burning. This inconsistency could lead to unexpected outcomes, **where packets intended for instant opening are not handled correctly when burned in a batch.**

```solidity
    function initiateBurnBatch(PacketBurnParams[] calldata params) external {
        for (uint256 i = 0; i < params.length; i++) {
            if (params[i].burnType == BurnType.NONE) {
                revert InvalidBurnType();
            }
            if (ownerOf(params[i].packetId) != msg.sender) {
                revert NotPacketOwner();
            }
            if (_packetBurnType[params[i].packetId] != BurnType.NONE) {
                revert PacketAlreadyInBurnState();
            }

            _packetBurnType[params[i].packetId] = params[i].burnType;
            emit BurnInitiated(params[i].packetId, params[i].burnType, msg.sender);
        }
    }
```

## Recommendations

To ensure consistency between the two functions, the `initiateBurnBatch` function should include logic to handle the `BurnType.INSTANT_OPEN_PACKET` case. Or simply prohibit the usage of `BurnType.INSTANT_OPEN_PACKET` in `initiateBurnBatch`.





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | RipIt_2025-04-25 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/RipIt-security-review_2025-04-25.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

