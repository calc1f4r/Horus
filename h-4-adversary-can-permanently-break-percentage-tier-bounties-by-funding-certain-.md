---
# Core Classification
protocol: OpenQ
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6599
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/39
source_link: none
github_link: https://github.com/sherlock-audit/2023-02-openq-judging/issues/267

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 8
finders:
  - TrungOre
  - 0x52
  - cccz
  - bin2chen
  - tsvetanovv
---

## Vulnerability Title

H-4: Adversary can permanently break percentage tier bounties by funding certain ERC20 tokens then refunding

### Overview


This bug report is about an issue found in the TieredPercentageBountyV1.sol contract of the OpenQ-Contracts project. This issue, found by a group of researchers, could be abused by an adversary in order to permanently break percentage tier bounties by funding certain ERC20 tokens then refunding them. This would cause the contract to try to send a 0 value transfer, which some ERC20 tokens will revert on. This would cause the payouts to become permanently bricked, with no way to recover since fundingTotals can't be set anywhere else.

The researchers have recommended two fixes for the issue: if a deposit is refunded and the contract has no tokens left then remove that token from the list of tokens, and add a condition to _transferERC20 that only transfers if _volume != 0. The protocol owners have implemented these fixes in three pull requests. After discussing the issue, one researcher suggested escalating it for 27 USDC, but this escalation was rejected by another researcher as reverting on 0 transfer is uncommon but not unlikely to happen on a legit token. As a result, the escalation was rejected and the researchers' escalation amount was deducted from their next payout.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-02-openq-judging/issues/267 

## Found by 
rvierdiiev, 0x52, bin2chen, TrungOre, cccz, tsvetanovv, unforgiven, ctf\_sec

## Summary

Some ERC20 tokens don't support 0 value transfers. An adversary can abuse this by adding it to a percentage tier bounty then refunding it. This is because after the refund the token will still be on the list of tokens to distribute but it will have a value saved of 0. This means that no matter what it will always try to transfer 0 token and this will always revert because the specified token doesn't support zero transfers.

## Vulnerability Detail

https://github.com/sherlock-audit/2023-02-openq/blob/main/contracts/Bounty/Implementations/TieredPercentageBountyV1.sol#L123-L136

TieredPercentageBountyV1#closeCompetition set the final fundingTotals for each token. If a token has no balance then the fundingTotals for that token will be zero.

https://github.com/sherlock-audit/2023-02-openq/blob/main/contracts/Bounty/Implementations/TieredPercentageBountyV1.sol#L104-L120

For each token in tokenAddresses it will send the claimedBalance to the claimant. If fundingTotal is 0 then it will attempt to call transfer with an amount of 0. Some ERC20 tokens will revert on transfers like this. 

An adversary can purposefully trigger these conditions by making a deposit with ERC20 token that has this problem. This will add the ERC20 token to tokenAddresses and cause the contract to try to send 0 when making a payout. Payouts will become completely bricked, with no way to recover since fundingTotals can't be set anywhere else.

Submitting as high because it can be used in conjunction with methods of breaking refunds to permanently trap user funds.

## Impact

Payouts are permanently bricked

## Code Snippet

https://github.com/sherlock-audit/2023-02-openq/blob/main/contracts/Bounty/Implementations/TieredPercentageBountyV1.sol#L104-L120

## Tool used

Manual Review

## Recommendation

Add two fixes:

1) If a deposit is refunded and the contract has no tokens left then remove that token from the list of tokens
2) Add a condition to _transferERC20 that only transfers if _volume != 0

## Discussion

**FlacoJones**

Valid. Will fix with an explicity token whitelist and requiring funder == issuer

**FlacoJones**

https://github.com/OpenQDev/OpenQ-Contracts/pull/112

and 

https://github.com/OpenQDev/OpenQ-Contracts/pull/113

and 

https://github.com/OpenQDev/OpenQ-Contracts/pull/116

**kiseln**

Escalate for 27 USDC

> Some ERC20 tokens don't support 0 value transfers

There are no relevant tokens that revert on 0 value transfers. `LEND` is often provided as an example, however, it was discontinued in 2020 and is supposed to be migrated to AAVE https://docs.aave.com/faq/migration-and-staking. I'd say there is 0 chance this token is whitelisted as a valid bounty token by the protocol owners.

I would consider `LEND` in the same category as any invalid/malicious token that can be added in a permissionless way, in which case this group of issues is a duplicate of #62 


**sherlock-admin**

 > Escalate for 27 USDC
> 
> > Some ERC20 tokens don't support 0 value transfers
> 
> There are no relevant tokens that revert on 0 value transfers. `LEND` is often provided as an example, however, it was discontinued in 2020 and is supposed to be migrated to AAVE https://docs.aave.com/faq/migration-and-staking. I'd say there is 0 chance this token is whitelisted as a valid bounty token by the protocol owners.
> 
> I would consider `LEND` in the same category as any invalid/malicious token that can be added in a permissionless way, in which case this group of issues is a duplicate of #62 
> 

You've created a valid escalation for 27 USDC!

To remove the escalation from consideration: Delete your comment.
To change the amount you've staked on this escalation: Edit your comment **(do not create a new comment)**.

You may delete or edit your escalation comment anytime before the 48-hour escalation window closes. After that, the escalation becomes final.

**Evert0x**

Escalation rejected.

Protocol signaled they were planning to use `any` token in this protocol, reverting on 0 transfer is uncommon but not unlikely to happen on a legit token.

**sherlock-admin**

> Escalation rejected.
> 
> Protocol signaled they were planning to use `any` token in this protocol, reverting on 0 transfer is uncommon but not unlikely to happen on a legit token.

This issue's escalations have been rejected!

Watsons who escalated this issue will have their escalation amount deducted from their next payout.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | OpenQ |
| Report Date | N/A |
| Finders | TrungOre, 0x52, cccz, bin2chen, tsvetanovv, unforgiven, rvierdiiev, ctf\_sec |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-02-openq-judging/issues/267
- **Contest**: https://app.sherlock.xyz/audits/contests/39

### Keywords for Search

`vulnerability`

