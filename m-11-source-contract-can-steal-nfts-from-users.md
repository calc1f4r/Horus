---
# Core Classification
protocol: Holograph
chain: everychain
category: access_control
vulnerability_type: access_control

# Attack Vector Details
attack_type: access_control
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5604
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-10-holograph-contest
source_link: https://code4rena.com/reports/2022-10-holograph
github_link: https://github.com/code-423n4/2022-10-holograph-findings/issues/290

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 3

# Context Tags
tags:
  - access_control

protocol_categories:
  - dexes
  - bridge
  - services
  - launchpad
  - nft_marketplace

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Jeiwan
  - __141345__  m9800
---

## Vulnerability Title

[M-11] Source contract can steal NFTs from users

### Overview


This bug report is about a vulnerability in the HolographERC721 contract, which is part of the 2022-10-holograph project. The vulnerability allows a source contract to burn and transfer NFTs of users without their permission. This could put users at risk of being robbed by the source contract owner or a hacker who hacked the source contract owner's key. 

The issue was identified through manual review. It is recommended that the `sourceBurn` and `sourceTransfer` functions of `HolographERC721` be removed and user approval be required to transfer or burn their tokens. This can be done by having the source contract call `burn` and `safeTransferFrom` instead of `sourceBurn` and `sourceTransfer`.

### Original Finding Content


A source contract can burn and transfer NFTs of users without their permission.

### Proof of Concept

Every Holographed ERC721 collection is paired with a source contract, which is the user created contract that's extended by the Holographed ERC721 contract ([HolographFactory.sol#L234-L246](https://github.com/code-423n4/2022-10-holograph/blob/f8c2eae866280a1acfdc8a8352401ed031be1373/contracts/HolographFactory.sol#L234-L246)). A source contract, however, has excessive privileges in the Holographed ERC721. Specifically, it can burn and transfer users' NFTs without their approval ([HolographERC721.sol#L500](https://github.com/code-423n4/2022-10-holograph/blob/f8c2eae866280a1acfdc8a8352401ed031be1373/contracts/enforcer/HolographERC721.sol#L500), [HolographERC721.sol#L577](https://github.com/code-423n4/2022-10-holograph/blob/f8c2eae866280a1acfdc8a8352401ed031be1373/contracts/enforcer/HolographERC721.sol#L577)):

```solidity
function sourceBurn(uint256 tokenId) external onlySource {
  address wallet = _tokenOwner[tokenId];
  _burn(wallet, tokenId);
}

function sourceTransfer(address to, uint256 tokenId) external onlySource {
  address wallet = _tokenOwner[tokenId];
  _transferFrom(wallet, to, tokenId);
}
```

While this might be desirable for extensibility and flexibility, this puts users at the risk of being robbed by the source contract owner or a hacker who hacked the source contract owner's key.

### Recommended Mitigation Steps

Consider removing the `sourceBurn` and `sourceTransfer` functions of `HolographERC721` and requiring user approval to transfer or burn their tokens (`burn` and `safeTransferFrom` can be called by a source contract instead of `sourceBurn` and `sourceTransfer`).

**[gzeon (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2022-10-holograph-findings/issues/290#issuecomment-1297281122):**
 > Also [`#403`](https://github.com/code-423n4/2022-10-holograph-findings/issues/403) brought up that source contract can also steal NFTs from burn address.

**[alexanderattar (Holograph) confirmed and commented](https://github.com/code-423n4/2022-10-holograph-findings/issues/290#issuecomment-1306692944):**
 > Need to add a `require(!_burnedTokens[tokenId], "ERC721: token has been burned");` check to sourceTransfer function

**[alexanderattar (Holograph) resolved](https://github.com/code-423n4/2022-10-holograph-findings/issues/290#event-7817138955):**
 > [Feature/HOLO-604: implementing critical issue fixes](https://github.com/holographxyz/holograph-protocol/pull/84)



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | Holograph |
| Report Date | N/A |
| Finders | Jeiwan, __141345__  m9800 |

### Source Links

- **Source**: https://code4rena.com/reports/2022-10-holograph
- **GitHub**: https://github.com/code-423n4/2022-10-holograph-findings/issues/290
- **Contest**: https://code4rena.com/contests/2022-10-holograph-contest

### Keywords for Search

`Access Control`

