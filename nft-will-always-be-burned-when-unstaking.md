---
# Core Classification
protocol: Lighthouse NFT Staking
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50358
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/seascape/lighthouse-nft-staking-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/seascape/lighthouse-nft-staking-smart-contract-security-assessment
github_link: none

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
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

NFT WILL ALWAYS BE BURNED WHEN UNSTAKING

### Overview


The bug report describes an issue with the `StakeNft.sol` contract where NFTs are being burned when unstaked. This means that users who stake their NFTs may lose them permanently. The code responsible for this is located in the `LightHouseStake.sol` and `StakeNft.sol` contracts. The impact and likelihood of this bug are both rated as 5. The recommendation is to remove the burning functionality and instead transfer the NFTs back to the user when they unstake. This issue has been resolved by the Seascape team.

### Original Finding Content

##### Description

Testing revealed that NFTs will always be burned when unstaked due to an error in the `StakeNft.sol` contract, which burns the token when the variable `burn` is set to false. Users might not be aware of this when staking their NFT, thus resulting in the loss of their asset.

Code Location
-------------

`LightHouseStake.sol` Lines #151-166

```
 function unstake(uint256 sessionId, uint256 nftId) external {
        address staker = msg.sender;
        Session storage session = sessions[sessionId];
        require(session.rewardPool > 0, "session does not exist");

        Player storage playerChallenge = playerParams[sessionId][nftId];
        require(playerChallenge.player != msg.sender, "forbidden");

        StakeNft handler = StakeNft(stakeHandler);
        handler.claim(sessionId, staker);

        handler.unstake(sessionId, staker, nftId, false);
        delete playerParams[sessionId][nftId];

        emit Unstake(staker, sessionId, nftId);
    }

```

`StakeNft.sol` Lines #79-99

```
 function unstake(uint key, address stakerAddr, uint id, bool burn)
        external
        nonReentrant
    {
        address stakeToken = periods[msg.sender][key].stakeToken;
        IERC721 nft = IERC721(stakeToken);

        require(nft.ownerOf(id) == address(this), "not owned");
        require(owners[msg.sender][key][id] == stakerAddr);

        delete owners[msg.sender][key][id];
        delete weights[msg.sender][key][id];

        if (burn) {
            nft.safeTransferFrom(address(this), stakerAddr, id);
        } else {
            nft.safeTransferFrom(address(this), 0x000000000000000000000000000000000000dEaD, id);
        }

        withdraw(key, stakerAddr, weights[msg.sender][key][id]);
    }

```

##### Score

Impact: 5  
Likelihood: 5

##### Recommendation

***SOLVED***: The `Seascape team` amended the contracts to remove the burning functionality. Every time a user unstakes their ERC721, it will not be burned, but transferred to them.

\newpage

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Lighthouse NFT Staking |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/seascape/lighthouse-nft-staking-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/seascape/lighthouse-nft-staking-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

