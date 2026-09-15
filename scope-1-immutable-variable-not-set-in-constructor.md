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
solodit_id: 41659
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/decentralized-governance-audit
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Scope 1 - Immutable Variable Not Set in Constructor

### Overview


The report discusses a bug in the Solidity programming language version 0.8.21, where immutable variables do not need to be explicitly assigned a value in the constructor. This can lead to contracts being deployed with unintended default values. The bug specifically affects the `ProtocolUpgradeHandler` contract, where an immutable variable called `ZKSYNC_ERA` was not initialized in the constructor. This makes the contract unusable as it is dependent on this variable for processing protocol upgrades. The solution is to set the correct address during contract construction, and the bug has been resolved in a recent commit.

### Original Finding Content

As of Solidity [0\.8\.21](https://github.com/ethereum/solidity/releases/tag/v0.8.21), immutable variables do not need to be explicitly assigned a value in the constructor of the contract. This could lead to cases where contracts are deployed with immutable variables unintentionally set to their default values.


Within the [`ProtocolUpgradeHandler` contract](https://github.com/ZKsync-Association/zk-governance/blob/a3e361d00d8100ed1724b079ea7509f7f13e3d94/ProtocolUpgradeHandler.sol), the immutable state variable [`ZKSYNC_ERA`](https://github.com/ZKsync-Association/zk-governance/blob/a3e361d00d8100ed1724b079ea7509f7f13e3d94/l1-contracts/src/ProtocolUpgradeHandler.sol#L53) was not initialized in the constructor. This basically makes the whole contract inoperable as no protocol upgrades can be processed through the [`startUpgrade` function](https://github.com/ZKsync-Association/zk-governance/blob/a3e361d00d8100ed1724b079ea7509f7f13e3d94/l1-contracts/src/ProtocolUpgradeHandler.sol#L111), which is dependent on this address.


Consider setting the correct address during contract construction.


***Update:** Resolved at commit [348a26a](https://github.com/ZKsync-Association/zk-governance/commits/348a26a243babd4d51ae9547b69b6da9037c613a).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

