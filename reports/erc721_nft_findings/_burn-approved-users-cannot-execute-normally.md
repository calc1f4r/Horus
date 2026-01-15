---
# Core Classification
protocol: ZeroLend
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54324
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/6d383aaf-8554-4a06-a224-86189f81f531
source_link: https://cdn.cantina.xyz/reports/cantina_competition_zerolend_jan2024.pdf
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
finders_count: 17
finders:
  - Ch301
  - 8olidity
  - pauleth
  - Naveen Kumar J - 1nc0gn170
  - jovi.eth
---

## Vulnerability Title

_burn() approved users cannot execute normally 

### Overview


This report discusses a bug found in the code of ZeroLocker.sol, specifically in lines 1118 to 1120. The bug affects the functionality of granting permission to other users to operate NFTs through the `approve()` or `setApprovalForAll()` methods. The bug is in the `_burn()` function, which is used to remove a token from a user's collection. The bug causes only the owner of the token to be able to execute the `withdraw()` and `merge()` methods, even if other users have been granted permission. This can impact the user experience as it limits the ability of other users to interact with the NFTs. The recommendation is to make two changes to the code in order to fix the bug and allow other users with permission to execute the methods. 

### Original Finding Content

## ZeroLocker.sol Review

## Context
**File:** ZeroLocker.sol  
**Lines:** L1118-L1120

## Description
In `ZeroLocker.sol`, we can grant other users permission to operate NFTs through `approve()` or `setApprovalForAll()`. However, the current implementation of `_burn()` is incorrect, resulting in only the owner being able to execute `withdraw()` and `merge()`.

```solidity
function _burn(uint256 _tokenId) internal {
    require(
        _isApprovedOrOwner(msg.sender, _tokenId),
        "caller is not owner nor approved"
    );
    address owner = _ownerOf(_tokenId);
    // Clear approval
    _approve(address(0), _tokenId);
    // Remove token
    _removeTokenFrom(msg.sender, _tokenId);
    emit Transfer(owner, address(0), _tokenId);
}
```

### Problems
There are two main issues with the above implementation:

1. The `_approve(address(0), _tokenId)` method internally checks whether `msg.sender` is the owner or `senderIsApprovedForAll`, and does not allow `idToApprovals[id]`. So even if the user has been granted permission through `approve(user,id)`, they still cannot execute `_burn()`. The correct usage should be: `_clearApproval(owner, _tokenId)`.

2. The `_removeTokenFrom(msg.sender, _tokenId)` method passes in the first parameter as `_from = msg.sender`. The method internally checks `assert(idToOwner[_tokenId] == _from);`. So even if the user is verified by `_isApprovedOrOwner()`, they still cannot execute `_burn()`. The correct usage should be: `_removeTokenFrom(owner, _tokenId)`.

## Impact
Even if the user is approved, they still cannot execute `withdraw()` and `merge()`.

## Recommendation
```solidity
function _burn(uint256 _tokenId) internal {
    require(
        _isApprovedOrOwner(msg.sender, _tokenId),
        "caller is not owner nor approved"
    );
    address owner = _ownerOf(_tokenId);
    // Clear approval
    - _approve(address(0), _tokenId);
    + _clearApproval(owner, _tokenId);
    // Remove token
    - _removeTokenFrom(msg.sender, _tokenId);
    + _removeTokenFrom(owner, _tokenId);
    emit Transfer(owner, address(0), _tokenId);
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | ZeroLend |
| Report Date | N/A |
| Finders | Ch301, 8olidity, pauleth, Naveen Kumar J - 1nc0gn170, jovi.eth, cccz, bin2chen, ravikiranweb3, AuditorPraise, Chinmay Farkya, elhaj, waﬄemakr, saucecri, 0xarno, atarpara, 0x175, osmanozdemir1 |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_zerolend_jan2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/6d383aaf-8554-4a06-a224-86189f81f531

### Keywords for Search

`vulnerability`

