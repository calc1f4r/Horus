---
# Core Classification
protocol: Sapien
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62037
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/sapien/ffb7e698-6178-46f0-8df8-52e537af70c0/index.html
source_link: https://certificate.quantstamp.com/full/sapien/ffb7e698-6178-46f0-8df8-52e537af70c0/index.html
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
finders_count: 4
finders:
  - Paul Clemson
  - Julio Aguilar
  - Mostafa Yassin
  - Tim Sigl
---

## Vulnerability Title

Bloom Filter Implementation Can Lead to False Positives Preventing Valid Reward Claims

### Overview


The client reported a bug in the Rewards contract, where a Bloom filter is used to track redeemed order IDs. However, this implementation can lead to false positives, preventing users from claiming legitimate rewards. The issue arises from the limited size of the filter (256 bits) and multiple hash insertions per order. This can result in collisions, causing valid orders to be incorrectly identified as already redeemed. The client recommended replacing the Bloom filter with a simple mapping to track redeemed orders.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `73264fb`.

![Image 34: Alert icon](https://certificate.quantstamp.com/full/sapien/ffb7e698-6178-46f0-8df8-52e537af70c0/static/media/success-icon-alert.4e26c8d3b65fdf9f4f0789a4086052ba.svg)

**Update**
Marked as "Fixed" by the client. Addressed in: `34c39e3637c09d1d5d850bae1897d1200c23cfef`. The client provided the following explanation:

> The Bloom filter implementation for tracking redeemed orders was replaced with a simple double mapping structure (mapping(address => mapping(bytes32 => bool)) private redeemedOrders).

![Image 35: Alert icon](https://certificate.quantstamp.com/full/sapien/ffb7e698-6178-46f0-8df8-52e537af70c0/static/media/success-icon-alert.4e26c8d3b65fdf9f4f0789a4086052ba.svg)

**Update**
Marked as "Fixed" by the client. Addressed in: `34c39e3637c09d1d5d850bae1897d1200c23cfef`. The client provided the following explanation:

> The Bloom filter implementation for tracking redeemed orders was replaced with a simple double mapping structure (mapping(address => mapping(bytes32 => bool)) private redeemedOrders).

**File(s) affected:**`Rewards.sol`

**Description:** The `Rewards` contract uses a Bloom filter to track redeemed order IDs, but this implementation can lead to false positives that prevent users from claiming legitimate rewards. The issue arises from the limited size of the filter (256 bits) combined with multiple hash insertions per order.

Each order sets 3 bits in the 256-bit filter. With users expected to claim up to 1000 rewards, this results in up to 3000 bits being set in a 256-bit space, leading to a high probability of collisions.

**Impact**

*   As users claim more rewards, the Bloom filter becomes increasingly saturated
*   This increases the probability of hash collisions causing false positives
*   Valid orders may be incorrectly identified as already redeemed
*   Users will be unable to claim legitimate rewards once collisions occur

**Exploit Scenario:**

1.   After claiming ~300 rewards:

    *   Each claim triggered 3 hash operations
    *   Many bits were hit multiple times
    *   The majority of the 256 bits in Alice's filter are now set to 1

2.   Alice attempts to claim a new legitimate reward: `claimReward(amount, "REWARD_1000", signature)`

3.   The transaction reverts because:

    *   The 3 hash positions for this orderId happen to map to bits that were already set by previous claims
    *   `isOrderRedeemed()` returns `true` (false positive)
    *   The legitimate claim is blocked

**Recommendation:** Replace the complex Bloom filter implementation with a simple mapping to track redeemed orders. Even high-volume contracts like USDC rely on simple mappings for state tracking such as user balances due to their reliability and reasonable gas costs. An example could be the following:

```
mapping(address => mapping(bytes32 => bool)) private redeemedOrders;

function isOrderRedeemed(address user, string calldata orderId) internal view returns (bool) {
return redeemedOrders[user][keccak256(abi.encodePacked(orderId))];
}

function addOrderToRedeemed(address user, string calldata orderId) internal {
redeemedOrders[user][keccak256(abi.encodePacked(orderId))] = true;
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Sapien |
| Report Date | N/A |
| Finders | Paul Clemson, Julio Aguilar, Mostafa Yassin, Tim Sigl |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/sapien/ffb7e698-6178-46f0-8df8-52e537af70c0/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/sapien/ffb7e698-6178-46f0-8df8-52e537af70c0/index.html

### Keywords for Search

`vulnerability`

