---
# Core Classification
protocol: Sweep n Flip
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46497
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/8d400356-5bf2-4bd4-91e2-93f0a785406e
source_link: https://cdn.cantina.xyz/reports/cantina_sweepnflip_bridge_november2024.pdf
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
finders_count: 2
finders:
  - slowfi
  - Sujith Somraaj
---

## Vulnerability Title

RefundAddress forwarded to LayerZero endpoint is incorrect 

### Overview


Summary:

The sendMessageUsingNative function in the LayerZeroAdapter contract is used to send messages using LayerZero. However, there is a bug where refunds from LayerZero's endpoint are sent to the Bridge contract instead of the specified refund address. This results in the refunds being locked indefinitely in the Bridge contract. To fix this, the bug can be addressed by forwarding a user-specified refund address or by making sure the msg.value is strictly equal to the quoted fee. The bug has been fixed in the snf-bridge-contracts-v1 PR 16.

### Original Finding Content

## Context
- LayerZeroAdapter.sol#L172
- LayerZeroAdapter.sol#L175

## Description
The `sendMessageUsingNative` function from the `LayerZeroAdapter.sol` contract is used by the `Bridge.sol` contract to send a message using LayerZero. This function, in turn, calls the `_sendMessage` function, which again calls `_lzSend` to call the LayerZero endpoint with the right parameters.

The `sendMessageUsingNative` function accepts `msg.value` equal to or greater than the fee quoted by LayerZero to cover LayerZero's messaging costs. It forwards them to the endpoint contract, from which any unused value is refunded to the `refundAddress` specified. 

However, these refunds don't work as expected as the refund address is always specified as the `Bridge.sol` contract, which is the `msg.sender` in the context of the `LayerZeroAdapter.sol` contract. Thus, any refunds received from LayerZero's endpoint are locked indefinitely in the `Bridge.sol` contract.

## Recommendation
The above-mentioned vulnerability could be fixed in multiple ways, including:
- Forwarding a user-specified refund address to LayerZero's endpoint to process refunds properly.
- Collecting all refunds from the endpoint to Bridge and refunding all the `msg.value` stored in `Bridge.sol` at the end of a bridging transaction back to the `msg.sender`.
- Making sure `msg.value` is strictly equal to the quoted fee, ensuring no refunds are possible.

## Sweep n' Flip
Fixed in snf-bridge-contracts-v1 PR 16.

## Cantina Managed
Verified fix. A new variable called `refundAddress` is forwarded from `Bridge.sol` to the LayerZero adapter, encoding `msg.sender` as the refund address.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Sweep n Flip |
| Report Date | N/A |
| Finders | slowfi, Sujith Somraaj |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_sweepnflip_bridge_november2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/8d400356-5bf2-4bd4-91e2-93f0a785406e

### Keywords for Search

`vulnerability`

