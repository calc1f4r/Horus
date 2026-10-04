---
# Core Classification
protocol: Ajna Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20078
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-05-ajna
source_link: https://code4rena.com/reports/2023-05-ajna
github_link: https://github.com/code-423n4/2023-05-ajna-findings/issues/132

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
finders_count: 3
finders:
  - shealtielanz
  - ABAIKUNANBAEV
  - Jorgect
---

## Vulnerability Title

[H-10] missing `isEpochClaimed` validation

### Overview


A bug has been found in the Ajna codebase, which allows users to claim rewards even when they have already been claimed. This is due to the \_claimRewards function not validating if isEpochClaimed mapping is true. This function is used in the claimRewards and moveStakedLiquidity functions, but the latter is calling \_claimRewards without validating if isEpochClaimed is true, which allows malicious users to claim rewards each time they want.

The recommended mitigation steps for this bug are to check if the isEpochClaime is true and revert in the \_claimReward function. This can be done by adding the following statement to the code:

`if (isEpochClaimed[tokenId_][epochToClaim_]) revert AlreadyClaimed();`

### Original Finding Content


User can claim rewards even when is already claimed

### Proof of Concept

The \_claimRewards function is using to calculate and send the reward to the caller but this function is no validating if isEpochClaimed mapping is true due that in claimRewards function is validated, see the stament in the following lines:

    file: ajna-core/src/RewardsManager.sol
    function claimRewards(
            uint256 tokenId_,
            uint256 epochToClaim_ 
        ) external override {
            StakeInfo storage stakeInfo = stakes[tokenId_];

            if (msg.sender != stakeInfo.owner) revert NotOwnerOfDeposit(); 

            if (isEpochClaimed[tokenId_][epochToClaim_]) revert AlreadyClaimed(); // checking if the epoch was claimed;

            _claimRewards(
                stakeInfo,
                tokenId_,
                epochToClaim_,
                true,
                stakeInfo.ajnaPool
            );
        }

<https://github.com/code-423n4/2023-05-ajna/blob/276942bc2f97488d07b887c8edceaaab7a5c3964/ajna-core/src/RewardsManager.sol#L114-L125>

Now the moveStakedLiquidity is calling \_claimRewards too without validate isEpochClaimed mapping:

    file: ajna-core/src/RewardsManager.sol
    function moveStakedLiquidity(
            uint256 tokenId_,
            uint256[] memory fromBuckets_,
            uint256[] memory toBuckets_,
            uint256 expiry_
        ) external override nonReentrant {
            StakeInfo storage stakeInfo = stakes[tokenId_];

            if (msg.sender != stakeInfo.owner) revert NotOwnerOfDeposit(); 

            uint256 fromBucketLength = fromBuckets_.length;
            if (fromBucketLength != toBuckets_.length)
                revert MoveStakedLiquidityInvalid();

            address ajnaPool = stakeInfo.ajnaPool;
            uint256 curBurnEpoch = IPool(ajnaPool).currentBurnEpoch();

            // claim rewards before moving liquidity, if any
            _claimRewards(stakeInfo, tokenId_, curBurnEpoch, false, ajnaPool); // no checking is isEpochClaimed is true and revert

<https://github.com/code-423n4/2023-05-ajna/blob/276942bc2f97488d07b887c8edceaaab7a5c3964/ajna-core/src/RewardsManager.sol#L135-L159>

Also we can see in the \_claimRewards function there is no validation is isEpochClaimed is true, this allow  a malicius user claimReward first and then move his liquidity to other bucket or the same bucket claiming the reward each time that he want.

    function _claimRewards(
            StakeInfo storage stakeInfo_,
            uint256 tokenId_,
            uint256 epochToClaim_,
            bool validateEpoch_,
            address ajnaPool_
        ) internal {
            // revert if higher epoch to claim than current burn epoch
            if (
                validateEpoch_ &&
                epochToClaim_ > IPool(ajnaPool_).currentBurnEpoch()
            ) revert EpochNotAvailable();

            // update bucket exchange rates and claim associated rewards
            uint256 rewardsEarned = _updateBucketExchangeRates(
                ajnaPool_,
                positionManager.getPositionIndexes(tokenId_)
            );

            rewardsEarned += _calculateAndClaimRewards(tokenId_, epochToClaim_);

            uint256[] memory burnEpochsClaimed = _getBurnEpochsClaimed(
                stakeInfo_.lastClaimedEpoch,
                epochToClaim_
            );

            emit ClaimRewards(
                msg.sender,
                ajnaPool_,
                tokenId_,
                burnEpochsClaimed,
                rewardsEarned
            );

            // update last interaction burn event
            stakeInfo_.lastClaimedEpoch = uint96(epochToClaim_);

            // transfer rewards to sender
            _transferAjnaRewards(rewardsEarned);
        }

### Recommended Mitigation Steps

Check if the isEpochClaime is true and revert in the \_claimReward function

    if (isEpochClaimed[tokenId_][epochToClaim_]) revert AlreadyClaimed();

**[ith-harvey (Ajna) disputed and commented](https://github.com/code-423n4/2023-05-ajna-findings/issues/132#issuecomment-1611598236):**
> The series of calls they are suggesting are possible:<br>
> stake<br>
> claimRewards() -> get rewards<br>
> moveStakedLiquidity() ->  get rewards
> 
> They should not be able to get these rewards because `_calculateAndClaimRewards()` iterates from last claimed epoch.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Ajna Protocol |
| Report Date | N/A |
| Finders | shealtielanz, ABAIKUNANBAEV, Jorgect |

### Source Links

- **Source**: https://code4rena.com/reports/2023-05-ajna
- **GitHub**: https://github.com/code-423n4/2023-05-ajna-findings/issues/132
- **Contest**: https://code4rena.com/reports/2023-05-ajna

### Keywords for Search

`vulnerability`

