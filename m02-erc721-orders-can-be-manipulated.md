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
solodit_id: 10682
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/1inch-limit-order-protocol-audit/
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

[M02] ERC721 orders can be manipulated

### Overview


The OrderMixin contract allows users to exchange more than just ERC20s. Out-of-scope proxies such as the ERC721Proxy, ERC721ProxySafe, and ERC1155Proxy contracts are used to provide support for ERC721 and ERC1155 tokens. These proxies must be called with the same pattern as an IERC20 transferFrom call, and the signature must start with address from, address to, and uint256 amount. Anything else that the proxies require can be passed in after, and is defined in the order as makerAssetData and takerAssetData. 

The ERC1155Proxy contract makes use of the amount field, while the ERC721Proxy and ERC721ProxySafe contracts use the required amount field as the tokenId instead. This creates the possibility of partially filling ERC721 orders in order to purchase separately listed tokens at discounted prices. 

To avoid this exploit, consider separating the amount and tokenId arguments and document this to alert users of this behavior. This issue was fixed in pull request #59.

### Original Finding Content

It is possible to exchange more than just ERC20s via the [`OrderMixin`](https://github.com/1inch/limit-order-protocol/blob/4d94eea25e4dac6271bfd703096a5c4a4d899b4a/contracts/OrderMixin.sol) by deploying a contract that shares the same function selector as IERC20’s `transferFrom`, and providing that contract as the [`makerAsset`](https://github.com/1inch/limit-order-protocol/blob/4d94eea25e4dac6271bfd703096a5c4a4d899b4a/contracts/OrderMixin.sol#L279) or the [`takerAsset`](https://github.com/1inch/limit-order-protocol/blob/4d94eea25e4dac6271bfd703096a5c4a4d899b4a/contracts/OrderMixin.sol#L259) in an order.


The out-of-scope proxies, namely, [`ERC721Proxy`](https://github.com/1inch/limit-order-protocol/blob/4d94eea25e4dac6271bfd703096a5c4a4d899b4a/contracts/helpers/ERC721Proxy.sol), [`ERC721ProxySafe`](https://github.com/1inch/limit-order-protocol/blob/4d94eea25e4dac6271bfd703096a5c4a4d899b4a/contracts/helpers/ERC721ProxySafe.sol), and [`ERC1155Proxy`](https://github.com/1inch/limit-order-protocol/blob/4d94eea25e4dac6271bfd703096a5c4a4d899b4a/contracts/helpers/ERC1155Proxy.sol) contracts follow this pattern to provide support for `ERC721` and `ERC1155` tokens. Since the proxies must be called with the same pattern as an IERC20 `transferFrom` call, the signature must start with `address from`, `address to` and `uint256 amount`. Anything else that the proxies require can be passed in after, and is defined in the order as [`makerAssetData`](https://github.com/1inch/limit-order-protocol/blob/4d94eea25e4dac6271bfd703096a5c4a4d899b4a/contracts/OrderMixin.sol#L279) and [`takerAssetData`](https://github.com/1inch/limit-order-protocol/blob/4d94eea25e4dac6271bfd703096a5c4a4d899b4a/contracts/OrderMixin.sol#L259).


ERC1155s can naturally transfer multiple of the same id tokens at once, which means the [`ERC1155Proxy`](https://github.com/1inch/limit-order-protocol/blob/4d94eea25e4dac6271bfd703096a5c4a4d899b4a/contracts/helpers/ERC1155Proxy.sol) contract makes use of the `amount` field. On the other hand, `ERC721`s do not have an obvious use for the `amount` field. Since they represent non-fungible tokens, a specific tokenId will only have one in existence, rendering the `amount` field useless. Because of this, the implementation for both [`ERC721Proxy`](https://github.com/1inch/limit-order-protocol/blob/4d94eea25e4dac6271bfd703096a5c4a4d899b4a/contracts/helpers/ERC721Proxy.sol) and [`ERC721ProxySafe`](https://github.com/1inch/limit-order-protocol/blob/4d94eea25e4dac6271bfd703096a5c4a4d899b4a/contracts/helpers/ERC721ProxySafe.sol) contracts use the required `amount` field as the `tokenId` instead.


This overloading of the `amount` parameter creates the possibility of partially filling `ERC721` orders in order to purchase separately listed tokens at discounted prices. For instance, there could be a case where a single user has multiple `ERC721`s of the same contract permitted to be transferred by the [`ERC721Proxy`](https://github.com/1inch/limit-order-protocol/blob/4d94eea25e4dac6271bfd703096a5c4a4d899b4a/contracts/helpers/ERC721Proxy.sol) contract and lists them in separate limit orders.  

If the limit orders also provide the [`getMakerAmount`](https://github.com/1inch/limit-order-protocol/blob/4d94eea25e4dac6271bfd703096a5c4a4d899b4a/contracts/OrderMixin.sol#L316) and [`getTakerAmount`](https://github.com/1inch/limit-order-protocol/blob/4d94eea25e4dac6271bfd703096a5c4a4d899b4a/contracts/OrderMixin.sol#L327) fields, it will be possible to partially fill these `ERC721` orders. Since the order’s [`amount`](https://github.com/1inch/limit-order-protocol/blob/4d94eea25e4dac6271bfd703096a5c4a4d899b4a/contracts/OrderMixin.sol#L278) field actually corresponds to the [`tokenId`](https://github.com/1inch/limit-order-protocol/blob/4d94eea25e4dac6271bfd703096a5c4a4d899b4a/contracts/helpers/ERC721Proxy.sol#L22), a malicious user can place a partial fill on the `ERC721` with the higher tokenId, resulting in a [`makingAmount`](https://github.com/1inch/limit-order-protocol/blob/4d94eea25e4dac6271bfd703096a5c4a4d899b4a/contracts/OrderMixin.sol#L278)/[`takingAmount`](https://github.com/1inch/limit-order-protocol/blob/4d94eea25e4dac6271bfd703096a5c4a4d899b4a/contracts/OrderMixin.sol#L258) of an `ERC721` that could correspond to a lower `tokenId`. The result is the `ERC721` with the lower `tokenId` would be transferred at the price of `(higher tokenId price) * (lower tokenId's id) / (higher tokenId's id)`.


This exploit has a few requirements:


* Multiple `ERC721`s from the same contract to be allowed on either `ERC721` proxy by a single owner.
* Open order for one of the `ERC721`s that is not the lowest `tokenId` of the ones allowed.
* Partial fills allowed on the order.


To completely remove the possibility of partial `ERC721` fills, consider separating the `amount` and `tokenId` arguments. Whether the arguments are separated or not, consider also documenting this to alert users of this behavior and to avoid this pattern in the future.


***Update:** Fixed in [pull request #59](https://github.com/1inch/limit-order-protocol/pull/59).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

