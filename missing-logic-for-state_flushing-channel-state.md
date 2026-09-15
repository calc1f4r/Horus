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
solodit_id: 59013
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/datachain-ibc/1e53ee14-4316-4cb1-9977-45753e49d5b2/index.html
source_link: https://certificate.quantstamp.com/full/datachain-ibc/1e53ee14-4316-4cb1-9977-45753e49d5b2/index.html
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
finders_count: 3
finders:
  - Andrei Stefan
  - Ed Zulkoski
  - Jonathan Mevs
---

## Vulnerability Title

Missing Logic for `STATE_FLUSHING` Channel State

### Overview


This bug report is about a missing logic in the ibc-solidity implementation. The issue occurs when the channel is in the `STATE_FLUSHING` state and actively completing an upgrade. This missing logic enforces a counterparty upgrade timeout, but it is not included in the `acknowledgePacket()` and `timeoutPacket()` functions. The recommendation is to add this logic to these functions and review the implementation against the specs to ensure all `STATE_FLUSHING` logic is included. 

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `43f77d23d18b06c21933ca08e5cc341524546eaf`, `deac22dcce61c488379e8a584dd323ca337d61d8`, `eadd74c653b91433b722afab8eb2e28d72b5ab21`.

**File(s) affected:**`IBCChannelPacketSendRecv.sol`, `IBCChannelPacketTimeout.sol`

**Description:** During several packet operations there is missing logic in the ibc-solidity implementation when the Channel is in the `STATE_FLUSHING` state and actively completing an upgrade. According to the specs, this logic enforces a counterparty upgrade timeout. The logic is missing from the `acknowledgePacket()` and `timeoutPacket()` functions.

**Recommendation:** The logic to handle a counterparty's upgrade timeout should be included in these functions. Further, we encourage the IBC team to closely review the ibc-solidity implementation against the specs to ensure all `STATE_FLUSHING` logic is included where specified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

