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
solodit_id: 47360
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

Missing Calldata Validation

### Overview


The bug in the code for the Bus::checkTickets function neglects to validate the numPassengers parameter, which can result in exceeding the recorded number of passengers/tickets in the bus state. This can cause issues with the drive function, which relies on the numPassengers parameter to determine the ticket range for processing. If numPassengers exceeds the actual number of tickets, this can lead to incorrect positioning and potentially overwrite existing ticket data. The solution is to check if lastTicketIdToDrive is greater than tailTicketId. This bug has been fixed in a recent patch.

### Original Finding Content

## Bus Ticket Validation Issue

`Bus::checkTickets` neglects to validate the `numPassengers` parameter to ensure it does not exceed the actual number of tickets. Consequently, `driveBus` is invoked with this invalid parameter, resulting in exceeding the recorded number of passengers/tickets in the bus state. `drive`, responsible for updating the bus state, depends on the `numPassengers` parameter provided in the payload to determine the ticket range for processing.

```solidity
> _stg-evm-v2/src/libs/Bus.sol

function checkTickets(
    [...]
) internal view returns (ThisBus memory drivingBus) {
    // check the hash of the last passenger
    uint56 lastTicketIdToDrive = startTicketId + numPassengers - 1;
    if (lastHash != _bus.hashChain[lastTicketIdToDrive % BUS_CAPACITY]) revert Bus_InvalidPassenger();
}
```

Since `drive` determines the head of the ticket list for the bus based on `numPassengers`, an invalid `numPassengers` value will result in incorrect positioning within `hashChain`. Suppose `numPassengers` exceeds the actual number of tickets. In that case, the function may set the head of the ticket list beyond the valid range, overwriting existing ticket data in `hashChain`. Consequently, if the head of the ticket list is incorrectly set due to an invalid `numPassengers`, subsequent calls to `driveBus` on the same bus may fail.

## Remediation
Check if `lastTicketIdToDrive` is greater than `tailTicketId`.

## Patch
Fixed in version `6342bb`.

© 2024 Otter Audits LLC. All Rights Reserved. 11/19

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

