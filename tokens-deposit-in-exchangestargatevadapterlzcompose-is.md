---
# Core Classification
protocol: IDEX
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61092
audit_firm: Immunefi
contest_link: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/IDEX/Boost%20_%20IDEX%2034494%20-%20%5BSmart%20Contract%20-%20High%5D%20Tokens%20deposit%20in%20ExchangeStargateVAdapterlzCompose%20is%20not%20protected%20by%20a%20trycatch%20block.md
source_link: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/IDEX/Boost%20_%20IDEX%2034494%20-%20%5BSmart%20Contract%20-%20High%5D%20Tokens%20deposit%20in%20ExchangeStargateVAdapterlzCompose%20is%20not%20protected%20by%20a%20trycatch%20block.md
github_link: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/IDEX/Boost%20_%20IDEX%2034494%20-%20%5BSmart%20Contract%20-%20High%5D%20Tokens%20deposit%20in%20ExchangeStargateVAdapterlzCompose%20is%20not%20protected%20by%20a%20trycatch%20block.md

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
  - Paludo0x
---

## Vulnerability Title

Tokens deposit in ExchangeStargateVAdapterlzCompose is

### Overview


This bug report is about a smart contract on GitHub that is used for transferring tokens from one blockchain to another. The contract has a function called `lzCompose()` that is responsible for transferring the tokens to the final contract. However, if the `IExchange(custodian.exchange()).deposit();` function is disabled for any reason, the transfer will fail and the funds will be temporarily frozen. This can happen if the exchange deposits are disabled permanently, even if there are attempts to retry the transfer. The report suggests implementing a `catch` block in the contract to transfer the funds to the destination wallet or a permissioned wallet with transfering functionality. The report also includes a proof of concept test that shows the transfer will fail if the exchange deposits are disabled. 

### Original Finding Content




Report type: Smart Contract


Target: https://github.com/idexio/idex-contracts-ikon/blob/main/contracts/bridge-adapters/ExchangeStargateV2Adapter.sol

Impacts:

* Temporary freezing of funds

## Description

## Brief/Intro

In `ExchangeStargateV2Adapter::lzCompose()` the `IExchange(custodian.exchange()).deposit();` function is called, if this is disabled for any reason the deposit will fail.

## Vulnerability Details

The tokens are bridged from L1 to L2 by means of Stargate protocol.

In order to transfer the tokens to the final contract the function `lzCompose` shall be implemented.

This is the implementation of the `ExchangeStargateV2Adapter` contract:

```
  function lzCompose(
    address _from,
    bytes32 /* _guid */,
    bytes calldata _message,
    address /* _executor */,
    bytes calldata /* _extraData */
  ) public payable override {
  ...
    // https://github.com/LayerZero-Labs/LayerZero-v2/blob/1fde89479fdc68b1a54cda7f19efa84483fcacc4/oapp/contracts/oft/libs/OFTComposeMsgCodec.sol#L52
    uint256 amountLD = OFTComposeMsgCodec.amountLD(_message);

    // https://github.com/LayerZero-Labs/LayerZero-v2/blob/1fde89479fdc68b1a54cda7f19efa84483fcacc4/oapp/contracts/oft/libs/OFTComposeMsgCodec.sol#L61
    address destinationWallet = abi.decode(OFTComposeMsgCodec.composeMsg(_message), (address));
    require(destinationWallet != address(0x0), "Invalid destination wallet");

    IExchange(custodian.exchange()).deposit(amountLD, destinationWallet); 
  } 

```

The call to `deposit` function is not inside a try/catch block as it is usual when tokens are transferred via a token/messagge bridge layer.

An example of implementation is reported in **Stargate** docs. https://stargateprotocol.gitbook.io/stargate/v/v2-developer-docs/integrate-with-stargate/composability#receive-1

The suggestion is to implement the `catch` block with a transfer to the destination wallet or to a permissioned wallet with transfering functionality implemented.

## Impact Details

The impact is that the funds can be stucked if the exchange deposits are disabled permanently for any reason, even if LayerZero and Stargate implements functionalities to retry sending a message

## Proof of concept

## Proof of Concept

In the test provided by the contract there's the POC that demonstrates that the call will revert if exchange deposits are disabled.

```
    it.only('should revert when deposits are disabled', async () => {
      await expect(
        stargateRouterMock.sgReceive(
          await adapter.getAddress(),
          1,
          '0x',
          0,
          await usdc.getAddress(),
          10000000000,
          ethers.AbiCoder.defaultAbiCoder().encode(
            ['address'],
            [ownerWallet.address],
          ),
        ),
      ).to.eventually.be.rejectedWith(/deposits disabled/i);
    });
```


### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Immunefi |
| Protocol | IDEX |
| Report Date | N/A |
| Finders | Paludo0x |

### Source Links

- **Source**: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/IDEX/Boost%20_%20IDEX%2034494%20-%20%5BSmart%20Contract%20-%20High%5D%20Tokens%20deposit%20in%20ExchangeStargateVAdapterlzCompose%20is%20not%20protected%20by%20a%20trycatch%20block.md
- **GitHub**: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/IDEX/Boost%20_%20IDEX%2034494%20-%20%5BSmart%20Contract%20-%20High%5D%20Tokens%20deposit%20in%20ExchangeStargateVAdapterlzCompose%20is%20not%20protected%20by%20a%20trycatch%20block.md
- **Contest**: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/IDEX/Boost%20_%20IDEX%2034494%20-%20%5BSmart%20Contract%20-%20High%5D%20Tokens%20deposit%20in%20ExchangeStargateVAdapterlzCompose%20is%20not%20protected%20by%20a%20trycatch%20block.md

### Keywords for Search

`vulnerability`

