---
# Core Classification
protocol: Aragon DAO Gov Plugin
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62262
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Aragon-Spearbit-Security-Review-July-2025.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Aragon-Spearbit-Security-Review-July-2025.pdf
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

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Om Parikh
  - Emanuelle Ricci
  - Patrick Drotleff
---

## Vulnerability Title

currentTokenSupply() can be gamed risk-free to manipulate either side of votes in certain assets

### Overview


The bug report discusses a potential issue in a piece of code that is used to check if certain thresholds have been reached in a voting system. The code uses a variable called `currentTotalSupply` to make these calculations. However, the report raises concerns about how this variable can be manipulated by malicious actors in certain scenarios, leading to inaccurate results. The report recommends avoiding the use of this variable and suggests alternative approaches to ensure accurate calculations. The issue has been fixed in a recent update.

### Original Finding Content

## Severity: Medium Risk

## Context
MajorityVotingBase.sol#L376-L379

## Description
`currentTotalSupply` is being used at the following places to check if various thresholds are reached:

### MajorityVotingBase.isSupportThresholdReachedEarly
```solidity
uint256 noVotesWorstCase = currentTokenSupply() - proposal_.tally.yes - proposal_.tally.abstain;
return (RATIO_BASE - proposal_.parameters.supportThresholdRatio) * proposal_.tally.yes > proposal_.parameters.supportThresholdRatio * noVotesWorstCase;
```

### MajorityVotingBase.isMinVotingPowerReached
```solidity
uint256 _minVotingPower = _applyRatioCeiled(currentTokenSupply(), proposal_.parameters.minParticipationRatio);
return proposal_.tally.yes + proposal_.tally.no + proposal_.tally.abstain >= _minVotingPower;
```

### MajorityVotingBase.isMinApprovalPowerReached
```solidity
uint256 _minApprovalPower = _applyRatioCeiled(currentTokenSupply(), proposals[_proposalId].parameters.minApprovalRatio);
return proposals[_proposalId].tally.yes >= _minApprovalPower;
```

However, in case of the following tokens being locked assets:
- ERC4626 shares which can be minted permissionlessly (morpho vault-v2 share, metamorpho share).
- Tokens which can be minted 1:1 (or almost 1:1) for underlying such as various RWA tokens or staked tokens (sUSDC, sUSDT, wstETH, USDe, etc...).
- Tokens with in-built flash mint & burn capabilities (DAI, RAI, FRAX, aTokens, cTokens, various other LP tokens & wrappers, WETH, etc...).

A malicious actor doesn't require an external flash loan and neither carries a significant risk to mint & burn such tokens to manipulate the proposal by skewing totalSupply when it is read by the contract. It can be bundled atomically in a single block via PBS (like flashbots) on Ethereum. The impact is much higher, especially when skewed during the last block of the given deadline of the proposal.

## Recommendation
- Avoid using `currentTotalSupply` where it can be skewed.
- If token supply has increased or decreased by x% compared to the last recorded supply, compute using both min and max token supply and take the conservative figures.
- Consider making such cases explicit in the documentation if risk is acceptable.

## Status
- Aragon: Fixed in PR 47
- Spearbit: Fix verified

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Aragon DAO Gov Plugin |
| Report Date | N/A |
| Finders | Om Parikh, Emanuelle Ricci, Patrick Drotleff |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Aragon-Spearbit-Security-Review-July-2025.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Aragon-Spearbit-Security-Review-July-2025.pdf

### Keywords for Search

`vulnerability`

