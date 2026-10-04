---
# Core Classification
protocol: Notional
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25543
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-08-notional
source_link: https://code4rena.com/reports/2021-08-notional
github_link: https://github.com/code-423n4/2021-08-notional-findings/issues/7

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
  - bridge
  - cdp
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[H-08] DOS by Frontrunning NoteERC20 `initialize()` Function

### Overview


The `scripts/` folder of the Notional team outlines a number of deployment scripts used by the Notional team. These scripts involve the ERC1967 upgradeable proxy standard, which involves deploying an implementation contract and a proxy contract which uses the implementation contract as its logic. 

When users make calls to the proxy contract, the proxy contract will delegate call to the underlying implementation contract. `NoteERC20.sol` and `Router.sol` both implement an `initialize()` function which is used to replace the role of the `constructor()` when deploying proxy contracts. It is important that these proxy contracts are deployed and initialized in the same transaction to avoid any malicious front-running.

However, `scripts/deployment.py` does not follow this pattern when deploying `NoteERC20.sol`'s proxy contract. As a result, a malicious attacker could monitor the Ethereum blockchain for bytecode that matches the `NoteERC20` contract and front-run the `initialize()` transaction to gain ownership of the contract. This could lead to unrecoverable gas expenses and a Denial Of Service (DOS) type of attack, effectively preventing Notional's contract deployment.

To fix this issue, it is suggested that the `NoteERC20.sol` proxy contract is deployed and initialized in the same transaction, or that the `initialize()` function is callable only by the deployer of the `NoteERC20.sol` contract. This could be set in the proxy contracts `constructor()`. Jeffywu (Notional) has confirmed this issue.

### Original Finding Content

_Submitted by leastwood_

The `scripts/` folder outlines a number of deployment scripts used by the Notional team. Some of the contracts deployed utilize the ERC1967 upgradeable proxy standard. This standard involves first deploying an implementation contract and later a proxy contract which uses the implementation contract as its logic.

When users make calls to the proxy contract, the proxy contract will delegate call to the underlying implementation contract. `NoteERC20.sol` and `Router.sol` both implement an `initialize()` function which aims to replace the role of the `constructor()` when deploying proxy contracts. It is important that these proxy contracts are deployed and initialized in the same transaction to avoid any malicious front-running.

However, `scripts/deployment.py` does not follow this pattern when deploying `NoteERC20.sol`'s proxy contract. As a result, a malicious attacker could monitor the Ethereum blockchain for bytecode that matches the `NoteERC20` contract and front-run the `initialize()` transaction to gain ownership of the contract. This can be repeated as a Denial Of Service (DOS) type of attack, effectively preventing Notional's contract deployment, leading to unrecoverable gas expenses. See [`deployment.py` L44-L60](https://github.com/code-423n4/2021-08-notional/blob/main/scripts/deployment.py#L44-L60), and [`deploy_governance.py` L71-L105](https://github.com/code-423n4/2021-08-notional/blob/main/scripts/mainnet/deploy_governance.py#L71-L105).

As the `GovernanceAlpha.sol` and `NoteERC20.sol` are co-dependent contracts in terms of deployment, it won't be possible to deploy the governance contract before deploying and initializing the token contract. Therefore, it would be worthwhile to ensure the `NoteERC20.sol` proxy contract is deployed and initialized in the same transaction, or ensure the `initialize()` function is callable only by the deployer of the `NoteERC20.sol` contract. This could be set in the proxy contracts `constructor()`.

**[jeffywu (Notional) confirmed](https://github.com/code-423n4/2021-08-notional-findings/issues/7)**



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Notional |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-08-notional
- **GitHub**: https://github.com/code-423n4/2021-08-notional-findings/issues/7
- **Contest**: https://code4rena.com/reports/2021-08-notional

### Keywords for Search

`vulnerability`

