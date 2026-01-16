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
solodit_id: 38225
audit_firm: Immunefi
contest_link: https://immunefi.com/bounty/alchemix-boost/
source_link: none
github_link: https://raw.githubusercontent.com/immunefi-team/Bounty_Boosts/main/Alchemix/31485%20-%20%5bSC%20-%20Critical%5d%20Miscalculation%20of%20distributed%20tokens%20at%20revenue....md

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

Miscalculation of distributed tokens at revenue handler

### Overview


This report is about a bug found in a smart contract on GitHub. The contract in question is the RevenueHandler.sol file in the Alchemix Finance repository. The bug can lead to the theft of unclaimed yield from users. The issue is caused by the contract using the total balance to calculate the distribution amount, which includes unclaimed rewards from previous distributions. This means that some users may receive more rewards than others, causing inconsistency between the contract balance and the amount that users can claim. The bug has been identified and a proof of concept has been provided to demonstrate the issue. 

### Original Finding Content

Report type: Smart Contract


Target: https://github.com/alchemix-finance/alchemix-v2-dao/blob/main/src/RevenueHandler.sol

Impacts:
- Theft of unclaimed yield

## Description
## Brief/Intro
Revenue handler uses contract balance to calculate distribution amount, so if users didn't claim their rewards from the last distribution, unclaimed amount is mistakenly considered as newly distributed rewards 

## Vulnerability Details
Every time the checkpoint is called at revenue handler to distribute revenues, it uses the contract balance as the amount to be distributed. However, if some users haven't claimed their rewards from previous distributions, those unclaimed rewards are mistakenly considered as newly distributed rewards so some users can receive more rewards while others can't receive their rewards.

## Impact Details
Inconsistency between contract balance and user claimable amount enables some users to receive more rewards while some users are not able to receive any rewards 

## References
https://github.com/alchemix-finance/alchemix-v2-dao/blob/f1007439ad3a32e412468c4c42f62f676822dc1f/src/RevenueHandler.sol#L245-L264



## Proof of Concept
```
      function testClaimAfterNextCheckpoint() external {
        uint256 revAmt = 1000e18;
        uint256 tokenId = _setupClaimableNonAlchemicRevenue(revAmt, bal);
        uint256 tokenId2 = _setupClaimableNonAlchemicRevenue(revAmt, bal);

        uint256 claimable = revenueHandler.claimable(tokenId, bal);
        uint256 claimable2 = revenueHandler.claimable(tokenId2, bal);
    
        // as we see contract balance is not sufficient for claimable amount 
        assert(claimable > IERC20(bal).balanceOf(address(revenueHandler)));
        assert(claimable + claimable2 > IERC20(bal).balanceOf(address(revenueHandler)));
        
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
- **GitHub**: https://raw.githubusercontent.com/immunefi-team/Bounty_Boosts/main/Alchemix/31485%20-%20%5bSC%20-%20Critical%5d%20Miscalculation%20of%20distributed%20tokens%20at%20revenue....md
- **Contest**: https://immunefi.com/bounty/alchemix-boost/

### Keywords for Search

`vulnerability`

