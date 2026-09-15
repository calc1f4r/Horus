---
# Core Classification
protocol: Tapioca DAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32323
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-02-tapioca
source_link: https://code4rena.com/reports/2024-02-tapioca
github_link: https://github.com/code-423n4/2024-02-tapioca-findings/issues/44

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

protocol_categories:
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - deadrxsezzz
---

## Vulnerability Title

[H-12] Adversary can steal user's NFT's if they have set Magnetar as `isApprovedForAll == true`

### Overview


The Magnetar contract, which is used as a router for multiple operations, has a bug that allows any user to make a `ERC721.approve` call through the `_processPermitOperation` function. This can lead to a security issue where a user who has been approved as `isApprovedForAll` can call `approve` for any NFT belonging to the owner. The recommended mitigation step is to not allow users to make a call with the `ERC721.approve` selector.

### Original Finding Content


Since Magnetar is supposed to be used as a router for multiple operations, it can be expected that user will have it pre-approved for their NFTs (such as `tOLP` as `oTAP` ones, as they'll be the ones primarily used).

The Magnetar contract allows for any user to make a `ERC721.approve`, via `_processPermitOperation`:

```solidity
    function _processPermitOperation(address _target, bytes calldata _actionCalldata, bool _allowFailure) private {
        if (!cluster.isWhitelisted(0, _target)) revert Magnetar_NotAuthorized(_target, _target);

        /// @dev owner address should always be first param.
        // permitAction(bytes,uint16)
        // permit(address owner...)
        // revoke(address owner...)
        // permitAll(address from,..)
        // permit(address from,...)
        // setApprovalForAll(address from,...)
        // setApprovalForAsset(address from,...)
        bytes4 funcSig = bytes4(_actionCalldata[:4]);
        if (
            funcSig == IPermitAll.permitAll.selector || funcSig == IPermitAll.revokeAll.selector
                || funcSig == IPermit.permit.selector || funcSig == IPermit.revoke.selector
                || funcSig == IYieldBox.setApprovalForAll.selector || funcSig == IYieldBox.setApprovalForAsset.selector 
                || funcSig == IERC20.approve.selector || funcSig == IPearlmit.approve.selector
                || funcSig == IERC721.approve.selector 
        ) {
            /// @dev Owner param check. See Warning above.
            _checkSender(abi.decode(_actionCalldata[4:36], (address)));
            // No need to send value on permit
            _executeCall(_target, _actionCalldata, 0, _allowFailure);
            return;
        }
        revert Magnetar_ActionNotValid(MagnetarAction.Permit, _actionCalldata);
    }
```

The problem is that for OZ ERC721s (such as `oTAP` and `tOLP`), if an NFT owner has approved a spender as `isApprovedForAll`, the spender can call `approve` for any NFTs belonging to the owner.

In other words, if user A has set Magnetar as `approvedForAll`, user B can call `NFT.approve(userB, id)` and get access to user A's NFT:

```solidity
    function approve(address to, uint256 tokenId) public virtual override {
        address owner = ERC721.ownerOf(tokenId);
        require(to != owner, "ERC721: approval to current owner");

        require(
            _msgSender() == owner || isApprovedForAll(owner, _msgSender()),
            "ERC721: approve caller is not token owner or approved for all"
        );

        _approve(to, tokenId);
    }
```

### Recommended Mitigation Steps

Do not allow users to make a call with  `ERC721.approve` selector.

**[0xWeiss (Tapioca) confirmed](https://github.com/code-423n4/2024-02-tapioca-findings/issues/44#issuecomment-2125599377)**

***
 


### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Tapioca DAO |
| Report Date | N/A |
| Finders | deadrxsezzz |

### Source Links

- **Source**: https://code4rena.com/reports/2024-02-tapioca
- **GitHub**: https://github.com/code-423n4/2024-02-tapioca-findings/issues/44
- **Contest**: https://code4rena.com/reports/2024-02-tapioca

### Keywords for Search

`vulnerability`

