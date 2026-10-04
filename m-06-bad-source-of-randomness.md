---
# Core Classification
protocol: Holograph
chain: everychain
category: uncategorized
vulnerability_type: vrf

# Attack Vector Details
attack_type: vrf
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5599
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-10-holograph-contest
source_link: https://code4rena.com/reports/2022-10-holograph
github_link: https://github.com/code-423n4/2022-10-holograph-findings/issues/427

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
  - vrf

protocol_categories:
  - dexes
  - bridge
  - services
  - launchpad
  - nft_marketplace

# Audit Details
report_date: unknown
finders_count: 10
finders:
  - d3e4
  - __141345__
  - Deivitto
  - cdahlheimer
  - ladboy233
---

## Vulnerability Title

[M-06] Bad source of randomness

### Overview


This bug report is about the vulnerability of using block.number and block.timestamp as a source of randomness in the code located at https://github.com/code-423n4/2022-10-holograph/blob/f8c2eae866280a1acfdc8a8352401ed031be1373/contracts/HolographOperator.sol#L491-L511. It is commonly advised against using these sources as the outcome can be manipulated by calling contracts. A malicious actor with access to the layer-zero-endpoint could retry the selection of the primary operator until the result is favorable to them. The attack consists of repeatedly calling the attack function with data that is known and output that is wished for until the results match and only then continuing to calling the operator. Manual review was used to identify the vulnerability. It is recommended to consider using a decentralized oracle for the generation of random numbers, such as Chainlinks VRF. However, considering the prerequirement of the layer-zero endpoint being compromised, using an unrecommended source of randomness may be acceptable.

### Original Finding Content


[HolographOperator.sol#L491-L511](https://github.com/code-423n4/2022-10-holograph/blob/f8c2eae866280a1acfdc8a8352401ed031be1373/contracts/HolographOperator.sol#L491-L511)<br>

Using `block.number` and `block.timestamp` as a source of randomness is commonly advised against, as the outcome can be manipulated by calling contracts. In this case a compromised layer-zero-endpoint would be able to retry the selection of the primary operator until the result is favorable to the malicious actor.

### Proof of Concept

An attack path for rerolling the result of bad randomness might look roughly like this:

```js
function attack(uint256 currentNonce, uint256 wantedPodIndex, uint256 numPods, uint256 wantedOperatorIndex, uint256 numOperators,  bytes calldata bridgeInRequestPayload) external{

    bytes32 jobHash = keccak256(bridgeInRequestPayload);

    //same calculation as in HolographOperator.crossChainMessage
    uint256 random = uint256(keccak256(abi.encodePacked(jobHash, currentNonce, block.number, block.timestamp)));

    require(wantedPodIndex == random % numPods)
    require(wantedOperatorIndex == random % numOperators);

    operator.crossChainMessage(bridgeInRequestPayload);
}
```

The attack basically consists of repeatedly calling the `attack` function with data that is known and output that is wished for until the results match and only then continuing to calling the operator.

### Recommended Mitigation Steps

Consider using a decentralized oracle for the generation of random numbers, such as [Chainlinks VRF](https://docs.chain.link/docs/vrf/v2/introduction/).

It should be noted, that in this case there is a prerequirement of the layer-zero endpoint being compromised, which confines the risk quite a bit, so using a normally unrecommended source of randomness could be acceptable here, considering the tradeoffs of integrating a decentralized oracle.

**[ACC01ADE (Holograph) confirmed and commented](https://github.com/code-423n4/2022-10-holograph-findings/issues/427#issuecomment-1308894416):**
 > Very valid issue.

**[gzeon (judge) commented](https://github.com/code-423n4/2022-10-holograph-findings/issues/427#issuecomment-1320939907):**
 > While sponsor noted this is a design choice to use pseudorandomness, as pointed out by the warden a compromised layer-zero-endpoint can exploit this for profit, judging this as Medium risk.



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
| Finders | d3e4, __141345__, Deivitto, cdahlheimer, ladboy233, nadin, teawaterwire, adriro, V_B, minhtrng |

### Source Links

- **Source**: https://code4rena.com/reports/2022-10-holograph
- **GitHub**: https://github.com/code-423n4/2022-10-holograph-findings/issues/427
- **Contest**: https://code4rena.com/contests/2022-10-holograph-contest

### Keywords for Search

`VRF`

