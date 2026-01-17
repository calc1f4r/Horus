---
# Core Classification
protocol: Stargate V2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47357
audit_firm: OtterSec
contest_link: https://stargate.finance/
source_link: https://stargate.finance/
github_link: https://github.com/stargate-protocol/stargate-v2

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
finders_count: 3
finders:
  - Robert Chen
  - Nicholas R.Putra
  - Jessica Clendinen
---

## Vulnerability Title

Incorrect Bounds Check

### Overview


This bug report is about a vulnerability in a code called BusLib::ride. This code is used to check if a bus is at full capacity before allowing a passenger to board. However, the condition used for this check is incorrect, which can lead to a situation where the bus appears full but can still allow a passenger to board. This can result in messages being lost and subsequent failures in the code. The solution to this issue is to revise the code to verify that the maximum number of passengers is one less than the bus capacity. This bug has been fixed in version 06d5975.

### Original Finding Content

## BusLib::ride Capacity Check

Within `BusLib::ride`, a check exists to verify if a bus is at full capacity before permitting a passenger to board. However, the condition employed for this assessment is `ticketId - _bus.headTicketId >= _busCapacity`. This condition examines whether the disparity between the current `ticketId` and the `headTicketId` of the bus surpasses or equals bus's capacity (`_busCapacity`).

```solidity
// File: src/libs/Bus.sol
function ride(
    [...]
) internal returns (uint56 ticketId, bytes memory passengerBytes, uint128 fare, uint256 refund) {
    [...]
    // check if the bus is full
    if (ticketId - _bus.headTicketId >= _busCapacity) revert Bus_BusFull();
    [...]
}
```

The vulnerability stems from the condition allowing the number of passengers to match the bus's capacity. This implies that the final available `ticketId` may equate to `_busCapacity + _bus.headTicketId - 1`. In such a scenario, `ride` permits a passenger to board despite the bus being technically full.

The bus serves as a means of grouping messages together. Each message's hash is stored in a linked chain, and if the hash is not inserted into the `hashChain` or if the position is overwritten in `hashChain`, then the message is lost, resulting in subsequent failures in the `checkTickets` logic.

```solidity
// File: src/libs/Bus.sol
function checkTickets(
    [...]
) internal view returns (ThisBus memory drivingBus) {
    [...]
    // check the hash of the last passenger
    uint56 lastTicketIdToDrive = startTicketId + numPassengers - 1;
    if (lastTicketIdToDrive >= _bus.tailTicketId || lastHash != _bus.hashChain[lastTicketIdToDrive % _busCapacity])
        revert Bus_InvalidPassenger();
}
```
© 2024 Otter Audits LLC. All Rights Reserved. 7/19

## Stargate Audit 04 — Vulnerabilities

### Remediation

Revise `ride` to verify that the maximum number of passengers is one less than the bus capacity:

```solidity
// File: src/libs/Bus.sol
function ride(
    Bus storage _bus,
    uint56 _busCapacity,
    uint32 _dstEid,
    TransferPayloadDetails memory _passenger,
    uint16 _baseFareMultiplierBps,
    uint128 _extraFare
) internal returns (uint56 ticketId, bytes memory passengerBytes, uint128 fare, uint256 refund) {
    [...]
    // check if the bus is full
    if (ticketId - _bus.headTicketId >= _busCapacity - 1) revert Bus_BusFull();
    [...]
}
```

### Patch

Fixed in 06d5975.

© 2024 Otter Audits LLC. All Rights Reserved. 8/19

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Stargate V2 |
| Report Date | N/A |
| Finders | Robert Chen, Nicholas R.Putra, Jessica Clendinen |

### Source Links

- **Source**: https://stargate.finance/
- **GitHub**: https://github.com/stargate-protocol/stargate-v2
- **Contest**: https://stargate.finance/

### Keywords for Search

`vulnerability`

