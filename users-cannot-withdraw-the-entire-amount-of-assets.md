---
# Core Classification
protocol: Gorples EVM
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51288
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/entangle-labs/gorples-evm
source_link: https://www.halborn.com/audits/entangle-labs/gorples-evm
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
  - Halborn
---

## Vulnerability Title

Users Cannot Withdraw The Entire Amount Of Assets

### Overview


The report describes an issue with two functions, `emergencyWithdraw()` and `withdrawFromPosition()`, that allow the owner or an approved user to withdraw deposited assets. These functions call the `_destroyPosition()` function, which burns the related NFT token and attempts to update the `ownerToId` mapping. However, the `ownerOf()` function, used in the ERC721 contract, will fail if the token has already been burnt, preventing the user from withdrawing their assets. A proof of concept test was used to demonstrate the issue. The BVSS score for this bug is 7.8, indicating a high severity. The recommendation is to update the `ownerToId` mapping before burning the NFT token. The Entangle team has solved this issue as recommended.

### Original Finding Content

##### Description

The `emergencyWithdraw()` and `withdrawFromPosition()` functions allow the owner of the related NFT token or approved user to withdraw the entire amount of deposited assets. In that scenarios, both functions internally call the `_destroyPosition()` function, which burns the intended NFT and attempts to set the `ownerToId` mapping of user to 0.

```
function _destroyPosition(uint256 tokenId, uint256 boostPoints) internal {
    // calls yieldBooster contract to deallocate the bspNFT's owner boost points if any
    if (boostPoints > 0) {
        IYieldBooster(yieldBooster()).deallocateAllFromPool(
            msg.sender,
            tokenId
        );
    }

    // burn bspNFT
    delete stakingPositions[tokenId];
    _burn(tokenId);
    ownerToId[ownerOf(tokenId)] = 0;
}
```

However, the `ownerOf()` function, implemented in the ERC721 contract, invokes the `requireOwned()` function, which will revert with an `ERC721NonexistentToken` error if the token has already been burnt, effectively preventing user from withdrawing the full amount of deposited assets.

```
function _requireOwned(uint256 tokenId) internal view returns (address) {
    address owner = _ownerOf(tokenId);
    if (owner == address(0)) {
        revert ERC721NonexistentToken(tokenId);
    }
    return owner;
}
```

##### Proof of Concept

The following `Foundry` test was used to prove the aforementioned issue:

```
function test_fullWithdrawBroken() public {
    //Admin adds the pool to the MasterBorpa
    masterBorpa.add(address(nftPool), 2);

    //User creates a position, becoming the owner of NFT 1
    vm.startPrank(user);
    mockERC20.approve(address(nftPool), 10e18);
    nftPool.createPosition(10e18, user);
    assertEq(nftPool.ownerToId(user), 1);
    vm.stopPrank();

    //User intends to withdraw all assets
    //Transaction reverts with ERC721NonexistentToken error
    vm.prank(user);
    vm.expectRevert();
    nftPool.emergencyWithdraw(1);

    vm.prank(user);
    vm.expectRevert();
    nftPool.withdrawFromPosition(1, 10e18);
}
```

  
![](https://halbornmainframe.com/proxy/audits/images/6676d7ed8b547eb4b0f90fd2)

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:N/A:M/D:M/Y:N/R:N/S:C (7.8)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:N/A:M/D:M/Y:N/R:N/S:C)

##### Recommendation

Update the `ownerToId` mapping before burning the NFT token.

### Remediation Plan

**SOLVED:** The **Entangle team** solved this issue as recommended.

##### Remediation Hash

<https://github.com/Entangle-Protocol/borpa/commit/63d1626da8edd3af265b39a71f9d7d6edbc0ca84>

##### References

[Entangle-Protocol/borpa/contracts/NFTPool.sol#L532-L545](https://github.com/Entangle-Protocol/borpa/blob/0747bab6a7523ece4adad20cb8e7b5b9c92c3c1d/contracts/NFTPool.sol#L532-L545)

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Gorples EVM |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/entangle-labs/gorples-evm
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/entangle-labs/gorples-evm

### Keywords for Search

`vulnerability`

