---
# Core Classification
protocol: Infinity NFT Marketplace
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 2786
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-06-infinity-nft-marketplace-contest
source_link: https://code4rena.com/reports/2022-06-infinity
github_link: https://github.com/code-423n4/2022-06-infinity-findings/issues/74

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
  - cross_chain
  - payments
  - nft_marketplace
  - gaming

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - 0xalpharush
---

## Vulnerability Title

[M-09] Malicious tokens can be used to grief buyers and cause loss of their WETH balance

### Overview


This bug report is about the function `matchOneToOneOrders` in the InfinityExchange smart contract. The function transfers an arbitrary amount of WETH from the user, `buy.signer`, in its inner call to `_execMatchOneToOneOrders`. This amount is calculated dynamically based off of the gas consumption consumed during the trace, and is controlled by the seller since the seller's token can be malicious and purposefully consume a large amount of gas to grief the buyer. If a buyer purchases a malicious token, the `_transferNFTs` will result in a call to an `ERC721.safeTransferFrom` that can exhibit any behavior such as wasting gas, resulting in the buyer's WETH being sent to the protocol. 

Proof of concept of this vulnerability is a buyer giving infinite WETH approval to the exchange contract and unknowingly purchasing a malicious token from an attacker. The attacker's token wastes gas in the transfer call and causes all of the buyer's WETH to be sent to the protocol when `matchOneToOneOrders` is performed by the match executor.

To mitigate this vulnerability, it is recommended to allow users to input a maximum fee/ gas cost they are willing to spend on each order. Manual gas accounting is error prone and it would make more sense to allow users to match orders themselves instead of extracting fees to compensate the matcher.

### Original Finding Content

_Submitted by 0xalpharush_

<https://github.com/code-423n4/2022-06-infinity/blob/765376fa238bbccd8b1e2e12897c91098c7e5ac6/contracts/core/InfinityExchange.sol#L739-L746>

<https://github.com/code-423n4/2022-06-infinity/blob/765376fa238bbccd8b1e2e12897c91098c7e5ac6/contracts/core/InfinityExchange.sol#L727>

<https://github.com/code-423n4/2022-06-infinity/blob/765376fa238bbccd8b1e2e12897c91098c7e5ac6/contracts/core/InfinityExchange.sol#L1087>

### Impact

The function `matchOneToOneOrders` transfers an arbitrary amount of WETH from the user, `buy.signer` ,  in its inner call to `_execMatchOneToOneOrders`. The amount charged to the user is calculated dynamically based off of the gas consumption consumed during the trace. Notably, this amount is controlled by the seller since the seller's token can be malicious and purposefully consume a large amount of gas to grief the buyer. For example, when a user purchases an ERC721 token, the `_transferNFTs` will result in a call to an `ERC721.safeTransferFrom` that can exhibit any behavior such as wasting gas. This scenario is unlikely given that a buyer would have to purchase a malicious token, but the impact would be devastating as any WETH that the buyer has approved to the exchange can be lost.

This vulnerability is potentially possible in these functions as well:<br>
<https://github.com/code-423n4/2022-06-infinity/blob/765376fa238bbccd8b1e2e12897c91098c7e5ac6/contracts/core/InfinityExchange.sol#L236-L242><br>
<https://github.com/code-423n4/2022-06-infinity/blob/765376fa238bbccd8b1e2e12897c91098c7e5ac6/contracts/core/InfinityExchange.sol#L787-L796>

### Proof of Concept

A buyer gives infinite WETH approval to the exchange contract and unknowingly purchases a malicious token from an attacker. The attacker's token wastes gas in the transfer call and causes *all* of the buyer's WETH to be sent to the protocol when `matchOneToOneOrders` is performed by the match executor.

### Recommended Mitigation Steps

Allow users to input a maximum fee/ gas cost they are willing to spend on each order. Pulling an arbitrary amount from a user's wallet without any restriction is a dangerous practice given that many users give large/ infinite approval to contracts.

In addition, manual gas accounting is error prone and it would make more sense to allow users to match orders themselves instead of extracting fees to compensate the matcher.

**[nneverlander (Infinity) acknowledged and commented](https://github.com/code-423n4/2022-06-infinity-findings/issues/74#issuecomment-1164323281):**
 > Thanks, we are adding a max price variable

**[HardlyDifficult (judge) commented](https://github.com/code-423n4/2022-06-infinity-findings/issues/74#issuecomment-1181073834):**
 > This is a clever way to leverage safeTransferFrom to grief users. Accepting as Medium risk.



***





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Infinity NFT Marketplace |
| Report Date | N/A |
| Finders | 0xalpharush |

### Source Links

- **Source**: https://code4rena.com/reports/2022-06-infinity
- **GitHub**: https://github.com/code-423n4/2022-06-infinity-findings/issues/74
- **Contest**: https://code4rena.com/contests/2022-06-infinity-nft-marketplace-contest

### Keywords for Search

`vulnerability`

