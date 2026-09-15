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
solodit_id: 21339
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

Proposal threshold can be bypassed through the proposeBySigs() function

### Overview


This bug report is about the function proposeBySigs() in the NounsDAOV3Proposals.sol#L229. It allows users to delegate their voting power to a proposer through signatures, with the only condition being that the sum of the signers' voting power should be higher than the proposal threshold. The bug is that the line uint256 proposalId = ds.proposalCount = ds.proposalCount + 1; increases the ds.proposalCount, but the proposal has not been created yet. This means that when the checkNoActiveProp() function is called, the proposal state is DEFEATED. As a result, the checkNoActiveProp() call would not revert in the case that a signer is repeated in the NounsDAOStorageV3.ProposerSignature[] array, allowing users to bypass the proposal threshold and create any proposal by signing multiple proposerSignatures with the same signer. This has a medium likelihood and a medium impact, making it a medium severity bug.

The recommendation is to consider creating the proposal before verifying the NounsDAOStorageV3.ProposerSignature[] array. This can be done by calling createNewProposal() before verifySignersCanBackThisProposalAndCountTheirVotes() function. By doing this, when verifySignersCanBackThisProposalAndCountTheirVotes() is called, the proposal state will be correct and any repeated signer would cause a revert during the checkNoActiveProp(ds, signer); call. Nouns followed Spearbit's recommendation and fixed the issue in PR 711, which was acknowledged.

### Original Finding Content

## Risk Assessment

## Severity: Medium Risk

### Context
NounsDAOV3Proposals.sol#L229

### Description
The function `proposeBySigs()` allows users to delegate their voting power to a proposer through signatures so the proposer can create a proposal. The only condition is that the sum of the signers voting power should be higher than the proposal threshold.

In the line `uint256 proposalId = ds.proposalCount = ds.proposalCount + 1;`, the `ds.proposalCount` is increased but the proposal has not been created yet, meaning that the `NounsDAOStorageV3.Proposal` struct is, at this point, uninitialized. So when the `checkNoActiveProp()` function is called, the proposal state is `DEFEATED`. 

As the proposal state is `DEFEATED`, the `checkNoActiveProp()` call would not revert in the case that a signer is repeated in the `NounsDAOStorageV3.ProposerSignature[]` array:

```solidity
function checkNoActiveProp(NounsDAOStorageV3.StorageV3 storage ds, address proposer) internal view {
    uint256 latestProposalId = ds.latestProposalIds[proposer];
    if (latestProposalId != 0) {
        NounsDAOStorageV3.ProposalState proposersLatestProposalState = state(ds, latestProposalId);
        if (
            proposersLatestProposalState == NounsDAOStorageV3.ProposalState.ObjectionPeriod ||
            proposersLatestProposalState == NounsDAOStorageV3.ProposalState.Active ||
            proposersLatestProposalState == NounsDAOStorageV3.ProposalState.Pending ||
            proposersLatestProposalState == NounsDAOStorageV3.ProposalState.Updatable
        ) revert ProposerAlreadyHasALiveProposal();
    }
}
```

Because of this, it is possible to bypass the proposal threshold and create any proposal by signing multiple `proposerSignatures` with the same signer over and over again. This would keep increasing the total voting power accounted by the smart contract until this voting power is higher than the proposal threshold.

**Medium likelihood + Medium Impact = Medium severity.**

### Recommendation
Consider creating the proposal before verifying the `NounsDAOStorageV3.ProposerSignature[]` array by calling `createNewProposal()` before the `verifySignersCanBackThisProposalAndCountTheirVotes()` function. By doing this, when `verifySignersCanBackThisProposalAndCountTheirVotes()` is called, the proposal state will be correct and any repeated signer would cause a revert during the `checkNoActiveProp(ds, signer);` call.

### Notes
- **Nouns:** Followed Spearbit's recommendation and fixed the issue in PR 711.
- **Spearbit:** Acknowledged.

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

