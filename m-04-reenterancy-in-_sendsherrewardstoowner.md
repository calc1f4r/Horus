---
# Core Classification
protocol: Sherlock
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42450
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-01-sherlock
source_link: https://code4rena.com/reports/2022-01-sherlock
github_link: https://github.com/code-423n4/2022-01-sherlock-findings/issues/60

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
  - liquid_staking
  - dexes
  - bridge
  - cdp
  - yield

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-04] Reenterancy in `_sendSherRewardsToOwner()`

### Overview


This bug report discusses a vulnerability in the SHER contract that could allow an attacker to drain the entire balance of the contract. The vulnerability involves reentrancy, which means that the attacker can repeatedly call certain functions to manipulate the contract and take control of its execution. This vulnerability can only be exploited if the contract implements ERC777 or makes external calls during the transfer function. The report also includes a proof of concept and steps to reproduce the attack. The recommended mitigation steps include adding a reentrancy guard or using the checks-effects-interactions pattern to prevent external calls from being made before all necessary checks and state changes are completed. The severity of the bug was initially considered high, but was later downgraded to medium as the SHER token does not currently have any hooks for external calls. The bug has since been resolved.

### Original Finding Content

_Submitted by kirk-baird_

This is a reentrancy vulnerability that would allow the attacker to drain the entire SHER balance of the contract.

Note: this attack requires gaining control of execution `sher.transfer()` which will depend on the implementation of the SHER token. Control may be gained by the attacker if the contract implements ERC777 or otherwise makes external calls during `transfer()`.

### Proof of Concept

See [\_sendSherRewards](https://github.com/code-423n4/2022-01-sherlock/blob/main/contracts/Sherlock.sol#L442)

```solidity
  function _sendSherRewardsToOwner(uint256 _id, address _nftOwner) internal {
    uint256 sherReward = sherRewards_[_id];
    if (sherReward == 0) return;

    // Transfers the SHER tokens associated with this NFT ID to the address of the NFT owner
    sher.safeTransfer(_nftOwner, sherReward);
    // Deletes the SHER reward mapping for this NFT ID
    delete sherRewards_[_id];
  }
```

Here `sherRewards` are deleted after the potential external call is made in `sher.safeTransfer()`. As a result if an attacker reenters this function `sherRewards_` they will still maintain the original balance of rewards and again transfer the SHER tokens.

As `_sendSherRewardsToOwner()` is `internal` the attack can be initiated through the `external` function `ownerRestake()` [see here.](https://github.com/code-423n4/2022-01-sherlock/blob/main/contracts/Sherlock.sol#L595)

Steps to produce the attack:

1.  Deploy attack contract to handle reenterancy
2.  Call `initialStake()` from the attack contract with the smallest `period`
3.  Wait for `period` amount of time to pass
4.  Have the attack contract call `ownerRestake()`. The attack contract will gain control of the (See note above about control flow). This will recursively call `ownerRestake()` until the balance of `Sherlock` is 0 or less than the user's reward amount. Then allow reentrancy loop to unwind and complete.

### Recommended Mitigation Steps

Reentrancy can be mitigated by one of two solutions.

The first option is to add a reentrancy guard like `nonReentrant` the is used in `SherlockClaimManager.sol`.

The second option is to use the checks-effects-interactions pattern. This would involve doing all validation checks and state changes before making any potential external calls. For example the above function could be modified as follows.

```solidity
  function _sendSherRewardsToOwner(uint256 _id, address _nftOwner) internal {
    uint256 sherReward = sherRewards_[_id];
    if (sherReward == 0) return;

    // Deletes the SHER reward mapping for this NFT ID
    delete sherRewards_[_id];

    // Transfers the SHER tokens associated with this NFT ID to the address of the NFT owner
    sher.safeTransfer(_nftOwner, sherReward);
  }
```

Additionally the following functions are not exploitable however should be updated to use the check-effects-interations pattern.

*   `Sherlock._redeemShares()` should do `_transferTokensOut()` last.
*   `Sherlock.initialStake()` should do `token.safeTransferFrom(msg.sender, address(this), _amount);` last
*   `SherClaim.add()` should do `sher.safeTransferFrom(msg.sender, address(this), _amount);` after updating `userClaims`
*   `SherlockProtocolManager.depositToActiveBalance()` should do `token.safeTransferFrom(msg.sender, address(this), _amount);` after updating `activeBalances`

**[Evert0x (Sherlock) confirmed, but disagreed with High severity and commented](https://github.com/code-423n4/2022-01-sherlock-findings/issues/60#issuecomment-1029420896):**
 > Good find. I think it's med-risk as it depends on the implementation of SHER token (does it allow callbacks).

**[Jack the Pug (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2022-01-sherlock-findings/issues/60#issuecomment-1064200957):**
 > Downgrade to `Med` as the SHER token is a known token that currently comes with no such hooks like ERC777.

 **[Evert0x (Sherlock) resolved](https://github.com/code-423n4/2022-01-sherlock-findings/issues/60)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Sherlock |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-01-sherlock
- **GitHub**: https://github.com/code-423n4/2022-01-sherlock-findings/issues/60
- **Contest**: https://code4rena.com/reports/2022-01-sherlock

### Keywords for Search

`vulnerability`

