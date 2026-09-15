---
# Core Classification
protocol: RipIt_2025-05-10
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62600
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/RipIt-security-review_2025-05-10.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[L-03] Missing validation for burned `packetIds` in `addCardBundlesToPacketPool()`

### Overview

See description below for full details.

### Original Finding Content


_Resolved_

In the `CardAllocationPool.addCardBundlesToPacketPool()` function, intended to be called by the redeemer manager to add cards to a specific packet type's pool as a bundle, there is no validation to ensure that the `packetIds` provided belong to the same `packetTypeId` being added.

This lack of validation can result in inconsistent or incorrect packet assignments. Additionally, it creates a potential security risk, as a malicious redeem manager could exploit this gap to burn any packet listed in the `PacketStore`, leading to the removal of unintended packets and causing possible disruptions in the system.

```solidity
  function addCardBundlesToPacketPool(
        uint256 packetType,
        uint256[] memory cardBundles,
        uint256[] memory packetIds,
        bytes32 bundleProvenance
    ) external noPendingRandomness onlyRole(redeemManagerRoleId) {
        //...

        packetTypeToCardBundles[packetType].push(CardBundle({cardIds: cardBundles, bundleProvenance: bundleProvenance}));
        for (uint256 i = 0; i < cardBundles.length; i++) {
            RipFunPacks(packetNFTAddress).burnFromInventory(packetIds[i]);
            IERC721(cardNFTAddress).safeTransferFrom(msg.sender, address(this), cardBundles[i]);
        }

        //...
    }
```

Recommendation:
Implement a validation step to ensure that all `packetIds` provided are associated with the provided `packetTypeId`.





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | RipIt_2025-05-10 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/RipIt-security-review_2025-05-10.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

