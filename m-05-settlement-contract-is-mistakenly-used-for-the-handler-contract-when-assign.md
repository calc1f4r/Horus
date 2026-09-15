---
# Core Classification
protocol: Chakra
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49152
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-08-chakra
source_link: https://code4rena.com/reports/2024-08-chakra
github_link: https://github.com/code-423n4/2024-08-chakra-findings/issues/171

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
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 7
finders:
  - said
  - AllTooWell
  - rbserver
  - ABAIKUNANBAEV
  - Draiakoo
---

## Vulnerability Title

[M-05] Settlement contract is mistakenly used for the handler contract when assigning `ReceivedCrossChainTx` struct

### Overview


The report discusses a bug in the code for the Chakra network's Settlement contract. The bug occurs in the `receive_cross_chain_msg()` function, where the contract mistakenly uses `address(this)` instead of `to_handler` address when creating a new `ReceivedCrossChainTx` struct. This results in incorrect parameters being stored in the `receive_cross_txs` mapping. The recommended mitigation step is to change `address(this)` to `to_handler` address in the mapping. The severity of this bug is considered to be medium, as it should not affect the processing of cross-chain transactions.

### Original Finding Content


### Impact

`receive_cross_chain_msg()` is located in the Settlement contract and is called after the Chakra network signature verification process. However, when creating `ReceivedCrossChainTx` struct for the new `receive_cross_txs[txid]`, the contract mistakenly uses `address(this)` instead of `to_handler` address.

### Proof of Concept

Currently `receive_cross_txs[txId]` is assigned this way:

<https://github.com/code-423n4/2024-08-chakra/blob/main/solidity/settlement/contracts/ChakraSettlement.sol#L205-214>

```
 receive_cross_txs[txid] = ReceivedCrossChainTx(
            txid,
            from_chain,
            contract_chain_name,
            from_address,
            from_handler,
            address(this),
            payload,
            CrossChainMsgStatus.Pending
        );

```

However, `address(this)` should be replaced by `to_handler`:

<https://github.com/code-423n4/2024-08-chakra/blob/main/solidity/settlement/contracts/ChakraSettlement.sol#L31-40>

```
struct ReceivedCrossChainTx {
        uint256 txid;
        string from_chain;
        string to_chain;
        uint256 from_address;
        uint256 from_handler;
        address to_handler;
        bytes payload;
        CrossChainMsgStatus status;
    }

```

As you can see here, after `from_handler`, there is `to_handler` address but it's mistakenly set as `address(this)` which is an address of the settlement contract in reality.

Therefore, `receive_cross_txs[txid]` has incorrect parameters when creating a new received transaction struct.

### Recommended Mitigation Steps

Change `address(this)` on `to_handler` address in a `receive_cross_txs[txid]` mapping.

**[pidb (Chakra) confirmed](https://github.com/code-423n4/2024-08-chakra-findings/issues/171#event-14332748972)**

**[0xsomeone (judge) commented](https://github.com/code-423n4/2024-08-chakra-findings/issues/171#issuecomment-2434857100):**
 > The Warden has identified that the `ChakraSettlement::receive_cross_chain_msg` function will improperly store a cross-chain message and will specifically store the `to_handler` address incorrectly.
> 
> The impact of this particular submission is not able to be identified properly and, given that the function appears to be invoked as the last step in a cross-chain process, a severity of medium is considered appropriate as it should not impact the actual processing of the cross-chain transaction.


***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Chakra |
| Report Date | N/A |
| Finders | said, AllTooWell, rbserver, ABAIKUNANBAEV, Draiakoo, 0xNirix, Abdessamed |

### Source Links

- **Source**: https://code4rena.com/reports/2024-08-chakra
- **GitHub**: https://github.com/code-423n4/2024-08-chakra-findings/issues/171
- **Contest**: https://code4rena.com/reports/2024-08-chakra

### Keywords for Search

`vulnerability`

