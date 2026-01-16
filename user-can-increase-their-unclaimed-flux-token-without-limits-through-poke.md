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
solodit_id: 38124
audit_firm: Immunefi
contest_link: https://immunefi.com/bounty/alchemix-boost/
source_link: none
github_link: https://raw.githubusercontent.com/immunefi-team/Bounty_Boosts/main/Alchemix/30788%20-%20%5bSC%20-%20Critical%5d%20User%20can%20increase%20their%20unclaimed%20Flux%20token%20wi....md

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
  - jecikpo
---

## Vulnerability Title

User can increase their unclaimed Flux token without limits through `poke()`

### Overview


This report discusses a bug found in the Smart Contract code for the Alchemix DAO on GitHub. The bug allows users to increase their unclaimed Flux token amount by calling a specific function multiple times. This can lead to the manipulation of governance voting results and potentially unlimited accrual of unclaimed Flux. This can be exploited to unfairly increase voting power or manipulate the market price of Flux. The report includes a proof of concept code to demonstrate the bug. 

### Original Finding Content

Report type: Smart Contract


Target: https://github.com/alchemix-finance/alchemix-v2-dao/blob/main/src/Voter.sol

Impacts:
- unbounded minting of token
- Manipulation of governance voting result deviating from voted outcome and resulting in a direct change from intended effect of original results

## Description
## Brief/Intro
A user can increase their unclaimed Flux token amount by calling `Voter.poke()` multiple times.

## Vulnerability Details
The `Voter._vote()` function calls `FluxToken.accrueFlux(_tokenId)` which increases the `unclaimed[_tokenId]` balance according the `_tokenId` voting power. `_vote()` is called by `vote()` which has the `onlyNewEpoch(_tokenId)` modifier attached, so it can be called only once during each epoch. 

The `_vote()` is also used inside `poke()`. `poke()` is supposed to vote based on the users previous voting weights. however `poke()` does not have the above mentioned modifier attached, hence it can be called multiple times during the epoch without any limits. Each time `poke()` is called the unclaimed FLUX is increased.

## Impact Details
The impact is that the user can accrue potentially unlimited amount of unclaimed Flux. The unclaimed Flux could be used to execute unfair voting by increasing the user's voting power. It could also be claimed and sold on the open market to suppress the Flux price which will allow other users to unlock their veALCX tokens at lower prices hence destroying the entire voting system credibility.

## References
https://github.com/alchemix-finance/alchemix-v2-dao/blob/f1007439ad3a32e412468c4c42f62f676822dc1f/src/Voter.sol#L195



## Proof of Concept
Add to the `VotingEscrow.t.sol` the following code:
```solidity
function testAbusePoke() public {
        hevm.startPrank(admin);

        uint256 tokenIdLarge = veALCX.createLock(TOKEN_100K, THREE_WEEKS, false);
        //uint256 tokenIdSmall = veALCX.createLock(TOKEN_1, THREE_WEEKS, false);


        voter.reset(tokenIdLarge);
        console.log("Unclaimed Flux on tokenIdLarge: %d", flux.unclaimedFlux(tokenIdLarge));
        voter.poke(tokenIdLarge);
        // we can see that the user amassed more unclaimed FLUX: 9420478183663114723056
        console.log("Unclaimed Flux on tokenIdLarge after poke called once: %d", flux.unclaimedFlux(tokenIdLarge));

        // even more after calling poke() again: 14130717275494672084584
        voter.poke(tokenIdLarge);
        console.log("Unclaimed Flux on tokenIdLarge after poke called twice: %d", flux.unclaimedFlux(tokenIdLarge));

        // and again: 18840956367326229446112
        voter.poke(tokenIdLarge);
        console.log("Unclaimed Flux on tokenIdLarge after poke called thrid time: %d", flux.unclaimedFlux(tokenIdLarge));

        hevm.stopPrank();
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
| Finders | jecikpo |

### Source Links

- **Source**: N/A
- **GitHub**: https://raw.githubusercontent.com/immunefi-team/Bounty_Boosts/main/Alchemix/30788%20-%20%5bSC%20-%20Critical%5d%20User%20can%20increase%20their%20unclaimed%20Flux%20token%20wi....md
- **Contest**: https://immunefi.com/bounty/alchemix-boost/

### Keywords for Search

`vulnerability`

