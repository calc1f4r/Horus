---
# Core Classification
protocol: Ax Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48248
audit_firm: OtterSec
contest_link: github.com/Ax-Protocol/usx/.
source_link: github.com/Ax-Protocol/usx/.
github_link: github.com/Ax-Protocol/usx/.

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
  - Robert Chen
  - Shiva Shankar
  - YoungJoo Lee
  - OtterSec
---

## Vulnerability Title

Missing Wormhole Bridge Fees

### Overview


The report states that there is a bug in the Wormhole messaging system where the message publishing process fails if an incorrect fee is applied. This is due to the current implementation not properly handling the fees. The suggested solution is to pass on the entire message value when calling the publishMessage function. This bug has been resolved in a recent patch.

### Original Finding Content

## Sending Messages Using Wormhole

In order to send messages using Wormhole, it is necessary to pay the bridge fee during message publication. If an incorrect fee is applied to the message call, the message publishing process will fail.

## Code Example

```solidity
function publishMessage(
    uint32 nonce,
    bytes memory payload,
    uint8 consistencyLevel
) public payable returns (uint64 sequence) {
    // check fee
    require(msg.value == messageFee(), "invalid fee");
    sequence = useSequence(msg.sender);
    // emit log
    emit LogMessagePublished(msg.sender, sequence, nonce, payload, consistencyLevel);
}
```

As a result, the current implementation would likely abort due to invalid fees.

## Remediation

Add code to pass on the entire message value to properly pay the Wormhole fees.

```diff
- sequence = wormholeCoreBridge.publishMessage(0, message, 200);
+ sequence = wormholeCoreBridge.publishMessage{value:msg.value}(0, message, 200);
```

Consider passing on the entire message value to send ETH values as much as the message fee when `publishMessage` is called. Note that message fees can be obtained by calling `IWormhole::messageFee`.

## Patch

Resolved in commit `777ba1d`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Ax Protocol |
| Report Date | N/A |
| Finders | Robert Chen, Shiva Shankar, YoungJoo Lee, OtterSec |

### Source Links

- **Source**: github.com/Ax-Protocol/usx/.
- **GitHub**: github.com/Ax-Protocol/usx/.
- **Contest**: github.com/Ax-Protocol/usx/.

### Keywords for Search

`vulnerability`

