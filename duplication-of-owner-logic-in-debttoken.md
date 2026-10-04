---
# Core Classification
protocol: Dharma Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11913
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/dharma-audit-2f1386455688/
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

Duplication of owner logic in DebtToken

### Overview


A bug was reported in the code of the DebtToken contract, which extends the NonFungibleToken contract. The bug was that DebtToken was redefining the setTokenOwner and ownerO internal functions of NonFungibleToken, which modifies the DebtRegistry instead of the NonFungibleToken’s own tracking of ownership. This could lead to some obscure hard-to-spot issues.

The suggested fix was to remove the redefinition of the _ownerOf function and to modify the _setTokenOwner function so that it runs super._setTokenOwner() in addition to calls on the registry. This would keep the registry in sync with the token’s tracking of ownership, but by intercepting changes of ownership instead of replacing that part of the token’s implementation. This bug was fixed in the 7a618cf commit.

### Original Finding Content

[`DebtToken`](https://github.com/dharmaprotocol/charta/blob/b110959477cf37375bf7e9344d40eb85219c8575/contracts/DebtToken.sol) extends [`NonFungibleToken`](https://github.com/dharmaprotocol/NonFungibleToken/blob/master/contracts/NonFungibleToken.sol) and redefines the latter’s [`setTokenOwne`](https://github.com/dharmaprotocol/charta/blob/b110959477cf37375bf7e9344d40eb85219c8575/contracts/DebtToken.sol#L143) and [`ownerO`](https://github.com/dharmaprotocol/charta/blob/b110959477cf37375bf7e9344d40eb85219c8575/contracts/DebtToken.sol#L155) internal functions, so that they modify the [`DebtRegistry`](https://github.com/dharmaprotocol/charta/blob/b110959477cf37375bf7e9344d40eb85219c8575/contracts/DebtRegistry.sol) instead of the NFT’s own tracking of ownership. This seems to result in coherent behavior, but we think it’s an unnecessary meddling with `NonFungibleToken`’s semantics, and could eventually cause some obscure hard-to-spot issues.


We would suggest to remove the redefinition of `_ownerOf`, and to modify `_setTokenOwner` so that it runs `super._setTokenOwner()` additionally to the calls on the registry. In this way the registry is kept in sync with the token’s tracking of ownership, but merely by intercepting changes of ownership, instead of entirely replacing that part of the token’s implementation.


***Update:** Fixed in [`7a618cf`](https://github.com/dharmaprotocol/charta/commit/7a618cf16e47a0829e0efe73092e1b5be7964f11).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Dharma Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/dharma-audit-2f1386455688/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

