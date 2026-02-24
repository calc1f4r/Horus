---
# Core Classification
protocol: Linea V2 Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32567
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/linea-v2-audit
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
  - OpenZeppelin
---

## Vulnerability Title

Relayer Claiming a Message to a Contract Destination Does Not Refund the User

### Overview


This bug report is about a problem with a messaging system called Linea. When a user sends a message from one platform to another, the fee paid to the relayer is not refunded, which means the relayer always takes the full fee. This happens because the fee is calculated based on unknown gas conditions, causing it to either be too high or too low. This issue only affects messages sent to contracts, not individual users. This can lead to higher costs and risks for cross-chain applications using this messaging system. The team behind Linea is aware of the issue and is looking into potential solutions.

### Original Finding Content

A relayer claiming a message on [L2 to a contract destination does not refund the user](https://github.com/Consensys/linea-contracts-audit/blob/bb6eb7284d1ac9574dc69e654abe5ccb8d8ded1a/contracts/messageService/l2/v1/L2MessageServiceV1.sol#L232), resulting in the fee always being fully taken by the relayer. During submission, when specifying the fee on L1, the fee will always either be overestimated or underestimated due to unknown gas conditions on L2 during claiming. Consequently, if underpaid, it will be uneconomical to relay, or if overpaid, it will unnecessarily leak value from users.


In contrast, for EOAs, the refund mechanism mitigates this issue by refunding overpayments, thus allowing sustained operation by the subsidized relayers. The absence of similar functionality for contract destinations limits the usefulness and reliability of cross-chain applications built on this messaging system, raising their maintenance costs since cross-chain applications will need to run and subsidize their own relay bots or force users to overpay for the gas fees. Since anything other than bridging ETH to an EOA requires calling contracts, this approach significantly impairs cross-chain functionality. Specifically, in times of rising gas prices, a backlog of unrelayed transactions will accumulate, causing unreliable user experiences for cross-chain applications relying on this mechanism.


In practice, the impact of this will likely be complexity and additional costs for cross-chain protocols, which will probably be passed on to their users as higher costs and risks. Alternatively, users will be directly forced to overpay for gas fees for cross-chain messaging. Both scenarios result in a low impact but highly likely value leakage from users.


Consider redesigning the gas metering system for cross-chain messages so that a refund mechanism for contract destinations is viable. For example, the cross-chain payload may [specify `maxFeePerGas`, `gasLimit`, and `refundRecipient`](https://docs.arbitrum.io/arbos/l1-to-l2-messaging) instead of a total amount and unlimited gas. Such a mechanism can limit overpayment by users by refunding any oversupplied fees to the refund recipient while providing a predictable incentive for relayers.


***Update:** Acknowledged, not resolved. The Linea team stated:*



> *We are considering options for this already and there are no changes for this audit.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Linea V2 Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/linea-v2-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

