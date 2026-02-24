---
# Core Classification
protocol: zkSync GnosisSafeZk Assessment
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32676
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/zksync-gnosissafezk-assessment-1
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

Unexpected Refund Recipient

### Overview


The report mentions a bug in the `GnosisSafeZk` contract where any address can invoke a transaction if it has been authorized and the relayer accepts the gas refund parameters. However, if no `refundRecipient` is specified, the `tx.origin` address will receive the refund. This is a problem on the zkEVM because if the initiator is a smart contract account, the bootloader will receive the refund instead of the correct address. To prevent this, it is suggested to always specify a `refundRecipient` when the initiator is the bootloader address. The bug has been acknowledged but not yet resolved by the Matter Labs team.

### Original Finding Content

Any address [is able](https://github.com/protofire/safe-contracts/blob/17d9fd5491f7e63543f51082e733220adb17a832/contracts/GnosisSafeZk.sol#L122) to invoke a transaction on behalf of the `GnosisSafeZk` contract, provided the transaction has been [authorized by enough owners](https://github.com/protofire/safe-contracts/blob/17d9fd5491f7e63543f51082e733220adb17a832/contracts/GnosisSafeZk.sol#L145) and the relayer accepts the corresponding [gas refund parameters](https://github.com/protofire/safe-contracts/blob/17d9fd5491f7e63543f51082e733220adb17a832/contracts/GnosisSafeZk.sol#L117-L119). However, if no `refundRecipient` is specified, the `tx.origin` address [will receive the refund](https://github.com/protofire/safe-contracts/blob/17d9fd5491f7e63543f51082e733220adb17a832/contracts/GnosisSafeZk.sol#L204).


This makes sense on the EVM but on the zkEVM there is an important subtlety. If the initiator is an EOA (the default account), then it is set as the `tx.origin` value, so it will correctly receive the refund. However, if the initiator is another smart contract account, [the bootloader will be set as `tx.origin`](https://github.com/matter-labs/era-system-contracts/blob/main/bootloader/bootloader.yul#L1364) and it will incorrectly receive the refund.


To avoid loss of funds, consider enforcing that the `refundRecipient` is specified whenever `tx.origin` is the bootloader address.


***Update:** Acknowledged, not resolved. The Matter Labs team stated:*



> *We agree that this complicates the usage of custom accounts with multisig wallet. However, the cost of supporting different codebases is also very high and the issue affects only custom zkSync functionality.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | zkSync GnosisSafeZk Assessment |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/zksync-gnosissafezk-assessment-1
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

