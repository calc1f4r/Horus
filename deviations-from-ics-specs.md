---
# Core Classification
protocol: Datachain - IBC
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59025
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/datachain-ibc/1e53ee14-4316-4cb1-9977-45753e49d5b2/index.html
source_link: https://certificate.quantstamp.com/full/datachain-ibc/1e53ee14-4316-4cb1-9977-45753e49d5b2/index.html
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
finders_count: 3
finders:
  - Andrei Stefan
  - Ed Zulkoski
  - Jonathan Mevs
---

## Vulnerability Title

Deviations From ICS-Specs

### Overview

See description below for full details.

### Original Finding Content

**Update**
Marked as "Acknowledged" by the client. Addressed in: `93311b1f8d6b289d35e4983c93c1bebca51127b7`, `476a6d81b9c0ba33a31759b6f7e3b41f05602ee7`. The client provided the following explanation:

> *   Check for the existence of generated channel ID was corrected at 93311b1f8d6b289d35e4983c93c1bebca51127b7.
> *   We have confirmed other deviations from the specifications pointed out by the audit ream. The main deviations are described in our doc at 476a6d81b9c0ba33a31759b6f7e3b41f05602ee7.

**File(s) affected:**`All`

**Description:** Below, we include a non-exhaustive list of all deviations from the ICS-Specs in the ibc-solidity implementatio. These deviations are not standalone issues, however we list these deviations for transparency for all future users of ibc-solidity. Many of these deviations are a result of the limitations of the Solidity language and the EVM environment, such as gas costs or transaction gas limits and are intentional design decisions made by the Datachain team. The team has documented these changes in the files at `docs/adr`.

Overall, we note that ibc-solidity does not support multi-hop connections or for the `ORDERED_ALLOW_TIMEOUT` channel ordering mechanism, as described in the ICS-Specs. Therefore, all logic associated with that is not present in the ibc-solidity implementation.

Deviations:

*   `authenticateCapability()` does not exist in the ibc-solidity implementation as a single function, as described in the ICS specs. Instead, the owner of the `IBCHandler` contract will invoke `bindPort()` to assign module address to given ports in the provable store of the `IBCHandler`. Then, throughout conneciton and channel handshakes, capabilities are authenticated through functions such as `IBCModuleManager.lookupModuleByPort()` and `lookupModuleByChannel()`, which proves there is a non-zero address mapped at the port or channel, showing that the module has been bound by an IBC admin, and the channel has been written. During handshakes, module callback functions such as `onRecvPacket()` will only be invoked on the module addresses assigned by the Admin.
*   `clientConnectionsPath()` providing a reverse mapping from clients to a set of connections is not included in the implementation.
    *   This means, there is no way that `queryClientConnections()` can be implemented and this data will have to be queried using other methods.

*   `ConnectionEnd` structural deviation:
    *   `delayPeriodBlocks` is not defined to be a field within a Connection. Instead, when this field is needed for message passing, it is calculated during the transaction, as a function of the `delayPeriodTime` and the `expectedTimePerBlock` which is configurable by the IBCHandler admin.
    *   Further, the `ConnectionEnd` doesn't have fields like `counterPartyPrefix` and instead, these fields are defined within a counterparty data structure which is a field within the ConnectionEnd itself

*   `channelOpenInit()`&`channelOpenTry()` do not confirm that the generated `channelId` is not already stored, as specified in the specs. We recognize that a clash is highly unlikely, as there are 2^64 possible ids. However, a check like this is done in `connectionOpenInit()` and we recommend verifying that there is nothing stored at the generated id for thoroughness.
*   `emit RecvPacket()` does not include the Order and Connection fields as [specified in ICS-specs](https://github.com/cosmos/ibc/blob/499818e9c4b136029717a436a04af15113f4424f/spec/core/ics-004-channel-and-packet-semantics/README.md?plain=1#L879)
*   the `_writeAcknowledgement()` function is emitting an event that is missing the following fields, that are otherwise specified in the specs:
    *   `timeoutHeight`
    *   `timeoutTimestamp`
    *   `packet.data`

*   `sendPacket()` does not check that the connection exists. However, since the connection is stored within the `Channel.Data` itself, and the channel's existence is confirmed, we see no major issue here and include this to note the discrepancy.
*   Specs allow for a packet to received more than once, with just an identical event being emitted, however, in the implementation, we cannot receive a packet more than once, and the transaction will revert. the Datachain team has already acknowledged this to be a design choice however we note here for thoroughness and transparency.
*   `counterpartyUpgradePaths()` are not written to the provable store

**Recommendation:** We recommend that during the fix review process, the Datachain team review this spec deviations and confirm that they are all expected.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Datachain - IBC |
| Report Date | N/A |
| Finders | Andrei Stefan, Ed Zulkoski, Jonathan Mevs |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/datachain-ibc/1e53ee14-4316-4cb1-9977-45753e49d5b2/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/datachain-ibc/1e53ee14-4316-4cb1-9977-45753e49d5b2/index.html

### Keywords for Search

`vulnerability`

