---
# Core Classification
protocol: ParaSpace
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25729
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-11-paraspace
source_link: https://code4rena.com/reports/2022-11-paraspace
github_link: https://github.com/code-423n4/2022-11-paraspace-findings/issues/481

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
  - dexes
  - cdp
  - services
  - cross_chain
  - indexes

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Trust
  - 0x52
  - ladboy233
---

## Vulnerability Title

[M-19] Rewards are not accounted for properly in NTokenApeStaking contracts, limiting user's collateral

### Overview


This bug report is about an issue with the ApeStakingLogic.sol contracts, which are used to stake ape coins through the NTokenApeStaking NFT. The important function getTokenIdStakingAmount() returns the entire stake amount mapping for a specific BAYC / MAYC NFT, but the calculation does not include the pendingRewards for the BAKC staked amount, which accrues over time as well. As a result, getTokenIdStakingAmount() returns a value lower than the correct user balance. This function is used in PTokenSApe.sol's balanceOf function, which is supposed to reflect the user's current balance in ape staking. When user unstakes their ape tokens, they will receive their fair share of rewards, but because balanceOf() shows a lower value, the rewards do not count as collateral for user's debt.

The impact of this bug is that rewards are not accounted for properly in NTokenApeStaking contracts, limiting user's collateral. The recommended mitigation steps to fix this issue is to make sure that the balance calculation includes pendingRewards from BAKC tokens if they exist.

### Original Finding Content


<https://github.com/code-423n4/2022-11-paraspace/blob/c6820a279c64a299a783955749fdc977de8f0449/paraspace-core/contracts/protocol/tokenization/libraries/ApeStakingLogic.sol#L253>

ApeStakingLogic.sol implements the logic for staking ape coins through the NTokenApeStaking NFT.

`getTokenIdStakingAmount()` is an important function which returns the entire stake amount mapping for a specific BAYC / MAYC NFT.

    function getTokenIdStakingAmount(
        uint256 poolId,
        ApeCoinStaking _apeCoinStaking,
        uint256 tokenId
    ) public view returns (uint256) {
        (uint256 apeStakedAmount, ) = _apeCoinStaking.nftPosition(
            poolId,
            tokenId
        );
        uint256 apeReward = _apeCoinStaking.pendingRewards(
            poolId,
            address(this),
            tokenId
        );
        (uint256 bakcTokenId, bool isPaired) = _apeCoinStaking.mainToBakc(
            poolId,
            tokenId
        );
        if (isPaired) {
            (uint256 bakcStakedAmount, ) = _apeCoinStaking.nftPosition(
                BAKC_POOL_ID,
                bakcTokenId
            );
            apeStakedAmount += bakcStakedAmount;
        }
        return apeStakedAmount + apeReward;
    }

We can see that the total returned amount is the staked amount through the direct NFT, plus rewards for the direct NFT, plus the staked amount of the BAKC token paired to the direct NFT. However, the calculation does not include the pendingRewards for the BAKC staked amount, which accrues over time as well.

As a result, getTokenIdStakingAmount() returns a value lower than the correct user balance. This function is used in PTokenSApe.sol's balanceOf function, as this type of PToken is supposed to reflect the user's current balance in ape staking.

When user unstakes their ape tokens through executeUnstakePositionAndRepay, they will receive their fair share of rewards.It will call ApeCoinStaking's \_withdrawPairNft which will claim rewards also for BAKC tokens. However, because balanceOf() shows a lower value, the rewards not count as collateral for user's debt, which is a major issue for lending platforms.

### Impact

Rewards are not accounted for properly in NTokenApeStaking contracts, limiting user's collateral.

### Recommended Mitigation Steps

Balance calculation should include pendingRewards from BAKC tokens if they exist.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | ParaSpace |
| Report Date | N/A |
| Finders | Trust, 0x52, ladboy233 |

### Source Links

- **Source**: https://code4rena.com/reports/2022-11-paraspace
- **GitHub**: https://github.com/code-423n4/2022-11-paraspace-findings/issues/481
- **Contest**: https://code4rena.com/reports/2022-11-paraspace

### Keywords for Search

`vulnerability`

