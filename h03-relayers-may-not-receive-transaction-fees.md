---
# Core Classification
protocol: Optimism Smart Contracts Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 10723
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/optimism-smart-contracts-audit/
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
  - cdp
  - services
  - cross_chain
  - payments

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[H03] Relayers may not receive transaction fees

### Overview


This bug report is about the `OVM_ECDSAContractAccount` contract, which is part of the Ethereum Optimism project. The contract is supposed to pay transaction fees to relayers when the `execute` function is called. However, the bug report states that in two common cases, the fees are not correctly paid to the relayer accounts. 

The first case is when the `execute` function is called by the `OVM_ProxySequencerEntrypoint` predeployed contract. In this case, the fees are sent to the address of the `OVM_ProxySequencerEntrypoint` contract, which does not have the functionality to handle the received fees. 

The second case is when the `execute` function is called by whoever enqueues the transaction in the Canonical Transaction Chain. In this case, the `ovmCALLER` will return the default address for `ovmCALLER`, which is determined by the `DEFAULT_ADDRESS` constant address of the `OVM_ExecutionManager` contract. As a result, the fees will be sent to this address.

The bug report suggests ensuring that when transaction fees are paid from instances of the `OVM_ECDSAContractAccount` contract, fees are correctly transferred to the expected relayer addresses. The bug has been fixed in pull request #1029. Fees are now transferred to a designated Sequencer Fee Wallet.

### Original Finding Content

Transactions that go through the [`execute` function](https://github.com/ben-chain/contracts-v2/blob/a935e276f5620b40802b52721e3474232e458f72/contracts/optimistic-ethereum/OVM/accounts/OVM_ECDSAContractAccount.sol#L46) of an instance of the `OVM_ECDSAContractAccount` contract are [expected to pay transaction fees to relayers](https://github.com/ben-chain/contracts-v2/blob/a935e276f5620b40802b52721e3474232e458f72/contracts/optimistic-ethereum/OVM/accounts/OVM_ECDSAContractAccount.sol#L92-L101). The function assumes that whoever called it is a relayer, and simply [transfers the fee](https://github.com/ben-chain/contracts-v2/blob/a935e276f5620b40802b52721e3474232e458f72/contracts/optimistic-ethereum/OVM/accounts/OVM_ECDSAContractAccount.sol#L97-L99), paid in ovmETH.


However, there are two common cases in which the `execute` function can be called, and in neither of them the fee appears to be correctly paid to relayer accounts.


* For sequenced transactions, their entrypoint is set to the address of the [`OVM_ProxySequencerEntrypoint`](https://github.com/ben-chain/contracts-v2/blob/a935e276f5620b40802b52721e3474232e458f72/contracts/optimistic-ethereum/OVM/predeploys/OVM_ProxySequencerEntrypoint.sol) predeployed contract. Ultimately, it is this proxy who [calls the `execute` function](https://github.com/ben-chain/contracts-v2/blob/a935e276f5620b40802b52721e3474232e458f72/contracts/optimistic-ethereum/OVM/predeploys/OVM_SequencerEntrypoint.sol#L62-L70) of any `OVM_ECDSAContractAccount` contract. As a result, when the `execute` function [queries the `ovmCALLER`](https://github.com/ben-chain/contracts-v2/blob/a935e276f5620b40802b52721e3474232e458f72/contracts/optimistic-ethereum/OVM/accounts/OVM_ECDSAContractAccount.sol#L94), the address returned will be the address of the `OVM_ProxySequencerEntrypoint` contract, and fees will be sent to it. It is worth noting that neither this contract nor its associated implementation [`OVM_SequencerEntrypoint`](https://github.com/ben-chain/contracts-v2/blob/a935e276f5620b40802b52721e3474232e458f72/contracts/optimistic-ethereum/OVM/predeploys/OVM_SequencerEntrypoint.sol)have any kind of functionality to handle the received fees.
* For queued transactions, their entrypoint is set by whoever [enqueues](https://github.com/ben-chain/contracts-v2/blob/a935e276f5620b40802b52721e3474232e458f72/contracts/optimistic-ethereum/OVM/chain/OVM_CanonicalTransactionChain.sol#L256) the transaction in the Canonical Transaction Chain. If this entrypoint is set to an instance of the `OVM_ECDSAContractAccount` contract, when the transaction is run and the `execute` function is called, the [internal call to `ovmCALLER`](https://github.com/ben-chain/contracts-v2/blob/a935e276f5620b40802b52721e3474232e458f72/contracts/optimistic-ethereum/OVM/accounts/OVM_ECDSAContractAccount.sol#L94), will simply return the default address for `ovmCALLER`, which is determined by the [`DEFAULT_ADDRESS` constant address](https://github.com/ben-chain/contracts-v2/blob/a935e276f5620b40802b52721e3474232e458f72/contracts/optimistic-ethereum/OVM/execution/OVM_ExecutionManager.sol#L75) of the `OVM_ExecutionManager` contract. As a result, the fees will be sent to this address.


Consider ensuring that when transaction fees are paid from instances of the `OVM_ECDSAContractAccount` contract, fees are correctly transferred to the expected relayer addresses.


***Update:** Fixed in [pull request #1029](https://github.com/ethereum-optimism/optimism/pull/1029/commits/4a5bb28203dc6460b6e7ddaff3cd89e45a6b4d54). Fees are now transferred to a designated Sequencer Fee Wallet.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Optimism Smart Contracts Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/optimism-smart-contracts-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

