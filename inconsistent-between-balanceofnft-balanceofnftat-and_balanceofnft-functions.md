---
# Core Classification
protocol: Velodrome Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21391
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Velodrome-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Velodrome-Spearbit-Security-Review.pdf
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
  - services
  - yield_aggregator
  - synthetics
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 6
finders:
  - Xiaoming90
  - 0xNazgul
  - Jonatas Martins
  - 0xLeastwood
  - Jonah1005
---

## Vulnerability Title

Inconsistent between balanceOfNFT ,balanceOfNFTAt and_balanceOfNFT functions

### Overview


This bug report is about the flash-loan protection in the VotingEscrow.sol contract. The flash-loan protection is supposed to return zero voting balance if ownershipChange[_tokenId] == block.number. However, this was not consistently applied to the balanceOfNFT and balanceOfNFTAt external functions. As a result, Velodrome or external protocols calling these functions will receive different voting balances for the same veNFT depending on which function they called. Additionally, the internal _balanceOfNFT function, which does not have flash-loan protection, is called by the VotingEscrow.getVotes function to compute the voting balance of an account. This could allow a malicious user to flash-loan the veNFTs to inflate the voting balance of their account.

The recommendation is that the flash-loan protection should be consistently implemented across all the related functions to make sure that newly transferred veNFTs have zero voting balance. Velodrome suggested that once timestamp governance is merged in, block-based balance functions will be removed and the consistency of ownership_change on the various functions will be assessed.

### Original Finding Content

## Severity: Medium Risk

## Context
- VotingEscrow.sol#L985
- VotingEscrow.sol#L976

## Description
The `balanceOfNFT` function implements a flash-loan protection that returns zero voting balance if `ownershipChange[_tokenId] == block.number`. However, this was not consistently applied to the `balanceOfNFTAt` and `balanceOfNFT` functions.

### VotingEscrow.sol

```solidity
function balanceOfNFT(uint256 _tokenId) external view returns (uint256) {
    if (ownershipChange[_tokenId] == block.number) return 0;
    return _balanceOfNFT(_tokenId, block.timestamp);
}
```

As a result, Velodrome or external protocols calling the `balanceOfNFT` and `balanceOfNFTAt` external functions will receive different voting balances for the same veNFT depending on which function they called. 

Additionally, the internal `_balanceOfNFT` function, which does not have flash-loan protection, is called by the `VotingEscrow.getVotes` function to compute the voting balance of an account. The `VotingEscrow.getVotes` function appears not to be used in any in-scope contracts; however, this function might be utilized by some external protocols or off-chain components to tally the votes. If that is the case, a malicious user could flash-loan the veNFTs to inflate the voting balance of their account.

## Recommendation
If the requirement is to have all newly transferred veNFTs (`ownershipChange[_tokenId] == block.number`) have zero voting balance to prevent someone from flash-loaning veNFT to increase their voting balance, the flash-loan protection should be consistently implemented across all the related functions.

## Velodrome
I think the current status of this issue is that once timestamp governance is merged in, block-based balance functions will be removed as the contract will adopt timestamps as its official "clock" (see EIP6372). Once it is merged, we will assess the consistency of `ownership_change` on the various functions.

## Spearbit
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Velodrome Finance |
| Report Date | N/A |
| Finders | Xiaoming90, 0xNazgul, Jonatas Martins, 0xLeastwood, Jonah1005, Alex the Entreprenerd |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Velodrome-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Velodrome-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

