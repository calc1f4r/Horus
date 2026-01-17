---
# Core Classification
protocol: Centrifuge
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35791
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Centrifuge-Spearbit-Security-Review-July-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Centrifuge-Spearbit-Security-Review-July-2024.pdf
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
  - Devtooligan
  - 0xLeastwood
  - Jonatas Martins
  - Gerard Persoon
---

## Vulnerability Title

Inconsistency in message library between rust and solidity implementations

### Overview


This bug report discusses inconsistencies in the formatting of data that is being passed between the Centrifuge chain and Ethereum. These inconsistencies are causing issues with certain messages, such as missing parameters and using different address formats. The recommendation is to maintain consistency between the two systems and update the PoolManager contract to comply with inbound messages from Centrifuge. The bug has been fixed in the latest commit on Centrifuge's end and by Spearbit.

### Original Finding Content

## Medium Risk Report

## Context
- **Files Affected:** 
  - `BytesLib.sol#L68`
  - `PoolManager.sol#L158-L163`

## Description
Message data is passed between Ethereum and Centrifuge through the gateway contract. Incoming messages are dispatched when quorum has been reached. The first byte indicates the intended action to be executed on a target manager contract. Each manager contract implements a `handle()` function which decodes this data according to the message ID. 

There are some inconsistencies in the formatting of data that is passed from Centrifuge chain to Ethereum. The inconsistencies apply to the following messages (as per latest commit):

- There is an extra 32 bytes that is expected from Centrifuge but not used in:
  - `TransferAssets`
  - `TransferTrancheTokens`
- `UpdateTrancheHook` is missing a 16 byte `tranchId` parameter.
- `UpdateCentrifugeGasPrice` should pass two parameters, a `uint128` and `uint64`, when only a `uint64` is being provided.
- `DisputeMessageRecovery` is missing the adapter address.
- `RecoverTokens` should decode the amount parameter to a `uint128` instead.
- Two types of addresses are used: a 20 byte address and a 32 byte address, while the Solidity `toAddress()` uses a 32 byte address.

## Recommendation
Maintain consistency between the message library implementations on Centrifuge chain and Ethereum. Doublecheck the used address formats. The `PoolManager` contract needs to be updated to enable tranch/asset token transfers and comply with inbound messages from Centrifuge.

```solidity
} else if (call == MessagesLib.Call.TransferAssets) {
    handleTransfer(message.toUint128(1), message.toAddress(17), message.toUint128(49));
} else if (call == MessagesLib.Call.TransferTrancheTokens) {
    handleTransferTrancheTokens(
        message.toUint64(1), message.toBytes16(9), message.toAddress(34), message.toUint128(66)
    );
}
```

## Status
- **Centrifuge:** Fixed in commit `223a0f36`.
- **Spearbit:** Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Centrifuge |
| Report Date | N/A |
| Finders | Devtooligan, 0xLeastwood, Jonatas Martins, Gerard Persoon |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Centrifuge-Spearbit-Security-Review-July-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Centrifuge-Spearbit-Security-Review-July-2024.pdf

### Keywords for Search

`vulnerability`

