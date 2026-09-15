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
solodit_id: 62574
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/RipIt-security-review_2025-04-25.md
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

[L-16] Data integrity issue with `revertBurnRequest` in `RipFunPacks`

### Overview

See description below for full details.

### Original Finding Content


_Acknowledged_

In the `RipFunPacks` function, if a packet of type `INSTANT_OPEN` undergoes a `revertBurnRequest`, it can lead to a failure when the `fulfillRandomWords` function is later called by the `Chainlink`.

```solidity
    function revertBurnRequest(uint256 packetId, string calldata revertBurnRequestMetadata)
        external
        onlyRole(REDEEM_MANAGER_ROLE)
    {
        if (_packetBurnType[packetId] == BurnType.NONE) {
            revert PacketNotInBurnState();
        }

        BurnType previousBurnType = _packetBurnType[packetId];
        _packetBurnType[packetId] = BurnType.NONE;

        emit BurnRequestReverted(packetId, revertBurnRequestMetadata, previousBurnType, msg.sender);
    }
```

However, in `CardAllocationPool` will call `finalizeOpen` in the function `fulfillRandomWords`.

```solidity
    function fulfillRandomWords(uint256 requestId, uint256[] memory randomWords) internal {
        PacketOpenRequest storage request = requestIdToPacketOpen[requestId];
        if (request.fulfilled) revert("Already fulfilled");

        // fetch the available card bundles
        CardBundle[] storage cardBundles = packetTypeToCardBundles[request.packetType];

        // Select random cards using the provided randomness
        uint256[] memory selectedCards = selectRandomCards(cardBundles, randomWords[0]);

        // Transfer cards to owner
        for (uint256 i = 0; i < selectedCards.length; i++) {
            IERC721(cardNFTAddress).transferFrom(address(this), request.owner, selectedCards[i]);
        }

        // Mark request as fulfilled
        request.fulfilled = true;

        // Call finalize open on packet contract
        RipFunPacks(packetNFTAddress).finalizeOpen(request.packetId, "");

        emit PacketOpenFulfilled(requestId, request.packetId, selectedCards);
    }
```

 This failure occurs because the state of the packet is not properly managed when the burn request is reverted.

```solidity
    function finalizeOpen(uint256 packetId, string memory openMetadata) external onlyRole(ALLOCATION_MANAGER_ROLE) {
        BurnType burnType = _packetBurnType[packetId];
        if (burnType != BurnType.OPEN_PACKET && burnType != BurnType.INSTANT_OPEN_PACKET) {
            revert InvalidBurnStateForOpen();
        } // <= revert here, due to status has been reset

        _burn(packetId);
        emit OpenFinalized(packetId, burnType, msg.sender, openMetadata);
    }
```

As a result, the `CardAllocationPool` may end up with inconsistent or "dirty" data, where the status of the packet does not accurately reflect its intended state.
- The request will never be fulfilled.
- The VRF subscription is still charged for the work done to generate your requested random values.

To mitigate this issue, it is crucial to implement proper state management to keep track of the status.





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
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

