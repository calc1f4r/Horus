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
solodit_id: 5597
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-10-holograph-contest
source_link: https://code4rena.com/reports/2022-10-holograph
github_link: https://github.com/code-423n4/2022-10-holograph-findings/issues/469

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
  - erc721

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
  - adriro
  - Trust
---

## Vulnerability Title

[M-04] Incorrect implementation of ERC721 may have bad consequences for receiver

### Overview


This bug report is about an issue found in the HolographERC721.sol contract, which is an enforcer contract that fully implements ERC721. The bug is related to the safeTransferFromFunction, in which the code deviates from the ERC721 standard. The standard requires that the first parameter should be the operator, but the enforcer passes the address(this) value instead. This means that any bookkeeping done in the target contract, and the decision of allowing or disallowing the transaction, is based on false information.

The impact of this bug is that the ERC721 transferFrom's "to" contract may fail to accept transfers, or record credit of transfers incorrectly. The bug was found through manual audit.

The recommended mitigation step for this bug is to pass the msg.sender parameter, as the ERC721 standard requires.

### Original Finding Content


[HolographERC721.sol#L467](https://github.com/code-423n4/2022-10-holograph/blob/f8c2eae866280a1acfdc8a8352401ed031be1373/contracts/enforcer/HolographERC721.sol#L467)<br>

HolographERC721.sol is an enforcer contract that fully implements ERC721. In its safeTransferFromFunction there is the following code:

    if (_isContract(to)) {
      require(
        (ERC165(to).supportsInterface(ERC165.supportsInterface.selector) &&
          ERC165(to).supportsInterface(ERC721TokenReceiver.onERC721Received.selector) &&
          ERC721TokenReceiver(to).onERC721Received(address(this), from, tokenId, data) ==
          ERC721TokenReceiver.onERC721Received.selector),
        "ERC721: onERC721Received fail"
      );
    }

If the target address is a contract, the enforcer requires the target's `onERC721Received()` to succeed. However, the call deviates from the [standard](https://eips.ethereum.org/EIPS/eip-721):

    interface ERC721TokenReceiver {
        /// @notice Handle the receipt of an NFT
        /// @dev The ERC721 smart contract calls this function on the recipient
        ///  after a `transfer`. This function MAY throw to revert and reject the
        ///  transfer. Return of other than the magic value MUST result in the
        ///  transaction being reverted.
        ///  Note: the contract address is always the message sender.
        /// @param _operator The address which called `safeTransferFrom` function
        /// @param _from The address which previously owned the token
        /// @param _tokenId The NFT identifier which is being transferred
        /// @param _data Additional data with no specified format
        /// @return `bytes4(keccak256("onERC721Received(address,address,uint256,bytes)"))`
        ///  unless throwing
        function onERC721Received(address _operator, address _from, uint256 _tokenId, bytes _data) external returns(bytes4);
    }

The standard mandates that the first parameter will be the operator - the caller of safeTransferFrom. The enforcer passes instead the `address(this)` value, in other words the Holographer address. The impact is that any bookkeeping done in target contract, and allow / disallow decision of the transaction, is based on false information.

### Impact

ERC721 transferFrom's "to" contract may fail to accept transfers, or record credit of transfers incorrectly.

### Recommended Mitigation Steps

Pass the msg.sender parameter, as the ERC721 standard requires.

**[alexanderattar (Holograph) commented](https://github.com/code-423n4/2022-10-holograph-findings/issues/469#issuecomment-1306626633):**
 > This will be updated to pass msg.sender instead of Holograph address to match the standard.

**[ACC01ADE (Holograph) linked a PR](https://github.com/code-423n4/2022-10-holograph-findings/issues/469#ref-pullrequest-1452472274):**
 > [Feature/HOLO-605: C4 medium risk fixes](https://github.com/holographxyz/holograph-protocol/pull/88)



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
| Finders | adriro, Trust |

### Source Links

- **Source**: https://code4rena.com/reports/2022-10-holograph
- **GitHub**: https://github.com/code-423n4/2022-10-holograph-findings/issues/469
- **Contest**: https://code4rena.com/contests/2022-10-holograph-contest

### Keywords for Search

`ERC721`

