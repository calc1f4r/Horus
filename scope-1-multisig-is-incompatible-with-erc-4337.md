---
# Core Classification
protocol: Decentralized Governance Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41660
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/decentralized-governance-audit
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

Scope 1 - Multisig Is Incompatible with ERC-4337

### Overview


The report discusses a bug in the EIP-4337 standard, which allows smart contracts to behave like user accounts. The bug affects the `Multisig` contract, which uses the OpenZeppelin `ECDSA` library to verify signatures. However, this library is incompatible with smart contract accounts. To fix this, the report suggests using the `SignatureChecker` library instead. The bug has been resolved in a recent commit, but the team suggests using an `EnumerableSet` for the multisig members to check signers against the members and provide a meaningful error message. The team also notes that they prefer to keep dependencies to a minimum.

### Original Finding Content

EIP\-4337 is a standard that allows smart contracts to behave like user accounts, thereby extending the user account landscape of Externally Owned Accounts (EOA) with smart contract accounts.


To verify the signatures, the `Multisig` contract [uses the OpenZeppelin `ECDSA` library](https://github.com/ZKsync-Association/zk-governance/blob/a3e361d00d8100ed1724b079ea7509f7f13e3d94/l1-contracts/src/Multisig.sol#L45) that makes a call to the `ecrecover` precompile contract, which is incompatible with smart contract accounts.


Hence, to enable [EIP\-1271](https://eips.ethereum.org/EIPS/eip-1271) smart contract account signature checks, consider using the [`SignatureChecker` library](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/v5.0.2/contracts/utils/cryptography/SignatureChecker.sol) instead.


***Update:** Resolved at commit [fef52f6](https://github.com/ZKsync-Association/zk-governance/commits/fef52f6ccf952dbf97eab5a2ccce2c3d3e0aad5c). Consider using an [`EnumerableSet`](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/v5.0.2/contracts/utils/structs/EnumerableSet.sol#L231) for the multisig members, to check the signers against the members and give a meaningful revert message otherwise. The ZKsync Association team stated:*



> *The proposal makes sense to me, but I am in favour of keeping dependency list as small as possible, especially when there is no strong reasons to add new one. I will acknowledge this issue for now.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Decentralized Governance Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/decentralized-governance-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

