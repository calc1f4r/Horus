---
# Core Classification
protocol: Stakehouse Protocol
chain: everychain
category: uncategorized
vulnerability_type: don't_update_state

# Attack Vector Details
attack_type: don't_update_state
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5937
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-11-lsd-network-stakehouse-contest
source_link: https://code4rena.com/reports/2022-11-stakehouse
github_link: https://github.com/code-423n4/2022-11-stakehouse-findings/issues/410

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
  - don't_update_state

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Trust
---

## Vulnerability Title

[M-29] User receives less rewards than they are eligible for if first passed BLS key is inactive

### Overview


This bug report is about an issue with the StakingFundsVault in the code-423n4/2022-11-stakehouse repository. The claimRewards() function is used to allow users to withdraw profits. The issue is that updateAccumulatedETHPerLP() is not guaranteed to be called, which means the ETH reward distribution in _distribute would use stale value, and users will not receive as many rewards as they should. This happens when the first BLS public key is inactive. The impact of this bug is that users receive less rewards than they are eligible for. The bug was found with a manual audit. The recommended mitigation step is to call updateAccumulatedETHPerLP() at the start of the function.

### Original Finding Content


<https://github.com/code-423n4/2022-11-stakehouse/blob/4b6828e9c807f2f7c569e6d721ca1289f7cf7112/contracts/liquid-staking/StakingFundsVault.sol#L224>

StakingFundsVault has the claimRewards() function to allow users to withdraw profits.

    function claimRewards(
        address _recipient,
        bytes[] calldata _blsPubKeys
    ) external nonReentrant {
        for (uint256 i; i < _blsPubKeys.length; ++i) {
            require(
                liquidStakingNetworkManager.isBLSPublicKeyBanned(_blsPubKeys[i]) == false,
                "Unknown BLS public key"
            );
            // Ensure that the BLS key has its derivatives minted
            require(
                getAccountManager().blsPublicKeyToLifecycleStatus(_blsPubKeys[i]) == IDataStructures.LifecycleStatus.TOKENS_MINTED,
                "Derivatives not minted"
            );
            if (i == 0 && !Syndicate(payable(liquidStakingNetworkManager.syndicate())).isNoLongerPartOfSyndicate(_blsPubKeys[i])) {
                // Withdraw any ETH accrued on free floating SLOT from syndicate to this contract
                // If a partial list of BLS keys that have free floating staked are supplied, then partial funds accrued will be fetched
                _claimFundsFromSyndicateForDistribution(
                    liquidStakingNetworkManager.syndicate(),
                    _blsPubKeys
                );
                // Distribute ETH per LP
                updateAccumulatedETHPerLP();
            }
            // If msg.sender has a balance for the LP token associated with the BLS key, then send them any accrued ETH
            LPToken token = lpTokenForKnot[_blsPubKeys[i]];
            require(address(token) != address(0), "Invalid BLS key");
            require(token.lastInteractedTimestamp(msg.sender) + 30 minutes < block.timestamp, "Last transfer too recent");
            _distributeETHRewardsToUserForToken(msg.sender, address(token), token.balanceOf(msg.sender), _recipient);
        }
    }

The issue is that `updateAccumulatedETHPerLP()` is not guaranteed to be called, which means the ETH reward distribution in \_distribute would use stale value, and users will not receive as many rewards as they should.<br>
`updateAccumulatedETHPerLP` is only called if the first BLS public key is part of the syndicate. However, for the other keys it makes no reason not to use the up to date accumulatedETHPerLPShare value.

### Impact

User receives less rewards than they are eligible for if first passed BLS key is inactive.

### Recommended Mitigation Steps

Call updateAccumulatedETHPerLP() at the start of the function.

**[vince0656 (Stakehouse) confirmed and commented](https://github.com/code-423n4/2022-11-stakehouse-findings/issues/410#issuecomment-1329370912):**
 > This is a dupe of issue [408 (M-28)](https://github.com/code-423n4/2022-11-stakehouse-findings/issues/408)

**[LSDan (judge) commented](https://github.com/code-423n4/2022-11-stakehouse-findings/issues/410#issuecomment-1335919764):**
 > I've asked the warden to come in and highlight the differences between this and M-28.

**[Trust (warden) commented](https://github.com/code-423n4/2022-11-stakehouse-findings/issues/410#issuecomment-1335928402):**
 > Hi. Both rewards show different ways in which users don't receive their eligible rewards.<br>
> 
> This report talks about use of an old accumulatedETHPerLPShare in the call to _distributeETHRewardsToUserForToken(). It will happen in any case where we don't go into the if block. Using an old value means users won't receive as much rewards as have been unlocked.<br>
> The second report (M-28) is about _claimFundsFromSyndicateForDistribution not being called although it should be. suppose the blsPubKeys array has first element which is no longer part of syndicate, but the rest of the array are part of syndicate. Then we skip claiming funds from them. Therefore, there will be less funds to give away as rewards.
> 
> One report is about incorrect *share value* leak, the second is about *total rewards* leak.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Stakehouse Protocol |
| Report Date | N/A |
| Finders | Trust |

### Source Links

- **Source**: https://code4rena.com/reports/2022-11-stakehouse
- **GitHub**: https://github.com/code-423n4/2022-11-stakehouse-findings/issues/410
- **Contest**: https://code4rena.com/contests/2022-11-lsd-network-stakehouse-contest

### Keywords for Search

`Don't update state`

