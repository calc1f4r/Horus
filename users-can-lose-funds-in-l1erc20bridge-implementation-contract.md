---
# Core Classification
protocol: zkSync Fee Model and Token Bridge Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 10321
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/zksync-fee-model-and-token-bridge-audit/
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
  - indexes

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Users Can Lose Funds in L1ERC20Bridge Implementation Contract

### Overview


This bug report is about the `L1ERC20Bridge` implementation contract. When the contract is constructed, a modifier called `reentrancyGuardInitializer` is executed and an immutable address is written to the bytecode that is deployed. This allows functions with the `nonReentrant` modifier to be called, such as the `deposit` function. However, many variables of the contract are not initialized, such as the `l2Bridge` variable, which holds the zero-address. This means that the `deposit` function would request an L2 transaction that attempts to finalize the withdrawal by calling the zero-address, triggering the non-reverting fallback function of the `EmptyContract`. This would result in the deposited tokens being locked and irrecoverable.

The bug report suggests implementing a stricter mechanism that prohibits direct calls to the contract if all or some of its variables were not properly initialized. Additionally, it suggests preventing the initialization of the implementation contract more directly, rather than relying on the implicit behavior of `reentrancyGuardInitializer`. The Matter Labs team acknowledged the issue, but did not believe it carried a significant security risk as the contract is intended to be used through a proxy.

### Original Finding Content

The `L1ERC20Bridge` is the implementation contract that is intended to be used with a proxy, so it is good practice to restrict how it can be invoked directly. When the contract is constructed, the `reentrancyGuardInitializer` modifier is executed and the immutable [`_mailbox` address is written](https://github.com/matter-labs/zksync-2-contracts/blob/9f3c6944e6320166edd96ef6586a9dd4548a27f2/ethereum/contracts/bridge/L1ERC20Bridge.sol#L58) to the bytecode that is deployed. During this invocation of `reentrancyGuardInitializer`, the reentrancy status is set to `_NOT_ENTERED`, which locks the `initialize` function from being called, but simultaneously allows functions with the `nonReentrant` modifier to be called.


Specifically, the `deposit` function of the implementation contract is callable. However, in the implementation contract itself, many variables are not initialized, such as the [`l2Bridge` variable](https://github.com/matter-labs/zksync-2-contracts/blob/9f3c6944e6320166edd96ef6586a9dd4548a27f2/ethereum/contracts/bridge/L1ERC20Bridge.sol#L126), so it holds the zero-address. Therefore, the `deposit` function would request an L2 transaction that attempts to finalize the withdrawal by calling the zero-address, thereby triggering the non-reverting fallback function of the [`EmptyContract`](https://github.com/matter-labs/system-contracts/blob/191246a878f1493a5ed5f0fa6d79af4ce3e7eb8f/contracts/EmptyContract.sol). Since this L2 call does not fail, the deposited tokens are locked and irrecoverable, as a call to [`claimFailedDeposit`](https://github.com/matter-labs/zksync-2-contracts/blob/9f3c6944e6320166edd96ef6586a9dd4548a27f2/ethereum/contracts/bridge/L1ERC20Bridge.sol#L185) cannot be proven.


Consider implementing a stricter mechanism that prohibits direct calls to the contract if all or some of its variables were not properly initialized. In addition, consider preventing the initialization of the implementation contract more directly, rather than relying on the implicit behavior of `reentrancyGuardInitializer`, which lacks visibility.


***Update:** Acknowledged, not resolved. The Matter Labs team stated:*



> *While we appreciate your insights and suggestions, we do not believe the issue carries a significant security risk. As the contract is intended to be used through a proxy, direct calls to the implementation contract are not recommended. Users could also call any other scam contract.*
> 
>

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | zkSync Fee Model and Token Bridge Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/zksync-fee-model-and-token-bridge-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

