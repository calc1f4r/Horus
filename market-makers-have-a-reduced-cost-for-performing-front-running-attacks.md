---
# Core Classification
protocol: 0x Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17375
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/0x-protocol.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/0x-protocol.pdf
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
  - Gustavo Grieco
  - Robert Tonic
  - Rajeev Gopalakrishna
  - Michael Colburn
---

## Vulnerability Title

Market makers have a reduced cost for performing front-running attacks

### Overview


This bug report describes an exploit scenario where a market maker, Eve, takes advantage of the 0x Protocol 3.0's protocol fee which is calculated with tx.gasprice * protocolFeeMultiplier. Eve is able to increase her profit by submitting a transaction with a higher gas cost and protocol fee, front-running Alice's transaction to sell her asset before the price decreases. To prevent this exploit, it is recommended to document the issue and establish a reasonable cap for the protocolFeeMultiplier, as well as consider using an alternative fee that does not depend on tx.gasprice.

### Original Finding Content

## Data Validation

## Target
`exchange/contracts/src/MixinExchangeCore.sol`

## Difficulty
High

## Description
The 0x Protocol 3.0 specification defines how protocol fees are calculated. The protocol fee can be calculated with `tx.gasprice * protocolFeeMultiplier`, where the `protocolFeeMultiplier` is an upgradable value meant to target a percentage of the gas used for filling a single order. The suggested initial value for the `protocolFeeMultiplier` is 150000, which is roughly equal to the average gas cost of filling a single order (thereby doubling the net average cost).

**Figure 2.1:** The protocol fee definition as defined in the 3.0 specification.

Market makers receive a portion of the protocol fee for each order filled, and the protocol fee is based on the transaction gas price. Therefore, market makers are able to specify a higher gas price for a reduced overall transaction rate, using the refund they will receive upon disbursement of protocol fee pools.

## Exploit Scenario
Eve is a market-maker maintaining a distribution pool. Alice submits a profitable transaction to Eve’s market. Eve sees the unconfirmed transaction and realizes it will result in a lower overall asset price, and submits a transaction with a higher gas cost and protocol fee, front-running Alice’s transaction to sell her asset before the price decreases and increasing her profit from the transaction. Because Eve is a market maker, she receives a portion of the protocol fee she paid to front run Alice’s transaction, reducing the overall cost.

## Recommendation
Short term, properly document this issue to make sure users are aware of this risk. Establish a reasonable cap for the `protocolFeeMultiplier` to mitigate this issue.

Long term, consider using an alternative fee that does not depend on the `tx.gasprice` to avoid reducing the cost of performing front-running attacks.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | 0x Protocol |
| Report Date | N/A |
| Finders | Gustavo Grieco, Robert Tonic, Rajeev Gopalakrishna, Michael Colburn |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/0x-protocol.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/0x-protocol.pdf

### Keywords for Search

`vulnerability`

