---
# Core Classification
protocol: Taiko Protocol Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34328
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/taiko-protocol-audit
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

Cross-Chain Owner Cannot Call Privileged Functions - Phase 2

### Overview


The CrossChainOwned contract allows for an owner on a different chain to execute privileged actions on a child contract. However, due to a bug, it is currently impossible for the cross-chain owner to call functions protected by onlyOwner on the TaikoL2 contract. This is because the contract calls itself with an external call, resulting in the msg.sender being address(this) instead of the cross-chain owner. The team has resolved this issue by removing the Cross-Chain owner and implementing a new DelegateOwner which will have the same role on L2 contracts.

### Original Finding Content

The [`CrossChainOwned`](https://github.com/taikoxyz/taiko-mono/blob/b47fc34cb0e7fe9b7ebd9416b3051a067483b860/packages/protocol/contracts/L2/CrossChainOwned.sol#L14) abstract contract can be inherited to allow an owner on a different chain to execute privileged actions on the child contract. For example, the [`TaikoL2`](https://github.com/taikoxyz/taiko-mono/blob/b47fc34cb0e7fe9b7ebd9416b3051a067483b860/packages/protocol/contracts/L2/TaikoL2.sol#L21) contract inherits from `CrossChainOwned`. When a `CrossChainOwned` contract is called by the bridge, the cross-chain sender and the original chain are [validated to correspond to the cross-chain owner](https://github.com/taikoxyz/taiko-mono/blob/b47fc34cb0e7fe9b7ebd9416b3051a067483b860/packages/protocol/contracts/L2/CrossChainOwned.sol#L45-L48), after which an [external call](https://github.com/taikoxyz/taiko-mono/blob/b47fc34cb0e7fe9b7ebd9416b3051a067483b860/packages/protocol/contracts/L2/CrossChainOwned.sol#L50) is made to itself.


However, it is impossible for a cross-chain owner to use this mechanism to call functions protected by [`onlyOwner`](https://github.com/taikoxyz/taiko-mono/blob/b47fc34cb0e7fe9b7ebd9416b3051a067483b860/packages/protocol/contracts/L2/TaikoL2EIP1559Configurable.sol#L31) on `TaikoL2`. This is because the `_owner` variable of the contract has to match the [address of the cross-chain owner](https://github.com/taikoxyz/taiko-mono/blob/b47fc34cb0e7fe9b7ebd9416b3051a067483b860/packages/protocol/contracts/L2/CrossChainOwned.sol#L46C47-L46C66), but the cross-chain owner calling the contract results in the contract calling itself with an [external call](https://github.com/taikoxyz/taiko-mono/blob/b47fc34cb0e7fe9b7ebd9416b3051a067483b860/packages/protocol/contracts/L2/CrossChainOwned.sol#L50). This means that calls to any function protected by `onlyOwner` would revert as the `msg.sender` would be `address(this)` and not the cross-chain owner. This makes it impossible for the cross-chain owner to call functions protected by `onlyOwner` on the `TaikoL2` contract, such as [`withdraw`](https://github.com/taikoxyz/taiko-mono/blob/b47fc34cb0e7fe9b7ebd9416b3051a067483b860/packages/protocol/contracts/L2/TaikoL2.sol#L168) or [`setConfigAndExcess`](https://github.com/taikoxyz/taiko-mono/blob/b47fc34cb0e7fe9b7ebd9416b3051a067483b860/packages/protocol/contracts/L2/TaikoL2EIP1559Configurable.sol#L31).


Consider allowing the cross-chain owner to call privileged functions.


***Update:** Resolved at commit [37fa853](https://github.com/taikoxyz/taiko-mono/commit/37fa853bd4d560a8ef0301437303f35f0d0c4c92#diff-7e648bef3a82cd6a4c5cf63b69fcff267ee72356cb05f42ca4acccc5e3026c5c). The Taiko team stated:*



> *Cross-Chain owner got removed (or reworked) and the new is "DelegateOwner", which will have the same role, to act like the owner essentially, for contracts deployed on L2.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Taiko Protocol Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/taiko-protocol-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

