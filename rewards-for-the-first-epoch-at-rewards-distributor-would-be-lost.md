---
# Core Classification
protocol: Alchemix
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 38224
audit_firm: Immunefi
contest_link: https://immunefi.com/bounty/alchemix-boost/
source_link: none
github_link: https://raw.githubusercontent.com/immunefi-team/Bounty_Boosts/main/Alchemix/31484%20-%20%5bSC%20-%20High%5d%20Rewards%20for%20the%20first%20epoch%20at%20rewards%20distribu....md

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
  - liquid_staking
  - dexes
  - yield
  - cross_chain
  - rwa

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - MahdiKarimi
---

## Vulnerability Title

Rewards for the first epoch at rewards distributor would be lost

### Overview


This is a report about a bug in a smart contract on GitHub. The contract in question is called "RewardsDistributor" and it distributes rewards to users who hold a certain type of token called "veALCX". The bug causes some of the rewards to be permanently frozen and unable to be claimed. This happens because the contract was deployed at the same time as another contract that mints the veALCX tokens, so there are no users at the start of the first reward distribution period. This means that no one can claim the rewards and they get stuck in the contract forever. This bug results in a loss of rewards for users in the first distribution period. The report includes a proof of concept code to demonstrate the bug.

### Original Finding Content

Report type: Smart Contract


Target: https://github.com/alchemix-finance/alchemix-v2-dao/blob/main/src/RewardsDistributor.sol

Impacts:
- Permanent freezing of unclaimed yield

## Description
## Brief/Intro
Some parts of rewards at rewards distributor would be lost

## Vulnerability Details
RewardsDistributor distributes ALCX rewards to veALCX holders, rewards are distributed based on the balance of users at the end of an epoch, for the first time that the minter distributes rewards, some part of it is being allocated to the first epoch which can be withdrawn only if there was a user at the start of the first epoch ( end of last epoch ) but since rewards distributor and voting escrow ( mints veALCX ) are being deployed in the same time so there is no user at that timestamp so no one can claim those rewards and rewards gets stuck in contract forever

## Impact Details
loss of rewards at rewards distributor in the first epoch 

## References
https://github.com/alchemix-finance/alchemix-v2-dao/blob/f1007439ad3a32e412468c4c42f62f676822dc1f/src/RewardsDistributor.sol#L244-L248


## Proof of Concept
```
        function testLostRewardsFirstEpoch() public {
        initializeVotingEscrow();

        // assert alcx balance of rewards distributor is zero
        uint256 distributorBalance = alcx.balanceOf(address(distributor));
        assertEq(distributorBalance, 0);

        // Fast forward 1/2 epoch
        // create a lock
        hevm.warp(block.timestamp + nextEpoch / 2);
        hevm.roll(block.number + 1);
        uint256 tokenId1 = createVeAlcx(admin, TOKEN_1, MAXTIME, false);

        // Finish the epoch and distribute some rewards 
        hevm.warp(newEpoch());
        voter.distribute();
        
        // assert alcx balance of rewards distributor is greater than zero which means some tokens has been transffered as reward 
        uint256 distributorBalanceEnd = alcx.balanceOf(address(distributor));
        assertGt(distributorBalanceEnd, 0);

        // calculate claimable amount by token1 
        uint256 claimable1 = distributor.claimable(tokenId1);
        // as we see token1 can't claim all alcx tokens despite that he's only user (on one can claim it)
        assert(distributorBalanceEnd > claimable1);
        // to ensure diffrence is high we check freezed amount is at least 3 time more than claimable amount  
        assert(distributorBalanceEnd > 3 * claimable1);

    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Immunefi |
| Protocol | Alchemix |
| Report Date | N/A |
| Finders | MahdiKarimi |

### Source Links

- **Source**: N/A
- **GitHub**: https://raw.githubusercontent.com/immunefi-team/Bounty_Boosts/main/Alchemix/31484%20-%20%5bSC%20-%20High%5d%20Rewards%20for%20the%20first%20epoch%20at%20rewards%20distribu....md
- **Contest**: https://immunefi.com/bounty/alchemix-boost/

### Keywords for Search

`vulnerability`

