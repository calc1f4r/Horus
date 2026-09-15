---
# Core Classification
protocol: Securitize Onofframp Bridge
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64273
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md
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
  - Hans
---

## Vulnerability Title

Pause modifier in bridge receiver functions causes receiver failures for in-flight messages

### Overview


This bug report discusses an issue with the `USDCBridge::receivePayloadAndUSDC` and `SecuritizeBridge::receiveWormholeMessages` functions in the bridge contracts. These functions are protected by the `whenNotPaused` modifier, which causes them to fail when the contracts are paused. This issue can result in funds becoming stuck without a way to recover them automatically. The recommended mitigation is to remove the `whenNotPaused` modifier and implement a way to track and retry failed messages. This issue has been partially fixed by removing the modifier in the `USDCBridge` contract. The bug has been verified by Cyfrin.

### Original Finding Content

**Description:** The `USDCBridge::receivePayloadAndUSDC` and `SecuritizeBridge::receiveWormholeMessages` functions are protected by the `whenNotPaused` modifier, which causes these functions to revert when the respective bridge contracts are paused. According to the [Wormhole documentation](https://wormhole.com/docs/products/messaging/guides/wormhole-relayers/#delivery-statuses), when receiver functions revert, the message status becomes "Receiver Failure" and there is no automatic retry mechanism available. The only way to recover from receiver failures is to restart the entire process from the source chain.

```solidity
// USDCBridge.sol
function receivePayloadAndUSDC(
    bytes memory payload,
    uint256 amountUSDCReceived,
    bytes32 sourceAddress,
    uint16 sourceChain,
    bytes32 deliveryHash
) internal override onlyWormholeRelayer whenNotPaused {
    // Function will revert if contract is paused
    // ...
}

// SecuritizeBridge.sol
function receiveWormholeMessages(
    bytes memory payload,
    bytes[] memory additionalVaas,
    bytes32 sourceBridge,
    uint16 sourceChain,
    bytes32 deliveryHash
) public override payable whenNotPaused {
    // Function will revert if contract is paused
    // ...
}
```

This creates an operational issue where funds associated with in-flight messages become stuck without any built-in recovery mechanism provided by the bridge contracts.

The problematic scenario:
1. User initiates a cross-chain transfer from Chain A to Chain B
2. Bridge contract on Chain B gets paused due to an emergency or maintenance
3. Wormhole relayer attempts to deliver the message to Chain B
4. The receiver function reverts due to the `whenNotPaused` modifier
5. Message status becomes "Receiver Failure" permanently
6. Funds are stuck with no automatic recovery mechanism

**Impact:** Funds associated with in-flight cross-chain messages become stuck when bridge contracts are paused, requiring manual intervention to recover assets.

**Recommended Mitigation:** Remove the `whenNotPaused` modifier from receiver functions to prevent receiver failures.
Furthermore, consider tracking received messages with the receive process success flag and allow the admin to retry the failed messages.

**Securitize:** Partially fixed in commit [97e37b](https://bitbucket.org/securitize_dev/bc-securitize-bridge-sc/commits/97e37bed37168bc1ca73fb18f06fbae06161819d), `whenNotPaused` has been removed for the `USDCBridge` receive function.

**Cyfrin:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Securitize Onofframp Bridge |
| Report Date | N/A |
| Finders | Hans |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

