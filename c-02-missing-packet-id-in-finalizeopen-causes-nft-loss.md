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
solodit_id: 62593
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/RipIt-security-review_2025-05-10.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[C-02] Missing packet ID in `finalizeOpen()` causes NFT loss

### Overview


The bug report is about a critical flaw in the `Packet.sol` contract that causes all transactions to fail when the `burnType` is **INSTANT_OPEN_PACKET**. This happens because the function `finalizeOpen()` does not properly assign the packet ID to an array before calling `packetStore.addPacketsToInventory()`. This results in the user losing their packet NFT without receiving anything in return. The report recommends adding the missing assignment to store the packet ID in the array to fix the issue.

### Original Finding Content


_Resolved_

## Severity

**Impact:** High

**Likelihood:** High

## Description

In the `Packet.sol` contract, the `finalizeOpen()` function has a critical flaw that will cause all transactions to fail when the `burnType` is **INSTANT_OPEN_PACKET**.
When processing an **INSTANT_OPEN_PACKET** burn type, the function attempts to add the packet to inventory by calling `packetStore.addPacketsToInventory(packetIds)`. However, it creates a new array to hold the packet ID but never actually assigns the packet ID to the array:
```solidity
if (burnType == BurnType.INSTANT_OPEN_PACKET) {
    _transfer(ownerOf(packetId), address(this), packetId);
    this.approve(address(packetStore), packetId);

    uint256[] memory packetIds = new uint256[](1);
    // Missing: packetIds[0] = packetId;
    packetStore.addPacketsToInventory(packetIds);
}
```
As a result, the `packetIds` array contains only default values (zeros), not the actual packet ID, causing `addPacketsToInventory()` to attempt to process an invalid packet ID. This will lead to a revert in `addPacketsToInventory()` when it tries to validate a zero packet ID

```solidity
if (!_validatePacketTypeId(packetTypeId)) revert InvalidPacketType(packetTypeId);
```

This issue results in the user losing their packet NFT (as it's transferred to the contract) but not receiving anything in return, as the transaction fails during the call to `packetStore.addPacketsToInventory()`.

### Proof of Concept

Please copy the following POC in `CardAllocationPoolTest.t.sol`

```solidity
function testPOC() public {
        uint256 packetType = 1;
        uint256 packetId = 1;
        uint256[] memory cardIds = _mintCardsToAdmin(3);

        // Add bundle to pool
        vm.startPrank(admin);
        bytes32 bundleProvenance = keccak256(abi.encode(cardIds));
        pool.addCardBundlesToPacketPool(packetType, cardIds, cardIds, bundleProvenance);
        vm.stopPrank();

        // Setup packet
        vm.startPrank(admin);
        packet.registerPacketType(
            PacketStorage.PacketTypeParams({packetTypeName: "Test Pack", packetTypeMetadata: "Test Metadata"})
        );

        packet.mintTo(
            PacketStorage.PacketMintParams({
                packetTypeId: packetType,
                packetMetadata: "Test Packet",
                packetSerialNumber: "TEST-001"
            }),user
        );

        vm.stopPrank(); 

        // User initiates burn which will trigger instantOpenPacket
        
        vm.startPrank(user);
        vm.expectRevert(RipFunStore.InvalidPacketType.selector);
        packet.initiateBurn(
            PacketStorage.PacketBurnParams({packetId: packetId, burnType: PacketStorage.BurnType.INSTANT_OPEN_PACKET})
        );
        vm.stopPrank();

        // Verify request was made
        //assertTrue(coordinator.lastRequestId() == 0);
    }
```
## Recommendations

Add the missing assignment to store the packet ID in the array before calling `addPacketsToInventory()`
```diff
 function finalizeOpen(uint256 packetId, uint256[] memory selectedBundle, string memory openMetadata)
        external
        onlyRole(ALLOCATION_MANAGER_ROLE)
    {
       //...
        if (burnType == BurnType.INSTANT_OPEN_PACKET) {
            _transfer(ownerOf(packetId), address(this), packetId);
            this.approve(address(packetStore), packetId);

            uint256[] memory packetIds = new uint256[](1);
+           packetIds[0] = packetId;
            packetStore.addPacketsToInventory(packetIds);
        } else {
          //...
        }
        //...
    }
```
This will ensure that the correct packet ID is passed to the `addPacketsToInventory()` function, allowing the transaction to complete successfully.





### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

