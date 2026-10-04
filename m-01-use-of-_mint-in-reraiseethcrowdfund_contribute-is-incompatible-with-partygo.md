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
solodit_id: 19988
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-04-party
source_link: https://code4rena.com/reports/2023-04-party
github_link: https://github.com/code-423n4/2023-04-party-findings/issues/42

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

[M-01] Use of `_mint` in `ReraiseETHCrowdfund#_contribute` is incompatible with `PartyGovernanceNFT#mint`

### Overview


A bug has been identified in the code of the 2023-04-party project, which contains contracts for a party platform. The bug is caused by the inconsistent use of minting methods in two different contracts - ReraiseETHCrowdfund#_contribute and PartyGovernanceNFT#mint. The former uses the standard minting method while the latter uses the safeMinting method. This is a problem because it means that a contract which does not implement ERC721Receiver can receive a CrowdfundNFT from the ReraiseETHCrowdfund#_contribute contract, but can never claim it because safeMinting will always revert. This can cause the party to be inadvertently DOS'd because CrowdfundNFTs are soul bound and can't be transferred.

The recommended mitigation steps to address this issue are to use _safeMint instead of _mint for ReraiseETHCrowdfund#_contribute. An alternative mitigation was also suggested by 0xble (Party), which is to allow the user to specify a 'receiver' address that can receive the party NFT when claiming, so if they cannot claim themselves they can specify another address that should receive it instead.

### Original Finding Content


Misconfigured receiver could accidentally DOS party.

### Proof of Concept

[ReraiseETHCrowdfund.sol#L238](https://github.com/code-423n4/2023-04-party/blob/440aafacb0f15d037594cebc85fd471729bcb6d9/contracts/crowdfund/ReraiseETHCrowdfund.sol#L238)

        if (previousVotingPower == 0) _mint(contributor); <- @audit-issue standard minting here

[ReraiseETHCrowdfund.sol#L374](https://github.com/code-423n4/2023-04-party/blob/440aafacb0f15d037594cebc85fd471729bcb6d9/contracts/crowdfund/ReraiseETHCrowdfund.sol#L374)

            uint256 tokenId = party.mint(contributor, votingPowerByCard[i], delegate); <- @audit-issue uses party.mint

[PartyGovernanceNFT.sol#L162](https://github.com/code-423n4/2023-04-party/blob/440aafacb0f15d037594cebc85fd471729bcb6d9/contracts/party/PartyGovernanceNFT.sol#L162)

        _safeMint(owner, tokenId); <- @audit-issue PartyGovernanceNFT#mint utilizes _safeMint

The issue at hand is that ReraiseETHCrowdfund#\_contribute and PartyGovernanceNFT#mint use inconsistent minting methods. PartyGovernanceNFT uses safeMint whereas ReraiseETHCrowdfund uses the standard mint. This is problematic because this means that a contract that doesn't implement ERC721Receiver can receive a CrowdfundNFT but they can never claim because safeMint will always revert. This can cause a party to be inadvertently DOS'd because CrowdfundNFTs are soul bound and can't be transferred.

### Recommended Mitigation Steps

Use \_safeMint instead of \_mint for ReraiseETHCrowdfund#\_contribute

**[0xble (Party) confirmed and commented](https://github.com/code-423n4/2023-04-party-findings/issues/42#issuecomment-1512115454):**
 > I think a better mitigation would be to allow the user to specify a `receiver` address that can receive the party NFT when claiming, so if they cannot claim themselves they can specify another address that should receive it instead. It works similarly in `Crowdfund`, used to implement prior crowdfunds.



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
- **GitHub**: https://github.com/code-423n4/2023-04-party-findings/issues/42
- **Contest**: https://code4rena.com/reports/2023-04-party

### Keywords for Search

`vulnerability`

