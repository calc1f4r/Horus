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
solodit_id: 32314
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-02-tapioca
source_link: https://code4rena.com/reports/2024-02-tapioca
github_link: https://github.com/code-423n4/2024-02-tapioca-findings/issues/142

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
finders_count: 10
finders:
  - carrotsmuggler
  - 3
  - ronnyx2017
  - immeas
  - cccz
---

## Vulnerability Title

[H-03] Absence of restrictions on the sender of the `twTAP.claimsReward()` function could enable attackers to freeze reward tokens within the Tap token contract

### Overview


The bug report discusses an issue with the function `twTAP.claimRewards()` in the `twTAP.sol` contract. This function is used to claim rewards for a specific position identified by `_tokenId`. The report explains that anyone can trigger this function as long as the receiver of the reward, `_to`, is either the owner of the position or an approved address. However, an attacker can exploit this by inserting a transaction to claim the rewards before the actual receiver can do so, resulting in the rewards being trapped in the contract. The report also suggests a mitigation step to update the function to restrict who can trigger it. 

### Original Finding Content


<https://github.com/Tapioca-DAO/tap-token/blob/20a83b1d2d5577653610a6c3879dff9df4968345/contracts/governance/twTAP.sol#L396-L404> 

The function `twTAP.claimRewards()` is utilized to claim the reward distributed to the position identified by `_tokenId`.

```solidity
function claimRewards(uint256 _tokenId, address _to)
    external
    nonReentrant
    whenNotPaused
    returns (uint256[] memory amounts_)
{
    _requireClaimPermission(_to, _tokenId);
    amounts_ = _claimRewards(_tokenId, _to);
}
```

This function can be triggered by anyone, provided that the receiver of the claimed reward `_to` is either the owner of the position or an address approved by the position's owner.

In the function `TapTokenReceiver._claimTwpTapRewardsReceiver()`, the `twTAP.claimRewards()` function is invoked at [line 156](https://github.com/Tapioca-DAO/tap-token/blob/20a83b1d2d5577653610a6c3879dff9df4968345/contracts/tokens/TapTokenReceiver.sol#L156) to calculate the reward assigned to `_tokenId` and claim the reward to this contract before transferring it to the receiver on another chain. To achieve this, the position's owner must first approve this contract to access the position before executing the function.

```solidity
function _claimTwpTapRewardsReceiver(bytes memory _data) internal virtual twTapExists {
    ClaimTwTapRewardsMsg memory claimTwTapRewardsMsg_ = TapTokenCodec.decodeClaimTwTapRewardsMsg(_data);
    uint256[] memory claimedAmount_ = twTap.claimRewards(claimTwTapRewardsMsg_.tokenId, address(this));

    ...
}
```

However, between the call to grant approval to the contract and the execution of the `_claimTwpTapRewardsReceiver()` function, an attacker can insert a transaction calling `twTAP.claimRewards(_tokenId, TapTokenReceiver)`. By doing so, the rewards will be claimed to the `TapTokenReceiver` contract before the `_claimTwpTapRewardsReceiver()` function is invoked. Consequently, the return value of `claimedAmount_ = twTap.claimRewards(claimTwTapRewardsMsg_.tokenId, address(this))` within the function will be `0` for all elements, resulting in no rewards being claimed for the receiver. As a result, the reward tokens will become trapped in the contract.

In the event that the sender utilizes multiple LayerZero composed messages containing two messages:

- Permit message: to approve permission of `_tokenId` to the `TapTokenReceiver` contract.
- Claim reward message: to trigger the `_claimTwpTapRewardsReceiver()` function and claim the reward.

The attacker cannot insert any `twTAP.claimRewards()` between these two messages, as they are executed within the same transaction on the destination chain. However, the permit message can be triggered by anyone, not just the contract `TapTokenReceiver`. The attacker can thus trigger the permit message on the destination chain and subsequently call the `twTAP.claimRewards()` function before the `_claimTwpTapRewardsReceiver()` message is delivered on the destination chain.

### Impact

The reward tokens will become trapped within the `TapTokenReceiver` contract.

### Recommended Mitigation Steps

Consider updating the function `twTAP.claimRewards()` as depicted below to impose restrictions on who can invoke this function:

```solidity
function claimRewards(uint256 _tokenId, address _to)
    external
    nonReentrant
    whenNotPaused
    returns (uint256[] memory amounts_)
{
    _requireClaimPermission(msg.sender, _tokenId);
    _requireClaimPermission(_to, _tokenId);
    amounts_ = _claimRewards(_tokenId, _to);
}
```

**[0xRektora (Tapioca) confirmed via duplicate Issue #120](https://github.com/code-423n4/2024-02-tapioca-findings/issues/120#issuecomment-2016850113)**

**[0xRektora (Tapioca) commented](https://github.com/code-423n4/2024-02-tapioca-findings/issues/142#issuecomment-2054134428):**
 > Just as reference, the proposed mitigation will not work, because in this context `msg.sender == _to`.

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
| Finders | carrotsmuggler, 3, ronnyx2017, immeas, cccz, 1, ladboy233, 2, KIntern\_NA |

### Source Links

- **Source**: https://code4rena.com/reports/2024-02-tapioca
- **GitHub**: https://github.com/code-423n4/2024-02-tapioca-findings/issues/142
- **Contest**: https://code4rena.com/reports/2024-02-tapioca

### Keywords for Search

`vulnerability`

