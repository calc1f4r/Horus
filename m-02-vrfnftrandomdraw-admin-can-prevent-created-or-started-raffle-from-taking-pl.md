---
# Core Classification
protocol: Forgeries
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6397
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-12-forgeries-contest
source_link: https://code4rena.com/reports/2022-12-forgeries
github_link: https://github.com/code-423n4/2022-12-forgeries-findings/issues/101

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - services
  - synthetics
  - gaming

# Audit Details
report_date: unknown
finders_count: 7
finders:
  - codeislight
  - BAHOZ
  - gasperpre
  - trustindistrust
  - 0xdeadbeef0x
---

## Vulnerability Title

[M-02] VRFNFTRandomDraw admin can prevent created or started raffle from taking place

### Overview


This bug report is about a vulnerability in the `VRFNFTRandomDraw` contract. The admin/owner of the contract can start a raffle including emitting the `SetupDraw` event, but in a way that ensures `fulfillRandomWords()` is never called. This can be done by providing an invalid `keyHash` to `coordinator.requestRandomWords()` or by ensuring that the owner-provided chain.link VRF subscription does not have sufficient funds to pay at the time the oracle attempts to supply random values. The recommended mitigation step is to make a successful callback to `fulfillRandomWords()` a precondition of the admin/owner reclaiming the reward NFT. This will help ensure the owner does not create raffles that they intend will never pay out a reward.

### Original Finding Content


<https://github.com/code-423n4/2022-12-forgeries/blob/fc271cf20c05ce857d967728edfb368c58881d85/src/VRFNFTRandomDraw.sol#L173> 

<https://github.com/code-423n4/2022-12-forgeries/blob/fc271cf20c05ce857d967728edfb368c58881d85/src/VRFNFTRandomDraw.sol#L162-L168>

### Impact

The admin/owner of `VRFNFTRandomDraw` can `startDraw()` a raffle, including emitting the `SetupDraw` event, but in a way that ensures `fulfillRandomWords()` is never called. For example:

*   `keyHash` is not validated within `coordinator.requestRandomWords()`. Providing an invalid `keyHash` will allow the raffle to start but prevent the oracle from actually supplying a random value to determine the raffle result.
    *   <https://github.com/smartcontractkit/chainlink/blob/00f9c6e41f843f96108cdaa118a6ca740b11df35/contracts/src/v0.8/VRFCoordinatorV2.sol#L407-L409>
    *   <https://github.com/code-423n4/2022-12-forgeries/blob/fc271cf20c05ce857d967728edfb368c58881d85/src/VRFNFTRandomDraw.sol#L163>
*   The admin/owner could alternatively ensure that the owner-provided chain.link VRF subscription does not have sufficient funds to pay at the time the oracle attempts to supply random values in `fulfillRandomWords()`.
    *   <https://github.com/smartcontractkit/chainlink/blob/00f9c6e41f843f96108cdaa118a6ca740b11df35/contracts/src/v0.8/VRFCoordinatorV2.sol#L594-L596>

In addition, the owner/admin could simply avoid ever calling `startDraw()` in the first place.

### Proof of Concept

Provide direct links to all referenced code in GitHub. Add screenshots, logs, or any other relevant proof that illustrates the concept.

### Recommended Mitigation Steps

Depending on the desired functionality with respect to the raffle owner, a successful callback to `fulfillRandomWords()` could be a precondition of the admin/owner reclaiming the reward NFT. This would help ensure the owner does not create raffles that they intend will never pay out a reward.

**[iainnash (Forgeries) confirmed](https://github.com/code-423n4/2022-12-forgeries-findings/issues/101#issuecomment-1448782416)**


***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Forgeries |
| Report Date | N/A |
| Finders | codeislight, BAHOZ, gasperpre, trustindistrust, 0xdeadbeef0x, deliriusz, 9svR6w |

### Source Links

- **Source**: https://code4rena.com/reports/2022-12-forgeries
- **GitHub**: https://github.com/code-423n4/2022-12-forgeries-findings/issues/101
- **Contest**: https://code4rena.com/contests/2022-12-forgeries-contest

### Keywords for Search

`vulnerability`

