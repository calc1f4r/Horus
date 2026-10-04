---
# Core Classification
protocol: Golom
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 8741
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-07-golom-contest
source_link: https://code4rena.com/reports/2022-07-golom
github_link: https://github.com/code-423n4/2022-07-golom-findings/issues/577

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
  - services
  - liquidity_manager
  - nft_marketplace
  - options_vault

# Audit Details
report_date: unknown
finders_count: 13
finders:
  - csanuragjain
  - IllIllI
  - 0x4non
  - rbserver
  - cccz
---

## Vulnerability Title

[M-04]  `VoteEscrowCore.safeTransferFrom` does not check correct magic bytes returned from receiver contract's `onERC721Received` function

### Overview


This bug report is about a vulnerability in the OpenZeppelin Contracts ERC721 token contract. The vulnerability is that the `VoteEscrowCore.safeTransferFrom` function does not check for the required “magic bytes” which is `IERC721.onERC721received.selector`. This means that NFT tokens may be sent to non-compliant contracts and lost. The proof of concept for this vulnerability is that the lines 604 - 605 of the VoteEscrowCore.sol file should be changed from `try IERC721Receiver(_to).onERC721Received(msg.sender, _from, _tokenId, _data) returns (bytes4) {} catch (bytes memory reason` to `try IERC721Receiver(to).onERC721Received(_msgSender(), from, tokenId, data) returns (bytes4 retval) { return retval == IERC721Receiver.onERC721Received.selector; } catch (bytes memory reason)`. To mitigate this vulnerability, it is recommended that the `safeTransferReturn` function should be implemented and should check for the required magic bytes.

### Original Finding Content


[ERC721.sol#L395-L417](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/ce0068c21ecd97c6ec8fb0db08570f4b43029dde/contracts/token/ERC721/ERC721.sol#L395-L417)<br>

While `VoteEscrowCore.safeTransferFrom` does try to call `onERC721Received` on the receiver it does not check the for the required "magic bytes" which is `IERC721.onERC721received.selector` in this case. See [OpenZeppelin docs](https://docs.openzeppelin.com/contracts/3.x/api/token/erc721#IERC721Receiver-onERC721Received-address-address-uint256-bytes-) for more information.

It's quite possible that a call to `onERC721Received` could succeed because the contract had a `fallback` function implemented, but the contract is not ERC721 compliant.

The impact is that NFT tokens may be sent to non-compliant contracts and lost.

### Proof of Concept

[Lines 604 - 605](https://github.com/code-423n4/2022-07-golom/blob/e5efa8f9d6dda92a90b8b2c4902320acf0c26816/contracts/vote-escrow/VoteEscrowCore.sol#L604-L605) are:

```solidity
try IERC721Receiver(_to).onERC721Received(msg.sender, _from, _tokenId, _data) returns (bytes4) {} catch (
    bytes memory reason
```

but they should be:

```solidity
try IERC721Receiver(to).onERC721Received(_msgSender(), from, tokenId, data) returns (bytes4 retval) {
    return retval == IERC721Receiver.onERC721Received.selector;
} catch (bytes memory reason)
```

### Recommended Mitigation Steps

Implement `safeTransferReturn` so that it checks the required magic bytes: `IERC721Receiver.onERC721Received.selector`.

**[zeroexdead (Golom) confirmed](https://github.com/code-423n4/2022-07-golom-findings/issues/577)**

**[zeroexdead (Golom) commented](https://github.com/code-423n4/2022-07-golom-findings/issues/577#issuecomment-1236183431):**
 > Fixed.<br>
> Ref: https://github.com/golom-protocol/contracts/commit/19ba6e83892e24b859f081525c7e0f751f5e7ebb

**[0xsaruman (Golom) resolved, but disagreed with severity](https://github.com/code-423n4/2022-07-golom-findings/issues/577)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Golom |
| Report Date | N/A |
| Finders | csanuragjain, IllIllI, 0x4non, rbserver, cccz, Jmaxmanblue, arcoun, rotcivegaf, minhquanym, berndartmueller, Lambda, JohnSmith, sseefried |

### Source Links

- **Source**: https://code4rena.com/reports/2022-07-golom
- **GitHub**: https://github.com/code-423n4/2022-07-golom-findings/issues/577
- **Contest**: https://code4rena.com/contests/2022-07-golom-contest

### Keywords for Search

`vulnerability`

