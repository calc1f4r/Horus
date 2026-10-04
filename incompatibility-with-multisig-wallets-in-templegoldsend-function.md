---
# Core Classification
protocol: TempleGold
chain: everychain
category: uncategorized
vulnerability_type: cross_chain

# Attack Vector Details
attack_type: cross_chain
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35290
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/clxyjvjkg0007isl3p290etog
source_link: none
github_link: https://github.com/Cyfrin/2024-07-templegold

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 3

# Context Tags
tags:
  - cross_chain

protocol_categories:
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 36
finders:
  - n0kto
  - KiteWeb3
  - WildSniper
  - ZdravkoHr
  - 0xDemon
---

## Vulnerability Title

Incompatibility with Multisig Wallets in `TempleGold::send` Function

### Overview


The `TempleGold` smart contract has a bug that prevents users from transferring their tokens across different chains using the `send` function. This is a problem for users with multisig wallets, as these wallets often have different addresses on different chains. The bug is caused by a condition that checks if the sender's address matches the recipient's address, which fails for multisig wallet users. This restricts the usability of the contract and may deter users from adopting it. A proof of concept and recommendations for addressing the bug are provided. 

### Original Finding Content

## Summary:

The `send` function in `TempleGold` smart contract is designed to facilitate cross-chain token transfers using LayerZero. However, it contains a restrictive condition that disallows transfers if the sender's address does not match the recipient's address. This creates a significant issue for users utilizing multisig wallets, as these wallets often have different addresses across different chains, preventing them from transferring their funds cross-chain.

## Vulnerability Detail:

The vulnerability lies in the address validation check: `if (msg.sender != _to) { revert ITempleGold.NonTransferrable(msg.sender, _to); }`. This condition ensures that the sender and the recipient addresses are identical, which is not the case for multisig wallets operating across different chains such as Ethereum and Arbitrum.

## Code Snippet:

```javascript
function send(
        SendParam calldata _sendParam,
        MessagingFee calldata _fee,
        address _refundAddress
    ) external payable virtual override(IOFT, OFTCore) returns (MessagingReceipt memory msgReceipt, OFTReceipt memory oftReceipt) {
        if (_sendParam.composeMsg.length > 0) { revert CannotCompose(); }
        /// cast bytes32 to address
        address _to = _sendParam.to.bytes32ToAddress();
        /// @dev user can cross-chain transfer to self
@>      if (msg.sender != _to) { revert ITempleGold.NonTransferrable(msg.sender, _to); }

        // @dev Applies the token transfers regarding this send() operation.
        (uint256 amountSentLD, uint256 amountReceivedLD) = _debit(
            msg.sender,
            _sendParam.amountLD,
            _sendParam.minAmountLD,
            _sendParam.dstEid
        );

        // @dev Builds the options and OFT message to quote in the endpoint.
        (bytes memory message, bytes memory options) = _buildMsgAndOptions(_sendParam, amountReceivedLD);

        // @dev Sends the message to the LayerZero endpoint and returns the LayerZero msg receipt.
        msgReceipt = _lzSend(_sendParam.dstEid, message, options, _fee, _refundAddress);
        // @dev Formulate the OFT receipt.
        oftReceipt = OFTReceipt(amountSentLD, amountReceivedLD);

        emit OFTSent(msgReceipt.guid, _sendParam.dstEid, msg.sender, amountSentLD, amountReceivedLD);
    }
```

## Impact:

This vulnerability prevents users of multisig wallets from performing cross-chain transfers of their tokens. The condition `if (msg.sender != _to)` fails for multisig wallet users due to differing addresses across chains, which:

* Restricts the usability of the contract for multisig wallet users.
* Limits the flexibility and accessibility of cross-chain token transfers.
* Potentially deters users from adopting the contract due to this inflexibility.

## Proof Of Concept:

1. User A, who owns a multisig wallet, attempts to transfer his temple tokens from Ethereum to Arbitrum using the `send` function.
2. The `send` function checks if the sender's address matches the recipient's address.
3. The condition `if (msg.sender != _to)` fails due to the differing addresses of the multisig wallet on Ethereum and Arbitrum.
4. The transaction reverts, preventing User A from completing the cross-chain transfer.

**Proof Of Code:**

Place the following code in the `TempleGoldLayerZero.t.sol` contract:

```javascript
    function test_FortisAudits_MultiSigWallet_LossFunds() public {
        address multisig_MainNet = makeAddr("multisig-mainnet"); // user's address
        address multisig_Arb = makeAddr("multisig-arb"); // user's same address which is undeployed in arbitrum
        vm.deal(multisig_MainNet, 100 ether);
        vm.deal(multisig_Arb, 100 ether);
        aTempleGold.mint(multisig_MainNet, 100 ether);
        uint256 tokensToSend = 1 ether;
        bytes memory options = OptionsBuilder.newOptions().addExecutorLzReceiveOption(200_000, 0);
        SendParam memory sendParam =
            SendParam(bEid, addressToBytes32(multisig_Arb), tokensToSend, tokensToSend, options, "", "");

        MessagingFee memory fee1 = aTempleGold.quoteSend(sendParam, false);

        // If a msg.sender uses a mulitisig wallet in the destination chain, thus funds cannot be
        // transferred and DOS the user
        vm.startPrank(multisig_MainNet);
        vm.expectRevert(abi.encodeWithSelector(ITempleGold.NonTransferrable.selector, multisig_MainNet, multisig_Arb));
        aTempleGold.send{ value: fee1.nativeFee }(sendParam, fee1, multisig_MainNet);
        verifyPackets(bEid, addressToBytes32(address(bTempleGold)));
        vm.stopPrank();
    }
```

## Tools Used:

Manual code review

Foundry

## Recommendations:

1. **Remove or Modify Address Check**: Consider modifying or removing the restrictive address check to accommodate multisig wallet users. For example:

   ```javascript
   if (msg.sender != _to) {
     // Additional validation to check if msg.sender is a multisig wallet or other criteria
     // revert ITempleGold.NonTransferrable(msg.sender, _to);
   }
   ```

2. **Implement Whitelisting**: Implement a whitelisting mechanism for known multisig wallet addresses across chains to bypass the restrictive check.

3. **User Validation**: Introduce a more sophisticated user validation process that allows for different addresses on different chains but ensures the integrity of the cross-chain transfer.

By addressing this vulnerability, the contract will become more inclusive and practical for a broader range of users, particularly those using multisig wallets.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 3/5 |
| Audit Firm | Codehawks |
| Protocol | TempleGold |
| Report Date | N/A |
| Finders | n0kto, KiteWeb3, WildSniper, ZdravkoHr, 0xDemon, billoBaggeBilleyan, nisedo, 0xsandy, zaevlad, 1337web3, y0ng0p3, ke1caM, Joshuajee, matej, abhishekthakur, 0xhals, adriro, y4y, 4rdiii, yotov721, turvec, blckhv, Pelz, Bauchibred, x18a6, 0xspryon, ebok21, pep7siup, n08ita, m4k2xmk, ptsanev, Bluedragon, Josh4324, 0xlucky, 0xlrivo, 0xaman |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2024-07-templegold
- **Contest**: https://codehawks.cyfrin.io/c/clxyjvjkg0007isl3p290etog

### Keywords for Search

`Cross Chain`

