---
# Core Classification
protocol: Escher
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6358
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-12-escher-contest
source_link: https://code4rena.com/reports/2022-12-escher
github_link: https://github.com/code-423n4/2022-12-escher-findings/issues/68

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - services
  - launchpad
  - rwa

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - HollaDieWaldfee
  - 0xNazgul
  - cccz
  - hansfriese
  - obront
---

## Vulnerability Title

[M-01] Escher721 contract does not have setTokenRoyalty function

### Overview


This bug report is about a vulnerability in the Escher721 contract. The issue is that the "SALES PATTERNS" section of the code4rena page of the contest states that an artist should be able to call the `setTokenRoyalty` function on the `Escher721` contract. However, this function does not exist. There is a `_setTokenRoyalty` in `ERC2981.sol` from openzeppelin, but it is `internal` and cannot be called by the artist. Therefore, an artist cannot set a royalty individually for a token as is stated in the documentation.

Proof of concept was attempted by trying to call `setTokenRoyalty` from inside `Escher721.t.sol` with a test, but it did not compile because the function does not exist. The recommended mitigation step is to add the following function to the `Escher721` contract to expose the internal `_setTokenRoyalty` function to the artist:

```solidity
function setTokenRoyalty(
    uint256 tokenId,
    address receiver,
    uint96 feeNumerator
) public onlyRole(DEFAULT_ADMIN_ROLE) {
    _setTokenRoyalty(tokenId,receiver,feeNumerator);
}
```

This bug report is about a vulnerability in the Escher721 contract, where an artist cannot set a royalty individually for a token as is stated in the documentation. Proof of concept was attempted, but it did not compile because the function does not exist. The recommended mitigation step is to add a function to the `Escher721` contract to expose the internal `_setTokenRoyalty` function to the artist.

### Original Finding Content


On the Code4rena page of this contest there is a "SALES PATTERNS" section that describes the flow of how to use Sales:

<https://code4rena.com/contests/2022-12-escher-contest>

It contains this statement:

> If the artist would like sales and royalties to go somewhere other than the default royalty receiver, they\
> must call setTokenRoyalty with the following variables

So an artist should be able to call the `setTokenRoyalty` function on the `Escher721` contract.

However this function cannot be called. It does not exist. There exists a `_setTokenRoyalty` in `ERC2981.sol` from OpenZeppelin. This function however is `internal` (<https://github.com/OpenZeppelin/openzeppelin-contracts/blob/3d7a93876a2e5e1d7fe29b5a0e96e222afdc4cfa/contracts/token/common/ERC2981.sol#L94>).

So there is no `setTokenRoyalty` function that can be called by the artist. So an artist cannot set a royalty individually for a token as is stated in the documentation.

### Proof of Concept

I tried calling `setTokenRoyalty` from inside `Escher721.t.sol` with the following test:

```solidity
function test_setDefaultRoyalty() public {
    edition.setTokenRoyalty(1,address(this), 5);
}
```

This won't even compile because the `setTokenRoyalty` function does not exist.

### Tools Used

VS Code

### Recommended Mitigation Steps

In order to expose the internal `_setTokenRoyalty` function to the artist, add the following function to the `Escher721` contract:

```solidity
function setTokenRoyalty(
    uint256 tokenId,
    address receiver,
    uint96 feeNumerato r
) public onlyRole(DEFAULT_ADMIN_ROLE) {
    _setTokenRoyalty(tokenId,receiver,feeNumerator);
}
```

**[mehtaculous (Escher) disputed](https://github.com/code-423n4/2022-12-escher-findings/issues/181)** 

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Escher |
| Report Date | N/A |
| Finders | HollaDieWaldfee, 0xNazgul, cccz, hansfriese, obront |

### Source Links

- **Source**: https://code4rena.com/reports/2022-12-escher
- **GitHub**: https://github.com/code-423n4/2022-12-escher-findings/issues/68
- **Contest**: https://code4rena.com/contests/2022-12-escher-contest

### Keywords for Search

`vulnerability`

