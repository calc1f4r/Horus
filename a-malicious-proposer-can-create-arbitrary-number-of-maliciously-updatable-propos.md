---
# Core Classification
protocol: Nouns DAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21324
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Nouns-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Nouns-Spearbit-Security-Review.pdf
github_link: none

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
  - dexes
  - yield
  - cross_chain
  - rwa
  - nft_marketplace

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - tchkvsky
  - Christos Papakonstantinou
  - Rajeev
  - r0bert
  - hyh
---

## Vulnerability Title

A malicious proposer can create arbitrary number of maliciously updatable proposals to significantly grief the protocol

### Overview


This bug report is about a vulnerability in the NounsDAOV3Proposals.sol protocol which could allow malicious proposers to create an arbitrary number of proposals from different addresses. This spam protection mechanism is based on the proposer address rather than the Noun itself, which allows the malicious proposer to transfer or delegate their Nouns to different addresses and create proposals from those new addresses to spam. Furthermore, proposal updation in the protocol does not check for the proposer meeting any voting power threshold at the time of updation. This bug has been given a medium severity due to its medium likelihood and medium impact. 

The recommendation for this bug is to consider a redesign where the proposal creation spam mitigation is not based on the Noun controlling address but the Noun itself, and to add a proposal threshold check for voting power during updation. It has been acknowledged that this is a known issue from the launch of Nouns and is mitigated by cancelling proposals once the proposer does not have enough balance to meet the threshold. It has also been acknowledged that when it comes to obvious spamming, the updatable proposals do not add any meaningful risk as the spammy behavior is the main red flag.

### Original Finding Content

## Severity: Medium Risk

## Context
- `NounsDAOV3Proposals.sol#L783-L798`
- `NounsDAOV3Proposals.sol#L171`
- `NounsDAOV3Proposals.sol#L818-L823`
- `NounsDAOV3Proposals.sol#L269-L423`

## Description
`checkNoActiveProp()` is documented as: 
> "This is a spam protection mechanism to limit the number of proposals each noun can back." 

However, this mitigation applies to proposer addresses holding Nouns but not the Nouns themselves because `checkNoActiveProp()` relies on checking the state of proposals tracked by the proposer via `latestProposalId = ds.latestProposalIds[proposer]`. A malicious proposer can move (transfer/delegate) their Noun(s) to different addresses to circumvent this mitigation and create proposals from those new addresses to spam. Furthermore, proposal updation in the protocol does not check for the proposer meeting any voting power threshold at the time of updation.

A malicious proposer can create an arbitrary number of proposals, each from a different address by transferring/delegating their Nouns, and then update any/all of them to be malicious. Substantial effort will be required to differentiate all such proposals from the authentic ones and then cancel them, leading to DAO governance DoS griefing.

> Medium likelihood + Medium impact = Medium severity.

## Recommendation
Consider:
1. A redesign where proposal creation spam mitigation is not based on the Noun controlling address but the Noun itself.
2. Adding proposal threshold check for voting power during updation.

## Nouns
**Won't Fix.** This is a known issue from the launch of Nouns, and is mitigated by canceling proposals once the proposer doesn’t have enough balance to meet the threshold, as well as the vetoer in extreme cases. Such spammy behavior should easily become suspicious and token holders will be ready to cancel all such proposals, same as they are today.

Specifically, when it comes to obvious spamming, we don’t think the updatable proposals add any meaningful risk. The spammy behavior is the main red flag, and using this new feature with more stealth is already discussed in:
> "A malicious proposer can update proposal past inattentive voters to sneak in otherwise unacceptable details."

## Spearbit
**Acknowledged.**

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Nouns DAO |
| Report Date | N/A |
| Finders | tchkvsky, Christos Papakonstantinou, Rajeev, r0bert, hyh |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Nouns-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Nouns-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

