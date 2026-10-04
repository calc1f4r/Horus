---
# Core Classification
protocol: Connext NXTP — Noncustodial Xchain Transfer Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13329
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2021/07/connext-nxtp-noncustodial-xchain-transfer-protocol/
github_link: none

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
  - services
  - synthetics

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Martin Ortner
  -  Heiko Fisch

  -  David Oz Kashi
---

## Vulnerability Title

TransactionManager - Relayer may use user’s cancel after expiry signature to steal user’s funds by colluding with a router  Acknowledged

### Overview


This bug report is about a risk situation where a relayer can collude with a router and use the user's "cancel" signature to withdraw both the user's and the router's funds. This is caused by the same signature being used for both services, allowing the router to withdraw funds before the expiry. As an immediate mitigation, sender-side cancellation via signature has been removed completely.

The recommendation is that the user must never sign a “cancel” that could be used on the receiving chain while fulfillment on the sending chain is still a possibility. To put it differently, the user may only sign a “cancel” that is valid on the receiving chain after sending-chain expiry or if they never have and won’t ever sign a “fulfill”. In order to make this easier to follow, it is suggested that different signatures for sending- and receiving-chain cancellations be used.

### Original Finding Content

#### Resolution



This has been acknowledged by the Connext team. As discussed below in the “Recommendation”, it is not a flaw in the contracts *per se* but rather a high-risk situation caused by cancellation signatures working on both sender and receiver side.
As immediate mitigation, sender-side cancellation via signature has been removed completely. The “signature rules” explained below still apply and have to be followed.


#### Description


Users that are willing to have a lower trust dependency on a relayer should have the ability to opt-in **only** for the service that allows the relayer to withdraw back users’ funds from the sending chain after expiry. However, in practice, a user is forced to opt-in for the service that refunds the router before the expiry, since the same signature is used for both services (lines 795,817 use the same signature).


Let’s consider the case of a user willing to call `fulfill` on his own, but to use the relayer only to withdraw back his funds from the sending chain after expiry. In this case, the relayer can collude with the router and use the user’s `cancel` signature (meant for withdrawing **his** only after expiry) as a front-running transaction for a user call to `fulfill`. This way the router will be able to withdraw both his funds and the user’s funds since the user’s `fulfill` signature is now public data residing in the mem-pool.


#### Examples


**code/packages/contracts/contracts/TransactionManager.sol:L795-L817**



```
      require(msg.sender == txData.user || recoverSignature(txData.transactionId, relayerFee, "cancel", signature) == txData.user, "#C:022");

      Asset.transferAsset(txData.sendingAssetId, payable(msg.sender), relayerFee);
    }

    // Get the amount to refund the user
    uint256 toRefund;
    unchecked {
      toRefund = amount - relayerFee;
    }

    // Return locked funds to sending chain fallback
    if (toRefund > 0) {
      Asset.transferAsset(txData.sendingAssetId, payable(txData.sendingChainFallback), toRefund);
    }
  }

} else {
  // Receiver side, router liquidity is returned
  if (txData.expiry >= block.timestamp) {
    // Timeout has not expired and tx may only be cancelled by user
    // Validate signature
    require(msg.sender == txData.user || recoverSignature(txData.transactionId, relayerFee, "cancel", signature) == txData.user, "#C:022");

```
#### Recommendation


The crucial point here is that the user must never sign a “cancel” that could be used on the receiving chain while fulfillment on the sending chain is still a possibility.  

Or, to put it differently: A user may only sign a “cancel” that is valid on the receiving chain after sending-chain expiry or if they never have and won’t ever sign a “fulfill” (or at least won’t sign until sending-chain expiry — but it is pointless to sign a “fulfill” after that, so “never” is a reasonable simplification).  

Or, finally, a more symmetric perspective on this requirement: If a user has signed “fulfill”, they must not sign a receiving-chain-valid “cancel” until sending-chain expiry, and if they have signed a receiving-chain-valid “cancel”, they must not sign a “fulfill” (until sending-chain expiry).


In this sense, “cancel” signatures that are valid on the receiving chain are dangerous, while sending-side cancellations are not. So the principle stated in the previous paragraph might be easier to follow with different signatures for sending- and receiving-chain cancellations.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Connext NXTP — Noncustodial Xchain Transfer Protocol |
| Report Date | N/A |
| Finders | Martin Ortner,  Heiko Fisch
,  David Oz Kashi |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2021/07/connext-nxtp-noncustodial-xchain-transfer-protocol/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

