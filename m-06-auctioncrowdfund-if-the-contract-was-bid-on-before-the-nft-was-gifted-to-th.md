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
solodit_id: 3314
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-09-partydao-contest
source_link: https://code4rena.com/reports/2022-09-party
github_link: https://github.com/code-423n4/2022-09-party-findings/issues/147

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
  - cccz
---

## Vulnerability Title

[M-06] AuctionCrowdfund: If the contract was bid on before the NFT was gifted to the contract, lastBid will not be totalContributions

### Overview


This bug report is about a vulnerability in the AuctionCrowdfund contract. This vulnerability can lead to a situation where only the user who contributed at the beginning will win, even if the contract was bid before the NFT was gifted to the contract. This is because the lastBid_ variable is not set to 0 when the NFT is gifted to the contract.

Proof of concept and lines of code are provided in the report. No tools were used to identify the vulnerability.

The recommended mitigation step is to determine whether the contract balance is greater than totalContributions to determine if the NFT is free to get.

### Original Finding Content

_Submitted by cccz_

In the finalize function of the AuctionCrowdfund contract, when the contract gets NFT and lastBid\_ == 0, it is considered that NFT is gifted to the contract and everyone who contributed wins.

            if (nftContract.safeOwnerOf(nftTokenId) == address(this)) {
                if (lastBid_ == 0) {
                    // The NFT was gifted to us. Everyone who contributed wins.
                    lastBid_ = totalContributions;

But if the contract was bid before the NFT was gifted to the contract, then since lastBid\_ ! = 0, only the user who contributed at the beginning will win.

### Proof of Concept

<https://github.com/PartyDAO/party-contracts-c4/blob/3896577b8f0fa16cba129dc2867aba786b730c1b/contracts/crowdfund/AuctionCrowdfund.sol#L233-L242>

<https://github.com/PartyDAO/party-contracts-c4/blob/3896577b8f0fa16cba129dc2867aba786b730c1b/contracts/crowdfund/AuctionCrowdfund.sol#L149-L175>

### Recommended Mitigation Steps

Whether or not NFT is free to get should be determined using whether the contract balance is greater than totalContributions.

**[merklejerk (PartyDAO) confirmed and commented](https://github.com/code-423n4/2022-09-party-findings/issues/147#issuecomment-1254403120):**
 > Gifted NFTs are expected to be an extremely exceptional (if ever) case, but we do want to make a best effort to make these situations somewhat fair to contributors.  We will implement the recommendation and check that `this.balance >= totalContributions` to see if the NFT was acquired for free.

**[0xble (PartyDAO) resolved](https://github.com/code-423n4/2022-09-party-findings/issues/147#issuecomment-1264678161):**
 > Resolved: https://github.com/PartyDAO/partybidV2/pull/133

**[HardlyDifficult (judge) commented](https://github.com/code-423n4/2022-09-party-findings/issues/147#issuecomment-1267170378):**
 > This could be seen as a form of leaking value, agree with Medium risk.



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
| Finders | cccz |

### Source Links

- **Source**: https://code4rena.com/reports/2022-09-party
- **GitHub**: https://github.com/code-423n4/2022-09-party-findings/issues/147
- **Contest**: https://code4rena.com/contests/2022-09-partydao-contest

### Keywords for Search

`vulnerability`

