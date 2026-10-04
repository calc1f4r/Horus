---
# Core Classification
protocol: Socket
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13189
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2023/02/socket/
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

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - David Oz
  -  George Kobakhidze

---

## Vulnerability Title

Funds Refunded From Celer Bridge Might Be Stolen

### Overview


This bug report is about the `refundCelerUser` function from `CelerImpl.sol` that allows a user that deposited into the Celer pool on the source chain, to be refunded for tokens that were not bridged to the destination chain. The function calls the `withdraw` method on the Celer pool to reimburse the user. The problem is that for some tokens, it is possible that the reimbursement will not be processed directly, but only after some delay. In this case, the address of the original sender will be reset to address(0) and the user will not receive the refund. This means that the funds will be sent back to the gateway contract and not to the original sender. Additionally, an attacker may be able to steal the refunded ETH or ERC-20 tokens by calling certain functions with the right parameters.

The bug was remediated by adding checks to see if the refund is received and equal to the expected amount and to make sure that `CelerImpl` supports also the delayed withdrawals functionality and that withdrawal requests are deleted only if the receiver has received the withdrawal in a single transaction. This ensures that the user will receive the refund and that the funds are not held post-transaction execution.

### Original Finding Content

#### Resolution



Remediated as per the client team in [SocketDotTech/socket-ll-contracts#144](https://github.com/SocketDotTech/socket-ll-contracts/pull/144) by adding checks to see if the refund is received and equal to the expected amount.


#### Description


The function `refundCelerUser` from `CelerImpl.sol` allows a user that deposited into the Celer pool on the source chain, to be refunded for tokens that were not bridged to the destination chain. The tokens are reimbursed to the user by calling the `withdraw` method on the Celer pool. This is what the `refundCelerUser` function is doing.


**src/bridges/cbridge/CelerImpl.sol:L413-L415**



```
if (!router.withdraws(transferId)) {
    router.withdraw(\_request, \_sigs, \_signers, \_powers);
}

```
From the point of view of the Celer bridge, the initial depositor of the tokens is the `SocketGateway`. As a consequence, the Celer contract transfers the tokens to be refunded to the gateway. The gateway is then in charge of forwarding the tokens to the initial depositor. To achieve this, it keeps a mapping of unique transfer IDs to depositor addresses. Once a refund is processed, the corresponding address in the mapping is reset to the zero address.


Looking at the `withdraw` function of the Celer pool, we see that for some tokens, it is possible that the reimbursement will not be processed directly, but only after some delay. From the gateway point of view, the reimbursement will be marked as successful, and the address of the original sender corresponding to this transfer ID will be reset to address(0).



```
if (delayThreshold > 0 && wdmsg.amount > delayThreshold) {
     _addDelayedTransfer(wdId, wdmsg.receiver, wdmsg.token, wdmsg. // <--- here
} else {
      _sendToken(wdmsg.receiver, wdmsg.token, wdmsg.
}

```
It is then the responsibility of the user, once the locking delay has passed, to call another function to claim the tokens. Unfortunately, in our case, this means that the funds will be sent back to the gateway contract and not to the original sender. Because the gateway implements `rescueEther`, and `rescueFunds` functions, the admin might be able to send the funds back to the user. However, this requires manual intervention and breaks the trustlessness assumptions of the system. Also, in that case, there is no easy way to trace back the original address of the sender, that corresponds to this refund.


However, there is an additional issue that might allow an attacker to steal some funds from the gateway. Indeed, when claiming the refund, if it is in ETH, the gateway will have some balance when the transaction completes. Any user can then call any function that consumes the gateway balance, such as the `swapAndBridge` from `CelerImpl`, to steal the refunded ETH. That is possible as the function relies on a user-provided amount as an input, and not on `msg.value`.
Additionally, if the refund is an ERC-20, an attacker can steal the funds by calling `bridgeAfterSwap` or `swapAndBridge` from the `Stargate` or `Celer` routes with the right parameters.


**src/bridges/cbridge/CelerImpl.sol:L120-L127**



```
function bridgeAfterSwap(
    uint256 amount,
    bytes calldata bridgeData
) external payable override {
    CelerBridgeData memory celerBridgeData = abi.decode(
        bridgeData,
        (CelerBridgeData)
    );

```
**src/bridges/stargate/l2/Stargate.sol:L183-L186**



```
function swapAndBridge(
    uint32 swapId,
    bytes calldata swapData,
    StargateBridgeDataNoToken calldata stargateBridgeData

```
Note that this violates the security assumption: “The contracts are not supposed to hold any funds post-tx execution.”


#### Recommendation


Make sure that `CelerImpl` supports also the delayed withdrawals functionality and that withdrawal requests are deleted only if the receiver has received the withdrawal in a single transaction.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Socket |
| Report Date | N/A |
| Finders | David Oz,  George Kobakhidze
 |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2023/02/socket/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

