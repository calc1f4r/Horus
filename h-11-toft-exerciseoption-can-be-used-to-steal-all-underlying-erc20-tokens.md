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
solodit_id: 27501
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-07-tapioca
source_link: https://code4rena.com/reports/2023-07-tapioca
github_link: https://github.com/code-423n4/2023-07-tapioca-findings/issues/1307

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
finders_count: 2
finders:
  - Ack
  - windhustler
---

## Vulnerability Title

[H-11] TOFT `exerciseOption` can be used to steal all underlying erc20 tokens

### Overview


This bug report is about a vulnerability in the Tapioca-DAO's BaseTOFT contract. The contract is a wrapper around an ERC20 token and extends the OFTV2 contract to enable smooth cross-chain transfers. The vulnerability allows an attacker to steal all the ERC20 tokens from the contract by sending unvalidated input data to the exerciseOption function.

The attack starts by sending the unvalidated input data to the exerciseOption function. This only costs the attacker the optionsData.paymentTokenAmount, which is a small amount. Once the message is received on the remote chain, the attacker needs to pass the following data: zero approval, the address of the underlying ERC20 token for the TOFT, the address of the attacker, and the balance of ERC20 tokens of the TOFT. This allows the attacker to transfer all the underlying ERC20 tokens to their own address.

The recommended mitigation step is to validate that the tapSendData.tapOftAddress is the address of the TapOFT token either while sending the message or during the reception of the message on the remote chain. This will prevent the attack from happening.

### Original Finding Content


Unvalidated input data for the [`exerciseOption`](https://github.com/Tapioca-DAO/tapiocaz-audit/blob/master/contracts/tOFT/BaseTOFT.sol#L127) function can be used to steal all the erc20 tokens from the contract.

### Proof of Concept

Each [BaseTOFT](https://github.com/Tapioca-DAO/tapiocaz-audit/blob/master/contracts/tOFT/BaseTOFT.sol) is a wrapper around an `erc20` token and extends the `OFTV2` contract to enable smooth cross-chain transfers through LayerZero.
Depending on the erc20 token which is used usually the erc20 tokens will be held on one chain and then only the shares of `OFTV2` get transferred around (burnt on one chain, minted on another chain).
Subject to this attack is `TapiocaOFTs` or `mTapiocaOFTs` which store as an [underlying token an erc20 token(not native)](https://github.com/Tapioca-DAO/tapiocaz-audit/blob/master/contracts/tOFT/TapiocaOFT.sol#L77). In order to mint `TOFT` shares you need to deposit the underlying erc20 tokens into the contract, and you get `TOFT` shares.

The attack flow is the following:

1.  The attack starts from the [`exerciseOption`](https://github.com/Tapioca-DAO/tapiocaz-audit/blob/master/contracts/tOFT/BaseTOFT.sol#L127-L146). Nothing is validated here and the only cost of the attack is the [`optionsData.paymentTokenAmount`](https://github.com/Tapioca-DAO/tapiocaz-audit/blob/master/contracts/tOFT/modules/BaseTOFTOptionsModule.sol#L87) which is burned from the attacker. This can be some small amount.
2.  When the message is received on the remote chain inside the [`exercise`](https://github.com/Tapioca-DAO/tapiocaz-audit/blob/master/contracts/tOFT/modules/BaseTOFTOptionsModule.sol#L153) function it is important that nothing reverts for the attacker.
3.  For the attacker to go through the attacker needs to pass the following data:

```soldity
function exerciseInternal(
        address from,
        uint256 oTAPTokenID,
        address paymentToken,
        uint256 tapAmount,
        address target,
        ITapiocaOptionsBrokerCrossChain.IExerciseLZSendTapData
            memory tapSendData,
        ICommonData.IApproval[] memory approvals
    ) public {
        // pass zero approval so this is skipped 
        if (approvals.length > 0) {
            _callApproval(approvals);
        }
        
        // target is the address which does nothing, but has the exerciseOption implemented
        ITapiocaOptionsBroker(target).exerciseOption(
            oTAPTokenID,
            paymentToken,
            tapAmount
        );
        // tapSendData.withdrawOnAnotherChain = false so we enter else branch
        if (tapSendData.withdrawOnAnotherChain) {
            ISendFrom(tapSendData.tapOftAddress).sendFrom(
                address(this),
                tapSendData.lzDstChainId,
                LzLib.addressToBytes32(from),
                tapAmount,
                ISendFrom.LzCallParams({
                    refundAddress: payable(from),
                    zroPaymentAddress: tapSendData.zroPaymentAddress,
                    adapterParams: LzLib.buildDefaultAdapterParams(
                        tapSendData.extraGas
                    )
                })
            );
        } else {
            // tapSendData.tapOftAddress is the address of the underlying erc20 token for this TOFT
            // from is the address of the attacker
            // tapAmount is the balance of erc20 tokens of this TOFT
            IERC20(tapSendData.tapOftAddress).safeTransfer(from, tapAmount);
        }
    }
```

4.  So the attack is just simply transferring all the underlying erc20 tokens to the attacker.

The underlying `ERC20` token for each `TOFT` can be queried through [`erc20()`](https://github.com/Tapioca-DAO/tapiocaz-audit/blob/master/contracts/tOFT/BaseTOFTStorage.sol#L28) function, and the `tapAmount` to pass is `ERC20` balance of the `TOFT`.

This attack is possible because the `msg.sender` inside the `exerciseInternal` is the address of the `TOFT` which is the owner of all the ERC20 tokens that get stolen.

### Recommended Mitigation Steps

Validate that `tapSendData.tapOftAddress` is the address of [`TapOFT`](https://github.com/Tapioca-DAO/tap-token-audit/blob/main/contracts/tokens/TapOFT.sol) token either while sending the message or during the reception of the message on the remote chain.

**[0xRektora (Tapioca) confirmed](https://github.com/code-423n4/2023-07-tapioca-findings/issues/1307#issuecomment-1703035021)**

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
| Finders | Ack, windhustler |

### Source Links

- **Source**: https://code4rena.com/reports/2023-07-tapioca
- **GitHub**: https://github.com/code-423n4/2023-07-tapioca-findings/issues/1307
- **Contest**: https://code4rena.com/reports/2023-07-tapioca

### Keywords for Search

`vulnerability`

