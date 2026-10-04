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
solodit_id: 49141
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-08-chakra
source_link: https://code4rena.com/reports/2024-08-chakra
github_link: https://github.com/code-423n4/2024-08-chakra-findings/issues/147

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
finders_count: 3
finders:
  - fyamf
  - klau5
  - 0xAsen
---

## Vulnerability Title

[H-08] In `settlement.cairo::receive_cross_chain_msg` - the `payload_type` can be passed by the user, confusing offchain systems

### Overview


This bug report discusses a potential issue in the `settlement.cairo::receive_cross_chain_msg` function where the `payload_type` parameter can be passed by the user, causing confusion for off-chain systems. This parameter is only used to emit events for Chakra nodes to detect and process, and there is no validation for it. This can lead to incorrect data being displayed and undefined behavior in the future. The recommended mitigation step is to include the `payload_type` in the message hash generation to ensure its value cannot be altered. The severity of this bug has been increased to High as it has the potential to result in unfinished transactions being processed by the Cairo code.

### Original Finding Content


### Impact

In `settlement.cairo::receive_cross_chain_msg` - the `payload_type` can be passed by the user, confusing offchain systems.

The `payload_type` parameter is only used to emit events so that the Chakra nodes can detect and process them.

There is no validation for it and given that it is used in an event to which off-chain systems listen to, the `payload_type` values will be displayed in the explorer, and there may be other extensions in the future, according to the sponsor.

This can lead to incorrect data being displayed and undefined behavior in the future.

### Proof of Concept

Let's see the code of `receive_cross_chain_msg`:

```
            fn receive_cross_chain_msg(
                ref self: ContractState,
                cross_chain_msg_id: u256,
                from_chain: felt252,
                to_chain: felt252,
                from_handler: u256,
                to_handler: ContractAddress,
                sign_type: u8,
                signatures: Array<(felt252, felt252, bool)>,
                payload: Array<u8>,
                payload_type: u8, <---
            ) -> bool {
                assert(to_chain == self.chain_name.read(), 'error to_chain');

                // verify signatures
                let mut message_hash: felt252 = LegacyHash::hash(from_chain, (cross_chain_msg_id, to_chain, from_handler, to_handler));
                let payload_span = payload.span();
                let mut i = 0;
                loop {
                    if i > payload_span.len()-1{
                        break;
                    }
                    message_hash = LegacyHash::hash(message_hash, * payload_span.at(i));
                    i += 1;
                };
                self.check_chakra_signatures(message_hash, signatures);

                // call handler receive_cross_chain_msg
                let handler = IHandlerDispatcher{contract_address: to_handler};
                let success = handler.receive_cross_chain_msg(cross_chain_msg_id, from_chain, to_chain, from_handler, to_handler , payload);

                let mut status = CrossChainMsgStatus::SUCCESS;
                if success{
                    status = CrossChainMsgStatus::SUCCESS;
                }else{
                    status = CrossChainMsgStatus::FAILED;
                }

                self.received_tx.write(cross_chain_msg_id, ReceivedTx{
                    tx_id:cross_chain_msg_id,
                    from_chain: from_chain,
                    from_handler: from_handler,
                    to_chain: to_chain,
                    to_handler: to_handler,
                    tx_status: status
                });

                // emit event
                self.emit(CrossChainHandleResult{
                    cross_chain_settlement_id: cross_chain_msg_id,
                    from_chain: to_chain,
                    from_handler: to_handler,
                    to_chain: from_chain,
                    to_handler: from_handler,
                    cross_chain_msg_status: status,
                    payload_type: payload_type <---
                });
                return true;
            }
```

You can see that the `payload_type` parameter is not used anywhere in the function except for the emission of the event.

So what could happen is:

*   a user or a bot sees the transaction being processed
*   calls the `receive_cross_chain_msg` function before the Chakra off-chain system with all the right parameters except for the `payload_type`
*   since the `payload_type` is not used in the message hash generation, the signatures verification and every other check passes successfully
*   the off-chain systems pick up wrong information from the event leading to corrupted information

### Recommended Mitigation Steps

Include the `payload_type` in the message hash generation thus making sure that it's value cannot be altered.

**[zvlwwj (Chakra) disputed and commented](https://github.com/code-423n4/2024-08-chakra-findings/issues/147#issuecomment-2363431109):**
 > Only validator can call this function.

**[0xsomeone (judge) increased severity to High and commented](https://github.com/code-423n4/2024-08-chakra-findings/issues/147#issuecomment-2434948388):**
 > The Warden has identified a mechanism via which the `payload_type` is not properly validated as having been signed by the Chakra team, permitting cross-chain messages to be received with a different payload type than the actual one.
> 
> I believe that a severity of high is appropriate as it should (in theory) result in a transaction being processed by the Cairo code but considered unfinished by the validator system.


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
| Finders | fyamf, klau5, 0xAsen |

### Source Links

- **Source**: https://code4rena.com/reports/2024-08-chakra
- **GitHub**: https://github.com/code-423n4/2024-08-chakra-findings/issues/147
- **Contest**: https://code4rena.com/reports/2024-08-chakra

### Keywords for Search

`vulnerability`

