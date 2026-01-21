---
# Core Classification
protocol: Celo Contracts Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11097
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/celo-contracts-audit/
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
  - yield
  - launchpad
  - liquidity_manager

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[M01] Deployment can be frontrun

### Overview


This bug report is about the MetaTransactionWalletDeployer contract, which is part of the Celo monorepo. This contract has a `deploy` function which allows any address saved in the `canDeploy` mapping to fronturun and create a new MetaTransactionWalletProxy instance. This is a security risk because it allows any address to set and initialize an implementation of a malicious wallet, resulting in the execution of a `delegatecall` from the MetaTransactionWalletProxy context. This could lead to dynamically loading code from a malicious wallet implementation at runtime.

To fix the issue, the `deploy` function was modified to use an implementation address saved in storage by the owner of the MetaTransactionWalletDeployer contract. This was done in PR#5683, which greatly simplified the MetaTransationWalletDeployer contract. Now the deployment of MetaTransactionWalletProxy proxy contracts is permissionless and does not depend on the deployer contract’s state.

### Original Finding Content

The [`deploy` function](https://github.com/celo-org/celo-monorepo/blob/af49272ef57a077ee6e704aad76d506c039798d3/packages/protocol/contracts/common/MetaTransactionWalletDeployer.sol#L86-L99) of the [`MetaTransactionWalletDeployer` contract](https://github.com/celo-org/celo-monorepo/blob/af49272ef57a077ee6e704aad76d506c039798d3/packages/protocol/contracts/common/MetaTransactionWalletDeployer.sol#L13) is fronturunnable by any address saved in the [`canDeploy` mapping](https://github.com/celo-org/celo-monorepo/blob/af49272ef57a077ee6e704aad76d506c039798d3/packages/protocol/contracts/common/MetaTransactionWalletDeployer.sol#L23). By analyzing the mempool, allowed addresses will be able to send a transaction that will create a new `MetaTransactionWalletProxy` instance and assign it to the same owner as the original transaction. 


This has two different outcomes:


* The `owner` address can no longer be set as the owner of another address due to [this `require` statement](https://github.com/celo-org/celo-monorepo/blob/af49272ef57a077ee6e704aad76d506c039798d3/packages/protocol/contracts/common/MetaTransactionWalletDeployer.sol#L90)
* The attacker can call the proxy’s [`_setAndInitializeImplementation` function](https://github.com/celo-org/celo-monorepo/blob/af49272ef57a077ee6e704aad76d506c039798d3/packages/protocol/contracts/common/Proxy.sol#L101-L111)  with any calldata they want by using the [`initCallData` parameter](https://github.com/celo-org/celo-monorepo/blob/af49272ef57a077ee6e704aad76d506c039798d3/packages/protocol/contracts/common/MetaTransactionWalletDeployer.sol#L93), which will lead to the execution of a [`delegatecall`](https://github.com/celo-org/celo-monorepo/blob/af49272ef57a077ee6e704aad76d506c039798d3/packages/protocol/contracts/common/Proxy.sol#L109) from the `MetaTransactionWalletProxy` context, resulting in the possibility of dynamically loading code from a malicious wallet implementation at runtime.


We can conclude that using a MetaTransactionWallet deployed by a malicious third party via the `MetaTransactionWalletDeployer` is not safe.


Consider modifying the `deploy` function to use an implementation address saved in storage by the owner of the `MetaTransactionWalletDeployer` contract and not using this value from untrusted sources such as the parameters of the function.


**Update**: *Fixed in [PR#5683](https://github.com/celo-org/celo-monorepo/pull/5683). The `MetaTransationWalletDeployer` contract has been greatly simplified. Now the deployment of `MetaTransactionWalletProxy` proxy contracts is permissionless and does not depend on the deployer contract’s state.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Celo Contracts Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/celo-contracts-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

