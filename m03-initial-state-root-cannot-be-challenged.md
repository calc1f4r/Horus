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
solodit_id: 10728
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/optimism-smart-contracts-audit/
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

[M03] Initial state root cannot be challenged

### Overview


The OVM_FraudVerifier contract contains an `initializeFraudVerification` function which is intended to ensure that the provided pre-state root and transaction correspond to each other. This is done by requiring the element at index N in the State Commitment Chain to be the post-state root of the transaction at index N in the Canonical Transaction Chain. 

However, since fraud proofs require the pre-state to exist in the State Commitment Chain, it is impossible to prove fraud against the first state root in the State Commitment Chain. This effectively introduces a trust assumption, where the entity that provides the first state root can decide on the OVM’s genesis state. Furthermore, since state roots are deleted in batches, if the genesis state root shares the same batch with other state roots, and one of them is successfully proven fraudulent, the entire batch of state roots (including the genesis state root) will be removed. 

The Optimism team has acknowledged this issue, but has no plans to fix it. They consider the initial state root to be analogous to Ethereum’s genesis block, and users must accept it in the same way that they accept the state transition rules for any blockchain.

### Original Finding Content

The [`initializeFraudVerification` function](https://github.com/ben-chain/contracts-v2/blob/a935e276f5620b40802b52721e3474232e458f72/contracts/optimistic-ethereum/OVM/verification/OVM_FraudVerifier.sol#L92) of the `OVM_FraudVerifier` contract intends to ensure that the provided [pre-state root](https://github.com/ben-chain/contracts-v2/blob/a935e276f5620b40802b52721e3474232e458f72/contracts/optimistic-ethereum/OVM/verification/OVM_FraudVerifier.sol#L94-L95) and [transaction](https://github.com/ben-chain/contracts-v2/blob/a935e276f5620b40802b52721e3474232e458f72/contracts/optimistic-ethereum/OVM/verification/OVM_FraudVerifier.sol#L98-L99) correspond to each other. In other words, that the referenced transaction was executed against the provided pre-state. This is implemented in [this `require` statement](https://github.com/ben-chain/contracts-v2/blob/a935e276f5620b40802b52721e3474232e458f72/contracts/optimistic-ethereum/OVM/verification/OVM_FraudVerifier.sol#L133-L136), where the offset suggests that the element at index N in the State Commitment Chain is the post-state root of the transaction at index N in the Canonical Transaction Chain. This is consistent with the fact that the size of the State Commitment Chain is [bounded by the total number of transactions in the Canonical Transaction Chain](https://github.com/ben-chain/contracts-v2/blob/a935e276f5620b40802b52721e3474232e458f72/contracts/optimistic-ethereum/OVM/chain/OVM_StateCommitmentChain.sol#L151-L154).


However, since fraud proofs [require the pre-state](https://github.com/ben-chain/contracts-v2/blob/a935e276f5620b40802b52721e3474232e458f72/contracts/optimistic-ethereum/OVM/verification/OVM_FraudVerifier.sol#L94) to exist in the State Commitment Chain, it is impossible to prove fraud against the first state root in the State Commitment Chain. As a result, the first transaction in the Canonical Transaction Chain can be considered meaningless, and the first state root in the State Commitment Chain will remain unchallenged. This effectively introduces a remarkable trust assumption, where the entity that provides the first state root can decide on the OVM’s genesis state.


Moreover, since state roots are [deleted in batches](https://github.com/ben-chain/contracts-v2/blob/a935e276f5620b40802b52721e3474232e458f72/contracts/optimistic-ethereum/OVM/verification/OVM_FraudVerifier.sol#L282) instead of individually, if the genesis state root shares the same batch with other state roots, and one of them is successfully proven fraudulent, the entire batch of state roots (including the genesis state root) will be removed, and therefore the next state root to be appended to the State Commitment Chain will become the new “genesis” state.


Consider thoroughly documenting the deployment procedure, including the fact that the first transaction is unused, and how the Optimism team intends to ensure the first state root will be the intended genesis state. Alternatively, consider introducing a mechanism to challenge the first post-state root against a known genesis state.


***Update**: Acknowledged, but won’t fix. Optimism’s statement for this issue:*



> 
> The initial state root is analogous to Ethereum’s genesis block. It cannot be the result of a fraudulent transaction, users of an Optimistic Ethereum deployment must accept the initial state root in the same way that they accept the state transition rules for any blockchain.
> 
> 
>

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

