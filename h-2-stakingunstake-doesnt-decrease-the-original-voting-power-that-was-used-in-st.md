---
# Core Classification
protocol: FrankenDAO
chain: everychain
category: uncategorized
vulnerability_type: add/subtract_match

# Attack Vector Details
attack_type: add/subtract_match
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3590
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/18
source_link: none
github_link: https://github.com/sherlock-audit/2022-11-frankendao-judging/issues/70

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:
  - add/subtract_match
  - dao

protocol_categories:
  - liquid_staking
  - dexes
  - yield
  - launchpad
  - payments

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Haruxe
  - 0x52
  - hansfriese
---

## Vulnerability Title

H-2: `Staking.unstake()` doesn't decrease the original voting power that was used in `Staking.stake()`.

### Overview


This bug report is about an issue found in the code of the FrankenDAO, a decentralized autonomous organization. The issue is that when users stake and unstake the underlying NFTs (non-fungible tokens), the token voting power is not being decreased accordingly. This is due to the fact that `getTokenVotingPower()` uses some parameters like `monsterMultiplier` and `baseVotes` and the output would be changed for the same `tokenId` after the admin changed these settings. As a result, users cannot unstake their NFTs and `votesFromOwnedTokens` might be updated wrongly. 

The issue was found by Haruxe, 0x52, and hansfriese and was fixed by zobront in the following pull request: https://github.com/Solidity-Guild/FrankenDAO/pull/17. The recommendation given was to add a mapping like `tokenVotingPower` to save an original token voting power when users stake the token and decrease the same amount when they unstake.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-11-frankendao-judging/issues/70 

## Found by 
Haruxe, 0x52, hansfriese

## Summary
`Staking.unstake()` doesn't decrease the original voting power that was used in `Staking.stake()`.

## Vulnerability Detail
When users stake/unstake the underlying NFTs, it calculates the token voting power using [getTokenVotingPower()](https://github.com/sherlock-audit/2022-11-frankendao/blob/main/src/Staking.sol#L507-L515) and increases/decreases their voting power accordingly.

```solidity
    function getTokenVotingPower(uint _tokenId) public override view returns (uint) {
      if (ownerOf(_tokenId) == address(0)) revert NonExistentToken();

      // If tokenId < 10000, it's a FrankenPunk, so 100/100 = a multiplier of 1
      uint multiplier = _tokenId < 10_000 ? PERCENT : monsterMultiplier;
      
      // evilBonus will return 0 for all FrankenMonsters, as they are not eligible for the evil bonus
      return ((baseVotes * multiplier) / PERCENT) + stakedTimeBonus[_tokenId] + evilBonus(_tokenId);
    }
```

But `getTokenVotingPower()` uses some parameters like `monsterMultiplier` and `baseVotes` and the output would be changed for the same `tokenId` after the admin changed these settings.

Currently, `_stake()` and `_unstake()` calculates the token voting power independently and the below scenario would be possible.

- At the first time, `baseVotes = 20, monsterMultiplier = 50`.
- A user staked a `FrankenMonsters` and his voting power = 10 [here](https://github.com/sherlock-audit/2022-11-frankendao/blob/main/src/Staking.sol#L369-L371).
- After that, the admin changed `monsterMultiplier = 60`.
- When a user tries to unstake the NFT, the token voting power will be `20 * 60 / 100 = 12` [here](https://github.com/sherlock-audit/2022-11-frankendao/blob/main/src/Staking.sol#L514).
- So it will revert with uint underflow [here](https://github.com/sherlock-audit/2022-11-frankendao/blob/main/src/Staking.sol#L436).
- After all, he can't unstake the NFT.

## Impact
`votesFromOwnedTokens` might be updated wrongly or users can't unstake for the worst case because it doesn't decrease the same token voting power while unstaking.

## Code Snippet
https://github.com/sherlock-audit/2022-11-frankendao/blob/main/src/Staking.sol#L427-L440

## Tool used
Manual Review

## Recommendation
I think we should add a mapping like `tokenVotingPower` to save an original token voting power when users stake the token and decrease the same amount when they unstake.

## Discussion

**zobront**

Fixed: https://github.com/Solidity-Guild/FrankenDAO/pull/17

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Sherlock |
| Protocol | FrankenDAO |
| Report Date | N/A |
| Finders | Haruxe, 0x52, hansfriese |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-11-frankendao-judging/issues/70
- **Contest**: https://app.sherlock.xyz/audits/contests/18

### Keywords for Search

`Add/Subtract Match, DAO`

