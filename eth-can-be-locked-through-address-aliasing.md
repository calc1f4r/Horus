---
# Core Classification
protocol: zkSync WETH Bridge Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32685
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/zksync-weth-bridge-audit
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

ETH Can Be Locked Through Address Aliasing

### Overview


The bug report discusses an issue where users may have their ETH locked in a L2 address that they do not control when interacting with L2 from L1. This can happen if the user specifies a refund recipient address when using certain functions. The report also mentions that this issue was previously attempted to be fixed, but it still persists. The report suggests removing address aliasing for the refund recipient and making it mandatory to provide a refund recipient address to prevent this issue. The team has acknowledged the issue but has not yet resolved it, stating that users can specify a refund recipient to eliminate the risk. However, the report suggests that mandatory parameter is a cleaner option.

### Original Finding Content

Whenever interacting with L2 from L1, either through the `Mailbox.requestL2Transaction` or the `L1WethBridge.deposit` function, the user can specify a refund recipient address. This address receives a refund (on L2) of any excessive ETH provided, up to a full refund in the case of a reverting transaction.


When calling one of the above functions, which refund recipient is chosen and whether that address is aliased depends on the provided `_refundRecipient` parameter, as well as `msg.sender`. The checks that differentiate these conditions can be seen in the `Mailbox` facet [[1]](https://github.com/matter-labs/zksync-2-contracts/blob/4346dfc55a3c56817934a1231b64d6ef246074a7/ethereum/contracts/zksync/facets/Mailbox.sol#L216-L219) [[2]](https://github.com/matter-labs/zksync-2-contracts/blob/4346dfc55a3c56817934a1231b64d6ef246074a7/ethereum/contracts/zksync/facets/Mailbox.sol#L278-L279), [`L1WethBridge` contract](https://github.com/matter-labs/zksync-2-contracts/blob/4346dfc55a3c56817934a1231b64d6ef246074a7/ethereum/contracts/bridge/L1WethBridge.sol#L170-L172), and [`_requestL2Transaction` function](https://github.com/matter-labs/zksync-2-contracts/blob/4346dfc55a3c56817934a1231b64d6ef246074a7/ethereum/contracts/zksync/facets/Mailbox.sol#L280-L283). The outcome of the used refund recipient is condensed into the following table:




| `msg.sender` | `_refundRecipient` | | |
| --- | --- | --- | --- |
|  | **Is Zero** | **Is L1 Contract** | **Is L1 EOA** |
| **Is L1 Contract** | aliased `msg.sender` (\*) | aliased `_refundRecipient` (\*) | `_refundRecipient` |
| **Is L1 EOA** | `msg.sender` | aliased `_refundRecipient` (\*) | `_refundRecipient` |


Firstly, the cases (\*) where the refund will be sent to an aliased address on L2 are confusing and error-prone, especially since the docstring states that the `_refundRecipient` is ["The address on L2 that will receive the refund for the transaction"](https://github.com/matter-labs/zksync-2-contracts/blob/4346dfc55a3c56817934a1231b64d6ef246074a7/ethereum/contracts/bridge/L1WethBridge.sol#L144-L145). Secondly, it is possible that the caller has no control over that address, thereby locking the ETH. An exception to this occurs if the L1 contract is able to initiate arbitrary L2 transaction requests, such that the caller can act as the aliased address through the `Mailbox` to transfer or withdraw the ETH.


It is noted that in a previous report, this issue was presented and a fix was attempted at commit [`201c99c`](https://github.com/matter-labs/zksync-2-contracts/pull/32/commits/201c99c117049813663b9ec9fc78f2cf52168a4b). While OpenZeppelin's previous review had deemed this fixed, upon further review, it has now been identified that this issue persists.


As of March 30th, 2023, the [`Mailbox` contract](https://etherscan.io/address/0x2ea0cfb9c942058ee5a84411ef2e37c6de5bfe5c#code#F11#L247) on mainnet appears to be affected by this issue. Thus, under the conditions above, users are currently at risk of having their ETH locked in a L2 address that they do not control. While the [developer documentation](https://era.zksync.io/docs/dev/developer-guides/bridging/l1-l2.html#interface) provides warnings regarding aliasing, it is still possible for users (particularly those less familiar with the inner workings of the system) to have their ETH locked.


The reasoning for the address aliasing of the refund recipient is unclear at the moment. It is understood that applying address aliasing to the `msg.sender` can help prevent cross-chain attacks. However, consider removing address aliasing for the refund recipient. In addition, consider requiring that a refund recipient is always provided.


***Update:** Acknowledged, not resolved. The Matter Labs team stated:*



> *Users can specify the needed refund receiver to eliminate the risk of a smart contract refund recipient that is not able to get the funds back. That being said, we agree that mandatory parameter is a cleaner option, but whether it is the better foolproof approach is debatable. As an example, one of our partners that are building a bridge asked us to implement this. Also, users seem to be used to this approach on Arbitrum, and since it is battle-tested, the risk is rather small. Lastly, the ERC-20 bridge was deployed on production and it is highly undesirable to change its behavior without an important reason. Thank you for highlighting the issue, we will keep eye on it.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | zkSync WETH Bridge Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/zksync-weth-bridge-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

