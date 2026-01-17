---
# Core Classification
protocol: Malda
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62723
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/1029
source_link: none
github_link: https://github.com/sherlock-audit/2025-07-malda-judging/issues/124

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
finders_count: 9
finders:
  - cergyk
  - ExtraCaterpillar
  - bulgari
  - elolpuer
  - axelot
---

## Vulnerability Title

H-1: Rebalancer can steal funds from markets by sending to custom receiver through Everclear Bridge

### Overview


The bug report discusses a potential issue found by a group of people in the rebalancer contract of the Malda Protocol. The contract allows for a message to be sent in the form of bytes, which is specific to the bridge contract. However, it was found that the parameter for the receiver was left unchecked, meaning that the rebalancer could potentially steal user funds by providing an address controlled by it. The recommendation is to check that the receiver is a valid market on the destination chain. The protocol team has already fixed this issue in a recent update. 

### Original Finding Content


Source: https://github.com/sherlock-audit/2025-07-malda-judging/issues/124 

## Found by 
Angry\_Mustache\_Man, ExtraCaterpillar, SafetyBytes, Sevyn, Ziusz, axelot, bulgari, cergyk, elolpuer

### Description
The rebalancer contract is called on `sendMsg` with a message encoded as bytes (`_msg.message`). This message is specific for the bridge contract, and in the case of `EverclearBridge` it is of the form `IntentParams`:

[EverclearBridge.sol#L40-L50](https://github.com/sherlock-audit/2025-07-malda/blob/main/malda-lending/src/rebalancer/bridges/EverclearBridge.sol#L40-L50):
```solidity
    struct IntentParams {
        uint32[] destinations;
        //@audit receiver is left unchecked
        bytes32 receiver;
        address inputAsset;
        bytes32 outputAsset;
        uint256 amount;
        uint24 maxFee;
        uint48 ttl;
        bytes data;
        IFeeAdapter.FeeParams feeParams;
    }
```

We notice that the parameter `receiver` is left entirely unchecked, and the rebalancer EOA can provide an address controlled by it, stealing the user funds which should be send for rebalancing.

[EverclearBridge.sol#L111-L121](https://github.com/sherlock-audit/2025-07-malda/blob/main/malda-lending/src/rebalancer/bridges/EverclearBridge.sol#L111-L121):
```solidity
(bytes32 id,) = everclearFeeAdapter.newIntent(
    params.destinations,
    params.receiver,
    params.inputAsset,
    params.outputAsset,
    params.amount,
    params.maxFee,
    params.ttl,
    params.data,
    params.feeParams
);
```

### Recommendation

Check that `params.receiver` is a valid market on the destination chain


## Discussion

**sherlock-admin2**

The protocol team fixed this issue in the following PRs/commits:
https://github.com/malda-protocol/malda-lending/pull/103


**CergyK**

Fix looks good, now `params.receiver` is forced to be equal to `_market`





### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Malda |
| Report Date | N/A |
| Finders | cergyk, ExtraCaterpillar, bulgari, elolpuer, axelot, Angry\_Mustache\_Man, Sevyn, SafetyBytes, Ziusz |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-07-malda-judging/issues/124
- **Contest**: https://app.sherlock.xyz/audits/contests/1029

### Keywords for Search

`vulnerability`

