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
solodit_id: 49142
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-08-chakra
source_link: https://code4rena.com/reports/2024-08-chakra
github_link: https://github.com/code-423n4/2024-08-chakra-findings/issues/141

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
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 7
finders:
  - said
  - 1
  - 2
  - SBSecurity
  - shaflow2
---

## Vulnerability Title

[H-09] Inconsistent Handler Validation Behavior in Cairo ERC20Handler's Cross-Chain Callback

### Overview


This bug report discusses a vulnerability in the Cairo implementation of ERC20Handler. The `receive_cross_chain_callback` function uses an assert statement to validate handlers, which can cause the function to revert if a handler is invalid. This behavior is different from the Solidity implementation, which returns false for invalid handlers. This vulnerability can lead to transactions remaining in a Pending state, inconsistent transaction states, and difficulty in handling and recovering from invalid handler scenarios. The recommended mitigation step is to update the Cairo implementation to check handler validity without using assert. The severity of this bug has been confirmed by a member of the team and increased by the judge to High.

### Original Finding Content


### Impact

The `receive_cross_chain_callback` function in the Cairo implementation of ERC20Handler uses an assert statement to validate handlers, which causes the function to revert if a handler is invalid or has been removed from the whitelist. This behavior differs from the Solidity implementation, which returns false for invalid handlers.

This vulnerability can lead to:

1.  Transactions remaining in a Pending state indefinitely in the Cairo implementation
2.  Inconsistent transaction states across different chain implementations
3.  Potential blocking of cross-chain operations
4.  Difficulty in handling and recovering from invalid handler scenarios

### Proof of Concept

Cairo implementation:

```
    fn receive_cross_chain_callback(ref self: ContractState, cross_chain_msg_id: felt252, from_chain: felt252, to_chain: felt252,
        from_handler: u256, to_handler: ContractAddress, cross_chain_msg_status: u8) -> bool{
        assert(to_handler == get_contract_address(),'error to_handler');
        assert(self.settlement_address.read() == get_caller_address(), 'not settlement');
        assert(self.support_handler.read((from_chain, from_handler)) && 
                self.support_handler.read((to_chain, contract_address_to_u256(to_handler))), 'not support handler');

        // ... rest of the function
    }
```

Solidity implementation:

```solidity
function receive_cross_chain_callback(
    uint256 txid,
    string memory from_chain,
    uint256 from_handler,
    CrossChainMsgStatus status,
    uint8 /* sign_type */,
    bytes calldata /* signatures */
) external onlySettlement returns (bool) {
    if (is_valid_handler(from_chain, from_handler) == false) {
        return false;
    }

    // ... rest of the function
}
```

```solidity
  function processCrossChainCallback(
        uint256 txid,
        string memory from_chain,
        uint256 from_handler,
        address to_handler,
        CrossChainMsgStatus status,
        uint8 sign_type,
        bytes calldata signatures
    ) internal {
        require(
            create_cross_txs[txid].status == CrossChainMsgStatus.Pending,
            "Invalid transaction status"
        );

        if (
            ISettlementHandler(to_handler).receive_cross_chain_callback(
                txid,
                from_chain,
                from_handler,
                status,
                sign_type,
                signatures
            )
        ) {
            create_cross_txs[txid].status = status;
        } else {
            create_cross_txs[txid].status = CrossChainMsgStatus.Failed;
        }
    }
```

In the Cairo version, if a handler is invalid, the function will revert due to the assert statement, leaving the transaction in its current state (likely Pending). In contrast, the Solidity version returns false, allowing the calling Settlement contract to handle the invalid handler case appropriately.

### Recommended Mitigation Steps

Update the Cairo implementation to check handler validity without using assert.

**[zvlwwj (Chakra) confirmed](https://github.com/code-423n4/2024-08-chakra-findings/issues/141#event-14356705423)**

**[0xsomeone (judge) increased severity to High](https://github.com/code-423n4/2024-08-chakra-findings/issues/141#issuecomment-2434981218)**


***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Chakra |
| Report Date | N/A |
| Finders | said, 1, 2, SBSecurity, shaflow2, 0xNirix, Abdessamed |

### Source Links

- **Source**: https://code4rena.com/reports/2024-08-chakra
- **GitHub**: https://github.com/code-423n4/2024-08-chakra-findings/issues/141
- **Contest**: https://code4rena.com/reports/2024-08-chakra

### Keywords for Search

`vulnerability`

