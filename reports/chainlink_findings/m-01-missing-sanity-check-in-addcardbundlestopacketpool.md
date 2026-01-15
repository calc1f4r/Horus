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
solodit_id: 62545
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

[M-01] Missing sanity check in `addCardBundlesToPacketPool`

### Overview


This bug report is about a problem in the CardAllocationPool contract that affects the instant redeem feature. The issue is caused by a gas limit being set too low in the initialize() function, which is used for a Chainlink VRF callback. This leads to the callback function failing and users not being able to receive their card NFTs. Additionally, there is a missing sanity check in the addCardBundlesToPacketPool function, which could cause further issues. The recommendation is to add a sanity check for the length of the card bundle.

### Original Finding Content


_Resolved_

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

In CardAllocationPool contract, we will generate one randomness via Chainlink VRF for the instant redeem. In initialize() function, we will initialize `callbackGasLimit` to 100_000. This gas limit is used for the Chainlink VRF callback gas limit.

In the callback function, there is one loop for transferring the selected cards. After the foundry's test, if we have 10 cards in this bundle, the gas limit will be insufficient. This will cause the callback function will fail, and users cannot get the card NFT.

Function `addCardBundlesToPacketPool` is used to add one card bundle. The problem here is that we don't add any sanity check about the card bundle's length.
```solidity
    function initialize(
        address packetAddress,
        address cardAddress,
        address _rbac,
        uint256 _redeemManagerRoleId,
        address vrfCoordinator,
        uint256 subscriptionId,
        bytes32 _keyHash
    ) external initializer {
        callbackGasLimit = 100000;
    }
    function fulfillRandomWords(uint256 requestId, uint256[] memory randomWords) internal {
        PacketOpenRequest storage request = requestIdToPacketOpen[requestId];
        if (request.fulfilled) revert("Already fulfilled");

        CardBundle[] storage cardBundles = packetTypeToCardBundles[request.packetType];

        uint256[] memory selectedCards = selectRandomCards(cardBundles, randomWords[0]);

@>        for (uint256 i = 0; i < selectedCards.length; i++) {
            IERC721(cardNFTAddress).transferFrom(address(this), request.owner, selectedCards[i]);
        }

        request.fulfilled = true;

        RipFunPacks(packetNFTAddress).finalizeOpen(request.packetId, "");

        emit PacketOpenFulfilled(requestId, request.packetId, selectedCards);
    }
    function addCardBundlesToPacketPool(uint256 packetType, uint256[] memory cardBundles, bytes32 bundleProvenance)
        external
        onlyRole(redeemManagerRoleId)
    {
        packetTypeToCardBundles[packetType].push(CardBundle({cardIds: cardBundles, bundleProvenance: bundleProvenance}));
        for (uint256 i = 0; i < cardBundles.length; i++) {
            IERC721(cardNFTAddress).transferFrom(msg.sender, address(this), cardBundles[i]);
        }

        emit CardsAddedToPool(packetType, cardBundles, bundleProvenance);
    }
```

## Recommendations

Add a sanity check for the card bundle's length.





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

