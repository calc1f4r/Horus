---
# Core Classification
protocol: Fenix Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41461
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-09-fenix-finance
source_link: https://code4rena.com/reports/2024-09-fenix-finance
github_link: https://github.com/code-423n4/2024-09-fenix-finance-findings/issues/21

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

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Ch\_301
---

## Vulnerability Title

[M-01] `mVeNFT` DOS can't trigger the vote function

### Overview


The `VoterUpgradeableV2.sol` contract has a function called `attachToManagedNFT()` that allows users to delegate their voting power to a `mVeNFT` token. However, there is a bug in this function that can be exploited by malicious users. After receiving the new voting power, the function will update the last voted timestamp of the `mVeNFT`, but this can cause the `mVeNFT` to be unable to trigger the vote function until the next epoch starts. This can lead to a denial of service attack where the `mVeNFT` cannot change the weight of gauges or reset its votes. The recommended mitigation step is to not check the vote delay, but this may come with some trade-offs. The assessed type of this bug is a denial of service attack. The severity of the bug has been decreased to Medium.

### Original Finding Content


<https://github.com/code-423n4/2024-09-fenix-finance/blob/main/contracts/core/VoterUpgradeableV2.sol#L485>

<https://github.com/code-423n4/2024-09-fenix-finance/blob/main/contracts/core/VoterUpgradeableV2.sol#L448>

### Description

The `VoterUpgradeableV2.sol` contract has the function `attachToManagedNFT()`, users use it to delegate their `veFNX` voting power to a `mVeNFT`. One of the things this function does after receiving the new voting power is sub-call to `_poke()` and it will update the last voted timestamp of the `mVeNFT`.

```solidity
lastVotedTimestamps[tokenId_] = _epochTimestamp() + 1;
```

At this point, the `mVeNFT` can't trigger the vote function until the next epoch starts due to the `_checkVoteDelay()`. Even this check inside the `vote()` doesn't help in this case.

```solidity
if (!managedNFTManagerCache.isWhitelistedNFT(tokenId_)) {
            _checkEndVoteWindow();
        }
```

However, to make things worse this protocol is deployed on Blast transactions are too cheap
malicious users can keep creating new locks every epoch with one wei in `amount`  to bypass the zero check.

```solidity
File: VotingEscrowUpgradeableV2.sol#_createLock()

 LibVotingEscrowValidation.checkNoValueZero(amount_);
```

Then at the start of every new epoch (after the start of the voting window), just call `attachToManagedNFT()`. By doing this it keeps forcing the `mVeNFT` to vote to the same gauges.

### Impact

DOS attack where `mVeNFT` can't invoke the vote function to change the weight of gauges; `mVeNFT` can't reset its votes.

### Recommended Mitigation Steps

One solution is to not check the vote delay, However, I believe this comes with some trade-offs.

```solidity
    function vote(
        uint256 tokenId_,
        address[] calldata poolsVotes_,
        uint256[] calldata weights_
    ) external nonReentrant onlyNftApprovedOrOwner(tokenId_) {
        if (poolsVotes_.length != weights_.length) {
            revert ArrayLengthMismatch();
        }
        bool x = managedNFTManagerCache.isWhitelistedNFT(tokenId_);
        if (!x) {
        _checkVoteDelay(tokenId_);
        }

        _checkStartVoteWindow();
        IManagedNFTManager managedNFTManagerCache = IManagedNFTManager(managedNFTManager);
        if (managedNFTManagerCache.isDisabledNFT(tokenId_)) {
            revert DisabledManagedNft();
        }
        if (!x) {
            _checkEndVoteWindow();
        }
        _vote(tokenId_, poolsVotes_, weights_);
        _updateLastVotedTimestamp(tokenId_);
    }
```

### Assessed type

DoS

**[b-hrytsak (Fenix) confirmed and commented via duplicate Issue #9](https://github.com/code-423n4/2024-09-fenix-finance-findings/issues/9#issuecomment-2382024977):**
> The `_updateLastVotedTimestamp` was not supposed to be in the `_poke` method, so cases like yours became possible.
> 
> ```
> /**
>      * @dev Updates the voting preferences for a given tokenId after changes in the system.
>      * @param tokenId_ The tokenId for which to update voting preferences.
>      */
>    function _poke(uint256 tokenId_) internal {
>       //** code **//
>        _updateLastVotedTimestamp(tokenId_);
>    }
>```

**[alcueca (judge) decreased severity to Medium](https://github.com/code-423n4/2024-09-fenix-finance-findings/issues/21#issuecomment-2383190704)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Fenix Finance |
| Report Date | N/A |
| Finders | Ch\_301 |

### Source Links

- **Source**: https://code4rena.com/reports/2024-09-fenix-finance
- **GitHub**: https://github.com/code-423n4/2024-09-fenix-finance-findings/issues/21
- **Contest**: https://code4rena.com/reports/2024-09-fenix-finance

### Keywords for Search

`vulnerability`

