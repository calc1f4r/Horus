---
# Core Classification
protocol: Connext
chain: everychain
category: logic
vulnerability_type: validation

# Attack Vector Details
attack_type: validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7211
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:
  - validation
  - front-running

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - 0xLeastwood
  - Jonah1005
---

## Vulnerability Title

Lack of transferId Verification Allows an Attacker to Front-Run Bridge Transfers

### Overview


This bug report is about the onReceive() function in NomadFacet.sol and BridgeRouter.sol contracts. The function does not properly verify the integrity of the transferId parameter against all other parameters. This could allow anyone to send arbitrary data to BridgeRouter.sendToHook(), which could be abused by a front-running attack.

In this attack, Alice is a bridge user who makes an honest call to transfer funds over to the destination chain. Bob does not make a transfer, but instead calls the sendToHook() function with the same _extraData but passes an _amount of 1 wei. Both Alice and Bob have their tokens debited on the source chain. Once the messages have been replicated onto the destination chain, Bob processes the message before Alice, causing onReceive() to be called on the same transferId. Because _amount is not verified against the transferId, Alice receives significantly less tokens and the s.reconciledTransfers mapping marks the transfer as reconciled. Hence, Alice has effectively lost all her tokens during an attempt to bridge them.

The same issue exists with _localToken, so a malicious user could perform the same attack by using a malicious token contract. Connext has solved this issue with Pull Requests 1630 and 1678. It is also important to conduct a separate review of that particular code, including the interface to Connext, and an extra audit for BridgeRouter is underway.

### Original Finding Content

## Severity: Critical Risk  

## Context  
- `NomadFacet.sol#L99-L149`  
- `BridgeRouter.sol#L176-L199`  
- `BridgeRouter.sol#L347-L381`  

## Description  
The `onReceive()` function does not verify the integrity of `transferId` against all other parameters. Although the `onlyBridgeRouter` modifier checks that the call originates from another BridgeRouter (assuming a correct configuration of the whitelist) to the `onReceive()` function, it does not check that the call originates from another Connext Diamond.

This allows anyone to send arbitrary data to `BridgeRouter.sendToHook()`, which is later interpreted as the `transferId` on Connext’s `NomadFacet.sol` contract. This can be abused by a front-running attack as described in the following scenario:

- **Alice** is a bridge user and makes an honest call to transfer funds over to the destination chain.  
- **Bob** does not make a transfer but instead calls the `sendToHook()` function with the same `_extraData` but passes an `_amount` of `1 wei`.  
- Both Alice and Bob have their tokens debited on the source chain and must wait for the Nomad protocol to optimistically verify incoming `TransferToHook` messages.  
- Once the messages have been replicated onto the destination chain, Bob processes the message before Alice, causing `onReceive()` to be called on the same `transferId`.  
- However, because `_amount` is not verified against the `transferId`, Alice receives significantly fewer tokens, and the `s.reconciledTransfers` mapping marks the transfer as reconciled. Hence, Alice has effectively lost all her tokens during an attempt to bridge them.  

### Function: `onReceive()`
```solidity
function onReceive(
  uint32, // _origin, not used
  uint32, // _tokenDomain, not used
  bytes32, // _tokenAddress, of canonical token, not used
  address _localToken,
  uint256 _amount,
  bytes memory _extraData
) external onlyBridgeRouter {
  bytes32 transferId = bytes32(_extraData);
  
  // Ensure the transaction has not already been handled (i.e. previously reconciled).
  if (s.reconciledTransfers[transferId]) {
    revert NomadFacet__reconcile_alreadyReconciled();
  }
  
  // Mark the transfer as reconciled.
  s.reconciledTransfers[transferId] = true;
}
```
> **Note:** The same issue exists with `_localToken`. As a result, a malicious user could perform the same attack by using a malicious token contract and transferring the same amount of tokens in the call to `sendToHook()`.  

## Recommendation  
Verify that the call originates from the Connext Diamond on the originator chain. In function `reconcile()`, verify that `transferId` is indeed a hash of the other parameters.  

## Connext  
Solved in PR 1630 and PR 1678.  
An extra audit for BridgeRouter is underway.  

## Spearbit  
> Note: The BridgeRouter and the interface to it has changed quite a lot during and after this audit. As it was out of scope for this audit, it is also important to conduct a separate review of that particular code, including the interface to Connext.  
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Spearbit |
| Protocol | Connext |
| Report Date | N/A |
| Finders | 0xLeastwood, Jonah1005 |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf

### Keywords for Search

`Validation, Front-Running`

