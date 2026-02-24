---
# Core Classification
protocol: Sablier
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54678
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/5febedab-9e34-4943-bdd3-891559384740
source_link: https://cdn.cantina.xyz/reports/cantina_sablier_jul2023.pdf
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
finders_count: 2
finders:
  - Zach Obront
  - RustyRabbit
---

## Vulnerability Title

Plugins and permissions storage variables are unprotected 

### Overview


The bug report discusses an issue with the storage of important access control features in the PRBProxy contract. These features, such as installed plugins and permissions given to envoys, are stored in mappings within the contract. However, this can lead to accidental or malicious manipulation of the mappings. The recommendation is to move these variables to the PRBProxyRegistry or use a custom namespace to protect against storage collisions. The issue has been fixed in the Sablier and Cantina projects.

### Original Finding Content

## Context
- [/prb-proxy/src/abstracts/PRBProxyStorage.sol#L17-L20](https://github.com/prb-proxy/src/abstracts/PRBProxyStorage.sol#L17-L20)
- [/prb-proxy/blob/src/PRBProxy.sol#L53](https://github.com/prb-proxy/blob/src/PRBProxy.sol#L53)
- [/prb-proxy/src/PRBProxy.sol#L89](https://github.com/prb-proxy/src/PRBProxy.sol#L89)
- [/prb-proxy/src/PRBProxy.sol#L148](https://github.com/prb-proxy/src/PRBProxy.sol#L148)

## Description
The installed plugins and the permissions given to the envoys are stored in mappings defined in the `PRBProxyStorage` contract, which is inherited by the proxy. As such, they are stored in the proxy. Any target or plugin contract is supposed to inherit the same `PRBProxyStorage` contract to avoid storage slot collisions.

```solidity
abstract contract PRBProxyStorage is IPRBProxyStorage {
    address public override owner;
    uint256 public override minGasReserve;
    mapping(bytes4 method => IPRBProxyPlugin plugin) public plugins;
    mapping(address envoy => mapping(address target => bool permission)) public permissions;
}
```

However, this can lead to accidental or malicious manipulation of the mappings that represent important access control features of the proxy. Some examples of possible scenarios are:
- A faulty target or plugin contract accidentally overwriting these storage slots.
- A malicious target or plugin contract assigning the attacker as envoy for other malicious contracts.
- A malicious envoy using faulty target contracts to try and manipulate the mappings to gain unauthorized control.

This problem also applies to the `owner` and `minGasReserve` storage variables, but they have additional impacts which are addressed in other findings.

## Recommendation
It is best to not store these variables inside the proxy contract. They are better stored in the `PRBProxyRegistry` based on the proxy address or, as discussed in the "Permission and plugins are not reset on proxy ownership transfer" finding, based on the owner address. Alternatively, to at least protect against accidental storage collisions, use EIP1967-type storage with a custom namespace.

## Sablier
Applied your recommendation here by moving both plugins and permissions to the registry, where only the owner is allowed to update them:
- PR 120.

Basically, the proxy contract itself doesn't have any storage layout anymore now, since we've also removed `transferOwnership` and `minGasReserve`:
- PR 119.
- PR 114.

## Cantina
Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Sablier |
| Report Date | N/A |
| Finders | Zach Obront, RustyRabbit |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_sablier_jul2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/5febedab-9e34-4943-bdd3-891559384740

### Keywords for Search

`vulnerability`

