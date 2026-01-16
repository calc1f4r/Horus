---
# Core Classification
protocol: ParaSpace
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 15986
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-11-paraspace-contest
source_link: https://code4rena.com/reports/2022-11-paraspace
github_link: https://github.com/code-423n4/2022-11-paraspace-findings/issues/235

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
finders_count: 5
finders:
  - csanuragjain
  - joestakey
  - Lambda
  - unforgiven
  - eierina
---

## Vulnerability Title

[M-03] safeTransfer is not implemented correctly

### Overview


A bug has been reported in the MintableIncentivizedERC721 contract, which is implemented by the NToken contract. The bug is in the safeTransferFrom function, which is supposed to check that the recipient is aware of the ERC721 protocol, but this safety check is missing. This means that non-secure ERC721 transfers can be made.

The bug is in the _safeTransferFrom function, which calls the _safeTransfer function and then the _transfer function. The _transfer function calls the MintableERC721Logic.executeTransfer, which simply transfers the asset without checking to see if the recipient can support ERC721. Additionally, the comment mentions that the data parameter passed in safeTransferFrom should be sent to the recipient, but this is not happening.

To fix this bug, it is recommended to add a call to the onERC721Received for the recipient and check if they can support ERC721. This will ensure that secure ERC721 transfers can be made.

### Original Finding Content


<https://github.com/code-423n4/2022-11-paraspace/blob/main/paraspace-core/contracts/protocol/tokenization/base/MintableIncentivizedERC721.sol#L320>

The safeTransfer function Safely transfers `tokenId` token from `from` to `to`, checking first that contract recipients are aware of the ERC721 protocol to prevent tokens from being forever locked. But seems like this safety check got missed in the `_safeTransfer` function leading to non secure ERC721 transfers

### Proof of Concept

1.  User calls the `safeTransferFrom` function (Using NToken contract which implements MintableIncentivizedERC721 contract)

<!---->

    function safeTransferFrom(
            address from,
            address to,
            uint256 tokenId,
            bytes memory _data
        ) external virtual override nonReentrant {
            _safeTransferFrom(from, to, tokenId, _data);
        }

2.  This makes an internal call to \_safeTransferFrom -> \_safeTransfer -> \_transfer

<!---->

    function safeTransferFrom(
            address from,
            address to,
            uint256 tokenId,
            bytes memory _data
        ) external virtual override nonReentrant {
            _safeTransferFrom(from, to, tokenId, _data);
        }

        function _safeTransferFrom(
            address from,
            address to,
            uint256 tokenId,
            bytes memory _data
        ) internal {
            require(
                _isApprovedOrOwner(_msgSender(), tokenId),
                "ERC721: transfer caller is not owner nor approved"
            );
            _safeTransfer(from, to, tokenId, _data);
        }

    function _safeTransfer(
            address from,
            address to,
            uint256 tokenId,
            bytes memory
        ) internal virtual {
            _transfer(from, to, tokenId);
        }

3.  Now lets see `_transfer` function

<!---->

    function _transfer(
            address from,
            address to,
            uint256 tokenId
        ) internal virtual {
            MintableERC721Logic.executeTransfer(
                _ERC721Data,
                POOL,
                ATOMIC_PRICING,
                from,
                to,
                tokenId
            );
        }

4.  This is calling `MintableERC721Logic.executeTransfer` which simply transfers the asset

5.  In this full flow there is no check to see whether `to` address can support ERC721 which fails the purpose of `safeTransferFrom` function

6.  Also notice the comment mentions that `data` parameter passed in safeTransferFrom is sent to recipient in call but there is no such transfer of `data`

### Recommended Mitigation Steps

Add a call to `onERC721Received` for recipient and see if the recipient actually supports ERC721.

**[WalidOfNow (Paraspace) commented via duplicate issue `#51`](https://github.com/code-423n4/2022-11-paraspace-findings/issues/51#issuecomment-1404062649):**
 > This is by design. We want to avoid re-entrancy to our contracts and so we removed calling the hook.


***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | ParaSpace |
| Report Date | N/A |
| Finders | csanuragjain, joestakey, Lambda, unforgiven, eierina |

### Source Links

- **Source**: https://code4rena.com/reports/2022-11-paraspace
- **GitHub**: https://github.com/code-423n4/2022-11-paraspace-findings/issues/235
- **Contest**: https://code4rena.com/contests/2022-11-paraspace-contest

### Keywords for Search

`vulnerability`

