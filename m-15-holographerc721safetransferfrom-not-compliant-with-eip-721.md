---
# Core Classification
protocol: Holograph
chain: everychain
category: uncategorized
vulnerability_type: erc721

# Attack Vector Details
attack_type: erc721
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5608
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-10-holograph-contest
source_link: https://code4rena.com/reports/2022-10-holograph
github_link: https://github.com/code-423n4/2022-10-holograph-findings/issues/203

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 4

# Context Tags
tags:
  - erc721
  - eip-165

protocol_categories:
  - dexes
  - bridge
  - services
  - launchpad
  - nft_marketplace

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Lambda
---

## Vulnerability Title

[M-15] `HolographERC721.safeTransferFrom` not compliant with EIP-721

### Overview


This bug report is about the `safeTransferFrom` function in the HolographERC721.sol code. According to the EIP-721 specification, the function must always call `onERC721Received` when transferring tokens, not only when it has determined via ERC-165 that the contract provides this function. However, many receivers will just implement the `onERC721Received` function, and not `supportsInterface` for ERC-165 support, leading to failed transfers when they should not fail. The recommended mitigation step is to remove the ERC-165 check in the `require` statement.

### Original Finding Content


[HolographERC721.sol#L366](https://github.com/code-423n4/2022-10-holograph/blob/24bc4d8dfeb6e4328d2c6291d20553b1d3eff00b/src/enforcer/HolographERC721.sol#L366)<br>

According to EIP-721, we have the following for `safeTransferFrom`:

```solidity
///  (...) When transfer is complete, this function
///  checks if `_to` is a smart contract (code size > 0). If so, it calls
///  `onERC721Received` on `_to` and throws if the return value is not
///  `bytes4(keccak256("onERC721Received(address,address,uint256,bytes)"))`.
```

According to the specification, the function must therefore always call `onERC721Received`, not only when it has determined via ERC-165 that the contract provides this function. Note that in the EIP, the provided interface for `ERC721TokenReceiver` does not mention ERC-165. For the token itself, we have: `interface ERC721 /* is ERC165 */ {`<br>
However, for the receiver, the provided interface there is just: `interface ERC721TokenReceiver {`<br>
This leads to failed transfers when they should not fail, because many receivers will just implement the `onERC721Received` function (which is sufficient according to the EIP), and not `supportsInterface` for ERC-165 support.

### Proof Of Concept

Let's say a receiver just implements the `IERC721Receiver` from OpenZeppelin: <https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/IERC721Receiver.sol><br>
Like the provided interface in the EIP itself, this interface does not derive from EIP-165. All of these receivers (which are most receivers in practice) will not be able to receive those tokens, because the `require` statement (that checks for ERC-165 support) reverts.

### Recommended Mitigation Steps

Remove the ERC-165 check in the `require` statement (like OpenZeppelin does: <https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/ERC721.sol#L436>).

**[alexanderattar (Holograph) commented](https://github.com/code-423n4/2022-10-holograph-findings/issues/203#issuecomment-1307809122):**
 > This will be updated to be fully ERC721 compliant

**[ACC01ADE (Holograph) linked a PR](https://github.com/code-423n4/2022-10-holograph-findings/issues/203#ref-pullrequest-1452472274):**
 > [Feature/HOLO-605: C4 medium risk fixes](https://github.com/holographxyz/holograph-protocol/pull/88)



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Holograph |
| Report Date | N/A |
| Finders | Lambda |

### Source Links

- **Source**: https://code4rena.com/reports/2022-10-holograph
- **GitHub**: https://github.com/code-423n4/2022-10-holograph-findings/issues/203
- **Contest**: https://code4rena.com/contests/2022-10-holograph-contest

### Keywords for Search

`ERC721, EIP-165`

