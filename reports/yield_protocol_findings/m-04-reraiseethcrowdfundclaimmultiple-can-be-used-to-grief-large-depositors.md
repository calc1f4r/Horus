---
# Core Classification
protocol: PartyDAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19991
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-04-party
source_link: https://code4rena.com/reports/2023-04-party
github_link: https://github.com/code-423n4/2023-04-party-findings/issues/35

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

protocol_categories:
  - liquid_staking
  - cdp
  - services
  - launchpad
  - payments

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - 0x52
---

## Vulnerability Title

[M-04] `ReraiseETHCrowdfund#claimMultiple` can be used to grief large depositors

### Overview


This bug report is about a problem with the ReraiseETHCrowdfund.sol contract, which can be found on Github. When a user attempts to claim multiple NFTs with their voting power, the contract can force them to mint a large number of NFTs with low voting power instead of one with high voting power. This dramatically inflates the gas costs for the user.

An example is given, where if the minimum and maximum contribution is set to 1 and 100 respectively, a user who contributes 100 should qualify for one NFT of the largest size, however instead they can be minted 100 NFTs with 1 vote each.

The recommended mitigation step is to add a condition to the contract, which forces the user to mint the minimum possible number of NFTs if the msg.sender is not the contributor. This suggestion was judged to be valid and was confirmed by the Party. They also commented that they have decided to refactor the way claiming works in the contract, which should mitigate this finding. This new system will make it so crowdfund NFTs are minted per contribution instead of per address, and claiming will work more like a 1:1 conversion of a crowdfund NFT into a party card instead of how it works now.

### Original Finding Content


User can be grieved by being force minted a large number of NFTs with low voting power instead of one with high voting power.

### Proof of Concept

[ReraiseETHCrowdfund.sol#L354-L377](https://github.com/code-423n4/2023-04-party/blob/440aafacb0f15d037594cebc85fd471729bcb6d9/contracts/crowdfund/ReraiseETHCrowdfund.sol#L354-L377)

        for (uint256 i; i < votingPowerByCard.length; ++i) {
            if (votingPowerByCard[i] == 0) continue;

            uint96 contribution = (votingPowerByCard[i] * 1e4) / exchangeRateBps;
            if (contribution < minContribution_) {
                revert BelowMinimumContributionsError(contribution, minContribution_);
            }

            if (contribution > maxContribution_) {
                revert AboveMaximumContributionsError(contribution, maxContribution_);
            }

            votingPower -= votingPowerByCard[i];

            // Mint contributor a new party card.
            uint256 tokenId = party.mint(contributor, votingPowerByCard[i], delegate);

            emit Claimed(contributor, tokenId, votingPowerByCard[i]);
        }

`ReraiseETHCrowdfund#claimMultiple` can be called by any user for any other user. The above loop uses the user specified `votingPowerByCard` to assign each token a voting power and mint them to the contributor. This is problematic because large contributors can have their voting power fragmented into a large number of NFTs which a small amount of voting power each. The dramatically inflates the gas costs of the affected user.

**Example:**<br>
`minContribution = 1` and `maxContribution = 100`. User A contributes 100. This means they should qualify for one NFT of the largest size. However instead they can be minted 100 NFTs with 1 vote each.

### Recommended Mitigation Steps

If msg.sender isn't contributor it should force the user to mint the minimum possible number of NFTs:

        uint256 votingPower = pendingVotingPower[contributor];

        if (votingPower == 0) return;

    +  if (msg.sender != contributor) {
    +      require(votingPowerByCard.length == (((votingPower - 1)/maxContribution) + 1));
    +  }

**[0xean (judge) commented](https://github.com/code-423n4/2023-04-party-findings/issues/35#issuecomment-1509846159):**
 > Looking forward to sponsor comment on this one, I do see the potential issue.

**[0xble (Party) confirmed and commented](https://github.com/code-423n4/2023-04-party-findings/issues/35#issuecomment-1511922104):**
 > To give more context, the reason we allow minting/claiming on another's behalf is to allow others to potentially unblock governance if a user with delegated voting power does not come to claim, so it is an important feature to enable. It also works this way in prior releases of the protocol with past crowdfunds.
> 
> This is a valid concern though and I like the recommended mitigation.

**[0xble (Party) commented](https://github.com/code-423n4/2023-04-party-findings/issues/35#issuecomment-1532057835):**
 > We've decided to refactor the way claiming works in the `ReraiseETHCrowdfund`, partially because a large number of findings like this being submitted around that one area that highlighted for us the need to rework its logic.
> 
> The change will make it so (1) crowdfund NFTs are minted per contribution instead of per address and (2) claiming works more like a 1:1 conversion of your crowdfund NFT into a party card instead of how it works now. In the future we will also add the ability to split/merge party cards.
> 
> This should mitigate this finding because in this new system you cannot decide how to allocate another person's voting power when claiming for them, there is only one choice which is to convert their crowdfund NFT into a party card of equivalent voting power.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | PartyDAO |
| Report Date | N/A |
| Finders | 0x52 |

### Source Links

- **Source**: https://code4rena.com/reports/2023-04-party
- **GitHub**: https://github.com/code-423n4/2023-04-party-findings/issues/35
- **Contest**: https://code4rena.com/reports/2023-04-party

### Keywords for Search

`vulnerability`

