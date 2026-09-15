---
# Core Classification
protocol: 1inch Limit Order Protocol Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 10678
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/1inch-limit-order-protocol-audit/
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

protocol_categories:
  - dexes
  - services
  - cross_chain
  - nft_lending
  - oracle

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[H01] Inconsistent data passed into _makeCall

### Overview


A bug was found in the OrderMixin contract which affects the _makeCall function. This function is used to transfer assets from the taker to the maker and then from the maker to the taker. In the latter transfer, the _makeCall function was incorrectly passed the order’s makerAsset as the last parameter, when it should be the order’s makerAssetData. As a result, any proxy functionality that relies on the makerAssetData argument will break. To fix the bug, the parameter should be updated to order.makerAssetData. The bug has since been fixed in pull request #57.

### Original Finding Content

In the [`OrderMixin`](https://github.com/1inch/limit-order-protocol/blob/4d94eea25e4dac6271bfd703096a5c4a4d899b4a/contracts/OrderMixin.sol) contract, the [`_makeCall`](https://github.com/1inch/limit-order-protocol/blob/4d94eea25e4dac6271bfd703096a5c4a4d899b4a/contracts/OrderMixin.sol#L308) function is used to transfer assets [from the taker to the maker](https://github.com/1inch/limit-order-protocol/blob/4d94eea25e4dac6271bfd703096a5c4a4d899b4a/contracts/OrderMixin.sol#L252) and then [from the maker to the taker](https://github.com/1inch/limit-order-protocol/blob/4d94eea25e4dac6271bfd703096a5c4a4d899b4a/contracts/OrderMixin.sol#L272). In the latter transfer, the `_makeCall` function is incorrectly passed the order’s [`makerAsset`](https://github.com/1inch/limit-order-protocol/blob/4d94eea25e4dac6271bfd703096a5c4a4d899b4a/contracts/OrderMixin.sol#L58) as the last parameter, when it should be the order’s [`makerAssetData`](https://github.com/1inch/limit-order-protocol/blob/4d94eea25e4dac6271bfd703096a5c4a4d899b4a/contracts/OrderMixin.sol#L65).


As a result, any proxy functionality that relies on the `makerAssetData` argument will break.


To be consistent with the earlier call to `_makeCall` and to fully support proxy functionality, consider updating the `order.makerAsset` parameter to `order.makerAssetData`.


***Update:** Fixed in [pull request #57](https://github.com/1inch/limit-order-protocol/pull/57).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | 1inch Limit Order Protocol Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/1inch-limit-order-protocol-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

