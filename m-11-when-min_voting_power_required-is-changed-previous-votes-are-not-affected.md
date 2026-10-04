---
# Core Classification
protocol: Golom
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 8748
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-07-golom-contest
source_link: https://code4rena.com/reports/2022-07-golom
github_link: https://github.com/code-423n4/2022-07-golom-findings/issues/626

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
  - services
  - liquidity_manager
  - nft_marketplace
  - options_vault

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - cccz
---

## Vulnerability Title

[M-11] When `MIN_VOTING_POWER_REQUIRED` is changed, previous votes are not affected

### Overview


This bug report is about a vulnerability in the code of the VoteEscrowDelegation.sol contract. The vulnerability occurs when the MIN_VOTING_POWER_REQUIRED value is changed. This value is used to reduce the influence of spam users, and when it is changed, tokenIDs with votes lower than MIN_VOTING_POWER_REQUIRED will not be able to vote through the delegate function, but the votes already cast will not be affected.

The impact of this vulnerability is that when MIN_VOTING_POWER_REQUIRED is changed, the votes from tokenIDs with votes lower than MIN_VOTING_POWER_REQUIRED will not be counted, even though they were cast prior to the change.

The recommended mitigation steps for this vulnerability are to modify the getVotes and getPriorVotes functions so that when the balance corresponding to tokenId is less than MIN_VOTING_POWER_REQUIRED, the value of votes will not be increased. This will ensure that the votes from tokenIDs with votes lower than MIN_VOTING_POWER_REQUIRED will not be counted.

### Original Finding Content


When `MIN_VOTING_POWER_REQUIRED` is changed, tokenIDs with votes lower than `MIN_VOTING_POWER_REQUIRED` will not be able to vote through the delegate function, but previous votes will not be affected.<br>
Since `MIN_VOTING_POWER_REQUIRED` is mainly used to reduce the influence of spam users, changing this value should affect previous votes.

### Proof of Concept

<https://github.com/code-423n4/2022-07-golom/blob/e5efa8f9d6dda92a90b8b2c4902320acf0c26816/contracts/vote-escrow/VoteEscrowDelegation.sol#L168-L194><br>

<https://github.com/code-423n4/2022-07-golom/blob/e5efa8f9d6dda92a90b8b2c4902320acf0c26816/contracts/vote-escrow/VoteEscrowDelegation.sol#L260-L262><br>

<https://github.com/code-423n4/2022-07-golom/blob/e5efa8f9d6dda92a90b8b2c4902320acf0c26816/contracts/vote-escrow/VoteEscrowDelegation.sol#L73-L74><br>

### Recommended Mitigation Steps

In the getPriorVotes and getVotes functions, when the balance corresponding to tokenId is less than MIN_VOTING_POWER_REQUIRED, the value of votes will not be increased

```diff
    function getVotes(uint256 tokenId) external view returns (uint256) {
        uint256[] memory delegated = _getCurrentDelegated(tokenId);
        uint256 votes = 0;
        for (uint256 index = 0; index < delegated.length; index++) {
+         if(this.balanceOfNFT(delegated[index]) >= MIN_VOTING_POWER_REQUIRED){
            votes = votes + this.balanceOfNFT(delegated[index]);
+       }
        }
        return votes;
    }


    /**
     * @notice Determine the prior number of votes for an account as of a block number
     * @dev Block number must be a finalized block or else this function will revert to prevent misinformation.
     * @param tokenId The address of the account to check
     * @param blockNumber The block number to get the vote balance at
     * @return The number of votes the account had as of the given block
     */
    function getPriorVotes(uint256 tokenId, uint256 blockNumber) public view returns (uint256) {
        require(blockNumber < block.number, 'VEDelegation: not yet determined');
        uint256[] memory delegatednft = _getPriorDelegated(tokenId, blockNumber);
        uint256 votes = 0;
        for (uint256 index = 0; index < delegatednft.length; index++) {
+         if(this.balanceOfAtNFT(delegatednft[index], blockNumber) >= MIN_VOTING_POWER_REQUIRED){
            votes = votes + this.balanceOfAtNFT(delegatednft[index], blockNumber);
+         }
        }
        return votes;
    }
```

**[zeroexdead (Golom) confirmed, but disagreed with severity](https://github.com/code-423n4/2022-07-golom-findings/issues/626)**

**[zeroexdead (Golom) commented](https://github.com/code-423n4/2022-07-golom-findings/issues/626#issuecomment-1236182938):**
 > When calling we `getVotes()` and `getPriorVotes()` we're considering `MIN_VOTING_POWER_REQUIRED`.<br>
> Reference: https://github.com/golom-protocol/contracts/commit/db650729b0805ec19906a0ea11de6af7a53ac382

**[0xsaruman (Golom) resolved](https://github.com/code-423n4/2022-07-golom-findings/issues/626)**

**[LSDan (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2022-07-golom-findings/issues/626#issuecomment-1279184086):**
 > Downgrading this to medium. Assets are not at direct risk.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Golom |
| Report Date | N/A |
| Finders | cccz |

### Source Links

- **Source**: https://code4rena.com/reports/2022-07-golom
- **GitHub**: https://github.com/code-423n4/2022-07-golom-findings/issues/626
- **Contest**: https://code4rena.com/contests/2022-07-golom-contest

### Keywords for Search

`vulnerability`

